import asyncio
import os
import random
import string
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

# Add src to path
import sys
sys.path.append(os.path.join(os.getcwd(), "src"))

# Import all models to ensure they are registered
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
    BankTransaction, Deferral, DeferralSchedule, CashFlowForecast
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

from dario_app.database import get_db, create_tenant_db, ORG_DB_DIR, master_session_maker
from dario_app.modules.tenants.models import Organization
from dario_app.modules.usuarios.routes import create_usuario, UsuarioCreate
from dario_app.modules.usuarios.models import Usuario

async def test_user_creation():
    print("--- Testing User Creation with Domain ---")
    
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    org_name = f"User Test {suffix}"
    email = f"admin_{suffix}@test.com"
    
    print(f"Creating Org: {org_name}")
    
    org_id = None
    
    try:
        # 1. Create Org in Master
        async with master_session_maker() as session:
            org = Organization(
                nombre=org_name,
                slug=f"user-test-{suffix}",
                email=email,
                plan="trial",
                estado="activo",
                activo=True
            )
            session.add(org)
            await session.commit()
            await session.refresh(org)
            org_id = org.id
            
        print(f"Org ID: {org_id}")
        
        # 2. Create Tenant DB
        print("Provisioning Tenant DB...")
        await create_tenant_db(org_id)
        
        # 3. Create User
        print("Creating new user...")
        user_data = UsuarioCreate(
            nombre="Juan",
            apellidos="Pérez",
            email_personal="juan.perez@gmail.com",
            telefono="123456789",
            es_admin=False
        )
        
        async for tenant_db in get_db(org_id):
            response = await create_usuario(
                usuario=user_data,
                org_id=org_id,
                db=tenant_db
            )
            
            print("User created successfully.")
            print(f"Generated Email: {response['email_empresa']}")
            
            expected_domain = f"user-test-{suffix}.com"
            if expected_domain in response['email_empresa']:
                print(f"SUCCESS: Email contains correct domain: {expected_domain}")
            else:
                print(f"FAILURE: Email domain mismatch. Expected {expected_domain}, got {response['email_empresa']}")
            
            break

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if org_id:
            print("Cleaning up...")
            db_path = ORG_DB_DIR / f"org_{org_id}.db"
            if db_path.exists():
                os.remove(db_path)
                print(f"Removed {db_path}")
            
            async with master_session_maker() as session:
                await session.execute(text(f"DELETE FROM organizations WHERE id = {org_id}"))
                await session.commit()

if __name__ == "__main__":
    asyncio.run(test_user_creation())
