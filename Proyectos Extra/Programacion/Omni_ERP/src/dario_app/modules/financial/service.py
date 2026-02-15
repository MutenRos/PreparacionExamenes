"""Financial service - Budget tracking, Bank reconciliation, Deferrals, Cash flow."""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any, Optional

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    Budget, BudgetActual, BankAccount, BankStatement, BankTransaction,
    Deferral, DeferralSchedule, CashFlowForecast, FinancialDimension,
    SEPARemittance, SEPARemittanceLine
)


class FinancialService:
    """Financial management service."""
    
    @staticmethod
    async def calculate_budget_actuals(
        db: AsyncSession,
        organization_id: int,
        budget_id: int
    ) -> BudgetActual:
        """Calculate actual vs budget variance."""
        from dario_app.modules.ventas.models import Venta
        from dario_app.modules.compras.models import Compra
        
        # Get budget
        stmt = select(Budget).where(
            Budget.id == budget_id,
            Budget.organization_id == organization_id
        )
        result = await db.execute(stmt)
        budget = result.scalar_one_or_none()
        
        if not budget:
            raise ValueError("Budget not found")
        
        # Calculate actual revenue from sales
        stmt_revenue = select(func.sum(Venta.total)).where(
            Venta.organization_id == organization_id,
            Venta.fecha >= budget.start_date,
            Venta.fecha <= budget.end_date,
            Venta.estado.in_(["confirmado", "facturado", "cobrado"])
        )
        result_revenue = await db.execute(stmt_revenue)
        actual_revenue = result_revenue.scalar_one() or Decimal("0")
        
        # Calculate actual expenses from purchases
        stmt_expense = select(func.sum(Compra.total)).where(
            Compra.organization_id == organization_id,
            Compra.fecha >= budget.start_date,
            Compra.fecha <= budget.end_date,
            Compra.estado.in_(["confirmado", "recibido", "pagado"])
        )
        result_expense = await db.execute(stmt_expense)
        actual_expense = result_expense.scalar_one() or Decimal("0")
        
        # Calculate variances
        revenue_variance = actual_revenue - budget.revenue_budget
        expense_variance = budget.expense_budget - actual_expense  # Positive = under budget
        
        revenue_variance_pct = (revenue_variance / budget.revenue_budget * 100) if budget.revenue_budget > 0 else None
        expense_variance_pct = (expense_variance / budget.expense_budget * 100) if budget.expense_budget > 0 else None
        
        # Upsert budget actual
        stmt_existing = select(BudgetActual).where(
            BudgetActual.budget_id == budget_id
        )
        result_existing = await db.execute(stmt_existing)
        existing = result_existing.scalar_one_or_none()
        
        if existing:
            existing.actual_revenue = actual_revenue
            existing.actual_expense = actual_expense
            existing.revenue_variance = revenue_variance
            existing.expense_variance = expense_variance
            existing.revenue_variance_percent = revenue_variance_pct
            existing.expense_variance_percent = expense_variance_pct
            existing.calculated_at = datetime.utcnow()
            budget_actual = existing
        else:
            budget_actual = BudgetActual(
                organization_id=organization_id,
                budget_id=budget_id,
                actual_revenue=actual_revenue,
                actual_expense=actual_expense,
                revenue_variance=revenue_variance,
                expense_variance=expense_variance,
                revenue_variance_percent=revenue_variance_pct,
                expense_variance_percent=expense_variance_pct
            )
            db.add(budget_actual)
        
        await db.commit()
        await db.refresh(budget_actual)
        
        return budget_actual
    
    @staticmethod
    async def auto_match_bank_transactions(
        db: AsyncSession,
        organization_id: int,
        bank_statement_id: int
    ) -> Dict[str, int]:
        """Auto-match bank transactions with sales/purchases."""
        from dario_app.modules.ventas.models import Venta
        from dario_app.modules.compras.models import Compra
        
        # Get unmatched transactions
        stmt = select(BankTransaction).where(
            BankTransaction.bank_statement_id == bank_statement_id,
            BankTransaction.organization_id == organization_id,
            BankTransaction.reconciliation_status == "unmatched"
        )
        result = await db.execute(stmt)
        transactions = result.scalars().all()
        
        matched_count = 0
        
        for trans in transactions:
            matched = False
            
            # Try to match credit transactions with sales
            if trans.transaction_type == "credit" and trans.amount > 0:
                stmt_venta = select(Venta).where(
                    Venta.organization_id == organization_id,
                    Venta.total == trans.amount,
                    Venta.estado.in_(["facturado", "cobrado"]),
                    # Look for invoices within +/- 7 days
                    Venta.fecha >= trans.transaction_date - timedelta(days=7),
                    Venta.fecha <= trans.transaction_date + timedelta(days=7)
                ).limit(1)
                result_venta = await db.execute(stmt_venta)
                venta = result_venta.scalar_one_or_none()
                
                if venta:
                    trans.reconciliation_status = "matched"
                    trans.matched_document_type = "venta"
                    trans.matched_document_id = venta.id
                    trans.matched_at = datetime.utcnow()
                    matched = True
                    matched_count += 1
            
            # Try to match debit transactions with purchases
            elif trans.transaction_type == "debit" and trans.amount < 0:
                amount_positive = abs(trans.amount)
                stmt_compra = select(Compra).where(
                    Compra.organization_id == organization_id,
                    Compra.total == amount_positive,
                    Compra.estado.in_(["confirmado", "recibido", "pagado"]),
                    Compra.fecha >= trans.transaction_date - timedelta(days=7),
                    Compra.fecha <= trans.transaction_date + timedelta(days=7)
                ).limit(1)
                result_compra = await db.execute(stmt_compra)
                compra = result_compra.scalar_one_or_none()
                
                if compra:
                    trans.reconciliation_status = "matched"
                    trans.matched_document_type = "compra"
                    trans.matched_document_id = compra.id
                    trans.matched_at = datetime.utcnow()
                    matched = True
                    matched_count += 1
        
        await db.commit()
        
        return {
            "total_transactions": len(transactions),
            "matched_count": matched_count,
            "unmatched_count": len(transactions) - matched_count
        }
    
    @staticmethod
    async def create_deferral_schedule(
        db: AsyncSession,
        organization_id: int,
        deferral_id: int
    ) -> List[DeferralSchedule]:
        """Create amortization schedule for a deferral."""
        
        # Get deferral
        stmt = select(Deferral).where(
            Deferral.id == deferral_id,
            Deferral.organization_id == organization_id
        )
        result = await db.execute(stmt)
        deferral = result.scalar_one_or_none()
        
        if not deferral:
            raise ValueError("Deferral not found")
        
        # Delete existing schedule
        stmt_del = select(DeferralSchedule).where(DeferralSchedule.deferral_id == deferral_id)
        result_del = await db.execute(stmt_del)
        existing = result_del.scalars().all()
        for sched in existing:
            await db.delete(sched)
        
        # Calculate number of periods
        months = (deferral.end_date.year - deferral.start_date.year) * 12 + \
                 (deferral.end_date.month - deferral.start_date.month) + 1
        
        if months <= 0:
            raise ValueError("Invalid date range")
        
        # Amount per period (straight line)
        amount_per_period = deferral.total_amount / Decimal(str(months))
        
        schedule_items = []
        current_date = deferral.start_date
        
        for i in range(months):
            period_str = current_date.strftime("%Y-%m")
            
            schedule = DeferralSchedule(
                organization_id=organization_id,
                deferral_id=deferral_id,
                period=period_str,
                recognition_date=current_date,
                scheduled_amount=amount_per_period
            )
            db.add(schedule)
            schedule_items.append(schedule)
            
            # Move to next month
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)
        
        # Update deferral remaining amount
        deferral.remaining_amount = deferral.total_amount
        
        await db.commit()
        
        return schedule_items
    
    @staticmethod
    async def recognize_deferrals(
        db: AsyncSession,
        organization_id: int,
        up_to_date: datetime
    ) -> Dict[str, Any]:
        """Recognize deferrals up to a specific date."""
        
        # Get pending deferral schedules
        stmt = select(DeferralSchedule).where(
            DeferralSchedule.organization_id == organization_id,
            DeferralSchedule.status == "pending",
            DeferralSchedule.recognition_date <= up_to_date
        )
        result = await db.execute(stmt)
        schedules = result.scalars().all()
        
        recognized_count = 0
        total_amount = Decimal("0")
        
        for schedule in schedules:
            # Get parent deferral
            stmt_def = select(Deferral).where(Deferral.id == schedule.deferral_id)
            result_def = await db.execute(stmt_def)
            deferral = result_def.scalar_one_or_none()
            
            if deferral and deferral.status == "active":
                # Mark as recognized
                schedule.status = "recognized"
                schedule.recognized_at = datetime.utcnow()
                
                # Update deferral amounts
                deferral.recognized_amount += schedule.scheduled_amount
                deferral.remaining_amount -= schedule.scheduled_amount
                
                # Check if fully recognized
                if deferral.remaining_amount <= Decimal("0.01"):
                    deferral.status = "completed"
                
                recognized_count += 1
                total_amount += schedule.scheduled_amount
        
        await db.commit()
        
        return {
            "recognized_count": recognized_count,
            "total_amount_recognized": float(total_amount)
        }
    
    @staticmethod
    async def calculate_cash_flow_forecast(
        db: AsyncSession,
        organization_id: int,
        forecast_date: datetime,
        user_id: Optional[int] = None
    ) -> CashFlowForecast:
        """Calculate cash flow forecast for a specific date."""
        from dario_app.modules.ventas.models import Venta
        from dario_app.modules.compras.models import Compra
        
        # Get current bank balance
        stmt_banks = select(func.sum(BankAccount.current_balance)).where(
            BankAccount.organization_id == organization_id,
            BankAccount.activo == True
        )
        result_banks = await db.execute(stmt_banks)
        opening_balance = result_banks.scalar_one() or Decimal("0")
        
        # Expected collections (pending invoices due before forecast date)
        stmt_collections = select(func.sum(Venta.total)).where(
            Venta.organization_id == organization_id,
            Venta.estado.in_(["facturado"]),
            Venta.fecha_vencimiento_pago <= forecast_date
        )
        result_collections = await db.execute(stmt_collections)
        expected_collections = result_collections.scalar_one() or Decimal("0")
        
        # Expected payments (pending purchases due before forecast date)
        stmt_payments = select(func.sum(Compra.total)).where(
            Compra.organization_id == organization_id,
            Compra.estado.in_(["confirmado", "recibido"]),
            Compra.fecha_entrega <= forecast_date
        )
        result_payments = await db.execute(stmt_payments)
        expected_payments = result_payments.scalar_one() or Decimal("0")
        
        total_inflows = expected_collections
        total_outflows = expected_payments
        closing_balance = opening_balance + total_inflows - total_outflows
        
        # Create or update forecast
        stmt_existing = select(CashFlowForecast).where(
            CashFlowForecast.organization_id == organization_id,
            CashFlowForecast.forecast_date == forecast_date
        )
        result_existing = await db.execute(stmt_existing)
        existing = result_existing.scalar_one_or_none()
        
        if existing:
            existing.opening_balance = opening_balance
            existing.expected_collections = expected_collections
            existing.total_inflows = total_inflows
            existing.expected_payments = expected_payments
            existing.total_outflows = total_outflows
            existing.closing_balance = closing_balance
            existing.calculated_at = datetime.utcnow()
            existing.calculated_by_user_id = user_id
            forecast = existing
        else:
            forecast = CashFlowForecast(
                organization_id=organization_id,
                forecast_date=forecast_date,
                opening_balance=opening_balance,
                expected_collections=expected_collections,
                total_inflows=total_inflows,
                expected_payments=expected_payments,
                total_outflows=total_outflows,
                closing_balance=closing_balance,
                calculated_by_user_id=user_id
            )
            db.add(forecast)
        
        await db.commit()
        await db.refresh(forecast)
        
        return forecast

    @staticmethod
    async def generate_sepa_xml(
        db: AsyncSession,
        remittance_id: int,
        organization_id: int
    ) -> str:
        """Generate SEPA XML content for a remittance."""
        # Fetch remittance with lines and bank account
        stmt = select(SEPARemittance).where(
            SEPARemittance.id == remittance_id,
            SEPARemittance.organization_id == organization_id
        )
        result = await db.execute(stmt)
        remittance = result.scalar_one_or_none()
        
        if not remittance:
            raise ValueError("Remittance not found")
            
        # Fetch lines
        stmt_lines = select(SEPARemittanceLine).where(
            SEPARemittanceLine.remittance_id == remittance_id
        )
        result_lines = await db.execute(stmt_lines)
        lines = result_lines.scalars().all()
        
        if not lines:
            raise ValueError("Remittance has no lines")

        # Fetch bank account
        stmt_bank = select(BankAccount).where(
            BankAccount.id == remittance.bank_account_id
        )
        result_bank = await db.execute(stmt_bank)
        bank_account = result_bank.scalar_one_or_none()
        
        if not bank_account:
            raise ValueError("Bank account not found")

        # Basic XML construction (simplified for example)
        # In a real implementation, use a proper library or template
        msg_id = f"MSG-{remittance.id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        cre_dt_tm = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        nb_of_txs = len(lines)
        ctrl_sum = sum(line.amount for line in lines)
        
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02">
  <CstmrDrctDbtInitn>
    <GrpHdr>
      <MsgId>{msg_id}</MsgId>
      <CreDtTm>{cre_dt_tm}</CreDtTm>
      <NbOfTxs>{nb_of_txs}</NbOfTxs>
      <CtrlSum>{ctrl_sum:.2f}</CtrlSum>
      <InitgPty>
        <Nm>{bank_account.account_name}</Nm>
      </InitgPty>
    </GrpHdr>
    <PmtInf>
      <PmtInfId>PMT-{remittance.id}</PmtInfId>
      <PmtMtd>DD</PmtMtd>
      <NbOfTxs>{nb_of_txs}</NbOfTxs>
      <CtrlSum>{ctrl_sum:.2f}</CtrlSum>
      <PmtTpInf>
        <SvcLvl>
          <Cd>SEPA</Cd>
        </SvcLvl>
        <LclInstrm>
          <Cd>{remittance.scheme}</Cd>
        </LclInstrm>
        <SeqTp>RCUR</SeqTp>
      </PmtTpInf>
      <ReqdColltnDt>{remittance.execution_date.strftime('%Y-%m-%d')}</ReqdColltnDt>
      <Cdtr>
        <Nm>{bank_account.account_name}</Nm>
      </Cdtr>
      <CdtrAcct>
        <Id>
          <IBAN>{bank_account.iban}</IBAN>
        </Id>
      </CdtrAcct>
      <CdtrAgt>
        <FinInstnId>
          <BIC>{bank_account.swift}</BIC>
        </FinInstnId>
      </CdtrAgt>
"""
        
        for line in lines:
            xml += f"""      <DrctDbtTxInf>
        <PmtId>
          <EndToEndId>{f'TX-{line.id}'}</EndToEndId>
        </PmtId>
        <InstdAmt Ccy="EUR">{line.amount:.2f}</InstdAmt>
        <DrctDbtTx>
          <MndtRltdInf>
            <MndtId>{line.mandate_reference or 'UNKNOWN'}</MndtId>
            <DtOfSgntr>{(line.mandate_date or datetime.utcnow()).strftime('%Y-%m-%d')}</DtOfSgntr>
          </MndtRltdInf>
        </DrctDbtTx>
        <DbtrAgt>
          <FinInstnId>
            <BIC>{line.debtor_bic or 'UNKNOWN'}</BIC>
          </FinInstnId>
        </DbtrAgt>
        <Dbtr>
          <Nm>{line.debtor_name}</Nm>
        </Dbtr>
        <DbtrAcct>
          <Id>
            <IBAN>{line.debtor_iban}</IBAN>
          </Id>
        </DbtrAcct>
        <RmtInf>
          <Ustrd>{line.concept or 'Payment'}</Ustrd>
        </RmtInf>
      </DrctDbtTxInf>
"""

        xml += """    </PmtInf>
  </CstmrDrctDbtInitn>
</Document>"""

        # Update remittance with XML content and status
        remittance.xml_content = xml
        remittance.status = "generated"
        remittance.generated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(remittance)
        
        return xml

    @staticmethod
    async def process_receipt_image(
        db: AsyncSession,
        organization_id: int,
        user_id: int,
        image_path: str,
        filename: str
    ) -> "ExpenseReceipt":
        """
        Process an uploaded receipt image.
        In a real scenario, this would call an OCR API (Google Vision, AWS Textract).
        Here we simulate extraction based on filename or random data.
        """
        from .models import ExpenseReceipt
        import random
        
        # Simulate OCR processing time
        # await asyncio.sleep(1)
        
        # Mock extraction logic
        extracted_amount = Decimal(f"{random.randint(10, 500)}.{random.randint(0, 99)}")
        extracted_tax = extracted_amount * Decimal("0.21")
        extracted_merchant = "Restaurante Ejemplo S.L." if "food" in filename.lower() else "Proveedor Genérico S.A."
        extracted_category = "Meals" if "food" in filename.lower() else "Office Supplies"
        
        receipt = ExpenseReceipt(
            organization_id=organization_id,
            user_id=user_id,
            image_path=image_path,
            filename=filename,
            merchant=extracted_merchant,
            date=datetime.utcnow().date(),
            total_amount=extracted_amount,
            tax_amount=extracted_tax,
            category=extracted_category,
            status="processing",
            ocr_raw_data={"confidence": 0.95, "source": "mock_ocr"}
        )
        
        db.add(receipt)
        await db.commit()
        await db.refresh(receipt)
        
        # Mark as verified automatically for demo purposes
        receipt.status = "verified"
        await db.commit()
        
        return receipt
