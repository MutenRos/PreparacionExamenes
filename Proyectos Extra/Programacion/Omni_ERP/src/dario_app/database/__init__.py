"""Database configuration and session management."""

from pathlib import Path
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Rutas absolutas para persistencia
# Base del repo: /home/dario/src
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Master DB (sistema / panel) — mantiene organizaciones y usuarios
MASTER_DB_PATH = DATA_DIR / "erp.db"
MASTER_DATABASE_URL = f"sqlite+aiosqlite:///{MASTER_DB_PATH}"

# Directorio para bases de datos por organización (tenant)
ORG_DB_DIR = DATA_DIR / "org_dbs"
ORG_DB_DIR.mkdir(exist_ok=True)

# Create master engine with persistence options
master_engine = create_async_engine(
    MASTER_DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False, "timeout": 30},
    pool_pre_ping=True,
    pool_recycle=3600,
)
master_session_maker = async_sessionmaker(
    master_engine, class_=AsyncSession, expire_on_commit=False
)

# Cache de engines por tenant
_tenant_engines: Dict[int, any] = {}


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


def _tenant_db_url(org_id: int) -> str:
    db_path = ORG_DB_DIR / f"org_{org_id}.db"
    # Ensure path exists and use absolute path for SQLite
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+aiosqlite:///{str(db_path)}"


def get_tenant_engine(org_id: int):
    """Return (and cache) async engine for a tenant DB."""
    if org_id in _tenant_engines:
        return _tenant_engines[org_id]
    # Create engine with persistence options
    # connect_args ensures SQLite writes to disk and handles concurrent access
    engine = create_async_engine(
        _tenant_db_url(org_id),
        echo=False,
        future=True,
        connect_args={"check_same_thread": False, "timeout": 30},
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,   # Recycle connections every hour
    )
    _tenant_engines[org_id] = engine
    return engine


async def get_db(org_id: int | None = None) -> AsyncSession:
    """Dependency for getting database sessions.

    - Si org_id está presente, abre la base del tenant.
    - Si no, usa la base maestra (para signup, login, administración global).
    """
    if org_id is None:
        async with master_session_maker() as session:
            try:
                yield session
            finally:
                await session.close()
    else:
        engine = get_tenant_engine(org_id)
        session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with session_maker() as session:
            try:
                yield session
            finally:
                await session.close()


async def create_tenant_db(org_id: int):
    """Crear base de datos para un tenant (si no existe), levantar schema y clonar la fila de organización."""
    engine = get_tenant_engine(org_id)
    db_path = ORG_DB_DIR / f"org_{org_id}.db"
    db_path.parent.mkdir(exist_ok=True)

    # Import all models to ensure they're registered
    from dario_app.modules.calendario.models import Evento
    from dario_app.modules.clientes.models import Cliente
    from dario_app.modules.compras.models import Compra, CompraDetalle
    from dario_app.modules.configuracion.models import (
        ConfiguracionGeneral,
        ConfiguracionFacturacion,
        ConfiguracionInventario,
        ConfiguracionPOS,
        ConfiguracionNotificaciones,
        ConfiguracionSeguridad,
        ConfiguracionIntegraciones,
        ConfiguracionAutomatizaciones,
        ConfiguracionVeriFactu,
    )
    from dario_app.modules.documentos.models import (
        DocumentoManual,
        DocumentTemplate,
        DocumentAttachment,
        DocumentAttachmentVersion,
        DocumentSearchIndex,
        DocumentFile,
    )
    from dario_app.modules.inventario.models import Producto, Proveedor
    from dario_app.modules.pos.models import VentaPOS, VentaPOSDetalle
    from dario_app.modules.tenants.models import Organization
    from dario_app.modules.usuarios.models import (
        Permission,
        Role,
        RolePermission,
        UserRole,
        Usuario,
        SoDRule,
        SoDViolation,
    )
    from dario_app.modules.ventas.models import Venta, VentaDetalle
    from dario_app.modules.crm.models import Lead, Opportunity, Activity, CustomerScore
    from dario_app.modules.supply_chain.models import (
        ReorderPolicy, MRPRun, MRPRequirement, LandedCostHeader, LandedCostLine,
        LandedCostAllocation, InventoryLocation, InventoryByLocation
    )
    from dario_app.modules.financial.models import (
        FinancialDimension, Budget, BudgetActual, BankAccount, BankStatement,
        BankTransaction, Deferral, DeferralSchedule, CashFlowForecast,
        SEPARemittance, SEPARemittanceLine, ExpenseReceipt
    )
    from dario_app.modules.hr.models import (
        Job, Position, Employee, LeaveRequest, Timesheet, TimesheetLine, PayrollRun, PayrollLine
    )
    from dario_app.modules.field_service.models import (
        ServiceAsset, WorkOrder, WorkOrderTask, WorkOrderSchedule
    )
    from dario_app.modules.project_ops.models import (
        Project, ProjectTask, ResourceAssignment, TimesheetEntry, Expense, BillingEvent
    )
    from dario_app.modules.customer_service.models import (
        Case, CaseComment, CSKnowledgeArticle, Entitlement
    )
    from dario_app.modules.marketing.models import (
        Campaign, CampaignActivity, MarketingList, EmailTemplate, CustomerJourney, LeadScore
    )
    from dario_app.modules.commerce.models import (
        Catalog, CatalogProduct, PriceList, PriceListItem, Discount, 
        OnlineOrder, OnlineOrderLine, CustomerReview
    )
    from dario_app.modules.asset_management.models import (
        Asset, MaintenanceSchedule, MaintenanceOrder, RentalAgreement, AssetTransfer, AssetMeter
    )
    from dario_app.modules.sales_orders.models import (
        Quote, QuoteLine, SalesOrder, SalesOrderLine, Shipment, ShipmentLine
    )
    from dario_app.modules.quality_management.models import (
        QualityOrder, QualityCheckpoint, NonConformance, QualitySpecification, 
        QualitySpecificationLine, QualityAudit
    )
    from dario_app.modules.subscription_billing.models import (
        SubscriptionPlan, Subscription, SubscriptionInvoice, SubscriptionUsage,
        SubscriptionChange, RevenueRecognition
    )
    from dario_app.modules.customer_insights.models import (
        CustomerSegment, CustomerSegmentMember, CustomerMetric, CustomerJourney,
        CustomerPrediction, CustomerInsightReport, CustomerFeedback
    )
    from dario_app.modules.transportation_management.models import (
        Carrier, TransportRoute, FreightOrder, LoadPlan, LoadPlanItem, RateQuote, TransportEvent
    )
    from dario_app.modules.advanced_warehouse.models import (
        WarehouseZone, WarehouseBin, Wave, PickTask, PackTask, CycleCount, Replenishment, PutawayTask
    )
    from dario_app.modules.product_information.models import (
        ProductCategory, ProductAttribute, ProductAttributeValue, ProductMedia,
        ProductRelationship, ProductVariant, ProductChannelListing, ProductLocalization, ProductPriceHistory
    )
    from dario_app.modules.recruitment.models import (
        JobPosition, Candidate, Application, Interview, JobOffer, CandidateRating
    )
    from dario_app.modules.service_scheduling.models import (
        ServiceResource, ServiceSlot, ServiceAppointment, ServiceScheduleTemplate, ResourceAvailability
    )
    from dario_app.modules.sustainability.models import (
        SustainabilityGoal, EmissionSource, EmissionRecord, WasteRecord, SustainabilityReport, ComplianceRequirement
    )
    from dario_app.modules.contract_management.models import (
        ContractTemplate, Contract, ContractClause, ContractApproval, ContractMilestone, ContractRenewal
    )
    from dario_app.modules.warranty_management.models import (
        WarrantyPolicy, ProductWarranty, WarrantyRegistration, WarrantyClaim, WarrantyService
    )
    from dario_app.modules.marketing_advanced.models import (
        MarketingCampaign, MarketingActivity, MarketingList, EmailTemplate, CustomerJourneyMap, LeadScoreModel
    )
    from dario_app.modules.sales_intelligence.models import (
        SalesInsight, OpportunityScoringModel, CompetitorIntelligence, SalesForecast
    )
    from dario_app.modules.iot_integration.models import (
        IoTDevice, DeviceReading, AlertRule, MaintenancePrediction
    )
    from dario_app.modules.demand_planning.models import (
        DemandForecast, SeasonalityFactor, ForecastAccuracy, PlanningScenario
    )
    from dario_app.modules.business_intelligence.models import (
        Dashboard, KPI, Report, DataVisualization, AnalyticsQuery, MetricDefinition
    )
    from dario_app.modules.resource_scheduling_optimization.models import (
        OptimizationJob, ScheduleOptimization, ResourceRequirement, SchedulingParameter, OptimizationResult
    )
    from dario_app.modules.compliance_management.models import (
        ComplianceFramework, Regulation, CertificationProcess, ComplianceAudit, ViolationReport
    )
    from dario_app.modules.learning_management.models import (
        Course, Lesson, Enrollment, Assessment, Certification, LearningPath
    )
    from dario_app.modules.knowledge_management.models import (
        KnowledgeArticle, ArticleCategory, ArticleVersion, ArticleRating, SearchQuery
    )
    from dario_app.modules.communication_hub.models import (
        CommunicationChannel, MessageTemplate, ConversationThread, Message, ContactPreference
    )
    from dario_app.modules.partner_relationship_management.models import (
        PartnerProgram, Partner, PartnerDealRegistration, PartnerIncentive, PartnerCertification
    )
    from dario_app.modules.self_service_portal.models import (
        PortalUserProfile, PortalCase, PortalRequest, PortalFeedback, PortalKnowledgeView
    )
    from dario_app.modules.security_threat_intelligence.models import (
        ThreatIndicator, SecurityAlert, Vulnerability, Incident, SecurityAssessment
    )
    from dario_app.modules.integration_platform.models import (
        ApiGateway, ApiEndpoint, ThrottlePolicy, ApiKey, IntegrationFlow
    )
    from dario_app.modules.localization.models import (
        MultiCurrencySetting, CurrencyRate, CurrencyConversionLog, LocalizationProfile, LanguageResource
    )
    from dario_app.modules.regulatory_reporting.models import (
        TaxEntity, TaxReturn, TaxFilingSchedule, TaxTransaction, TaxAuditTrail
    )
    from dario_app.modules.copilot_ai_insights.models import (
        AIInsight, InsightDetail, CopilotAssistant, CopilotInteraction, PredictiveModel, CopilotPrediction, AIPromptTemplate, MarketInsight, InsightAction
    )
    from dario_app.modules.viva_employee_experience.models import (
        EmployeeEngagementSurvey, SurveyQuestion, SurveyResponse, SurveyQuestionResponse,
        EmployeeWellnessProfile, WellnessInitiative, WellnessActivity,
        VivaGoal, GoalCheckIn, EmployeeFeedback, RecognitionEvent
    )
    from dario_app.modules.manufacturing_execution.models import (
        ShopFloorWorkOrder, Equipment, QualityInspection, ProductionEventLog,
        WorkCenter, MaintenanceRecord, ProductionSchedule, LaborTracking,
        ScrapTracking, MaterialConsumption
    )
    from dario_app.modules.financial_reporting_advanced.models import (
        FinancialReportTemplate, GeneratedReport, ConsolidationGroup, ConsolidatedEntity,
        IntercompanyTransaction, ReportingVariance, AuditTrail, SegmentReporting
    )
    from dario_app.modules.advanced_inventory_optimization.models import (
        ABCAnalysisResult, DemandForecast, SafetyStockCalculation, SupplierPerformance,
        ReorderOptimization, InventoryTurnoverAnalysis, StockoutPrevention, InventoryOptimizationReport
    )
    from dario_app.modules.real_estate_management.models import (
        Property, LeaseAgreement, RentCollection, MaintenanceRequest,
        SpaceAllocation, FacilityCondition, PropertyPortfolioAnalysis
    )
    from dario_app.modules.ml_platform.models import (
        MLModel, TrainingPipeline, MLPrediction, FeatureStore,
        ModelPerformanceMetric, AutoMLExperiment, PredictionBatch, ModelDeployment
    )
    from dario_app.modules.automatizaciones.models import (
        Automatizacion,
        Accion,
        RegistroAutomatizacion,
        CondicionAutomatizacion,
    )
    from dario_app.modules.tutorial.models import UserTutorialProgress
    from dario_app.modules.oficina_tecnica.models import BOMHeader, BOMLine, BOMOperacion
    from dario_app.modules.puertas.models import Puerta, MovimientoPuerta, RecepcionDetalle
    from dario_app.modules import produccion_ordenes  # noqa: F401 ensure production models are registered
    from dario_app.models.workflow_instance import WorkflowInstance, WorkflowTransition, WorkflowActionLog
    from dario_app.modules.supply_chain.models import (
        ReorderPolicy, MRPRun, MRPRequirement, LandedCostHeader, LandedCostLine,
        LandedCostAllocation, InventoryLocation, InventoryByLocation
    )
    from dario_app.modules.financial.models import (
        FinancialDimension, Budget, BudgetActual, BankAccount, BankStatement,
        BankTransaction, Deferral, DeferralSchedule, CashFlowForecast,
        SEPARemittance, SEPARemittanceLine
    )
    from dario_app.modules.hr.models import (
        Job, Position, Employee, LeaveRequest, Timesheet, TimesheetLine, PayrollRun, PayrollLine
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Clonar la fila de organización al tenant DB para respetar FKs
    from sqlalchemy import select

    async with master_session_maker() as master_session:
        org_row = await master_session.get(Organization, org_id)
        if org_row:
            async with async_sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False
            )() as tenant_session:
                exists = await tenant_session.get(Organization, org_id)
                if not exists:
                    clone = Organization(
                        id=org_row.id,
                        nombre=org_row.nombre,
                        slug=org_row.slug,
                        tipo_negocio=org_row.tipo_negocio,
                        descripcion=org_row.descripcion,
                        razon_social=org_row.razon_social,
                        nif_cif=org_row.nif_cif,
                        nif_valido=org_row.nif_valido,
                        domicilio_fiscal=org_row.domicilio_fiscal,
                        municipio=org_row.municipio,
                        provincia=org_row.provincia,
                        codigo_postal=org_row.codigo_postal,
                        pais=org_row.pais,
                        regimen_iva=org_row.regimen_iva,
                        porcentaje_iva=org_row.porcentaje_iva,
                        aplica_irpf=org_row.aplica_irpf,
                        porcentaje_irpf=org_row.porcentaje_irpf,
                        website=org_row.website,
                        datos_fiscales_completos=org_row.datos_fiscales_completos,
                        email=org_row.email,
                        telefono=org_row.telefono,
                        direccion=org_row.direccion,
                        plan=org_row.plan,
                        estado=org_row.estado,
                        trial_hasta=org_row.trial_hasta,
                        max_usuarios=org_row.max_usuarios,
                        max_productos=org_row.max_productos,
                        max_sucursales=org_row.max_sucursales,
                        configuracion=org_row.configuracion,
                        activo=org_row.activo,
                        creado_en=org_row.creado_en,
                        actualizado_en=org_row.actualizado_en,
                    )
                    tenant_session.add(clone)
                    await tenant_session.commit()

    # Seed permissions and roles (Discord-like structure)
    from dario_app.modules.usuarios.services import seed_tenant_permissions
    async with async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)() as session:
        await seed_tenant_permissions(session, org_id)

    return str(db_path)


async def init_db():
    """Initialize master database tables (system)."""
    # Import all models to ensure they're registered
    from dario_app.modules.calendario.models import Evento
    from dario_app.modules.clientes.models import Cliente
    from dario_app.modules.compras.models import Compra, CompraDetalle
    from dario_app.modules.configuracion.models import (
        ConfiguracionGeneral,
        ConfiguracionFacturacion,
        ConfiguracionInventario,
        ConfiguracionPOS,
        ConfiguracionNotificaciones,
        ConfiguracionSeguridad,
        ConfiguracionIntegraciones,
        ConfiguracionAutomatizaciones,
        ConfiguracionVeriFactu,
    )
    from dario_app.modules.documentos.models import DocumentoManual, DocumentTemplate
    from dario_app.modules.inventario.models import Producto, Proveedor
    from dario_app.modules.pos.models import VentaPOS, VentaPOSDetalle
    from dario_app.modules.tenants.models import Organization
    from dario_app.modules.usuarios.models import (
        Permission,
        Role,
        RolePermission,
        UserRole,
        Usuario,
    )
    from dario_app.modules.ventas.models import Venta, VentaDetalle
    from dario_app.modules.supply_chain.models import (
        ReorderPolicy, MRPRun, MRPRequirement, LandedCostHeader, LandedCostLine,
        LandedCostAllocation, InventoryLocation, InventoryByLocation
    )
    from dario_app.modules.financial.models import (
        FinancialDimension, Budget, BudgetActual, BankAccount, BankStatement,
        BankTransaction, Deferral, DeferralSchedule, CashFlowForecast,
        SEPARemittance, SEPARemittanceLine, ExpenseReceipt
    )
    from dario_app.modules.field_service.models import (
        ServiceAsset, WorkOrder, WorkOrderTask, WorkOrderSchedule
    )
    from dario_app.modules.project_ops.models import (
        Project, ProjectTask, ResourceAssignment, TimesheetEntry, Expense, BillingEvent
    )
    from dario_app.modules.customer_service.models import (
        Case, CaseComment, CSKnowledgeArticle, Entitlement
    )
    from dario_app.modules.marketing.models import (
        Campaign, CampaignActivity, MarketingList, EmailTemplate, CustomerJourney, LeadScore
    )
    from dario_app.modules.commerce.models import (
        Catalog, CatalogProduct, PriceList, PriceListItem, Discount,
        OnlineOrder, OnlineOrderLine, CustomerReview
    )
    from dario_app.modules.asset_management.models import (
        Asset, MaintenanceSchedule, MaintenanceOrder, RentalAgreement, AssetTransfer, AssetMeter
    )
    from dario_app.modules.sales_orders.models import (
        Quote, QuoteLine, SalesOrder, SalesOrderLine, Shipment, ShipmentLine
    )
    from dario_app.modules.quality_management.models import (
        QualityOrder, QualityCheckpoint, NonConformance, QualitySpecification,
        QualitySpecificationLine, QualityAudit
    )
    from dario_app.modules.subscription_billing.models import (
        SubscriptionPlan, Subscription, SubscriptionInvoice, SubscriptionUsage,
        SubscriptionChange, RevenueRecognition
    )
    from dario_app.modules.oficina_tecnica.models import BOMHeader, BOMLine, BOMOperacion
    from dario_app.modules.puertas.models import Puerta, MovimientoPuerta, RecepcionDetalle
    from dario_app.modules import produccion_ordenes  # noqa: F401 ensure production models are registered
    from dario_app.models.workflow_instance import WorkflowInstance, WorkflowTransition, WorkflowActionLog

    async with master_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
