"""Financial Management models - Budgets, Dimensions, Bank Reconciliation, Deferrals."""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, Date, ForeignKey, Integer, Numeric, String, Text, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dario_app.database import Base


class FinancialDimension(Base):
    """Financial dimensions for multi-dimensional analysis."""
    
    __tablename__ = "financial_dimensions"
    __table_args__ = (
        Index("idx_fin_dim_org_code", "organization_id", "dimension_code", unique=True),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Dimension type: department, project, cost_center, region, product_line
    dimension_type: Mapped[str] = mapped_column(String(50), nullable=False)
    dimension_code: Mapped[str] = mapped_column(String(50), nullable=False)
    dimension_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Parent for hierarchical dimensions
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("financial_dimensions.id"))
    
    # Manager
    manager_id: Mapped[Optional[int]] = mapped_column(Integer)
    manager_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Budget(Base):
    """Budget definitions."""
    
    __tablename__ = "budgets"
    __table_args__ = (
        Index("idx_budget_org_period", "organization_id", "fiscal_year", "period"),
        Index("idx_budget_dimension", "organization_id", "dimension_id"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    budget_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Period
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[str] = mapped_column(String(20), nullable=False)  # Q1, Q2, Q3, Q4, M01-M12, YEAR
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Financial dimension
    dimension_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("financial_dimensions.id"))
    dimension_code: Mapped[Optional[str]] = mapped_column(String(50))
    dimension_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Budget amounts
    revenue_budget: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    expense_budget: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    capex_budget: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    
    # Status: draft, approved, active, closed
    status: Mapped[str] = mapped_column(String(50), default="draft")
    
    # Approval
    approved_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    approved_by_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    notas: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BudgetActual(Base):
    """Actual financial results vs budget."""
    
    __tablename__ = "budget_actuals"
    __table_args__ = (
        Index("idx_budget_actual_budget", "budget_id"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    budget_id: Mapped[int] = mapped_column(Integer, ForeignKey("budgets.id"), nullable=False)
    
    # Actuals
    actual_revenue: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    actual_expense: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    actual_capex: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    
    # Variance
    revenue_variance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    expense_variance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    capex_variance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    
    # Percentage
    revenue_variance_percent: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    expense_variance_percent: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BankAccount(Base):
    """Bank accounts for reconciliation."""
    
    __tablename__ = "bank_accounts"
    __table_args__ = (
        Index("idx_bank_org_account", "organization_id", "account_number", unique=True),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    account_name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_number: Mapped[str] = mapped_column(String(100), nullable=False)
    iban: Mapped[Optional[str]] = mapped_column(String(50))
    swift: Mapped[Optional[str]] = mapped_column(String(20))
    
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False)
    branch: Mapped[Optional[str]] = mapped_column(String(255))
    
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    
    # Current balance
    current_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    last_reconciled_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    last_reconciled_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BankStatement(Base):
    """Bank statement imports."""
    
    __tablename__ = "bank_statements"
    __table_args__ = (
        Index("idx_bank_stmt_account", "bank_account_id"),
        Index("idx_bank_stmt_date", "organization_id", "statement_date"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    bank_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    
    statement_number: Mapped[Optional[str]] = mapped_column(String(100))
    statement_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    opening_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    closing_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Import details
    imported_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    imported_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    imported_by_user_name: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Status: imported, reconciling, reconciled
    status: Mapped[str] = mapped_column(String(50), default="imported")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BankTransaction(Base):
    """Bank statement transactions."""
    
    __tablename__ = "bank_transactions"
    __table_args__ = (
        Index("idx_bank_trans_stmt", "bank_statement_id"),
        Index("idx_bank_trans_status", "organization_id", "reconciliation_status"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    bank_statement_id: Mapped[int] = mapped_column(Integer, ForeignKey("bank_statements.id"), nullable=False)
    bank_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    
    transaction_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Transaction details
    transaction_type: Mapped[str] = mapped_column(String(50))  # debit, credit
    reference: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    counterparty_name: Mapped[Optional[str]] = mapped_column(String(255))
    counterparty_account: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Reconciliation
    reconciliation_status: Mapped[str] = mapped_column(String(50), default="unmatched")  # unmatched, matched, ignored
    matched_document_type: Mapped[Optional[str]] = mapped_column(String(50))  # venta, compra, payment
    matched_document_id: Mapped[Optional[int]] = mapped_column(Integer)
    matched_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    matched_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Deferral(Base):
    """Deferred revenue and expenses (accruals/deferrals)."""
    
    __tablename__ = "deferrals"
    __table_args__ = (
        Index("idx_deferral_org_status", "organization_id", "status"),
        Index("idx_deferral_dates", "start_date", "end_date"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Type: deferred_revenue, deferred_expense, accrued_revenue, accrued_expense
    deferral_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Source document
    source_type: Mapped[str] = mapped_column(String(50))  # venta, compra
    source_id: Mapped[Optional[int]] = mapped_column(Integer)
    source_reference: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Amount and period
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Amortization
    amortization_method: Mapped[str] = mapped_column(String(50), default="straight_line")  # straight_line, daily
    recognized_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    remaining_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    
    # Status: active, completed, cancelled
    status: Mapped[str] = mapped_column(String(50), default="active")
    
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DeferralSchedule(Base):
    """Deferral recognition schedule."""
    
    __tablename__ = "deferral_schedules"
    __table_args__ = (
        Index("idx_deferral_sched_parent", "deferral_id"),
        Index("idx_deferral_sched_date", "organization_id", "recognition_date"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    deferral_id: Mapped[int] = mapped_column(Integer, ForeignKey("deferrals.id"), nullable=False)
    
    period: Mapped[str] = mapped_column(String(20), nullable=False)  # 2024-01, 2024-02, etc.
    recognition_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    scheduled_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    
    # Recognition status: pending, recognized
    status: Mapped[str] = mapped_column(String(50), default="pending")
    recognized_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CashFlowForecast(Base):
    """Cash flow forecasting."""
    
    __tablename__ = "cash_flow_forecasts"
    __table_args__ = (
        Index("idx_cashflow_org_date", "organization_id", "forecast_date"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    forecast_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Opening balance
    opening_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    
    # Inflows
    expected_collections: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    other_inflows: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    total_inflows: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    
    # Outflows
    expected_payments: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    payroll: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    other_outflows: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    total_outflows: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    
    # Closing balance
    closing_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    
    # Calculation details
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    calculated_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    notas: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SEPARemittance(Base):
    """SEPA Direct Debit Remittances (Remesas Bancarias)."""
    
    __tablename__ = "sepa_remittances"
    __table_args__ = (
        Index("idx_sepa_org_date", "organization_id", "execution_date"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    bank_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    
    remittance_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # e.g. REM-2024-001
    execution_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Scheme: CORE, B2B
    scheme: Mapped[str] = mapped_column(String(10), default="CORE")
    description: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Status: draft, generated, sent, paid, cancelled
    status: Mapped[str] = mapped_column(String(50), default="draft")
    
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0"))
    total_transactions: Mapped[int] = mapped_column(Integer, default=0)
    
    xml_content: Mapped[Optional[str]] = mapped_column(Text)  # Generated XML
    
    created_by_user_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    lines = relationship("SEPARemittanceLine", back_populates="remittance", cascade="all, delete-orphan")


class SEPARemittanceLine(Base):
    """Individual transactions within a SEPA remittance."""
    
    __tablename__ = "sepa_remittance_lines"
    __table_args__ = (
        Index("idx_sepa_line_remittance", "remittance_id"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    remittance_id: Mapped[int] = mapped_column(Integer, ForeignKey("sepa_remittances.id"), nullable=False)
    
    # Link to invoice (optional but recommended)
    invoice_id: Mapped[Optional[int]] = mapped_column(Integer)  # ForeignKey("ventas.id") - loose coupling
    
    debtor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    debtor_iban: Mapped[str] = mapped_column(String(50), nullable=False)
    debtor_bic: Mapped[Optional[str]] = mapped_column(String(20))
    
    mandate_reference: Mapped[str] = mapped_column(String(50), nullable=False)
    mandate_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    concept: Mapped[str] = mapped_column(String(140), nullable=False)
    
    # Sequence: FRST, RCUR, OOFF, FNAL
    sequence_type: Mapped[str] = mapped_column(String(4), default="RCUR")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    remittance = relationship("SEPARemittance", back_populates="lines")


class ExpenseReceipt(Base):
    """Smart Expense Receipts (Digitalización de Gastos)."""
    
    __tablename__ = "expense_receipts"
    __table_args__ = (
        Index("idx_exp_receipt_org_user", "organization_id", "user_id"),
        {"extend_existing": True}
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False) # User who uploaded
    
    # Image
    image_path: Mapped[str] = mapped_column(String(500), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Extracted Data (OCR)
    merchant: Mapped[Optional[str]] = mapped_column(String(255))
    date: Mapped[Optional[date]] = mapped_column(Date)
    total_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    tax_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Status: pending, processing, verified, rejected
    status: Mapped[str] = mapped_column(String(50), default="pending")
    
    ocr_raw_data: Mapped[Optional[dict]] = mapped_column(JSON)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
