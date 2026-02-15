"""CRM service - Business logic for leads, opportunities, scoring."""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Lead, Opportunity, Activity, CustomerScore


class CRMService:
    """CRM business logic service."""
    
    @staticmethod
    async def calculate_lead_score(
        db: AsyncSession,
        lead: Lead,
        organization_id: int
    ) -> int:
        """Calculate lead score based on multiple factors."""
        score = 0
        
        # Company size (if available)
        if lead.empresa:
            score += 10
        
        # Contact completeness
        if lead.telefono:
            score += 10
        if lead.email:
            score += 10
        if lead.cargo:
            score += 5
        
        # Website presence
        if lead.website:
            score += 10
        
        # Source quality
        source_scores = {
            "referral": 30,
            "campaign": 20,
            "web": 15,
            "cold_call": 5
        }
        score += source_scores.get(lead.source, 0)
        
        # Engagement (activities)
        activities_stmt = select(func.count(Activity.id)).where(
            Activity.organization_id == organization_id,
            Activity.related_to_type == "lead",
            Activity.related_to_id == lead.id
        )
        result = await db.execute(activities_stmt)
        activity_count = result.scalar_one()
        score += min(activity_count * 5, 20)  # Max 20 points
        
        # Recency
        if lead.last_contacted_at:
            days_ago = (datetime.utcnow() - lead.last_contacted_at).days
            if days_ago < 7:
                score += 10
            elif days_ago < 30:
                score += 5
        
        return min(score, 100)
    
    @staticmethod
    async def calculate_opportunity_weighted_value(
        oportunidad: Opportunity
    ) -> Decimal:
        """Calculate weighted value (value * probability)."""
        return oportunidad.valor_estimado * Decimal(oportunidad.probabilidad / 100)
    
    @staticmethod
    async def get_pipeline_metrics(
        db: AsyncSession,
        organization_id: int
    ) -> Dict[str, Any]:
        """Get sales pipeline metrics."""
        
        # Opportunities by stage
        stmt = select(
            Opportunity.stage,
            func.count(Opportunity.id).label("count"),
            func.sum(Opportunity.valor_estimado).label("total_value"),
            func.sum(Opportunity.valor_ponderado).label("weighted_value")
        ).where(
            Opportunity.organization_id == organization_id,
            Opportunity.stage.not_in(["closed_won", "closed_lost"])
        ).group_by(Opportunity.stage)
        
        result = await db.execute(stmt)
        stages = result.all()
        
        pipeline = {
            "stages": [
                {
                    "stage": stage[0],
                    "count": stage[1],
                    "total_value": float(stage[2] or 0),
                    "weighted_value": float(stage[3] or 0)
                }
                for stage in stages
            ]
        }
        
        # Win rate
        stmt_wins = select(func.count(Opportunity.id)).where(
            Opportunity.organization_id == organization_id,
            Opportunity.stage == "closed_won",
            Opportunity.actual_close_date >= datetime.utcnow() - timedelta(days=90)
        )
        stmt_losses = select(func.count(Opportunity.id)).where(
            Opportunity.organization_id == organization_id,
            Opportunity.stage == "closed_lost",
            Opportunity.actual_close_date >= datetime.utcnow() - timedelta(days=90)
        )
        
        wins = (await db.execute(stmt_wins)).scalar_one()
        losses = (await db.execute(stmt_losses)).scalar_one()
        
        total_closed = wins + losses
        win_rate = (wins / total_closed * 100) if total_closed > 0 else 0
        
        pipeline["win_rate"] = round(win_rate, 2)
        pipeline["wins_90d"] = wins
        pipeline["losses_90d"] = losses
        
        return pipeline
    
    @staticmethod
    async def calculate_customer_rfm_score(
        db: AsyncSession,
        organization_id: int,
        cliente_id: int
    ) -> Dict[str, Any]:
        """Calculate RFM (Recency, Frequency, Monetary) score for customer."""
        from dario_app.modules.ventas.models import Venta
        
        # Get customer purchases
        stmt = select(Venta).where(
            Venta.organization_id == organization_id,
            Venta.cliente_id == cliente_id,
            Venta.estado != "cancelado"
        ).order_by(Venta.fecha.desc())
        
        result = await db.execute(stmt)
        ventas = result.scalars().all()
        
        if not ventas:
            return {
                "recency_score": 0,
                "frequency_score": 0,
                "monetary_score": 0,
                "rfm_segment": "new",
                "score": 0
            }
        
        # Recency (days since last purchase)
        last_purchase = ventas[0].fecha
        days_since = (datetime.utcnow() - last_purchase).days
        
        if days_since < 30:
            recency_score = 5
        elif days_since < 90:
            recency_score = 4
        elif days_since < 180:
            recency_score = 3
        elif days_since < 365:
            recency_score = 2
        else:
            recency_score = 1
        
        # Frequency (number of purchases)
        frequency = len(ventas)
        
        if frequency >= 20:
            frequency_score = 5
        elif frequency >= 10:
            frequency_score = 4
        elif frequency >= 5:
            frequency_score = 3
        elif frequency >= 2:
            frequency_score = 2
        else:
            frequency_score = 1
        
        # Monetary (total spent)
        total_spent = sum(float(v.total) for v in ventas)
        
        if total_spent >= 10000:
            monetary_score = 5
        elif total_spent >= 5000:
            monetary_score = 4
        elif total_spent >= 1000:
            monetary_score = 3
        elif total_spent >= 100:
            monetary_score = 2
        else:
            monetary_score = 1
        
        # RFM Segment
        rfm_code = f"{recency_score}{frequency_score}{monetary_score}"
        
        # Simplified segmentation
        if rfm_code in ["555", "554", "545", "544", "455", "454", "445", "444"]:
            segment = "Champions"
        elif rfm_code in ["543", "534", "443", "434", "353", "344", "335"]:
            segment = "Loyal Customers"
        elif rfm_code in ["525", "524", "523", "522", "521", "515", "514", "513", "512", "511"]:
            segment = "Potential Loyalist"
        elif rfm_code in ["155", "154", "144", "214", "215", "115", "114"]:
            segment = "At Risk"
        elif rfm_code in ["155", "154", "153", "152", "151", "145", "143", "142", "141", "135", "134", "133"]:
            segment = "Cannot Lose Them"
        elif recency_score <= 2:
            segment = "Lost"
        else:
            segment = "Regular"
        
        # Overall score (weighted average)
        overall_score = int((recency_score * 0.4 + frequency_score * 0.3 + monetary_score * 0.3) * 20)
        
        return {
            "recency_score": recency_score,
            "frequency_score": frequency_score,
            "monetary_score": monetary_score,
            "rfm_segment": segment,
            "score": overall_score,
            "total_compras": Decimal(str(total_spent)),
            "numero_compras": frequency,
            "promedio_compra": Decimal(str(total_spent / frequency)) if frequency > 0 else Decimal("0"),
            "dias_ultima_compra": days_since
        }
    
    @staticmethod
    async def update_all_customer_scores(
        db: AsyncSession,
        organization_id: int
    ) -> int:
        """Update scores for all customers. Returns count updated."""
        from dario_app.modules.clientes.models import Cliente
        
        stmt = select(Cliente).where(Cliente.organization_id == organization_id)
        result = await db.execute(stmt)
        clientes = result.scalars().all()
        
        updated = 0
        for cliente in clientes:
            rfm_data = await CRMService.calculate_customer_rfm_score(
                db, organization_id, cliente.id
            )
            
            # Upsert score
            stmt_existing = select(CustomerScore).where(
                CustomerScore.organization_id == organization_id,
                CustomerScore.cliente_id == cliente.id
            )
            result = await db.execute(stmt_existing)
            existing_score = result.scalar_one_or_none()
            
            if existing_score:
                existing_score.recency_score = rfm_data["recency_score"]
                existing_score.frequency_score = rfm_data["frequency_score"]
                existing_score.monetary_score = rfm_data["monetary_score"]
                existing_score.rfm_segment = rfm_data["rfm_segment"]
                existing_score.score = rfm_data["score"]
                existing_score.total_compras = rfm_data["total_compras"]
                existing_score.numero_compras = rfm_data["numero_compras"]
                existing_score.promedio_compra = rfm_data["promedio_compra"]
                existing_score.dias_ultima_compra = rfm_data["dias_ultima_compra"]
                existing_score.calculated_at = datetime.utcnow()
            else:
                new_score = CustomerScore(
                    organization_id=organization_id,
                    cliente_id=cliente.id,
                    **rfm_data
                )
                db.add(new_score)
            
            updated += 1
        
        await db.commit()
        return updated
