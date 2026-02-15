"""FastAPI application factory and configuration."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from dario_app.core import settings
from dario_app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name, 
        version=settings.version, 
        lifespan=lifespan,
        description="Enterprise ERP System - Microsoft Dynamics 365 Class",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )

    # Import routers here to avoid circular imports
    from dario_app.modules.ai.routes import router as ai_router
    from dario_app.modules.auth.routes import router as auth_router
    from dario_app.modules.calendario.routes import router as calendario_router
    from dario_app.modules.clientes.routes import router as clientes_router
    from dario_app.modules.compras.routes import router as compras_router
    from dario_app.modules.documentos.routes import router as documentos_router, attachments_router as documentos_adjuntos_router
    from dario_app.modules.inventario.routes import router as inventario_router
    from dario_app.modules.pos.routes import router as pos_router
    from dario_app.modules.reportes.public_routes import router as reportes_public_router
    from dario_app.modules.reportes.routes import router as reportes_router
    from dario_app.modules.tenants.routes import router as tenants_router
    from dario_app.modules.usuarios.routes import router as usuarios_router
    from dario_app.modules.ventas.routes import router as ventas_router
    from dario_app.modules.configuracion.routes import router as configuracion_router
    # Automatizaciones internas
    from dario_app.modules.automatizaciones.routes import router as automatizaciones_router
    
    # Tutorial interactivo
    from dario_app.modules.tutorial.routes import router as tutorial_router
    
    # Voice Assistant
    from dario_app.modules.voice_assistant.routes import router as voice_assistant_router
    from dario_app.modules.security.routes import router as security_router
    
    # CRM - Customer Relationship Management
    from dario_app.modules.crm.routes import router as crm_router
    
    # Supply Chain Management
    from dario_app.modules.supply_chain.routes import router as supply_chain_router
    
    # Financial Management
    from dario_app.modules.financial.routes import router as financial_router

    # Human Resources & Payroll
    from dario_app.modules.hr.routes import router as hr_router

    # Field Service
    from dario_app.modules.field_service.routes import router as field_service_router

    # Project Operations
    from dario_app.modules.project_ops.routes import router as project_ops_router

    # Customer Service
    from dario_app.modules.customer_service.routes import router as customer_service_router

    # Marketing
    from dario_app.modules.marketing.routes import router as marketing_router

    # Commerce
    from dario_app.modules.commerce.routes import router as commerce_router

    # Asset Management
    from dario_app.modules.asset_management.routes import router as asset_management_router

    # Sales Orders & Quotes
    from dario_app.modules.sales_orders.routes import router as sales_orders_router

    # Quality Management
    from dario_app.modules.quality_management.routes import router as quality_management_router

    # Subscription Billing
    from dario_app.modules.subscription_billing.routes import router as subscription_billing_router

    # Customer Insights
    from dario_app.modules.customer_insights.routes import router as customer_insights_router

    # Transportation Management
    from dario_app.modules.transportation_management.routes import router as transportation_router

    # Advanced Warehouse Management
    from dario_app.modules.advanced_warehouse.routes import router as advanced_warehouse_router

    # Product Information Management
    from dario_app.modules.product_information.routes import router as pim_router

    # Recruitment Management
    from dario_app.modules.recruitment.routes import router as recruitment_router
    
    # Service Scheduling
    from dario_app.modules.service_scheduling.routes import router as service_scheduling_router
    
    # Sustainability Management
    from dario_app.modules.sustainability.routes import router as sustainability_router
    
    # Contract Lifecycle Management
    from dario_app.modules.contract_management.routes import router as contract_management_router
    
    # Warranty Management
    from dario_app.modules.warranty_management.routes import router as warranty_router

    # Advanced Marketing
    from dario_app.modules.marketing_advanced.routes import router as marketing_advanced_router

    # Sales Intelligence
    from dario_app.modules.sales_intelligence.routes import router as sales_intelligence_router

    # IoT Integration
    from dario_app.modules.iot_integration.routes import router as iot_integration_router

    # Demand Planning
    from dario_app.modules.demand_planning.routes import router as demand_planning_router

    # Business Intelligence & Analytics
    from dario_app.modules.business_intelligence.routes import router as business_intelligence_router

    # Resource Scheduling Optimization
    from dario_app.modules.resource_scheduling_optimization.routes import router as resource_scheduling_optimization_router

    # Compliance Management
    from dario_app.modules.compliance_management.routes import router as compliance_management_router

    # Learning Management System
    from dario_app.modules.learning_management.routes import router as learning_management_router

    # Knowledge Management
    from dario_app.modules.knowledge_management.routes import router as knowledge_management_router

    # Multi-Channel Communication Hub
    from dario_app.modules.communication_hub.routes import router as communication_hub_router

    # Partner Relationship Management
    from dario_app.modules.partner_relationship_management.routes import router as partner_relationship_router

    # Customer Self-Service Portal
    from dario_app.modules.self_service_portal.routes import router as self_service_portal_router

    # Advanced Security & Threat Intelligence
    from dario_app.modules.security_threat_intelligence.routes import router as security_threat_router

    # Integration Platform / API Management
    from dario_app.modules.integration_platform.routes import router as integration_platform_router

    # Advanced Localization & Multi-currency
    from dario_app.modules.localization.routes import router as localization_router

    # Regulatory Reporting & Tax Management
    from dario_app.modules.regulatory_reporting.routes import router as regulatory_reporting_router

    # Dynamics 365 Copilot & AI Insights
    from dario_app.modules.copilot_ai_insights.routes import router as copilot_ai_router

    # Dynamics 365 Viva - Employee Experience
    from dario_app.modules.viva_employee_experience.routes import router as viva_router

    # Manufacturing Execution System
    from dario_app.modules.manufacturing_execution.routes import router as mes_router

    # Financial Reporting Advanced
    from dario_app.modules.financial_reporting_advanced.routes import router as financial_reporting_router

    # Advanced Inventory Optimization
    from dario_app.modules.advanced_inventory_optimization.routes import router as inventory_optimization_router

    # Real Estate Management
    from dario_app.modules.real_estate_management.routes import router as real_estate_router

    # Advanced Machine Learning Platform
    from dario_app.modules.ml_platform.routes import router as ml_platform_router


    # Oficina Técnica (BOM)
    from dario_app.modules.oficina_tecnica.routes import router as oficina_tecnica_router
    
    # Producción Ordenes
    from dario_app.modules.produccion_ordenes.routes import router as produccion_ordenes_router
    
    # Bombas Omni API
    from dario_app.modules.bombas_omni_api import router as bombas_omni_router
    
    # Demo API (public, no auth)
    from dario_app.modules.demo.routes import router as demo_router
    
    # Puertas (Doors management)
    from dario_app.modules.puertas.routes import router as puertas_router
    
    # Reception and internal logistics
    from dario_app.modules.recepcion.routes import router as recepcion_router
    
    # Workflow Execution Engine
    from dario_app.modules.workflows.routes import router as workflows_router

    # Enterprise Middleware
    from dario_app.middleware.rate_limiter import RateLimitMiddleware
    
    # CORS middleware (production: restrict origins)
    cors_origins = settings.cors_origins.split(",") if settings.cors_origins != "*" else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Rate limiting middleware
    app.add_middleware(RateLimitMiddleware)

    # Include routers
    app.include_router(auth_router)
    app.include_router(tenants_router)
    app.include_router(usuarios_router)
    app.include_router(inventario_router)
    app.include_router(ventas_router)
    app.include_router(compras_router)
    app.include_router(clientes_router)
    app.include_router(pos_router)
    app.include_router(reportes_router)
    app.include_router(documentos_router)
    app.include_router(documentos_adjuntos_router)
    app.include_router(reportes_public_router)
    app.include_router(ai_router)
    app.include_router(calendario_router)
    app.include_router(configuracion_router)
    app.include_router(automatizaciones_router)
    app.include_router(voice_assistant_router)
    app.include_router(tutorial_router)
    app.include_router(crm_router)
    app.include_router(supply_chain_router)
    app.include_router(financial_router)
    app.include_router(hr_router)
    app.include_router(field_service_router)
    app.include_router(project_ops_router)
    app.include_router(customer_service_router)
    app.include_router(marketing_router)
    app.include_router(commerce_router)
    app.include_router(asset_management_router)
    app.include_router(sales_orders_router)
    app.include_router(quality_management_router)
    app.include_router(subscription_billing_router)
    app.include_router(customer_insights_router)
    app.include_router(transportation_router)
    app.include_router(advanced_warehouse_router)
    app.include_router(pim_router)
    app.include_router(recruitment_router)
    app.include_router(service_scheduling_router)
    app.include_router(sustainability_router)
    app.include_router(contract_management_router)
    app.include_router(warranty_router)
    app.include_router(marketing_advanced_router)
    app.include_router(sales_intelligence_router)
    app.include_router(iot_integration_router)
    app.include_router(demand_planning_router)
    app.include_router(business_intelligence_router)
    app.include_router(resource_scheduling_optimization_router)
    app.include_router(compliance_management_router)
    app.include_router(learning_management_router)
    app.include_router(knowledge_management_router)
    app.include_router(communication_hub_router)
    app.include_router(partner_relationship_router)
    app.include_router(self_service_portal_router)
    app.include_router(security_threat_router)
    app.include_router(integration_platform_router)
    app.include_router(localization_router)
    app.include_router(regulatory_reporting_router)
    app.include_router(copilot_ai_router)
    app.include_router(viva_router)
    app.include_router(mes_router)
    app.include_router(financial_reporting_router)
    app.include_router(inventory_optimization_router)
    app.include_router(real_estate_router)
    app.include_router(ml_platform_router)
    app.include_router(oficina_tecnica_router)

    app.include_router(produccion_ordenes_router)
    app.include_router(bombas_omni_router)
    app.include_router(demo_router)
    app.include_router(puertas_router)
    app.include_router(recepcion_router)
    app.include_router(workflows_router)
    app.include_router(security_router)
    
    # Enterprise Features
    from dario_app.modules.enterprise.routes import router as enterprise_router
    app.include_router(enterprise_router)
    
    # Workflow Automation (Dynamics 365-style)
    from dario_app.modules.workflows_automation.routes import router as workflows_automation_router
    app.include_router(workflows_automation_router)
    
    # OData V4 API (Power BI integration)
    from dario_app.modules.odata.routes import router as odata_router
    app.include_router(odata_router)
    
    # GraphQL API (optional)
    if settings.enable_graphql:
        try:
            from dario_app.api.graphql_api import create_graphql_router
            app.include_router(create_graphql_router(), prefix="/graphql", tags=["graphql"])
        except ImportError:
            pass  # GraphQL dependencies not installed

    # Static files and templates
    static_dir = Path(__file__).parent.parent / "static"
    templates_dir = Path(__file__).parent.parent / "templates"

    static_dir.mkdir(exist_ok=True)
    templates_dir.mkdir(exist_ok=True)

    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    templates = Jinja2Templates(directory=str(templates_dir))

    # Root endpoint
    from fastapi import Request
    from fastapi.responses import HTMLResponse

    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request):
        """Serve the landing page."""
        return templates.TemplateResponse("landing.html", {"request": request, "title": settings.app_name})

    @app.get("/demo", response_class=HTMLResponse)
    async def demo(request: Request):
        """Demo page."""
        return templates.TemplateResponse("index.html", {"request": request, "title": settings.app_name})

    @app.get("/terms", response_class=HTMLResponse)
    async def terms(request: Request):
        """Terms and conditions page."""
        from datetime import datetime

        return templates.TemplateResponse(
            "terms.html", {"request": request, "title": "Términos y Condiciones", "now": datetime.now()}
        )

    @app.get("/privacy", response_class=HTMLResponse)
    async def privacy(request: Request):
        """Privacy policy page."""
        from datetime import datetime

        return templates.TemplateResponse(
            "privacy.html", {"request": request, "title": "Política de Privacidad", "now": datetime.now()}
        )

    @app.get("/contact", response_class=HTMLResponse)
    async def contact(request: Request):
        """Contact page."""
        return templates.TemplateResponse("contact.html", {"request": request, "title": "Contacto"})

    @app.get("/app/pos", response_class=HTMLResponse)
    async def pos_page(request: Request):
        """Point of Sale page."""
        return templates.TemplateResponse("pos.html", {"request": request, "title": "Punto de Venta"})

    @app.get("/app/pos/widgets", response_class=HTMLResponse)
    async def pos_widgets_page(request: Request):
        """POS Widgets management page (PRO feature)."""
        return templates.TemplateResponse("pos_widgets.html", {"request": request, "title": "Widgets POS"})

    @app.get("/app/clientes", response_class=HTMLResponse)
    async def clientes_page(request: Request):
        """Customers page."""
        return templates.TemplateResponse("clientes.html", {"request": request, "title": "Clientes"})

    @app.get("/app/proveedores", response_class=HTMLResponse)
    async def proveedores_page(request: Request):
        """Suppliers page."""
        return templates.TemplateResponse("proveedores.html", {"request": request, "title": "Proveedores"})

    @app.get("/app/finanzas", response_class=HTMLResponse)
    async def finanzas_page(request: Request):
        """Unified Finance and Accounting page."""
        return templates.TemplateResponse("finanzas.html", {"request": request, "title": "Finanzas y Contabilidad"})

    @app.get("/app/contabilidad", response_class=HTMLResponse)
    async def contabilidad_page(request: Request):
        """Redirect to unified finance page."""
        return RedirectResponse(url="/app/finanzas", status_code=301)
    
    @app.get("/app/financial", response_class=HTMLResponse)
    async def financial_page(request: Request):
        """Redirect to unified finance page."""
        return RedirectResponse(url="/app/finanzas", status_code=301)

    @app.get("/app/finances", response_class=HTMLResponse)
    async def finances_alias(request: Request):
        """Alias: redirect English path to unified finance page."""
        return RedirectResponse(url="/app/finanzas", status_code=301)

    @app.get("/app/technical-office", response_class=HTMLResponse)
    async def technical_office_alias(request: Request):
        """Alias: redirect English path to Oficina Técnica."""
        return RedirectResponse(url="/app/oficina-tecnica", status_code=301)

    @app.get("/app/ventas", response_class=HTMLResponse)
    async def ventas_page(request: Request):
        """Sales page."""
        return templates.TemplateResponse("ventas.html", {"request": request, "title": "Ventas"})

    @app.get("/app/compras", response_class=HTMLResponse)
    async def compras_page(request: Request):
        """Purchases page."""
        return templates.TemplateResponse("compras.html", {"request": request, "title": "Compras"})

    @app.get("/app/inventario", response_class=HTMLResponse)
    async def inventario_page(request: Request):
        """Inventory page."""
        return templates.TemplateResponse("inventario.html", {"request": request, "title": "Inventario"})

    @app.get("/app/usuarios", response_class=HTMLResponse)
    async def usuarios_page(request: Request):
        """Users, roles and permissions management page."""
        return templates.TemplateResponse(
            "usuarios.html", {"request": request, "title": "Usuarios, Roles & Permisos"}
        )

    @app.get("/app/roles", response_class=HTMLResponse)
    async def roles_page(request: Request):
        """Roles and Permissions page."""
        return templates.TemplateResponse("roles.html", {"request": request, "title": "Roles y Permisos"})

    @app.get("/app/reportes", response_class=HTMLResponse)
    async def reportes_page(request: Request):
        """Reports page."""
        return templates.TemplateResponse("reportes.html", {"request": request, "title": "Reportes"})

    @app.get("/app/calendario", response_class=HTMLResponse)
    async def calendario_page(request: Request):
        """Calendar page."""
        return templates.TemplateResponse("calendario.html", {"request": request, "title": "Calendario"})

    @app.get("/app/configuracion", response_class=HTMLResponse)
    async def configuracion_page(request: Request):
        """System configuration page."""
        return templates.TemplateResponse("configuracion.html", {"request": request, "title": "Configuración del Sistema"})
    @app.get("/app/produccion-ordenes", response_class=HTMLResponse)
    async def produccion_ordenes_page(request: Request):
        """Production orders management page."""
        return templates.TemplateResponse("produccion_ordenes.html", {"request": request, "title": "Órdenes de Producción"})


    @app.get("/app/erp", response_class=HTMLResponse)
    async def erp_landing_page(request: Request):
        """ERP landing page - Entry point to the system."""
        return templates.TemplateResponse("erp_landing.html", {"request": request, "title": "OmniERP - Sistema de Gestión Empresarial"})

    @app.get("/app/correo", response_class=HTMLResponse)
    async def correo_page(request: Request):
        """Email management page."""
        return templates.TemplateResponse("correo.html", {"request": request, "title": "Correo Electrónico"})

    @app.get("/app/documentos", response_class=HTMLResponse)
    async def documentos_page(request: Request):
        """Documents management page."""
        return templates.TemplateResponse("historico_documentos.html", {"request": request, "title": "Histórico de Documentos"})

    @app.get("/app/historico-documentos", response_class=HTMLResponse)
    async def historico_documentos_page(request: Request):
        """Documents history page."""
        return RedirectResponse(url="/app/documentos", status_code=302)

    @app.get("/app/almacen", response_class=HTMLResponse)
    async def almacen_page(request: Request):
        """Warehouse/Almacén management page."""
        return templates.TemplateResponse("almacen.html", {"request": request, "title": "Almacén"})

    @app.get("/app/oficina-tecnica", response_class=HTMLResponse)
    async def oficina_tecnica_page(request: Request):
        """Technical Office/Oficina Técnica management page."""
        return templates.TemplateResponse("oficina_tecnica.html", {"request": request, "title": "Oficina Técnica"})

    @app.get("/app/produccion", response_class=HTMLResponse)
    async def produccion_page(request: Request):
        """Production management page."""
        return templates.TemplateResponse("produccion.html", {"request": request, "title": "Producción"})

    @app.get("/app/puertas", response_class=HTMLResponse)
    async def puertas_page(request: Request):
        """Doors management page - Entry and exit points."""
        return templates.TemplateResponse("puertas.html", {"request": request, "title": "Gestión de Puertas"})

    @app.get("/app/puertas/entrada", response_class=HTMLResponse)
    async def puertas_entrada_page(request: Request):
        """Entry door dashboard - Material reception."""
        response = templates.TemplateResponse("puertas_entrada.html", {"request": request, "title": "Puerta de Entrada"})
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.get("/app/puertas/entrada/debug", response_class=HTMLResponse)
    async def puertas_entrada_debug_page(request: Request):
        """Entry door dashboard - Debug page."""
        return templates.TemplateResponse("puertas_entrada_debug.html", {"request": request, "title": "Debug - Puerta de Entrada"})

    @app.get("/app/voice-assistant", response_class=HTMLResponse)
    async def voice_assistant_page(request: Request):
        """Voice-controlled AI assistant interface."""
        return templates.TemplateResponse("voice_assistant.html", {"request": request, "title": "Asistente de Voz"})

    @app.get("/widget/calendario-demo", response_class=HTMLResponse)
    async def widget_calendario_demo(request: Request):
        """Widget calendar demo page."""
        return templates.TemplateResponse(
            "widget_calendario.html", {"request": request, "title": "Widget de Calendario"}
        )

    @app.get("/widget/calendario", response_class=HTMLResponse)
    async def widget_calendario_iframe(request: Request):
        """Widget calendar iframe."""
        return templates.TemplateResponse(
            "widget_calendario_iframe.html", {"request": request, "title": "Reservar Cita"}
        )

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy", "version": settings.version}

    @app.get("/api/me")
    async def get_current_user_info(request: Request):
        """Get current user information from JWT token."""
        from dario_app.core.auth import get_current_user_org
        
        user_context = await get_current_user_org(request)
        if not user_context:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
        
        return user_context

    @app.get("/app/example", response_class=HTMLResponse)
    async def example_styled_module(request: Request):
        """Example page showing all available CSS components and styles."""
        return templates.TemplateResponse(
            "example_module_styled.html", 
            {"request": request, "title": "Ejemplo de Módulo Estilizado - Componentes CSS"}
        )

    return app


# Create the app instance for use with uvicorn
app = create_app()
