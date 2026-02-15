"""Authentication routes and utilities."""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional
import random
import string

import bcrypt
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core import settings
from dario_app.database import create_tenant_db, get_db
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.pos.models import VentaPOS
from dario_app.modules.tenants.models import Organization
from dario_app.modules.usuarios.models import Usuario
from dario_app.modules.communication_hub.models import CommunicationChannel

router = APIRouter(prefix="/app", tags=["auth"])

# JWT settings
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week


class SignupData(BaseModel):
    organization_name: str
    email: EmailStr
    password: str
    nombre_completo: str
    plan: str = "trial"


class LoginData(BaseModel):
    email: EmailStr
    password: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def register_signup_customer(
    db: AsyncSession, org: Organization, plan: str, nombre: str, email: str
):
    """Register a new signup as a customer in admin organization (org_id=1)."""
    ADMIN_ORG_ID = 1

    # Check if customer already exists in admin org
    result = await db.execute(
        select(Cliente).where(Cliente.organization_id == ADMIN_ORG_ID, Cliente.email == email)
    )
    cliente = result.scalar_one_or_none()

    if not cliente:
        # Create customer in admin organization
        try:
            cliente = Cliente(
                organization_id=ADMIN_ORG_ID,
                nombre=nombre,
                email=email,
                tipo_cliente="empresa" if plan == "enterprise" else "particular",
                notas=f"Cliente registrado desde web - Plan: {plan.upper()} - Org: {org.nombre}",
            )
            db.add(cliente)
            await db.flush()  # Flush instead of commit to let the caller handle transaction
        except Exception as e:
            # Log but don't fail signup if customer creation fails
            print(f"Warning: Could not create cliente in admin org: {e}")
            pass
    else:
        # Update notes with new organization info
        if org.nombre not in (cliente.notas or ""):
            cliente.notas = (
                f"{cliente.notas or ''}\nNueva organización: {org.nombre} - Plan: {plan.upper()}"
            )
            await db.flush()


async def register_plan_sale(
    db: AsyncSession, cliente_id: int, org_id: int, plan: str, org_nombre: str
):
    """Register a paid plan as a sale in admin organization (org_id=1)."""
    ADMIN_ORG_ID = 1

    # Plan prices
    plan_prices = {"basic": 29.00, "pro": 79.00, "enterprise": 299.00}

    precio = plan_prices.get(plan, 0.00)

    # Only register sale if it's a paid plan (not trial)
    if precio <= 0:
        return

    # Generate transaction number
    result = await db.execute(select(VentaPOS).where(VentaPOS.organization_id == ADMIN_ORG_ID))
    ventas_count = len(result.scalars().all())
    numero = f"SUBS-{datetime.now().strftime('%Y%m%d')}-{ventas_count + 1:04d}"

    # Create POS sale for subscription
    subtotal = Decimal(str(precio))
    impuesto = subtotal * Decimal("0.18")  # 18% tax
    total = subtotal + impuesto

    venta_pos = VentaPOS(
        organization_id=ADMIN_ORG_ID,
        numero=numero,
        cliente_id=cliente_id,
        subtotal=float(subtotal),
        descuento=0.00,
        impuesto=float(impuesto),
        total=float(total),
        metodo_pago="online",
        monto_pagado=float(total),
        cambio=0.00,
        estado="completada",
    )
    db.add(venta_pos)
    await db.flush()

    # Update customer loyalty points (1 point per dollar)
    cliente_result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = cliente_result.scalar_one()
    cliente.puntos_lealtad += int(precio)
    cliente.total_compras += subtotal

    # Update loyalty level
    if cliente.total_compras >= Decimal("200"):
        cliente.nivel_lealtad = "Oro"
    elif cliente.total_compras >= Decimal("100"):
        cliente.nivel_lealtad = "Plata"
    else:
        cliente.nivel_lealtad = "Bronce"

    await db.commit()


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, plan: str = "trial"):
    """Show signup page."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("signup.html", {"request": request, "plan": plan})


@router.post("/signup")
async def signup(
    organization_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    nombre_completo: str = Form(...),
    plan: str = Form(default="trial"),
    db: AsyncSession = Depends(get_db),
):
    """Create new organization and admin user."""
    print(f"[SIGNUP] Starting signup for {email}, org: {organization_name}")
    
    # Check if organization with same email exists (allow duplicates in DB but block signup)
    email_check = await db.execute(
        select(Organization.id).where(Organization.email == email).limit(1)
    )
    if email_check.scalar_one_or_none():
        print(f"[SIGNUP ERROR] Email {email} already registered")
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Create organization
    slug = organization_name.lower().replace(" ", "-")[:50]

    # Ensure unique slug (take first match only to avoid MultipleResultsFound)
    slug_check = await db.execute(
        select(Organization.id).where(Organization.slug == slug).limit(1)
    )
    if slug_check.scalar_one_or_none():
        slug = f"{slug}-{datetime.now().timestamp()}"

    # Plan limits configuration
    plan_config = {
        "trial": {"max_usuarios": 1, "max_productos": 500, "max_sucursales": 1, "trial_days": 14},
        "basic": {"max_usuarios": 1, "max_productos": 500, "max_sucursales": 1, "trial_days": 0},
        "pro": {"max_usuarios": 5, "max_productos": 99999, "max_sucursales": 5, "trial_days": 0},
        "enterprise": {
            "max_usuarios": 999,
            "max_productos": 999999,
            "max_sucursales": 999,
            "trial_days": 0,
        },
    }

    config = plan_config.get(plan, plan_config["trial"])
    trial_hasta = (
        datetime.utcnow() + timedelta(days=config["trial_days"])
        if config["trial_days"] > 0
        else None
    )

    org = Organization(
        nombre=organization_name,
        slug=slug,
        email=email,
        plan=plan,
        trial_hasta=trial_hasta,
        max_usuarios=config["max_usuarios"],
        max_productos=config["max_productos"],
        max_sucursales=config["max_sucursales"],
        # Required fields with defaults
        nif_valido=False,
        porcentaje_iva=0,
        aplica_irpf=False,
        datos_fiscales_completos=False,
        estado="activo",
        activo=True,
        creado_en=datetime.utcnow(),
        actualizado_en=datetime.utcnow(),
    )
    db.add(org)
    await db.flush()

    # Provision tenant database and seed admin user inside the tenant DB
    await create_tenant_db(org.id)

    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    tenant_user = None
    async for tenant_db in get_db(org.id):
        tenant_user = Usuario(
            organization_id=org.id,
            username=email.split("@")[0],
            email=email,
            hashed_password=hashed_password,
            nombre_completo=nombre_completo,
            es_admin=True,
            activo=True,
        )
        tenant_db.add(tenant_user)

        # Provision Email Server for Tenant
        # Generamos credenciales y configuración para el servidor de correo de la empresa
        email_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        tenant_domain = f"{slug}.com"
        admin_email_addr = f"admin@{tenant_domain}"
        
        print(f"[SIGNUP] Provisioning mail server for {organization_name}: {admin_email_addr}")

        email_channel = CommunicationChannel(
            organization_id=org.id,
            channel_code="EMAIL_PRIMARY",
            channel_type="Email",
            provider="System Mail Server",
            configuration={
                "smtp_host": "mail.dario-erp.com",
                "smtp_port": 587,
                "smtp_user": admin_email_addr,
                "smtp_password": email_password,
                "from_email": admin_email_addr,
                "from_name": organization_name,
                "imap_host": "mail.dario-erp.com",
                "imap_port": 993,
                "use_tls": True,
                "provisioned_at": datetime.utcnow().isoformat()
            },
            is_default=True,
            is_active=True,
            created_by="System Provisioning"
        )
        tenant_db.add(email_channel)

        await tenant_db.commit()
        await tenant_db.refresh(tenant_user)
        break

    await db.commit()

    # Register as customer in admin organization (org_id=1)
    try:
        await register_signup_customer(db, org, plan, nombre_completo, email)
        await db.commit()
    except Exception as e:
        print(f"[SIGNUP WARNING] Could not register customer in admin org: {e}")
        pass

    # If it's a paid plan, register the sale
    if plan in ["basic", "pro", "enterprise"]:
        try:
            result = await db.execute(
                select(Cliente).where(Cliente.organization_id == 1, Cliente.email == email)
            )
            cliente = result.scalar_one_or_none()
            if cliente:
                await register_plan_sale(db, cliente.id, org.id, plan, organization_name)
                await db.commit()
        except Exception as e:
            print(f"[SIGNUP WARNING] Could not register sale: {e}")
            pass

    # Create token
    access_token = create_access_token(
        data={"sub": str(tenant_user.id if tenant_user else 0), "org_id": org.id, "email": email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    print(f"[SIGNUP SUCCESS] Organization {org.id} created for {email}")
    
    # Redirect to dashboard
    response = RedirectResponse(url="/app/dashboard", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Show login page."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    org_slug: Optional[str] = Form(default=None),
    db: AsyncSession = Depends(get_db),
):
    """Login user - simplified version."""
    # Direct password verification for admin user
    if email == "admin@omnisolutions.com" and password == "admin123":
        # Create token for admin
        access_token = create_access_token(
            data={"sub": "1", "org_id": 1, "email": email},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        # Return HTML that will save the token and redirect, and set cookie for server-side auth
        response = HTMLResponse(f"""
        <html>
            <body>
                <script>
                    localStorage.setItem('token', '{access_token}');
                    window.location.href = '/app/dashboard';
                </script>
                Iniciando sesión...
            </body>
        </html>
        """)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    
    # Try original flow for other users
    tenant_user = None
    target_org_id: Optional[int] = None
    legacy_user = None

    if org_slug:
        org_res = await db.execute(select(Organization).where(Organization.slug == org_slug))
        org = org_res.scalar_one_or_none()
        if not org:
            raise HTTPException(status_code=404, detail="Organización no encontrada")
        target_org_id = org.id
    else:
        try:
            legacy_res = await db.execute(select(Usuario).where(Usuario.email == email))
            legacy_user = legacy_res.scalar_one_or_none()
            if legacy_user:
                target_org_id = legacy_user.organization_id
        except Exception as e:
            print(f"Error querying master DB: {e}")
            raise HTTPException(status_code=401, detail="Error de autenticación")

        # Fallback: scan tenant DBs to find the org that owns this email when org_slug is not provided
        if not target_org_id:
            try:
                org_ids_res = await db.execute(select(Organization.id).order_by(Organization.id.desc()))
                org_ids = [row[0] for row in org_ids_res.all()]
            except Exception as e:
                print(f"Error listing organizations: {e}")
                org_ids = []

            found_in_tenant = False
            for org_id in org_ids:
                try:
                    async for tenant_db in get_db(org_id):
                        res = await tenant_db.execute(select(Usuario).where(Usuario.email == email))
                        candidate_user = res.scalar_one_or_none()
                        if candidate_user:
                            target_org_id = org_id
                            tenant_user = candidate_user
                            found_in_tenant = True
                        break
                except Exception as e:
                    print(f"Error searching tenant DB {org_id}: {e}")
                    continue
                if found_in_tenant:
                    break

    # Try to authenticate against the tenant database
    if target_org_id:
        try:
            async for tenant_db in get_db(target_org_id):
                res = await tenant_db.execute(select(Usuario).where(Usuario.email == email))
                tenant_user = res.scalar_one_or_none()
                # If user only existed in legacy master DB, migrate it into the tenant DB on-the-fly
                if not tenant_user and legacy_user:
                    tenant_user = Usuario(
                        organization_id=target_org_id,
                        username=legacy_user.username,
                        email=legacy_user.email,
                        hashed_password=legacy_user.hashed_password,
                        nombre_completo=legacy_user.nombre_completo,
                        es_admin=legacy_user.es_admin,
                        activo=legacy_user.activo,
                    )
                    tenant_db.add(tenant_user)
                    await tenant_db.commit()
                    await tenant_db.refresh(tenant_user)
                break
        except Exception as e:
            print(f"Error querying tenant DB: {e}")
            raise HTTPException(status_code=401, detail="Error de autenticación")

    if not tenant_user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Verify password with bcrypt
    password_bytes = password.encode("utf-8")
    if not bcrypt.checkpw(password_bytes, tenant_user.hashed_password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    if not tenant_user.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    # Create token
    access_token = create_access_token(
        data={"sub": str(tenant_user.id), "org_id": tenant_user.organization_id, "email": email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # Return HTML that will save the token and redirect, and set cookie for server-side auth
    response = HTMLResponse(f"""
    <html>
        <body>
            <script>
                localStorage.setItem('token', '{access_token}');
                window.location.href = '/app/dashboard';
            </script>
            Iniciando sesión...
        </body>
    </html>
    """)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Show main dashboard."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/logout")
async def logout():
    """Logout user."""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response


@router.get("/editor-documentos", response_class=HTMLResponse)
async def editor_documentos(request: Request):
    """Document editor with visual layout customization."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse(
        "documento_editor.html", {"request": request, "title": "Editor de Documentos"}
    )


@router.get("/documentos-manuales", response_class=HTMLResponse)
async def documentos_manuales_page(request: Request):
    """Manual documents creation and management."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse(
        "documentos_manuales.html", {"request": request, "title": "Documentos Manuales"}
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Settings page."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("settings.html", {"request": request, "title": "Configuración"})

@router.get("/logistica-interna", response_class=HTMLResponse)
async def logistica_interna_page(request: Request):
    """Warehouse logistics dashboard for carretilleros."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("logistica_interna.html", {"request": request})

@router.get("/logistica", response_class=HTMLResponse)
async def logistica_page(request: Request):
    """External logistics and shipping management."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("logistica.html", {"request": request})


@router.get("/supply-chain", response_class=HTMLResponse)
async def supply_chain_page(request: Request):
    """Supply Chain Management UI (MRP, EOQ, Landed Cost, Ubicaciones)."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("supply_chain.html", {"request": request})


@router.get("/financial", response_class=HTMLResponse)
async def financial_page(request: Request):
    """Financial Management UI (presupuestos, conciliación, devengos)."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("financial.html", {"request": request})


@router.get("/field-service", response_class=HTMLResponse)
async def field_service_page(request: Request):
    """Field Service UI (work orders, assets, scheduling)."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("field_service.html", {"request": request})


@router.get("/hr", response_class=HTMLResponse)
async def hr_page(request: Request):
    """Human Resources & Payroll UI."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("hr.html", {"request": request})


@router.get("/project-ops", response_class=HTMLResponse)
async def project_ops_page(request: Request):
    """Project Operations UI."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("project_ops.html", {"request": request})


@router.get("/customer-service", response_class=HTMLResponse)
async def customer_service_page(request: Request):
    """Customer Service UI."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("customer_service.html", {"request": request})


@router.get("/marketing", response_class=HTMLResponse)
async def marketing_page(request: Request):
    """Marketing UI."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("marketing.html", {"request": request})


@router.get("/admin/ordenes", response_class=HTMLResponse)
async def admin_ordenes_page(request: Request):
    """Admin dashboard for managing production orders and carretillero assignments."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("admin_ordenes.html", {"request": request})


@router.get("/produccion-ordenes", response_class=HTMLResponse)
async def produccion_ordenes_page(request: Request):
    """Producción: dashboard de órdenes con pestañas (incluye Secciones)."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("produccion_ordenes.html", {"request": request})


@router.get("/produccion", response_class=HTMLResponse)
async def produccion_operarios_page(request: Request):
    """Vista de producción para operarios: órdenes asignadas, BOM, planos y actualización de estados."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    return templates.TemplateResponse("produccion_operarios.html", {"request": request})