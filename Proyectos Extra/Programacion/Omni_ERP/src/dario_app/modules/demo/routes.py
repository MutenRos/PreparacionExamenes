"""Public API endpoints for demo data without authentication."""

import sqlite3
from decimal import Decimal
from pathlib import Path
from typing import List
from datetime import datetime, timedelta

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import func, select

from dario_app.database import create_tenant_db, get_db as get_async_db
from dario_app.modules.auth.routes import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from dario_app.modules.inventario.models import Producto
from dario_app.modules.tenants.models import Organization
from dario_app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/api/demo", tags=["demo"])

# Import auth for debug endpoint
from dario_app.core.auth import get_current_user_org
from fastapi import Request

# Corrected path: use /src/data not /src/dario_app/data
DB_PATH = Path(__file__).parent.parent.parent.parent / "data" / "org_dbs" / "org_1.db"


def get_db():
    """Get a direct SQLite connection."""
    return sqlite3.connect(DB_PATH)


def ensure_produccion_tables(conn: sqlite3.Connection):
    """Create production-related tables if missing (demo safety net)."""
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ordenes_produccion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            venta_id INTEGER NOT NULL,
            bom_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            numero VARCHAR(50) UNIQUE NOT NULL,
            descripcion VARCHAR(500),
            cantidad_ordenada FLOAT NOT NULL DEFAULT 1.0,
            cantidad_completada FLOAT DEFAULT 0.0,
            cantidad_rechazada FLOAT DEFAULT 0.0,
            estado VARCHAR(50) NOT NULL DEFAULT 'pendiente_asignacion',
            prioridad VARCHAR(50) NOT NULL DEFAULT 'media',
            fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fecha_inicio_estimada DATETIME,
            fecha_fin_estimada DATETIME,
            fecha_inicio_real DATETIME,
            fecha_fin_real DATETIME,
            asignado_a VARCHAR(100),
            centro_trabajo VARCHAR(100),
            costo_materiales NUMERIC(10, 2) DEFAULT 0,
            costo_mano_obra NUMERIC(10, 2) DEFAULT 0,
            costo_operaciones_externas NUMERIC(10, 2) DEFAULT 0,
            costo_total NUMERIC(10, 2) DEFAULT 0,
            notas_produccion TEXT,
            notas_internas TEXT
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS operaciones_produccion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            orden_produccion_id INTEGER NOT NULL,
            bom_operacion_id INTEGER NOT NULL,
            secuencia INTEGER DEFAULT 10,
            duracion_estimada FLOAT,
            duracion_real FLOAT,
            estado VARCHAR(50) NOT NULL DEFAULT 'pendiente_asignacion',
            asignado_a VARCHAR(100),
            centro_trabajo VARCHAR(100),
            fecha_inicio_estimada DATETIME,
            fecha_fin_estimada DATETIME,
            fecha_inicio_real DATETIME,
            fecha_fin_real DATETIME,
            inspecciones_realizadas BOOLEAN DEFAULT 0,
            resultado_control_calidad VARCHAR(50),
            comentarios_qc TEXT,
            defectos_encontrados TEXT,
            acciones_correctivas TEXT
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movimientos_almacen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            orden_produccion_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            tipo_movimiento VARCHAR(50) NOT NULL,
            cantidad FLOAT NOT NULL,
            ubicacion_origen VARCHAR(100),
            ubicacion_destino VARCHAR(100),
            estado VARCHAR(50) DEFAULT 'pendiente',
            fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fecha_movimiento DATETIME,
            responsable VARCHAR(100),
            observaciones TEXT
        );
        """
    )
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ordenes_produccion_org ON ordenes_produccion(organization_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ordenes_produccion_estado ON ordenes_produccion(estado);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_operaciones_produccion_orden ON operaciones_produccion(orden_produccion_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_movimientos_almacen_orden ON movimientos_almacen(orden_produccion_id);")
    conn.commit()


@router.get("/jdm-demo-login", response_class=HTMLResponse)
async def jdm_demo_login(force_refresh: bool = False):
    """Provision and auto-login into the 90s JDM dealership demo without credentials.
    
    Args:
        force_refresh: If True, delete and recreate all products. Use ?force_refresh=true
    """
    demo_slug = "demo-jdm-90s"
    demo_email = "demo.jdm@omnierp.test"
    demo_name = "JDM Legends 90s"
    demo_password = "demo-jdm-90s"

    org = None
    async for master_db in get_async_db():
        res = await master_db.execute(select(Organization).where(Organization.slug == demo_slug))
        org = res.scalar_one_or_none()
        if not org:
            org = Organization(
                nombre=demo_name,
                slug=demo_slug,
                tipo_negocio="Concesionario y alquiler JDM 90s",
                descripcion="Demo pública: compra y alquiler de coches japoneses de los 90, sin login.",
                email=demo_email,
                plan="trial",
                estado="active",
                max_usuarios=5,
                max_productos=500,
                max_sucursales=1,
            )
            master_db.add(org)
            await master_db.commit()
            await master_db.refresh(org)
        break

    if org is None:
        raise HTTPException(status_code=500, detail="No se pudo preparar la demo JDM")

    await create_tenant_db(org.id)

    user = None
    async for tenant_db in get_async_db(org.id):
        user_res = await tenant_db.execute(select(Usuario).where(Usuario.email == demo_email))
        user = user_res.scalar_one_or_none()
        if not user:
            hashed = bcrypt.hashpw(demo_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            user = Usuario(
                organization_id=org.id,
                username="demo-jdm",
                email=demo_email,
                nombre_completo="Demo Concesionario JDM",
                hashed_password=hashed,
                es_admin=True,
                activo=True,
            )
            tenant_db.add(user)
            await tenant_db.commit()
            await tenant_db.refresh(user)

        # If force_refresh, delete all products first
        if force_refresh:
            from sqlalchemy import delete
            await tenant_db.execute(delete(Producto).where(Producto.organization_id == org.id))
            await tenant_db.commit()

        count_res = await tenant_db.execute(select(func.count(Producto.id)))
        product_count = count_res.scalar_one()
        if product_count == 0 or force_refresh:
            cars = [
                {
                    "codigo": "JDM-R32-GTR",
                    "nombre": "Nissan Skyline GT-R R32 (Venta)",
                    "descripcion": "Godzilla importado, volante a la derecha, historial de mantenimiento completo.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 73000,
                    "precio_compra": 58000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom A",
                },
                {
                    "codigo": "JDM-SUPRA-A80",
                    "nombre": "Toyota Supra MkIV 2JZ (Venta)",
                    "descripcion": "Twin-turbo 6MT de 1997, especificación japonesa con 2JZ-GTE.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 82000,
                    "precio_compra": 66000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom A",
                },
                {
                    "codigo": "JDM-NSX-NA1",
                    "nombre": "Honda NSX NA1 (Venta)",
                    "descripcion": "Chasis de aluminio, VTEC 3.0, mantenimiento oficial Honda Japón.",
                    "categoria": "JDM - Superdeportivos",
                    "precio_venta": 98000,
                    "precio_compra": 78000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom B",
                },
                {
                    "codigo": "JDM-FD3S",
                    "nombre": "Mazda RX-7 FD3S (Venta)",
                    "descripcion": "Rotativo 13B-REW biturbo, rebuild hace 5.000 km, listo para track days.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 62000,
                    "precio_compra": 48000,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Showroom B",
                },
                {
                    "codigo": "JDM-LC80",
                    "nombre": "Toyota Land Cruiser 80 VX (Venta)",
                    "descripcion": "4x4 icónico con bloqueos, ideal para importación y proyectos overlanding.",
                    "categoria": "JDM - 4x4",
                    "precio_venta": 45000,
                    "precio_compra": 36000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Patio 4x4",
                },
                {
                    "codigo": "JDM-R32-RENT",
                    "nombre": "Nissan Skyline GT-R R32 (Alquiler)",
                    "descripcion": "Paquetes track day y fin de semana con seguro incluido.",
                    "categoria": "Alquiler - Deportivos",
                    "precio_venta": 590,
                    "precio_compra": 0,
                    "stock": 2,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler A",
                },
                {
                    "codigo": "JDM-SUPRA-RENT",
                    "nombre": "Toyota Supra MkIV (Alquiler)",
                    "descripcion": "2JZ-GTE automático, entrega con telemetría básica y combustible premium.",
                    "categoria": "Alquiler - Deportivos",
                    "precio_venta": 540,
                    "precio_compra": 0,
                    "stock": 2,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler A",
                },
                {
                    "codigo": "JDM-MIATA-RENT",
                    "nombre": "Mazda MX-5 NA (Alquiler)",
                    "descripcion": "Roadster ligero para rutas costeras, ideal para experiencias en pareja.",
                    "categoria": "Alquiler - Roadsters",
                    "precio_venta": 220,
                    "precio_compra": 0,
                    "stock": 3,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler B",
                },
                {
                    "codigo": "JDM-PAJERO-RENT",
                    "nombre": "Mitsubishi Pajero Evo (Alquiler)",
                    "descripcion": "Homologado rally raid, incluye guía offroad y puntos de entrega flexibles.",
                    "categoria": "Alquiler - 4x4",
                    "precio_venta": 350,
                    "precio_compra": 0,
                    "stock": 2,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler B",
                },
                {
                    "codigo": "JDM-NSX-RENT",
                    "nombre": "Honda NSX NA1 (Alquiler VIP)",
                    "descripcion": "Experiencia premium con instructor y briefing de pista incluido.",
                    "categoria": "Alquiler - Superdeportivos",
                    "precio_venta": 820,
                    "precio_compra": 0,
                    "stock": 1,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler VIP",
                },
                {
                    "codigo": "JDM-EVO6-TME",
                    "nombre": "Mitsubishi Lancer Evolution VI TME (Venta)",
                    "descripcion": "Tommi Makinen Edition, 280 CV, 4G63T, solo 2.500 unidades fabricadas.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 68000,
                    "precio_compra": 54000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom A",
                },
                {
                    "codigo": "JDM-WRX-STI-GC8",
                    "nombre": "Subaru Impreza WRX STi Type R GC8 (Venta)",
                    "descripcion": "22B tribute, 2-puertas, boxer EJ20, rally heritage certificado.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 58000,
                    "precio_compra": 46000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom B",
                },
                {
                    "codigo": "JDM-S15-SILVIA",
                    "nombre": "Nissan Silvia S15 Spec-R (Venta)",
                    "descripcion": "SR20DET, 6MT, volante RHD, nunca modificado, historial completo.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 49000,
                    "precio_compra": 39000,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Showroom B",
                },
                {
                    "codigo": "JDM-R34-GTR",
                    "nombre": "Nissan Skyline GT-R R34 V-Spec (Venta)",
                    "descripcion": "La evolución de Godzilla, RB26DETT, N1 block, midnight purple II.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 145000,
                    "precio_compra": 118000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom VIP",
                },
                {
                    "codigo": "JDM-INTEGRA-R",
                    "nombre": "Honda Integra Type R DC2 (Venta)",
                    "descripcion": "Championship white, B18C, 8.000 RPM, asientos Recaro originales.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 42000,
                    "precio_compra": 34000,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Showroom B",
                },
                {
                    "codigo": "JDM-CIVIC-EK9",
                    "nombre": "Honda Civic Type R EK9 (Venta)",
                    "descripcion": "1.6 VTEC B16B, 185 CV/tonelada, homologado para circuito.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 39000,
                    "precio_compra": 31000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom B",
                },
                {
                    "codigo": "JDM-SW20-MR2",
                    "nombre": "Toyota MR2 SW20 Turbo (Venta)",
                    "descripcion": "Motor central 3S-GTE, T-top removible, japones spec.",
                    "categoria": "JDM - Deportivos",
                    "precio_venta": 34000,
                    "precio_compra": 27000,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Patio Exterior",
                },
                {
                    "codigo": "JDM-AE86-TRUENO",
                    "nombre": "Toyota Sprinter Trueno AE86 (Venta)",
                    "descripcion": "Panda trueno, 4A-GE 16V, LSD, la leyenda de Initial D.",
                    "categoria": "JDM - Clásicos",
                    "precio_venta": 41000,
                    "precio_compra": 33000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom A",
                },
                {
                    "codigo": "JDM-S2000-AP1",
                    "nombre": "Honda S2000 AP1 (Venta)",
                    "descripcion": "F20C 9.000 RPM, berlina wind edition, roadster purasangre.",
                    "categoria": "JDM - Roadsters",
                    "precio_venta": 52000,
                    "precio_compra": 42000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom A",
                },
                {
                    "codigo": "JDM-SOARER",
                    "nombre": "Toyota Soarer JZZ30 (Venta)",
                    "descripcion": "Gran turismo 2JZ-GTE, luxury cruiser, importación reciente.",
                    "categoria": "JDM - Gran Turismo",
                    "precio_venta": 38000,
                    "precio_compra": 30000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Patio Exterior",
                },
                {
                    "codigo": "JDM-EVO9-RENT",
                    "nombre": "Mitsubishi Lancer Evolution IX (Alquiler)",
                    "descripcion": "MIVEC 4G63, ACD, paquete track day con telemetría avanzada.",
                    "categoria": "Alquiler - Deportivos",
                    "precio_venta": 480,
                    "precio_compra": 0,
                    "stock": 2,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler A",
                },
                {
                    "codigo": "JDM-INTEGRA-R-RENT",
                    "nombre": "Honda Integra Type R DC2 (Alquiler)",
                    "descripcion": "Experiencia VTEC pura, ideal para rutas de montaña y curvas.",
                    "categoria": "Alquiler - Deportivos",
                    "precio_venta": 320,
                    "precio_compra": 0,
                    "stock": 2,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler B",
                },
                {
                    "codigo": "JDM-S2000-RENT",
                    "nombre": "Honda S2000 AP1 (Alquiler)",
                    "descripcion": "Roadster F20C, top descapotable, rutas costeras premium.",
                    "categoria": "Alquiler - Roadsters",
                    "precio_venta": 380,
                    "precio_compra": 0,
                    "stock": 2,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler B",
                },
                {
                    "codigo": "JDM-CAMRY-V6",
                    "nombre": "Toyota Camry V6 XV10 (Venta)",
                    "descripcion": "Sedan familiar 3.0 V6, automático, ideal para importación económica.",
                    "categoria": "JDM - Sedanes",
                    "precio_venta": 6500,
                    "precio_compra": 4800,
                    "stock": 3,
                    "es_alquiler": False,
                    "ubicacion": "Patio Económicos",
                },
                {
                    "codigo": "JDM-ACCORD-CD",
                    "nombre": "Honda Accord CD5 SiR (Venta)",
                    "descripcion": "Sedan deportivo H22A VTEC, transmisión manual, muy buscado.",
                    "categoria": "JDM - Sedanes",
                    "precio_venta": 9800,
                    "precio_compra": 7500,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Patio Económicos",
                },
                {
                    "codigo": "JDM-COROLLA-AE100",
                    "nombre": "Toyota Corolla AE101 (Venta)",
                    "descripcion": "4A-FE económico, bajo kilometraje, mantenimiento al día.",
                    "categoria": "JDM - Compactos",
                    "precio_venta": 5200,
                    "precio_compra": 3900,
                    "stock": 4,
                    "es_alquiler": False,
                    "ubicacion": "Patio Económicos",
                },
                {
                    "codigo": "JDM-CIVIC-EG",
                    "nombre": "Honda Civic EG6 SiR (Venta)",
                    "descripcion": "Hatchback B16A VTEC, ligero y divertido, proyecto o daily.",
                    "categoria": "JDM - Compactos",
                    "precio_venta": 11500,
                    "precio_compra": 8900,
                    "stock": 3,
                    "es_alquiler": False,
                    "ubicacion": "Patio Económicos",
                },
                {
                    "codigo": "JDM-LEGACY-GT",
                    "nombre": "Subaru Legacy GT Wagon BH5 (Venta)",
                    "descripcion": "Familiar deportivo boxer turbo, AWD, ideal para familias activas.",
                    "categoria": "JDM - Familiares",
                    "precio_venta": 12800,
                    "precio_compra": 9800,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Patio 4x4",
                },
                {
                    "codigo": "JDM-ODYSSEY-RA",
                    "nombre": "Honda Odyssey RA1 Absolute (Venta)",
                    "descripcion": "MPV 7 plazas, puertas correderas, familia numerosa JDM style.",
                    "categoria": "JDM - Familiares",
                    "precio_venta": 8900,
                    "precio_compra": 6700,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Patio Económicos",
                },
                {
                    "codigo": "JDM-DELICA-D5",
                    "nombre": "Mitsubishi Delica Space Gear (Venta)",
                    "descripcion": "4x4 camperizable, diesel turbo, outdoor lifestyle ready.",
                    "categoria": "JDM - 4x4",
                    "precio_venta": 14500,
                    "precio_compra": 11200,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Patio 4x4",
                },
                {
                    "codigo": "JDM-CROWN-MS",
                    "nombre": "Toyota Crown Majesta JZS171 (Venta)",
                    "descripcion": "Luxury sedan V8 1UZ-FE, asientos eléctricos, executive class.",
                    "categoria": "JDM - Sedanes Premium",
                    "precio_venta": 13500,
                    "precio_compra": 10200,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom B",
                },
                {
                    "codigo": "JDM-PRIMERA-P11",
                    "nombre": "Nissan Primera P11 GT (Venta)",
                    "descripcion": "Sedan deportivo SR20DE, suspensión sport, underdog fiable.",
                    "categoria": "JDM - Sedanes",
                    "precio_venta": 6800,
                    "precio_compra": 5100,
                    "stock": 3,
                    "es_alquiler": False,
                    "ubicacion": "Patio Económicos",
                },
                {
                    "codigo": "JDM-STAGEA-260RS",
                    "nombre": "Nissan Stagea 260RS (Venta)",
                    "descripcion": "Wagon deportivo RB26DETT (motor GT-R), sleeper familiar único.",
                    "categoria": "JDM - Familiares",
                    "precio_venta": 28000,
                    "precio_compra": 22000,
                    "stock": 1,
                    "es_alquiler": False,
                    "ubicacion": "Showroom B",
                },
                {
                    "codigo": "JDM-HIACE-VAN",
                    "nombre": "Toyota HiAce Super GL (Venta)",
                    "descripcion": "Van comercial o camper conversion, diesel, ultra confiable.",
                    "categoria": "JDM - Comerciales",
                    "precio_venta": 11200,
                    "precio_compra": 8500,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Patio Exterior",
                },
                {
                    "codigo": "JDM-FORESTER-SF",
                    "nombre": "Subaru Forester SF5 STi (Venta)",
                    "descripcion": "SUV compacto turbo, perfecto para nieve y offroad ligero.",
                    "categoria": "JDM - 4x4",
                    "precio_venta": 13800,
                    "precio_compra": 10600,
                    "stock": 2,
                    "es_alquiler": False,
                    "ubicacion": "Patio 4x4",
                },
                {
                    "codigo": "JDM-HIACE-RENT",
                    "nombre": "Toyota HiAce Super GL (Alquiler)",
                    "descripcion": "Van para mudanzas, roadtrips o proyectos, 10 plazas disponibles.",
                    "categoria": "Alquiler - Utilitarios",
                    "precio_venta": 95,
                    "precio_compra": 0,
                    "stock": 3,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler Utilitarios",
                },
                {
                    "codigo": "JDM-DELICA-RENT",
                    "nombre": "Mitsubishi Delica Space Gear (Alquiler)",
                    "descripcion": "Adventure van 4x4, incluye equipo camping básico, para grupos.",
                    "categoria": "Alquiler - Utilitarios",
                    "precio_venta": 145,
                    "precio_compra": 0,
                    "stock": 2,
                    "es_alquiler": True,
                    "ubicacion": "Alquiler Utilitarios",
                },
            ]

            for car in cars:
                tenant_db.add(
                    Producto(
                        organization_id=org.id,
                        codigo=car["codigo"],
                        sku=car.get("sku"),
                        nombre=car["nombre"],
                        descripcion=car["descripcion"],
                        categoria=car["categoria"],
                        precio_compra=Decimal(str(car["precio_compra"])),
                        precio_venta=Decimal(str(car["precio_venta"])),
                        margen_porcentaje=Decimal("25"),
                        stock_actual=car["stock"],
                        stock_minimo=0,
                        cantidad_minima_compra=1,
                        unidad_medida="vehiculo",
                        ubicacion_almacen=car.get("ubicacion"),
                        proveedor_id=None,
                        activo=True,
                        visible_en_pos=True,
                        es_alquiler=car["es_alquiler"],
                    )
                )

            await tenant_db.commit()
        break

    if user is None:
        raise HTTPException(status_code=500, detail="No se pudo preparar el usuario demo")

    access_token = create_access_token(
        data={"sub": str(user.id), "org_id": org.id, "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = HTMLResponse(
        f"""
        <html>
            <body>
                <script>
                    localStorage.setItem('token', '{access_token}');
                    window.location.href = '/app/dashboard';
                </script>
                Accediendo a la demo de concesionario JDM...
            </body>
        </html>
        """
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.post("/seed-partes-bombas")
async def seed_partes_bombas():
    """Populate inventory with pump parts and components."""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Clear existing parts (keep pumps)
        cursor.execute("DELETE FROM productos WHERE organization_id = 1 AND categoria LIKE '%Parte%'")
        
        # Pump parts and components
        partes = [
            # MOTORES
            {"codigo": "MOT-0.5HP", "nombre": "Motor Eléctrico 0.5 HP", "categoria": "Partes - Motores", "precio": 145.00, "stock": 25},
            {"codigo": "MOT-0.75HP", "nombre": "Motor Eléctrico 0.75 HP", "categoria": "Partes - Motores", "precio": 185.00, "stock": 30},
            {"codigo": "MOT-1HP", "nombre": "Motor Eléctrico 1 HP", "categoria": "Partes - Motores", "precio": 220.00, "stock": 35},
            {"codigo": "MOT-1.5HP", "nombre": "Motor Eléctrico 1.5 HP", "categoria": "Partes - Motores", "precio": 285.00, "stock": 28},
            {"codigo": "MOT-2HP", "nombre": "Motor Eléctrico 2 HP", "categoria": "Partes - Motores", "precio": 350.00, "stock": 22},
            {"codigo": "MOT-3HP", "nombre": "Motor Eléctrico 3 HP", "categoria": "Partes - Motores", "precio": 465.00, "stock": 18},
            {"codigo": "MOT-5HP", "nombre": "Motor Eléctrico 5 HP", "categoria": "Partes - Motores", "precio": 720.00, "stock": 15},
            {"codigo": "MOT-7.5HP", "nombre": "Motor Eléctrico 7.5 HP", "categoria": "Partes - Motores", "precio": 980.00, "stock": 12},
            {"codigo": "MOT-10HP", "nombre": "Motor Eléctrico 10 HP", "categoria": "Partes - Motores", "precio": 1250.00, "stock": 10},
            {"codigo": "MOT-15HP", "nombre": "Motor Eléctrico 15 HP", "categoria": "Partes - Motores", "precio": 1680.00, "stock": 8},
            {"codigo": "MOT-20HP", "nombre": "Motor Eléctrico 20 HP", "categoria": "Partes - Motores", "precio": 2150.00, "stock": 6},
            
            # IMPULSORES
            {"codigo": "IMP-50MM-BRONCE", "nombre": "Impulsor 50mm Bronce", "categoria": "Partes - Impulsores", "precio": 85.00, "stock": 40},
            {"codigo": "IMP-65MM-BRONCE", "nombre": "Impulsor 65mm Bronce", "categoria": "Partes - Impulsores", "precio": 105.00, "stock": 35},
            {"codigo": "IMP-80MM-BRONCE", "nombre": "Impulsor 80mm Bronce", "categoria": "Partes - Impulsores", "precio": 135.00, "stock": 30},
            {"codigo": "IMP-50MM-INOX", "nombre": "Impulsor 50mm AISI 316", "categoria": "Partes - Impulsores", "precio": 125.00, "stock": 35},
            {"codigo": "IMP-65MM-INOX", "nombre": "Impulsor 65mm AISI 316", "categoria": "Partes - Impulsores", "precio": 155.00, "stock": 30},
            {"codigo": "IMP-80MM-INOX", "nombre": "Impulsor 80mm AISI 316", "categoria": "Partes - Impulsores", "precio": 195.00, "stock": 25},
            {"codigo": "IMP-100MM-INOX", "nombre": "Impulsor 100mm AISI 316", "categoria": "Partes - Impulsores", "precio": 245.00, "stock": 20},
            
            # CARCASAS Y VOLUTES
            {"codigo": "CARC-50-FUND", "nombre": "Carcasa 50mm Fundición", "categoria": "Partes - Carcasas", "precio": 95.00, "stock": 30},
            {"codigo": "CARC-65-FUND", "nombre": "Carcasa 65mm Fundición", "categoria": "Partes - Carcasas", "precio": 125.00, "stock": 25},
            {"codigo": "CARC-80-FUND", "nombre": "Carcasa 80mm Fundición", "categoria": "Partes - Carcasas", "precio": 165.00, "stock": 20},
            {"codigo": "CARC-50-INOX", "nombre": "Carcasa 50mm AISI 316", "categoria": "Partes - Carcasas", "precio": 185.00, "stock": 25},
            {"codigo": "CARC-65-INOX", "nombre": "Carcasa 65mm AISI 316", "categoria": "Partes - Carcasas", "precio": 235.00, "stock": 20},
            {"codigo": "CARC-80-INOX", "nombre": "Carcasa 80mm AISI 316", "categoria": "Partes - Carcasas", "precio": 295.00, "stock": 15},
            
            # EJES
            {"codigo": "EJE-10MM-INOX", "nombre": "Eje 10mm Ø AISI 304", "categoria": "Partes - Ejes", "precio": 35.00, "stock": 50},
            {"codigo": "EJE-12MM-INOX", "nombre": "Eje 12mm Ø AISI 304", "categoria": "Partes - Ejes", "precio": 42.00, "stock": 45},
            {"codigo": "EJE-14MM-INOX", "nombre": "Eje 14mm Ø AISI 304", "categoria": "Partes - Ejes", "precio": 48.00, "stock": 40},
            {"codigo": "EJE-16MM-INOX", "nombre": "Eje 16mm Ø AISI 304", "categoria": "Partes - Ejes", "precio": 55.00, "stock": 35},
            {"codigo": "EJE-20MM-INOX", "nombre": "Eje 20mm Ø AISI 316", "categoria": "Partes - Ejes", "precio": 75.00, "stock": 30},
            {"codigo": "EJE-25MM-INOX", "nombre": "Eje 25mm Ø AISI 316", "categoria": "Partes - Ejes", "precio": 95.00, "stock": 25},
            
            # SELLOS MECÁNICOS
            {"codigo": "SELLO-10MM", "nombre": "Sello Mecánico 10mm", "categoria": "Partes - Sellos", "precio": 28.00, "stock": 60},
            {"codigo": "SELLO-12MM", "nombre": "Sello Mecánico 12mm", "categoria": "Partes - Sellos", "precio": 32.00, "stock": 55},
            {"codigo": "SELLO-14MM", "nombre": "Sello Mecánico 14mm", "categoria": "Partes - Sellos", "precio": 36.00, "stock": 50},
            {"codigo": "SELLO-16MM", "nombre": "Sello Mecánico 16mm", "categoria": "Partes - Sellos", "precio": 42.00, "stock": 45},
            {"codigo": "SELLO-20MM", "nombre": "Sello Mecánico 20mm", "categoria": "Partes - Sellos", "precio": 52.00, "stock": 40},
            {"codigo": "SELLO-25MM-CARB", "nombre": "Sello Mecánico 25mm Carburo", "categoria": "Partes - Sellos", "precio": 85.00, "stock": 30},
            
            # RODAMIENTOS
            {"codigo": "ROD-6201", "nombre": "Rodamiento 6201 ZZ", "categoria": "Partes - Rodamientos", "precio": 8.50, "stock": 100},
            {"codigo": "ROD-6202", "nombre": "Rodamiento 6202 ZZ", "categoria": "Partes - Rodamientos", "precio": 9.50, "stock": 90},
            {"codigo": "ROD-6203", "nombre": "Rodamiento 6203 ZZ", "categoria": "Partes - Rodamientos", "precio": 11.00, "stock": 85},
            {"codigo": "ROD-6204", "nombre": "Rodamiento 6204 ZZ", "categoria": "Partes - Rodamientos", "precio": 13.50, "stock": 80},
            {"codigo": "ROD-6205", "nombre": "Rodamiento 6205 ZZ", "categoria": "Partes - Rodamientos", "precio": 16.00, "stock": 75},
            {"codigo": "ROD-6206", "nombre": "Rodamiento 6206 ZZ", "categoria": "Partes - Rodamientos", "precio": 19.50, "stock": 70},
            
            # JUNTAS Y EMPAQUETADURAS
            {"codigo": "JUNTA-50MM-NBR", "nombre": "Junta 50mm NBR", "categoria": "Partes - Juntas", "precio": 4.50, "stock": 120},
            {"codigo": "JUNTA-65MM-NBR", "nombre": "Junta 65mm NBR", "categoria": "Partes - Juntas", "precio": 5.50, "stock": 110},
            {"codigo": "JUNTA-80MM-NBR", "nombre": "Junta 80mm NBR", "categoria": "Partes - Juntas", "precio": 6.80, "stock": 100},
            {"codigo": "JUNTA-50MM-VITON", "nombre": "Junta 50mm Viton", "categoria": "Partes - Juntas", "precio": 12.50, "stock": 80},
            {"codigo": "JUNTA-65MM-VITON", "nombre": "Junta 65mm Viton", "categoria": "Partes - Juntas", "precio": 15.00, "stock": 75},
            {"codigo": "JUNTA-80MM-VITON", "nombre": "Junta 80mm Viton", "categoria": "Partes - Juntas", "precio": 18.50, "stock": 70},
            
            # TORNILLERÍA
            {"codigo": "TORN-M6X20-INOX", "nombre": "Tornillo M6x20 AISI 304 (Pack 10)", "categoria": "Partes - Tornillería", "precio": 3.20, "stock": 200},
            {"codigo": "TORN-M8X25-INOX", "nombre": "Tornillo M8x25 AISI 304 (Pack 10)", "categoria": "Partes - Tornillería", "precio": 4.50, "stock": 180},
            {"codigo": "TORN-M10X30-INOX", "nombre": "Tornillo M10x30 AISI 304 (Pack 10)", "categoria": "Partes - Tornillería", "precio": 6.20, "stock": 160},
            {"codigo": "TORN-M12X40-INOX", "nombre": "Tornillo M12x40 AISI 316 (Pack 10)", "categoria": "Partes - Tornillería", "precio": 9.50, "stock": 140},
            
            # PRENSAESTOPAS
            {"codigo": "PRENSA-12MM", "nombre": "Prensaestopas 12mm Latón", "categoria": "Partes - Prensaestopas", "precio": 15.00, "stock": 60},
            {"codigo": "PRENSA-16MM", "nombre": "Prensaestopas 16mm Latón", "categoria": "Partes - Prensaestopas", "precio": 18.50, "stock": 55},
            {"codigo": "PRENSA-20MM", "nombre": "Prensaestopas 20mm Latón", "categoria": "Partes - Prensaestopas", "precio": 22.00, "stock": 50},
            {"codigo": "PRENSA-25MM-INOX", "nombre": "Prensaestopas 25mm AISI 316", "categoria": "Partes - Prensaestopas", "precio": 38.00, "stock": 40},
            
            # DIFUSORES
            {"codigo": "DIF-50MM-BRONCE", "nombre": "Difusor 50mm Bronce", "categoria": "Partes - Difusores", "precio": 65.00, "stock": 35},
            {"codigo": "DIF-65MM-BRONCE", "nombre": "Difusor 65mm Bronce", "categoria": "Partes - Difusores", "precio": 82.00, "stock": 30},
            {"codigo": "DIF-50MM-INOX", "nombre": "Difusor 50mm AISI 316", "categoria": "Partes - Difusores", "precio": 95.00, "stock": 30},
            {"codigo": "DIF-65MM-INOX", "nombre": "Difusor 65mm AISI 316", "categoria": "Partes - Difusores", "precio": 118.00, "stock": 25},
            
            # CABLES Y CONECTORES
            {"codigo": "CABLE-3X2.5", "nombre": "Cable Sumergible 3x2.5mm (metro)", "categoria": "Partes - Cables", "precio": 4.80, "stock": 500},
            {"codigo": "CABLE-3X4", "nombre": "Cable Sumergible 3x4mm (metro)", "categoria": "Partes - Cables", "precio": 6.50, "stock": 400},
            {"codigo": "CABLE-3X6", "nombre": "Cable Sumergible 3x6mm (metro)", "categoria": "Partes - Cables", "precio": 8.80, "stock": 350},
            {"codigo": "CONECTOR-IP68", "nombre": "Conector IP68 para Cable Sumergible", "categoria": "Partes - Conectores", "precio": 28.00, "stock": 80},
            
            # VÁLVULAS Y ACCESORIOS
            {"codigo": "VALV-CHECK-50", "nombre": "Válvula Check 50mm Bronce", "categoria": "Partes - Válvulas", "precio": 35.00, "stock": 45},
            {"codigo": "VALV-CHECK-65", "nombre": "Válvula Check 65mm Bronce", "categoria": "Partes - Válvulas", "precio": 45.00, "stock": 40},
            {"codigo": "VALV-CHECK-80", "nombre": "Válvula Check 80mm Bronce", "categoria": "Partes - Válvulas", "precio": 58.00, "stock": 35},
            {"codigo": "MANOMETRO-10BAR", "nombre": "Manómetro 0-10 Bar con Glicerina", "categoria": "Partes - Instrumentos", "precio": 22.00, "stock": 60},
            {"codigo": "PRESOSTATO-AUTO", "nombre": "Presostato Automático Regulable", "categoria": "Partes - Controles", "precio": 48.00, "stock": 50},
        ]
        
        for parte in partes:
            cursor.execute(
                """INSERT INTO productos 
                   (organization_id, codigo, nombre, categoria, precio_venta, precio_compra, 
                    stock_actual, stock_minimo, unidad_medida, activo, visible_en_pos, 
                    creado_en, actualizado_en)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                (1, parte["codigo"], parte["nombre"], parte["categoria"], 
                 parte["precio"], parte["precio"] * 0.55, parte["stock"], 10, "unidad", 1, 0)
            )
        
        conn.commit()
        return {"success": True, "message": f"Se añadieron {len(partes)} partes y componentes de bombas", "count": len(partes)}
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.post("/seed-bombas-ideal")
async def seed_bombas_ideal():
    """Populate inventory with real pumps from Bombas Ideal catalog."""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Clear existing products
        cursor.execute("DELETE FROM productos WHERE organization_id = 1")
        
        # Real pump data from bombasideal.com
        bombas = [
            # BOMBAS HORIZONTALES
            {"codigo": "CP-50-125", "nombre": "Bomba Centrífuga Horizontal Cámara Partida CP-50-125", "categoria": "Horizontales", "precio": 2850.00, "stock": 5},
            {"codigo": "CP-65-160", "nombre": "Bomba Centrífuga Horizontal Cámara Partida CP-65-160", "categoria": "Horizontales", "precio": 3200.00, "stock": 3},
            {"codigo": "CP-80-200", "nombre": "Bomba Centrífuga Horizontal Cámara Partida CP-80-200", "categoria": "Horizontales", "precio": 4500.00, "stock": 4},
            {"codigo": "CEB-100", "nombre": "Bomba Centrífuga Autoaspirante CEB-100", "categoria": "Horizontales", "precio": 1850.00, "stock": 8},
            {"codigo": "CEB-150", "nombre": "Bomba Centrífuga Autoaspirante CEB-150", "categoria": "Horizontales", "precio": 2100.00, "stock": 6},
            {"codigo": "RFXA-50", "nombre": "Electrobomba Monobloc Inox RFXA-50", "categoria": "Horizontales", "precio": 1650.00, "stock": 10},
            {"codigo": "RFXA-65", "nombre": "Electrobomba Monobloc Inox RFXA-65", "categoria": "Horizontales", "precio": 1890.00, "stock": 7},
            {"codigo": "RN-50-125", "nombre": "Bomba Centrífuga Horizontal Aspiración Axial RN-50-125", "categoria": "Horizontales", "precio": 1420.00, "stock": 12},
            {"codigo": "RN-65-160", "nombre": "Bomba Centrífuga Horizontal Aspiración Axial RN-65-160", "categoria": "Horizontales", "precio": 1680.00, "stock": 9},
            {"codigo": "RNL-50", "nombre": "Bomba Vertical In-Line RNL-50", "categoria": "Horizontales", "precio": 1590.00, "stock": 11},
            {"codigo": "RNI-80", "nombre": "Bomba Horizontal Normalizada RNI-80", "categoria": "Horizontales", "precio": 1750.00, "stock": 8},
            {"codigo": "GNI-65", "nombre": "Bomba Monoblock Normalizada GNI-65", "categoria": "Horizontales", "precio": 1480.00, "stock": 10},
            {"codigo": "RFI-50", "nombre": "Electrobomba Monoblock Eje Prolongado RFI-50", "categoria": "Horizontales", "precio": 1320.00, "stock": 15},
            
            # BOMBAS SUMERGIDAS
            {"codigo": "S4-10", "nombre": "Electrobomba Sumergida 4\" Serie S", "categoria": "Sumergidas", "precio": 980.00, "stock": 20},
            {"codigo": "S4-15", "nombre": "Electrobomba Sumergida 4\" Serie S (15 etapas)", "categoria": "Sumergidas", "precio": 1180.00, "stock": 18},
            {"codigo": "SD4-12", "nombre": "Electrobomba Sumergida 4\" Serie SD", "categoria": "Sumergidas", "precio": 1250.00, "stock": 16},
            {"codigo": "SD6-18", "nombre": "Electrobomba Sumergida 6\" Serie SD", "categoria": "Sumergidas", "precio": 1850.00, "stock": 12},
            {"codigo": "SD8-20", "nombre": "Electrobomba Sumergida 8\" Serie SD", "categoria": "Sumergidas", "precio": 2650.00, "stock": 8},
            {"codigo": "SDX4-15", "nombre": "Electrobomba Sumergida 4\" Serie SDX (AISI 316)", "categoria": "Sumergidas", "precio": 1680.00, "stock": 14},
            {"codigo": "SDX6-20", "nombre": "Electrobomba Sumergida 6\" Serie SDX (AISI 316)", "categoria": "Sumergidas", "precio": 2380.00, "stock": 10},
            {"codigo": "SDX8-25", "nombre": "Electrobomba Sumergida 8\" Serie SDX (AISI 316)", "categoria": "Sumergidas", "precio": 3450.00, "stock": 6},
            {"codigo": "SDX10-30", "nombre": "Electrobomba Sumergida 10\" Serie SDX (AISI 316)", "categoria": "Sumergidas", "precio": 4850.00, "stock": 4},
            {"codigo": "ST4-12", "nombre": "Electrobomba Sumergida 4\" Serie ST/STI", "categoria": "Sumergidas", "precio": 1120.00, "stock": 15},
            {"codigo": "ST6-16", "nombre": "Electrobomba Sumergida 6\" Serie ST/STI", "categoria": "Sumergidas", "precio": 1680.00, "stock": 11},
            {"codigo": "TRITON-4", "nombre": "Electrobomba Sumergida 4\" Serie TRITON", "categoria": "Sumergidas", "precio": 890.00, "stock": 22},
            {"codigo": "TRITON-6", "nombre": "Electrobomba Sumergida 6\" Serie TRITON", "categoria": "Sumergidas", "precio": 1250.00, "stock": 18},
            {"codigo": "SVHT-4", "nombre": "Electrobomba Sumergida Flujo Axial SVHT-4", "categoria": "Sumergidas", "precio": 2150.00, "stock": 7},
            {"codigo": "SVA-6", "nombre": "Electrobomba Sumergida Flujo Axial SVA-6", "categoria": "Sumergidas", "precio": 2450.00, "stock": 6},
            {"codigo": "SVAT-8", "nombre": "Electrobomba Sumergida Flujo Axial SVAT-8", "categoria": "Sumergidas", "precio": 3200.00, "stock": 5},
            
            # BOMBAS MULTICELULARES
            {"codigo": "VIPH-32/4", "nombre": "Electrobomba Multicelular Horizontal VIPH-32/4", "categoria": "Multicelulares", "precio": 1980.00, "stock": 9},
            {"codigo": "VIPH-50/6", "nombre": "Electrobomba Multicelular Horizontal VIPH-50/6", "categoria": "Multicelulares", "precio": 2450.00, "stock": 7},
            {"codigo": "NLV-32/4", "nombre": "Multicelular Vertical In-Line NLV-32/4", "categoria": "Multicelulares", "precio": 1750.00, "stock": 12},
            {"codigo": "NLV-50/6", "nombre": "Multicelular Vertical In-Line NLV-50/6", "categoria": "Multicelulares", "precio": 2180.00, "stock": 8},
            {"codigo": "NLX-32/4", "nombre": "Multicelular Vertical In-Line NLX-32/4 (AISI 316)", "categoria": "Multicelulares", "precio": 2350.00, "stock": 6},
            {"codigo": "NLX-50/6", "nombre": "Multicelular Vertical In-Line NLX-50/6 (AISI 316)", "categoria": "Multicelulares", "precio": 2980.00, "stock": 5},
            {"codigo": "VIPV-32/5", "nombre": "Electrobomba Multicelular Vertical VIPV-32/5", "categoria": "Multicelulares", "precio": 1850.00, "stock": 10},
            {"codigo": "VIPV-50/7", "nombre": "Electrobomba Multicelular Vertical VIPV-50/7", "categoria": "Multicelulares", "precio": 2320.00, "stock": 7},
            {"codigo": "NXA-32/6", "nombre": "Electrobomba Multicelular Vertical NXA-32/6", "categoria": "Multicelulares", "precio": 2100.00, "stock": 8},
            {"codigo": "NXA-50/8", "nombre": "Electrobomba Multicelular Vertical NXA-50/8", "categoria": "Multicelulares", "precio": 2650.00, "stock": 6},
            {"codigo": "APM-50-4", "nombre": "Bomba Multicelular Alta Presión APM-50-4", "categoria": "Multicelulares", "precio": 3200.00, "stock": 4},
            {"codigo": "APM-65-6", "nombre": "Bomba Multicelular Alta Presión APM-65-6", "categoria": "Multicelulares", "precio": 3850.00, "stock": 3},
            
            # BOMBAS VERTICALES
            {"codigo": "VT-100", "nombre": "Bomba Vertical VT-100", "categoria": "Verticales", "precio": 3500.00, "stock": 5},
            {"codigo": "VT-150", "nombre": "Bomba Vertical VT-150", "categoria": "Verticales", "precio": 4200.00, "stock": 3},
            
            # EQUIPOS HYDRO
            {"codigo": "HYDRO-2P", "nombre": "Grupo Hydro 2 Bombas", "categoria": "Grupos Hydro", "precio": 5200.00, "stock": 2},
            {"codigo": "HYDRO-3P", "nombre": "Grupo Hydro 3 Bombas", "categoria": "Grupos Hydro", "precio": 6800.00, "stock": 2},
        ]
        
        for bomba in bombas:
            cursor.execute(
                """INSERT INTO productos 
                   (organization_id, codigo, nombre, categoria, precio_venta, precio_compra, 
                    stock_actual, stock_minimo, unidad_medida, activo, visible_en_pos, 
                    creado_en, actualizado_en)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
                (1, bomba["codigo"], bomba["nombre"], bomba["categoria"], 
                 bomba["precio"], bomba["precio"] * 0.6, bomba["stock"], 5, "unidad", 1, 1)
            )
        
        conn.commit()
        return {"success": True, "message": f"Se añadieron {len(bombas)} bombas del catálogo Bombas Ideal", "count": len(bombas)}
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.post("/seed")
async def seed_database():
    """Seed the database with demo data (one-time operation)."""
    if not DB_PATH.exists():
        return {"error": "Database not initialized yet. Start the server first."}
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM productos WHERE organization_id = 1")
        count = cursor.fetchone()[0]
        
        if count > 0:
            return {"message": "Database already seeded"}
        
        # Insert proveedores
        proveedores = [
            ("Motores Industriales SA", "contacto@motores-industriales.mx", "+52 555 1234 5678", "Carlos Mendoza", "Av. Industrial 123, CDMX", "30 días", 7, "RFC: MIS-001"),
            ("Aceros y Metales Import", "ventas@aceros-metal.mx", "+52 555 2345 6789", "María González", "Blvd. Sur 456, Monterrey", "45 días", 10, "RFC: AMI-002"),
            ("Plásticos y Polímeros Ltd", "orden@plasticos-polimeros.mx", "+52 555 3456 7890", "Juan López", "Carretera Central 789, Puebla", "30 días", 5, "RFC: PPL-003"),
            ("Electrónica Profesional", "compras@electronica-pro.mx", "+52 555 4567 8901", "Roberto Sánchez", "Av. Tecnología 321, Guadalajara", "Net 30", 8, "RFC: ELP-004"),
            ("Componentes Hidráulicos", "sales@componentes-hidra.mx", "+52 555 5678 9012", "Alfredo García", "Parque Industrial 654, León", "60 días", 14, "RFC: CHI-005"),
            ("Pintura Industrial México", "ventas@pintura-industrial.mx", "+52 555 6789 0123", "Patricia Ruiz", "Zona Industrial 987, Querétaro", "Net 45", 6, "RFC: PIM-006"),
            ("Empaques y Logística", "logistica@empaques-log.mx", "+52 555 7890 1234", "Sofía Martínez", "Centro Logístico 246, Toluca", "Net 30", 3, "RFC: EYL-007"),
        ]
        
        now = datetime.utcnow().isoformat()
        for prov in proveedores:
            cursor.execute("""
                INSERT INTO proveedores 
                (organization_id, nombre, email, telefono, contacto_nombre, direccion, terminos_pago, dias_entrega_promedio, documento_proveedor, es_activo, creado_en, actualizado_en)
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """, (*prov, now, now))
        
        # Insert clientes
        clientes = [
            ("Hidroservicios del Norte", "Hidroservicios del Norte SA de CV", "HSN-001-0001", "empresa", "compras@hidroservicios-norte.mx", "+52 555 1000 1111", "Av. Agua 100", "Monterrey", "Nuevo León", "64000"),
            ("Sistemas de Riego Agrícola", "Sistemas de Riego Agrícola SA", "SRA-002-0002", "empresa", "ventas@riego-agricola.mx", "+52 555 2000 2222", "Carretera Federal 200", "Guanajuato", "Guanajuato", "36000"),
            ("Acuacultura México", "Acuacultura México SC", "ACM-003-0003", "empresa", "operaciones@acuacultura-mx.mx", "+52 555 3000 3333", "Puerto 300", "Veracruz", "Veracruz", "91700"),
            ("Constructoras y Proyectos", "Constructoras y Proyectos SA", "CYP-004-0004", "empresa", "adquisiciones@const-proyectos.mx", "+52 555 4000 4444", "Edificio 400", "CDMX", "CDMX", "01200"),
            ("Minería y Extracción", "Minería y Extracción Industrial", "MEI-005-0005", "empresa", "suministros@mineria-extraccion.mx", "+52 555 5000 5555", "Mina 500", "Zacatecas", "Zacatecas", "98000"),
            ("Industria Textil del Bajío", "Industria Textil del Bajío SA", "ITB-006-0006", "empresa", "compras@textil-bajio.mx", "+52 555 6000 6666", "Textile Park 600", "Aguascalientes", "Aguascalientes", "20000"),
            ("Generación de Energía Verde", "Generación de Energía Verde SA", "GEV-007-0007", "empresa", "proyectos@energia-verde.mx", "+52 555 7000 7777", "Solar Farm 700", "Durango", "Durango", "34000"),
            ("Distribuidora Integral Técnica", "Distribuidora Integral Técnica", "DIT-008-0008", "empresa", "mayorista@dist-integral.mx", "+52 555 8000 8888", "Zona Comercial 800", "Guadalajara", "Jalisco", "44100"),
        ]
        
        for cliente in clientes:
            cursor.execute("""
                INSERT INTO clientes 
                (organization_id, nombre, razon_social, nif_nie, nif_valido, tipo_cliente, email, telefono, domicilio, municipio, provincia, codigo_postal, puntos_lealtad, nivel_lealtad, total_compras, activo, creado_en, actualizado_en)
                VALUES (1, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, 0, 'Plata', 0, 1, ?, ?)
            """, (*cliente, now, now))
        
        # Insert productos
        productos = [
            ("BC-100-001", "PUMP-BC100-2024", "Bomba Centrífuga BC-100", "Bomba centrífuga de 1 HP, flujo 50 L/min, presión 2 bar", "Bombas - Acabadas", 450.00, 720.00, 20, 15, 5, 1),
            ("BS-200-001", "PUMP-BS200-2024", "Bomba Sumergible BS-200", "Bomba sumergible 2 HP, profundidad 50m, caudal 80 L/min", "Bombas - Acabadas", 680.00, 1100.00, 20, 12, 4, 1),
            ("BA-150-001", "PUMP-BA150-2024", "Bomba Axial BA-150", "Bomba axial 1.5 HP, caudal 120 L/min, para sistemas de refrigeración", "Bombas - Acabadas", 520.00, 850.00, 20, 8, 3, 1),
            ("BD-300-001", "PUMP-BD300-2024", "Bomba Diafragma BD-300", "Bomba diafragma 3 HP, caudal variable 200 L/min, baja vibración", "Bombas - Acabadas", 890.00, 1450.00, 20, 6, 2, 1),
            ("BP-180-001", "PUMP-BP180-2024", "Bomba Periférica BP-180", "Bomba periférica 2.5 HP, caudal 100 L/min, para pequeños sistemas", "Bombas - Acabadas", 620.00, 1000.00, 20, 10, 3, 1),
            ("BI-500-001", "PUMP-BI500-2024", "Bomba Industrial BI-500", "Bomba industrial de gran caudal, 5 HP, 300 L/min, aplicaciones pesadas", "Bombas - Acabadas", 1250.00, 2000.00, 20, 4, 1, 1),
            ("MOT-1HP-001", "MOTOR-1HP-IE3", "Motor Eléctrico 1 HP IE3", "Motor 1 HP 3 fases, 1700 RPM, eficiencia IE3", "Motores", 280.00, 450.00, 20, 25, 10, 0),
            ("MOT-2HP-001", "MOTOR-2HP-IE3", "Motor Eléctrico 2 HP IE3", "Motor 2 HP 3 fases, 1700 RPM, eficiencia IE3", "Motores", 420.00, 680.00, 20, 18, 8, 0),
            ("MOT-3HP-001", "MOTOR-3HP-IE3", "Motor Eléctrico 3 HP IE3", "Motor 3 HP 3 fases, 1700 RPM, eficiencia IE3", "Motores", 580.00, 950.00, 20, 12, 5, 0),
            ("MOT-5HP-001", "MOTOR-5HP-IE3", "Motor Eléctrico 5 HP IE3", "Motor 5 HP 3 fases, 1700 RPM, eficiencia IE3", "Motores", 890.00, 1450.00, 20, 8, 3, 0),
            ("CHASS-STD-001", "CHASSIS-STANDARD", "Chasis Estándar Acero", "Chasis de acero inoxidable para montaje de bombas", "Componentes", 95.00, 150.00, 1, 50, 20, 0),
            ("MANG-PVC-001", "HOSE-PVC-FLEX", "Manguito PVC Flexible", "Manguito de PVC flexible 5m para conexiones", "Componentes", 35.00, 55.00, 1, 120, 50, 0),
            ("HELM-ACERO-001", "IMPELLER-STEEL", "Hélice Acero Inoxidable", "Hélice de acero inoxidable 6 aspas para centrifugas", "Componentes", 120.00, 200.00, 1, 40, 15, 0),
            ("SELLO-MECA-001", "SEAL-MECHANICAL", "Sello Mecánico", "Sello mecánico para eje de bombas centrifugas", "Componentes", 45.00, 75.00, 1, 80, 30, 0),
            ("RODAMIENTOS-1-001", "BEARING-6206", "Rodamiento 6206", "Rodamiento de bola serie 6206", "Componentes", 28.00, 45.00, 1, 200, 80, 0),
            ("KIT-MANTEN-001", "KIT-MAINTENANCE", "Kit Mantenimiento Anual", "Kit completo de mantenimiento anual para bombas", "Servicios", 150.00, 250.00, 1, 30, 10, 1),
            ("INST-PROFESIONAL", "SERVICE-INSTALL", "Instalación Profesional", "Servicio de instalación profesional en sitio", "Servicios", 0.00, 500.00, 1, 999, 0, 1),
        ]
        
        for prod in productos:
            cursor.execute("""
                INSERT INTO productos 
                (organization_id, codigo, sku, nombre, descripcion, categoria, precio_compra, precio_venta, margen_porcentaje, stock_actual, stock_minimo, unidad_medida, activo, visible_en_pos, creado_en, actualizado_en)
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'unidad', 1, ?, ?, ?)
            """, (*prod, now, now))
        
        conn.commit()
        return {
            "message": "Database seeded successfully",
            "proveedores": len(proveedores),
            "clientes": len(clientes),
            "productos": len(productos),
        }
        
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()


@router.get("/productos", response_model=List[dict])
async def get_productos_demo():
    """Get all products (demo data, no auth required)."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, codigo, nombre, sku, categoria, precio_compra, precio_venta, stock_actual, stock_minimo
        FROM productos
        WHERE organization_id = 1
        ORDER BY categoria, nombre
    """)
    productos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return productos


@router.get("/proveedores", response_model=List[dict])
async def get_proveedores_demo():
    """Get all suppliers (demo data, no auth required)."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, email, telefono, contacto_nombre, direccion, terminos_pago
        FROM proveedores
        WHERE organization_id = 1
        ORDER BY nombre
    """)
    proveedores = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return proveedores


@router.get("/clientes", response_model=List[dict])
async def get_clientes_demo():
    """Get all customers (demo data, no auth required)."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre, razon_social, email, telefono, municipio, provincia
        FROM clientes
        WHERE organization_id = 1
        ORDER BY nombre
    """)
    clientes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return clientes


@router.get("/stats", response_model=dict)
async def get_stats_demo():
    """Get general statistics."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Count products
    cursor.execute("SELECT COUNT(*) as total, SUM(CAST(stock_actual as REAL) * CAST(precio_compra as REAL)) as valor FROM productos WHERE organization_id = 1")
    prod_row = dict(cursor.fetchone())
    
    # Count bajo stock
    cursor.execute("SELECT COUNT(*) as bajo_stock FROM productos WHERE organization_id = 1 AND stock_actual < stock_minimo")
    bajo_stock = dict(cursor.fetchone())
    
    # Count suppliers
    cursor.execute("SELECT COUNT(*) as total FROM proveedores WHERE organization_id = 1")
    prov_row = dict(cursor.fetchone())
    
    # Count customers
    cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE organization_id = 1")
    cli_row = dict(cursor.fetchone())
    
    conn.close()
    
    return {
        "productos_total": prod_row.get("total", 0),
        "productos_bajo_stock": bajo_stock.get("bajo_stock", 0),
        "valor_inventario": round(prod_row.get("valor", 0) or 0, 2),
        "proveedores": prov_row.get("total", 0),
        "clientes": cli_row.get("total", 0),
    }


@router.get("/debug/user-context")
async def debug_user_context(request: Request):
    """Debug endpoint to see user org_id."""
    user = await get_current_user_org(request)
    return {"user_context": user, "has_auth": user is not None}


@router.post("/seed-boms-bombas")
async def seed_boms_bombas():
    """Create BOMs (Bills of Materials) for ALL 45 pump models."""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Clear existing BOMs
        cursor.execute("DELETE FROM bom_lines WHERE bom_header_id IN (SELECT id FROM bom_headers WHERE organization_id = 1)")
        cursor.execute("DELETE FROM bom_headers WHERE organization_id = 1")
        
        # Define component templates by pump type/series
        bom_templates = {
            # HORIZONTALES
            "CP-50": [("MOT-1.5HP", 1), ("IMP-50MM-BRONCE", 1), ("CARC-50-FUND", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-50MM-NBR", 4), ("TORN-M8X25-INOX", 8), ("DIF-50MM-BRONCE", 1)],
            "CP-65": [("MOT-2HP", 1), ("IMP-65MM-BRONCE", 1), ("CARC-65-FUND", 1), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 2), ("ROD-6203", 2), ("JUNTA-65MM-NBR", 4), ("TORN-M10X30-INOX", 10), ("DIF-65MM-BRONCE", 1)],
            "CP-80": [("MOT-3HP", 1), ("IMP-80MM-BRONCE", 1), ("CARC-80-FUND", 1), ("EJE-16MM-INOX", 1), ("SELLO-16MM", 2), ("ROD-6204", 2), ("JUNTA-80MM-NBR", 5), ("TORN-M10X30-INOX", 12), ("DIF-80MM-BRONCE", 1), ("VALV-CHECK-50", 1)],
            "RN-50": [("MOT-2HP", 1), ("IMP-50MM-BRONCE", 1), ("CARC-50-FUND", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-50MM-NBR", 4), ("TORN-M8X25-INOX", 8), ("DIF-50MM-BRONCE", 1)],
            "RN-65": [("MOT-2.2HP", 1), ("IMP-65MM-BRONCE", 1), ("CARC-65-FUND", 1), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 2), ("ROD-6203", 2), ("JUNTA-65MM-NBR", 4), ("TORN-M10X30-INOX", 10), ("DIF-65MM-BRONCE", 1)],
            "RNI": [("MOT-2HP", 1), ("IMP-80MM-BRONCE", 1), ("CARC-80-FUND", 1), ("EJE-16MM-INOX", 1), ("SELLO-16MM", 2), ("ROD-6204", 2), ("JUNTA-80MM-NBR", 5), ("TORN-M10X30-INOX", 12), ("DIF-80MM-BRONCE", 1)],
            "RFI": [("MOT-1.5HP", 1), ("IMP-50MM-BRONCE", 1), ("CARC-50-FUND", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-50MM-NBR", 4), ("TORN-M8X25-INOX", 8), ("DIF-50MM-BRONCE", 1)],
            "RFXA": [("MOT-2HP", 1), ("IMP-65MM-INOX", 1), ("CARC-65-INOX", 1), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 2), ("ROD-6203", 2), ("JUNTA-65MM-VITON", 4), ("TORN-M10X30-INOX", 10), ("DIF-65MM-INOX", 1)],
            "GNI": [("MOT-2HP", 1), ("IMP-65MM-BRONCE", 1), ("CARC-65-FUND", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-50MM-NBR", 4), ("TORN-M8X25-INOX", 8), ("DIF-65MM-BRONCE", 1)],
            "CEB": [("MOT-2HP", 1), ("IMP-65MM-BRONCE", 1), ("CARC-65-FUND", 1), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 2), ("ROD-6203", 2), ("JUNTA-65MM-NBR", 4), ("TORN-M10X30-INOX", 10), ("DIF-65MM-BRONCE", 1)],
            
            # SUMERGIDAS
            "SDX4": [("MOT-1HP", 1), ("IMP-50MM-INOX", 1), ("CARC-50-INOX", 1), ("EJE-10MM-INOX", 1), ("SELLO-10MM", 2), ("ROD-6201", 2), ("JUNTA-50MM-VITON", 3), ("CABLE-3X2.5", 50), ("CONECTOR-IP68", 1), ("PRENSA-12MM", 1)],
            "SDX6": [("MOT-1.5HP", 1), ("IMP-65MM-INOX", 1), ("CARC-65-INOX", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-65MM-VITON", 4), ("CABLE-3X4", 50), ("CONECTOR-IP68", 1), ("PRENSA-16MM", 1), ("MANOMETRO-10BAR", 1)],
            "SDX8": [("MOT-2HP", 1), ("IMP-80MM-INOX", 1), ("CARC-80-INOX", 1), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 2), ("ROD-6203", 2), ("JUNTA-80MM-VITON", 5), ("CABLE-3X6", 100), ("CONECTOR-IP68", 1), ("PRENSA-20MM", 1), ("MANOMETRO-10BAR", 1)],
            "SDX10": [("MOT-5HP", 1), ("IMP-100MM-INOX", 1), ("CARC-80-INOX", 2), ("EJE-20MM-INOX", 1), ("SELLO-20MM", 2), ("ROD-6205", 2), ("JUNTA-80MM-VITON", 6), ("CABLE-3X6", 150), ("CONECTOR-IP68", 2), ("PRENSA-25MM-INOX", 2), ("VALV-CHECK-80", 1)],
            "SD4": [("MOT-1HP", 1), ("IMP-50MM-INOX", 1), ("CARC-50-INOX", 1), ("EJE-10MM-INOX", 1), ("SELLO-10MM", 2), ("ROD-6201", 2), ("JUNTA-50MM-VITON", 3), ("CABLE-3X2.5", 50), ("CONECTOR-IP68", 1), ("PRENSA-12MM", 1)],
            "SD6": [("MOT-1.5HP", 1), ("IMP-65MM-INOX", 1), ("CARC-65-INOX", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-65MM-VITON", 4), ("CABLE-3X4", 50), ("CONECTOR-IP68", 1), ("PRENSA-16MM", 1), ("MANOMETRO-10BAR", 1)],
            "SD8": [("MOT-2HP", 1), ("IMP-80MM-INOX", 1), ("CARC-80-INOX", 1), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 2), ("ROD-6203", 2), ("JUNTA-80MM-VITON", 5), ("CABLE-3X6", 100), ("CONECTOR-IP68", 1), ("PRENSA-20MM", 1), ("MANOMETRO-10BAR", 1)],
            "S4": [("MOT-1.5HP", 1), ("IMP-50MM-INOX", 1), ("CARC-50-INOX", 1), ("EJE-10MM-INOX", 1), ("SELLO-10MM", 2), ("ROD-6201", 2), ("JUNTA-50MM-VITON", 3), ("CABLE-3X2.5", 50), ("CONECTOR-IP68", 1), ("PRENSA-12MM", 1)],
            "ST4": [("MOT-1.5HP", 1), ("IMP-50MM-INOX", 1), ("CARC-50-INOX", 1), ("EJE-10MM-INOX", 1), ("SELLO-10MM", 2), ("ROD-6201", 2), ("JUNTA-50MM-VITON", 3), ("CABLE-3X2.5", 50), ("CONECTOR-IP68", 1), ("PRENSA-12MM", 1)],
            "ST6": [("MOT-2HP", 1), ("IMP-65MM-INOX", 1), ("CARC-65-INOX", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-65MM-VITON", 4), ("CABLE-3X4", 50), ("CONECTOR-IP68", 1), ("PRENSA-16MM", 1)],
            "TRITON": [("MOT-2HP", 1), ("IMP-65MM-INOX", 1), ("CARC-65-INOX", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-65MM-VITON", 4), ("CABLE-3X4", 50), ("CONECTOR-IP68", 1), ("PRENSA-16MM", 1)],
            "SVA": [("MOT-1.5HP", 1), ("IMP-65MM-INOX", 1), ("CARC-65-INOX", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-65MM-VITON", 4), ("CABLE-3X4", 50), ("CONECTOR-IP68", 1), ("PRENSA-16MM", 1)],
            "SVAT": [("MOT-2HP", 1), ("IMP-80MM-INOX", 1), ("CARC-80-INOX", 1), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 2), ("ROD-6203", 2), ("JUNTA-80MM-VITON", 5), ("CABLE-3X6", 100), ("CONECTOR-IP68", 1), ("PRENSA-20MM", 1)],
            "SVHT": [("MOT-1.5HP", 1), ("IMP-50MM-INOX", 1), ("CARC-50-INOX", 1), ("EJE-10MM-INOX", 1), ("SELLO-10MM", 2), ("ROD-6201", 2), ("JUNTA-50MM-VITON", 3), ("CABLE-3X2.5", 50), ("CONECTOR-IP68", 1), ("PRENSA-12MM", 1)],
            
            # MULTICELULARES
            "APM-50": [("MOT-2HP", 1), ("IMP-50MM-BRONCE", 4), ("CARC-50-FUND", 4), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 4), ("ROD-6202", 4), ("JUNTA-50MM-NBR", 8), ("TORN-M8X25-INOX", 32), ("DIF-50MM-BRONCE", 4), ("VALV-CHECK-50", 1), ("PRESOSTATO-AUTO", 1)],
            "APM-65": [("MOT-3HP", 1), ("IMP-65MM-BRONCE", 6), ("CARC-65-FUND", 6), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 6), ("ROD-6203", 6), ("JUNTA-65MM-NBR", 12), ("TORN-M10X30-INOX", 48), ("DIF-65MM-BRONCE", 6), ("VALV-CHECK-65", 1), ("PRESOSTATO-AUTO", 1)],
            "VIPH-32": [("MOT-2HP", 1), ("IMP-50MM-BRONCE", 4), ("CARC-50-FUND", 4), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 4), ("ROD-6202", 4), ("JUNTA-50MM-NBR", 8), ("TORN-M8X25-INOX", 32), ("DIF-50MM-BRONCE", 4), ("VALV-CHECK-50", 1), ("PRESOSTATO-AUTO", 1)],
            "VIPH-50": [("MOT-3HP", 1), ("IMP-65MM-BRONCE", 6), ("CARC-65-FUND", 6), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 6), ("ROD-6203", 6), ("JUNTA-65MM-NBR", 12), ("TORN-M10X30-INOX", 48), ("DIF-65MM-BRONCE", 6), ("VALV-CHECK-65", 1), ("PRESOSTATO-AUTO", 1), ("MANOMETRO-10BAR", 1)],
            "VIPV-32": [("MOT-2HP", 1), ("IMP-50MM-BRONCE", 5), ("CARC-50-FUND", 5), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 5), ("ROD-6202", 5), ("JUNTA-50MM-NBR", 10), ("TORN-M8X25-INOX", 40), ("DIF-50MM-BRONCE", 5), ("VALV-CHECK-50", 1), ("PRESOSTATO-AUTO", 1)],
            "VIPV-50": [("MOT-3HP", 1), ("IMP-65MM-BRONCE", 7), ("CARC-65-FUND", 7), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 7), ("ROD-6203", 7), ("JUNTA-65MM-NBR", 14), ("TORN-M10X30-INOX", 56), ("DIF-65MM-BRONCE", 7), ("VALV-CHECK-65", 1), ("PRESOSTATO-AUTO", 1), ("MANOMETRO-10BAR", 1)],
            "NLV-32": [("MOT-2HP", 1), ("IMP-50MM-BRONCE", 4), ("CARC-50-FUND", 4), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 4), ("ROD-6202", 4), ("JUNTA-50MM-NBR", 8), ("TORN-M8X25-INOX", 32), ("DIF-50MM-BRONCE", 4), ("VALV-CHECK-50", 1), ("PRESOSTATO-AUTO", 1)],
            "NLV-50": [("MOT-3HP", 1), ("IMP-65MM-BRONCE", 6), ("CARC-65-FUND", 6), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 6), ("ROD-6203", 6), ("JUNTA-65MM-NBR", 12), ("TORN-M10X30-INOX", 48), ("DIF-65MM-BRONCE", 6), ("VALV-CHECK-65", 1), ("PRESOSTATO-AUTO", 1)],
            "NLX-32": [("MOT-2HP", 1), ("IMP-50MM-INOX", 4), ("CARC-50-INOX", 4), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 4), ("ROD-6202", 4), ("JUNTA-50MM-VITON", 8), ("TORN-M8X25-INOX", 32), ("DIF-50MM-INOX", 4), ("VALV-CHECK-50", 1), ("PRESOSTATO-AUTO", 1)],
            "NLX-50": [("MOT-3HP", 1), ("IMP-65MM-INOX", 6), ("CARC-65-INOX", 6), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 6), ("ROD-6203", 6), ("JUNTA-65MM-VITON", 12), ("TORN-M10X30-INOX", 48), ("DIF-65MM-INOX", 6), ("VALV-CHECK-65", 1), ("PRESOSTATO-AUTO", 1)],
            "NXA-32": [("MOT-2HP", 1), ("IMP-50MM-INOX", 6), ("CARC-50-INOX", 6), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 6), ("ROD-6202", 6), ("JUNTA-50MM-VITON", 12), ("TORN-M8X25-INOX", 48), ("DIF-50MM-INOX", 6), ("VALV-CHECK-50", 1), ("PRESOSTATO-AUTO", 1)],
            "NXA-50": [("MOT-3HP", 1), ("IMP-65MM-INOX", 8), ("CARC-65-INOX", 8), ("EJE-14MM-INOX", 1), ("SELLO-14MM", 8), ("ROD-6203", 8), ("JUNTA-65MM-VITON", 16), ("TORN-M10X30-INOX", 64), ("DIF-65MM-INOX", 8), ("VALV-CHECK-65", 1), ("PRESOSTATO-AUTO", 1)],
            
            # VERTICALES
            "VT-100": [("MOT-3HP", 1), ("IMP-65MM-INOX", 1), ("CARC-65-INOX", 1), ("EJE-16MM-INOX", 1), ("SELLO-16MM", 2), ("ROD-6204", 3), ("JUNTA-65MM-VITON", 5), ("TORN-M10X30-INOX", 12), ("PRENSA-20MM", 1), ("VALV-CHECK-65", 1)],
            "VT-150": [("MOT-5HP", 1), ("IMP-80MM-INOX", 1), ("CARC-80-INOX", 1), ("EJE-20MM-INOX", 1), ("SELLO-25MM-CARB", 2), ("ROD-6205", 3), ("JUNTA-80MM-VITON", 6), ("TORN-M12X40-INOX", 16), ("PRENSA-25MM-INOX", 2), ("VALV-CHECK-80", 1)],
            "RNL": [("MOT-2HP", 1), ("IMP-65MM-BRONCE", 1), ("CARC-65-FUND", 1), ("EJE-12MM-INOX", 1), ("SELLO-12MM", 2), ("ROD-6202", 2), ("JUNTA-65MM-NBR", 4), ("TORN-M10X30-INOX", 10), ("DIF-65MM-BRONCE", 1)],
            
            # GRUPOS HYDRO
            "HYDRO": [("MOT-7.5HP", 2), ("IMP-80MM-BRONCE", 2), ("CARC-80-FUND", 2), ("EJE-16MM-INOX", 2), ("SELLO-16MM", 4), ("ROD-6204", 4), ("JUNTA-80MM-NBR", 8), ("TORN-M10X30-INOX", 32), ("DIF-80MM-BRONCE", 2), ("VALV-CHECK-80", 2), ("PRESOSTATO-AUTO", 2), ("MANOMETRO-10BAR", 2)],
        }
        
        # Get all pump products
        cursor.execute("""SELECT id, codigo, nombre FROM productos 
                        WHERE categoria IN ('Horizontales', 'Sumergidas', 'Multicelulares', 'Verticales', 'Grupos Hydro') 
                        AND organization_id = 1 ORDER BY codigo""")
        bomba_rows = cursor.fetchall()
        
        created = 0
        for row in bomba_rows:
            producto_id, codigo_bomba, nombre_bomba = row
            
            # Find matching template based on codigo prefix
            template_key = None
            for key in bom_templates.keys():
                if codigo_bomba.startswith(key):
                    template_key = key
                    break
            
            if not template_key:
                continue
            
            bom_codigo = f"BOM-{codigo_bomba}"
            cursor.execute("""INSERT INTO bom_headers (organization_id, producto_id, nombre, codigo, descripcion, activo)
                            VALUES (?, ?, ?, ?, ?, 1)""",
                          (1, producto_id, f"BOM {nombre_bomba}", bom_codigo, f"Bill of Materials para {nombre_bomba}"))
            bom_header_id = cursor.lastrowid
            created += 1
            
            # Insert BOM lines
            for codigo_parte, cantidad in bom_templates[template_key]:
                cursor.execute("SELECT id FROM productos WHERE codigo = ? AND organization_id = 1", (codigo_parte,))
                parte_result = cursor.fetchone()
                if parte_result:
                    cursor.execute("""INSERT INTO bom_lines (organization_id, bom_header_id, componente_id, cantidad, secuencia)
                                   VALUES (?, ?, ?, ?, ?)""",
                                  (1, bom_header_id, parte_result[0], cantidad, 0))
        
        conn.commit()
        return {"success": True, "message": f"Se crearon BOMs para {created} bombas", "count": created}
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.post("/seed-boms")
async def seed_boms_demo():
    """Seed BOM (Bill of Materials) data for all 6 pump types."""
    if not DB_PATH.exists():
        return {"error": "Database not initialized yet. Start the server first."}
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Check if BOMs already exist
        cursor.execute("SELECT COUNT(*) FROM bom_headers WHERE organization_id = 1")
        if cursor.fetchone()[0] > 0:
            return {"message": "BOMs already seeded"}
        
        # Get product IDs
        cursor.execute("""
            SELECT id, codigo FROM productos 
            WHERE organization_id = 1 AND codigo IN 
            ('BC-100-001', 'BS-200-001', 'BA-150-001', 'BD-300-001', 'BP-180-001', 'BI-500-001')
        """)
        producto_map = {row[1]: row[0] for row in cursor.fetchall()}
        
        # Get a component product ID (any product to use as component)
        cursor.execute("SELECT id FROM productos WHERE organization_id = 1 LIMIT 1")
        component_id = cursor.fetchone()[0]
        
        now = datetime.utcnow().isoformat()
        bom_count = 0
        line_count = 0
        op_count = 0
        
        # BOM definitions
        boms = [
            {
                "nombre": "BOM Bomba Centrífuga BC-100",
                "codigo": "BOM-BC100-001",
                "producto_codigo": "BC-100-001",
                "version": "1.0",
                "descripcion": "Bill of Materials para ensamblaje de Bomba Centrífuga BC-100",
                "notas": "Bomba de una etapa, impulsión lateral. Voltaje 220V/380V",
                "materiales": [
                    (10, "Motor Eléctrico 1 HP", 1),
                    (20, "Carcasa / Chassis", 1),
                    (30, "Manguera PVC", 2),
                    (40, "Impulsor acero", 1),
                    (50, "Sello mecánico", 1),
                    (60, "Rodamientos", 2),
                ],
                "operaciones": [
                    (10, "OP-BC100-001", "Mecanizado eje", "mecanizado_interno", 1.5, "45.00"),
                    (20, "OP-BC100-002", "Ensamblaje rodamiento", "ensamblaje", 0.5, "15.00"),
                    (30, "OP-BC100-003", "Ensamblaje impulsor", "ensamblaje", 1.0, "25.00"),
                    (40, "OP-BC100-004", "Ensamblaje motor-bomba", "ensamblaje", 2.0, "50.00"),
                    (50, "OP-BC100-005", "Control de calidad", "control_calidad", 1.0, "20.00"),
                ]
            },
            {
                "nombre": "BOM Bomba Sumergible BS-200",
                "codigo": "BOM-BS200-001",
                "producto_codigo": "BS-200-001",
                "version": "1.0",
                "descripcion": "Bill of Materials para ensamblaje de Bomba Sumergible BS-200",
                "notas": "Bomba sumergible para pozos. Motor hermético 2HP.",
                "materiales": [
                    (10, "Motor Eléctrico 2 HP", 1),
                    (20, "Carcasa sumergible", 1),
                    (30, "Manguera reforzada", 3),
                    (40, "Impulsor acero inox", 2),
                    (50, "Sello mecánico doble", 2),
                    (60, "Rodamientos especiales", 3),
                ],
                "operaciones": [
                    (10, "OP-BS200-001", "Mecanizado eje largo", "mecanizado_interno", 2.5, "75.00"),
                    (20, "OP-BS200-002", "Mecanizado externo", "mecanizado_externo", 3.0, "120.00"),
                    (30, "OP-BS200-003", "Ensamblaje multiétapas", "ensamblaje", 3.0, "85.00"),
                    (40, "OP-BS200-004", "Prueba estanqueidad", "control_calidad", 1.5, "40.00"),
                ]
            },
            {
                "nombre": "BOM Bomba Autoaspirante BA-150",
                "codigo": "BOM-BA150-001",
                "producto_codigo": "BA-150-001",
                "version": "1.0",
                "descripcion": "Bill of Materials para ensamblaje de Bomba Autoaspirante BA-150",
                "notas": "Bomba autoaspirante. Bajo costo operacional. Motor 1.5HP.",
                "materiales": [
                    (10, "Motor Eléctrico 1.5 HP", 1),
                    (20, "Carcasa estándar", 1),
                    (30, "Manguera PVC", 2),
                    (40, "Impulsor acero", 1),
                    (50, "Sello mecánico", 1),
                    (60, "Rodamientos", 2),
                ],
                "operaciones": [
                    (10, "OP-BA150-001", "Mecanizado álabes", "mecanizado_interno", 2.0, "60.00"),
                    (20, "OP-BA150-002", "Balanceo dinámico", "control_calidad", 1.5, "35.00"),
                    (30, "OP-BA150-003", "Ensamblaje y prueba", "ensamblaje", 1.5, "40.00"),
                ]
            },
            {
                "nombre": "BOM Bomba Diésel BD-300",
                "codigo": "BOM-BD300-001",
                "producto_codigo": "BD-300-001",
                "version": "1.0",
                "descripcion": "Bill of Materials para ensamblaje de Bomba Diésel BD-300",
                "notas": "Bomba diésel para aplicaciones remotas. Motor 3HP.",
                "materiales": [
                    (10, "Motor Diésel 3 HP", 1),
                    (20, "Carcasa reforzada", 1),
                    (30, "Tanque combustible", 1),
                    (40, "Manguera industrial", 3),
                    (50, "Impulsor acero inox", 1),
                    (60, "Sello mecánico reforzado", 2),
                ],
                "operaciones": [
                    (10, "OP-BD300-001", "Ensamblaje motor-bomba", "ensamblaje", 3.0, "90.00"),
                    (20, "OP-BD300-002", "Instalación combustible", "ensamblaje", 2.0, "70.00"),
                    (30, "OP-BD300-003", "Prueba potencia", "control_calidad", 2.0, "60.00"),
                ]
            },
            {
                "nombre": "BOM Bomba de Presión BP-180",
                "codigo": "BOM-BP180-001",
                "producto_codigo": "BP-180-001",
                "version": "1.0",
                "descripcion": "Bill of Materials para ensamblaje de Bomba de Presión BP-180",
                "notas": "Bomba compacta de presión. Motor 2.5HP. Presión 4 bar.",
                "materiales": [
                    (10, "Motor Eléctrico 2.5 HP", 1),
                    (20, "Carcasa compacta", 1),
                    (30, "Manguera presión", 2),
                    (40, "Impulsor acero", 1),
                    (50, "Válvula alivio", 1),
                    (60, "Rodamientos", 2),
                ],
                "operaciones": [
                    (10, "OP-BP180-001", "Mecanizado eje y válvula", "mecanizado_interno", 2.0, "60.00"),
                    (20, "OP-BP180-002", "Ensamblaje sistema presión", "ensamblaje", 1.5, "45.00"),
                    (30, "OP-BP180-003", "Prueba presión", "control_calidad", 1.0, "30.00"),
                ]
            },
            {
                "nombre": "BOM Bomba Industrial BI-500",
                "codigo": "BOM-BI500-001",
                "producto_codigo": "BI-500-001",
                "version": "1.0",
                "descripcion": "Bill of Materials para ensamblaje de Bomba Industrial BI-500",
                "notas": "Bomba industrial alta capacidad. Motor 5HP trifásico. Caudal 300 L/min.",
                "materiales": [
                    (10, "Motor 5 HP trifásico", 1),
                    (20, "Carcasa industrial", 1),
                    (30, "Manguera industrial 2 pulgadas", 2),
                    (40, "Impulsor acero inox dúplex", 2),
                    (50, "Sello mecánico doble", 2),
                    (60, "Rodamientos especiales", 4),
                ],
                "operaciones": [
                    (10, "OP-BI500-001", "Mecanizado multiétapas", "mecanizado_interno", 4.0, "120.00"),
                    (20, "OP-BI500-002", "Subcontratación mecanizado", "mecanizado_externo", 5.0, "200.00"),
                    (30, "OP-BI500-003", "Ensamblaje multiétapas", "ensamblaje", 4.0, "120.00"),
                    (40, "OP-BI500-004", "Balanceo dinámico", "control_calidad", 2.5, "80.00"),
                    (50, "OP-BI500-005", "Prueba bajo carga", "control_calidad", 3.0, "100.00"),
                ]
            },
        ]
        
        # Create BOMs
        for bom_def in boms:
            producto_id = producto_map.get(bom_def["producto_codigo"])
            if not producto_id:
                continue
            
            # Insert BOM header
            cursor.execute("""
                INSERT INTO bom_headers 
                (organization_id, producto_id, nombre, codigo, version, descripcion, notas_tecnicas, cantidad_producida, unidad_medida, activo, es_principal, creado_en, actualizado_en)
                VALUES (1, ?, ?, ?, ?, ?, ?, 1.0, 'unidad', 1, 1, ?, ?)
            """, (producto_id, bom_def["nombre"], bom_def["codigo"], bom_def["version"], bom_def["descripcion"], bom_def.get("notas"), now, now))
            
            bom_id = cursor.lastrowid
            bom_count += 1
            
            # Insert materials
            for seq, desc, qty in bom_def.get("materiales", []):
                cursor.execute("""
                    INSERT INTO bom_lines 
                    (organization_id, bom_header_id, componente_id, cantidad, unidad_medida, secuencia, es_opcional, factor_desperdicio, notas, creado_en, actualizado_en)
                    VALUES (1, ?, ?, ?, 'unidad', ?, 0, 0.05, ?, ?, ?)
                """, (bom_id, component_id, qty, seq, desc, now, now))
                line_count += 1
            
            # Insert operations
            for seq, codigo, nombre, tipo, duracion, costo in bom_def.get("operaciones", []):
                cursor.execute("""
                    INSERT INTO bom_operaciones 
                    (organization_id, bom_header_id, nombre, codigo, tipo_operacion, secuencia, duracion_estimada, centro_trabajo, costo_operacion, descripcion, instrucciones, creado_en, actualizado_en)
                    VALUES (1, ?, ?, ?, ?, ?, ?, 'Producción', ?, ?, ?, ?, ?)
                """, (bom_id, nombre, codigo, tipo, seq, duracion, costo, nombre, nombre, now, now))
                op_count += 1
        
        conn.commit()
        return {
            "message": "BOMs seeded successfully",
            "boms_created": bom_count,
            "materials_added": line_count,
            "operaciones_agregadas": op_count,
        }
        
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()


@router.get("/boms-list")
async def get_boms_list_demo():
    """Get all BOMs for display in UI (demo data, no auth required)."""
    if not DB_PATH.exists():
        return []
    
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                bom_headers.id,
                bom_headers.codigo,
                bom_headers.nombre,
                bom_headers.version,
                bom_headers.activo,
                productos.nombre as producto_nombre,
                productos.codigo as producto_codigo,
                (SELECT COUNT(*) FROM bom_lines WHERE bom_header_id = bom_headers.id) as total_componentes,
                (SELECT COUNT(*) FROM bom_operaciones WHERE bom_header_id = bom_headers.id) as total_operaciones
            FROM bom_headers
            LEFT JOIN productos ON bom_headers.producto_id = productos.id
            WHERE bom_headers.organization_id = 1
            ORDER BY bom_headers.codigo
        """)
        
        boms = []
        for row in cursor.fetchall():
            boms.append({
                "id": row["id"],
                "codigo": row["codigo"],
                "nombre": row["nombre"],
                "version": row["version"],
                "activo": row["activo"],
                "producto_nombre": row["producto_nombre"] or "Desconocido",
                "producto_codigo": row["producto_codigo"],
                "total_componentes": row["total_componentes"] or 0,
                "total_operaciones": row["total_operaciones"] or 0,
            })
        
        conn.close()
        return boms
        
    except Exception as e:
        conn.close()
        return []


@router.get("/boms/{bom_id}")
async def get_bom_detail_demo(bom_id: int):
    """Get BOM detail for UI (demo data, no auth required)."""
    if not DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Database not found")

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
                SELECT 
                    bh.id,
                    bh.codigo,
                    bh.nombre,
                    bh.version,
                    bh.descripcion,
                    bh.notas_tecnicas,
                    p.nombre as producto_nombre,
                    p.codigo as producto_codigo
                FROM bom_headers bh
                LEFT JOIN productos p ON bh.producto_id = p.id
                WHERE bh.id = ? AND bh.organization_id = 1
            """,
            (bom_id,),
        )

        bom_row = cursor.fetchone()
        if not bom_row:
            raise HTTPException(status_code=404, detail="BOM not found")

        cursor.execute(
            """
                SELECT 
                    bl.secuencia,
                    bl.cantidad,
                    bl.unidad_medida,
                    bl.factor_desperdicio,
                    pr.codigo AS componente_codigo,
                    pr.nombre AS componente_nombre
                FROM bom_lines bl
                LEFT JOIN productos pr ON bl.componente_id = pr.id
                WHERE bl.bom_header_id = ? AND bl.organization_id = 1
                ORDER BY bl.secuencia
            """,
            (bom_id,),
        )

        lineas = [
            {
                "secuencia": row["secuencia"],
                "cantidad": float(row["cantidad"] or 0),
                "unidad_medida": row["unidad_medida"] or "unidad",
                "factor_desperdicio": float(row["factor_desperdicio"] or 0),
                "componente_codigo": row["componente_codigo"] or "SIN-COD",
                "componente_nombre": row["componente_nombre"] or "Componente",
            }
            for row in cursor.fetchall()
        ]

        cursor.execute(
            """
                SELECT 
                    bo.secuencia,
                    bo.nombre,
                    bo.tipo_operacion,
                    bo.duracion_estimada,
                    bo.costo_operacion,
                    bo.centro_trabajo
                FROM bom_operaciones bo
                WHERE bo.bom_header_id = ? AND bo.organization_id = 1
                ORDER BY bo.secuencia
            """,
            (bom_id,),
        )

        operaciones = [
            {
                "secuencia": row["secuencia"],
                "nombre": row["nombre"],
                "tipo_operacion": row["tipo_operacion"],
                "duracion_estimada": float(row["duracion_estimada"] or 0),
                "costo_operacion": float(row["costo_operacion"] or 0),
                "centro_trabajo": row["centro_trabajo"],
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return {
            "id": bom_row["id"],
            "codigo": bom_row["codigo"],
            "nombre": bom_row["nombre"],
            "version": bom_row["version"],
            "descripcion": bom_row["descripcion"],
            "notas_tecnicas": bom_row["notas_tecnicas"],
            "producto_nombre": bom_row["producto_nombre"] or "Desconocido",
            "producto_codigo": bom_row["producto_codigo"],
            "lineas": lineas,
            "operaciones": operaciones,
        }

    except HTTPException:
        conn.close()
        raise
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ordenes-produccion")
async def get_ordenes_produccion_demo():
    """Get all production orders for display in UI (demo data, no auth required)."""
    if not DB_PATH.exists():
        return []
    
    conn = get_db()
    ensure_produccion_tables(conn)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                ordenes_produccion.id,
                ordenes_produccion.numero,
                ordenes_produccion.estado,
                ordenes_produccion.prioridad,
                ordenes_produccion.cantidad_ordenada,
                ordenes_produccion.cantidad_completada,
                ordenes_produccion.cantidad_rechazada,
                ordenes_produccion.fecha_creacion,
                ordenes_produccion.fecha_inicio_estimada,
                ordenes_produccion.fecha_fin_estimada,
                ordenes_produccion.asignado_a,
                productos.nombre as producto_nombre,
                productos.codigo as producto_codigo,
                (SELECT COUNT(*) FROM operaciones_produccion WHERE orden_produccion_id = ordenes_produccion.id) as total_operaciones
            FROM ordenes_produccion
            LEFT JOIN productos ON ordenes_produccion.producto_id = productos.id
            WHERE ordenes_produccion.organization_id = 1
            ORDER BY ordenes_produccion.fecha_creacion DESC
        """)
        
        ordenes = []
        for row in cursor.fetchall():
            completado = (row["cantidad_completada"] / row["cantidad_ordenada"] * 100) if row["cantidad_ordenada"] > 0 else 0
            ordenes.append({
                "id": row["id"],
                "numero": row["numero"],
                "estado": row["estado"],
                "prioridad": row["prioridad"],
                "cantidad_ordenada": row["cantidad_ordenada"],
                "cantidad_completada": row["cantidad_completada"],
                "cantidad_rechazada": row["cantidad_rechazada"],
                "porcentaje_completado": round(completado, 1),
                "fecha_creacion": row["fecha_creacion"],
                "fecha_inicio_estimada": row["fecha_inicio_estimada"],
                "fecha_fin_estimada": row["fecha_fin_estimada"],
                "asignado_a": row["asignado_a"],
                "producto_nombre": row["producto_nombre"] or "Desconocido",
                "producto_codigo": row["producto_codigo"],
                "total_operaciones": row["total_operaciones"] or 0,
                "venta_id": None,
                "venta_numero": "Venta demo",
                "cliente_nombre": "Cliente demo",
            })
        
        conn.close()
        return ordenes
        
    except Exception as e:
        conn.close()
        return []


@router.get("/ventas")
async def get_ventas_demo():
    """List all sales (POS + traditional) - demo, no auth."""
    if not DB_PATH.exists():
        return []
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        # Get POS sales with client info and detail count
        cursor.execute(
            """
            SELECT 
                'pos' as tipo,
                vp.id, vp.numero, vp.cliente_id, vp.total, vp.estado, vp.creado_en, vp.observaciones,
                COALESCE(c.nombre, 'Sin cliente') as cliente_nombre,
                NULL as cliente_email, NULL as factura_generada, NULL as factura_enviada,
                (SELECT COUNT(*) FROM ventas_pos_detalle WHERE venta_pos_id = vp.id) as tiene_detalles
            FROM ventas_pos vp
            LEFT JOIN clientes c ON vp.cliente_id = c.id
            WHERE vp.organization_id = 1
            ORDER BY vp.creado_en DESC
            """
        )
        rows = [dict(r) for r in cursor.fetchall()]
        return rows
    except Exception as e:
        return []
    finally:
        conn.close()


@router.get("/ventas-pos-pendientes")
async def get_ventas_pos_pendientes_demo():
    """List POS sales pending approval (demo, no auth)."""
    if not DB_PATH.exists():
        return []
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, numero, cliente_id, total, estado, creado_en, observaciones
            FROM ventas_pos
            WHERE organization_id = 1 AND estado = 'pendiente_aprobacion'
            ORDER BY creado_en DESC
            """
        )
        rows = [dict(r) for r in cursor.fetchall()]
        return rows
    except Exception:
        return []
    finally:
        conn.close()


@router.get("/ventas-pos/{venta_id}/detalles")
async def get_venta_pos_detalles_demo(venta_id: int):
    """Get POS sale details (line items) - demo, no auth."""
    if not DB_PATH.exists():
        return []
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                d.id, d.producto_id, d.cantidad, d.precio_unitario, 
                d.descuento, d.subtotal,
                p.nombre as producto_nombre, p.codigo as producto_codigo
            FROM ventas_pos_detalle d
            LEFT JOIN productos p ON d.producto_id = p.id
            WHERE d.venta_pos_id = ?
            ORDER BY d.id
            """,
            (venta_id,)
        )
        rows = [dict(r) for r in cursor.fetchall()]
        return rows
    except Exception:
        return []
    finally:
        conn.close()


@router.post("/ventas-pos/{venta_id}/aprobar")
async def aprobar_venta_pos_demo(venta_id: int):
    """Approve a pending POS sale and create production orders (demo, no auth)."""
    if not DB_PATH.exists():
        return JSONResponse(content={"success": False, "message": "Database not found"}, status_code=500)
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Update venta status
        cursor.execute(
            "UPDATE ventas_pos SET estado = 'completada' WHERE id = ? AND organization_id = 1",
            (venta_id,)
        )
        
        if cursor.rowcount == 0:
            return JSONResponse(content={"success": False, "message": "Venta no encontrada"}, status_code=404)
        
        # Get venta details
        cursor.execute("SELECT numero, observaciones FROM ventas_pos WHERE id = ?", (venta_id,))
        venta_row = cursor.fetchone()
        venta_numero = venta_row[0] if venta_row else f"POS-{venta_id}"
        venta_obs = venta_row[1] if venta_row and len(venta_row) > 1 else ""
        
        # Get line items
        cursor.execute(
            """
            SELECT d.producto_id, d.cantidad, p.codigo, p.nombre
            FROM ventas_pos_detalle d
            JOIN productos p ON d.producto_id = p.id
            WHERE d.venta_pos_id = ?
            """,
            (venta_id,)
        )
        detalles = cursor.fetchall()
        detalles_list = list(detalles)  # Convert to list to avoid cursor issues
        
        conn.commit()
        conn.close()  # Close connection BEFORE making HTTP calls
        
        # Now create production orders (connection is closed, no locks)
        ordenes_creadas = []
        import httpx
        async with httpx.AsyncClient() as client:
            for detalle in detalles_list:
                producto_id, cantidad, producto_codigo, producto_nombre = detalle
                
                payload = {
                    "producto_codigo": producto_codigo,
                    "cantidad": cantidad,
                    "prioridad": "media",
                    "descripcion": f"Venta {venta_numero}: {venta_obs}".strip(),
                    "asignado_a": "Supervisor Producción",
                    "centro_trabajo": "Línea de Ensamblaje",
                }
                
                try:
                    resp = await client.post("http://127.0.0.1:8001/api/demo/ordenes-produccion", json=payload, timeout=10.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("success"):
                            ordenes_creadas.append({
                                "numero": data.get("numero"),
                                "orden_id": data.get("orden_id"),
                                "producto": producto_nombre
                            })
                except Exception as e:
                    print(f"Error creating production order: {e}")
        
        return JSONResponse(content={
            "success": True,
            "message": f"Venta aprobada. Se crearon {len(ordenes_creadas)} órdenes de producción.",
            "venta_id": venta_id,
            "ordenes_produccion": ordenes_creadas
        })
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)


@router.post("/ventas-pos/{venta_id}/rechazar")
async def rechazar_venta_pos_demo(venta_id: int):
    """Reject a pending POS sale (demo, no auth)."""
    if not DB_PATH.exists():
        return JSONResponse(content={"success": False, "message": "Database not found"}, status_code=500)
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE ventas_pos SET estado = 'cancelada' WHERE id = ? AND organization_id = 1",
            (venta_id,)
        )
        
        if cursor.rowcount == 0:
            return JSONResponse(content={"success": False, "message": "Venta no encontrada"}, status_code=404)
        
        conn.commit()
        
        return JSONResponse(content={
            "success": True,
            "message": "Venta rechazada",
            "venta_id": venta_id
        })
        
    except Exception as e:
        conn.rollback()
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)
    finally:
        conn.close()


@router.get("/ordenes-produccion/{orden_id}")
async def get_orden_produccion_demo(orden_id: int):
    """Get production order detail with operations and movements (demo, no auth)."""
    if not DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Database not found")

    conn = get_db()
    ensure_produccion_tables(conn)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT 
                op.id, op.numero, op.estado, op.prioridad, op.descripcion,
                op.cantidad_ordenada, op.cantidad_completada, op.cantidad_rechazada,
                op.fecha_creacion, op.fecha_inicio_estimada, op.fecha_fin_estimada,
                op.fecha_inicio_real, op.fecha_fin_real,
                op.asignado_a, op.centro_trabajo,
                op.costo_materiales, op.costo_mano_obra, op.costo_operaciones_externas, op.costo_total,
                op.notas_produccion,
                p.nombre AS producto_nombre, p.codigo AS producto_codigo,
                b.codigo AS bom_codigo
            FROM ordenes_produccion op
            LEFT JOIN productos p ON op.producto_id = p.id
            LEFT JOIN bom_headers b ON op.bom_id = b.id
            WHERE op.id = ? AND op.organization_id = 1
            """,
            (orden_id,),
        )

        orden = cursor.fetchone()
        if not orden:
            raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

        cursor.execute(
            """
            SELECT 
                id, secuencia, estado, asignado_a, centro_trabajo,
                duracion_estimada, duracion_real,
                fecha_inicio_estimada, fecha_fin_estimada,
                fecha_inicio_real, fecha_fin_real,
                inspecciones_realizadas, resultado_control_calidad
            FROM operaciones_produccion
            WHERE orden_produccion_id = ? AND organization_id = 1
            ORDER BY secuencia
            """,
            (orden_id,),
        )
        operaciones = [dict(row) for row in cursor.fetchall()]

        cursor.execute(
            """
            SELECT 
                id, producto_id, tipo_movimiento, cantidad, estado,
                ubicacion_origen, ubicacion_destino,
                fecha_creacion, fecha_movimiento,
                responsable, observaciones
            FROM movimientos_almacen
            WHERE orden_produccion_id = ? AND organization_id = 1
            ORDER BY fecha_creacion
            """,
            (orden_id,),
        )
        movimientos = [dict(row) for row in cursor.fetchall()]

        conn.close()
        
        # Compute porcentaje_completado
        orden_dict = dict(orden)
        cantidad_ordenada = orden_dict.get("cantidad_ordenada", 0) or 1
        cantidad_completada = orden_dict.get("cantidad_completada", 0) or 0
        porcentaje = round((cantidad_completada / cantidad_ordenada) * 100, 1) if cantidad_ordenada > 0 else 0
        
        return {
            **orden_dict,
            "porcentaje_completado": porcentaje,
            "operaciones": operaciones,
            "movimientos": movimientos,
        }

    except HTTPException:
        conn.close()
        raise
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/ordenes-produccion/{orden_id}/estado")
async def update_orden_estado_demo(orden_id: int, nuevo_estado: str):
    """Update production order status (demo endpoint, no auth required)."""
    if not DB_PATH.exists():
        return {"error": "Database not found"}
    conn = get_db()
    ensure_produccion_tables(conn)
    
    # Validate status
    valid_states = ["planificada", "en_proceso", "completada", "cancelada", "pausada"]
    if nuevo_estado not in valid_states:
        return {"error": f"Invalid status. Must be one of: {', '.join(valid_states)}"}
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE ordenes_produccion 
            SET estado = ?
            WHERE id = ? AND organization_id = 1
        """, (nuevo_estado, orden_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return {"success": True, "mensaje": f"Order {orden_id} updated to {nuevo_estado}"}
        else:
            conn.close()
            return {"error": "Order not found"}
        
    except Exception as e:
        conn.close()
        return {"error": str(e)}


@router.put("/ordenes-produccion/{orden_id}/cantidad")
async def update_orden_cantidad_demo(orden_id: int, cantidad_completada: float):
    """Update production order completed quantity (demo endpoint, no auth required)."""
    if not DB_PATH.exists():
        return {"error": "Database not found"}
    
    conn = get_db()
    ensure_produccion_tables(conn)
    cursor = conn.cursor()
    
    try:
        # Get the order to check total quantity
        cursor.execute("""
            SELECT cantidad_ordenada FROM ordenes_produccion
            WHERE id = ? AND organization_id = 1
        """, (orden_id,))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return {"error": "Order not found"}
        
        cantidad_total = result[0]
        if cantidad_completada > cantidad_total:
            conn.close()
            return {"error": f"Completed quantity cannot exceed total ({cantidad_total})"}
        
        cursor.execute("""
            UPDATE ordenes_produccion 
            SET cantidad_completada = ?,
                estado = CASE 
                    WHEN ? >= cantidad_ordenada THEN 'completada'
                    WHEN ? > 0 THEN 'en_proceso'
                    ELSE estado
                END
            WHERE id = ? AND organization_id = 1
        """, (cantidad_completada, cantidad_completada, cantidad_completada, orden_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return {"success": True, "mensaje": f"Order {orden_id} updated"}
        else:
            conn.close()
            return {"error": "Order not found"}
        
    except Exception as e:
        conn.close()
        return {"error": str(e)}


@router.post("/ordenes-produccion")
async def create_orden_produccion_demo(data: dict):
    """Create a demo production order (no auth)."""
    if not DB_PATH.exists():
        return JSONResponse(status_code=500, content={"error": "Database not found"})
    
    conn = get_db()
    ensure_produccion_tables(conn)
    cursor = conn.cursor()

    try:
        producto_codigo = data.get("producto_codigo")
        cantidad = float(data.get("cantidad", 1) or 1)
        prioridad = data.get("prioridad", "media")
        descripcion = data.get("descripcion") or "Orden demo creada desde UI"
        asignado_a = data.get("asignado_a") or "Supervisor Producción"
        centro_trabajo = data.get("centro_trabajo") or "Línea A"

        # Find product and BOM
        cursor.execute(
            """
            SELECT p.id, b.id, b.codigo, p.categoria
            FROM productos p
            LEFT JOIN bom_headers b ON b.producto_id = p.id
            WHERE p.codigo = ? AND p.organization_id = 1 AND b.organization_id = 1
            """,
            (producto_codigo,),
        )
        row = cursor.fetchone()
        if not row:
            conn.close()
            return JSONResponse(status_code=404, content={"error": "Producto o BOM no encontrado"})
        
        producto_id, bom_id, bom_codigo, categoria = row
        categoria = categoria or ""
        es_vehiculo = "JDM" in categoria or "Alquiler" in categoria or "Veh" in categoria

        # Generate order number
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM ordenes_produccion WHERE organization_id = 1")
        next_seq = cursor.fetchone()[0]
        order_number = f"OP-{datetime.utcnow().year}-{next_seq:05d}"

        now = datetime.utcnow()
        cursor.execute(
            """
            INSERT INTO ordenes_produccion (
                organization_id, venta_id, bom_id, producto_id, numero, descripcion,
                cantidad_ordenada, cantidad_completada, cantidad_rechazada,
                estado, prioridad,
                fecha_creacion, fecha_inicio_estimada, fecha_fin_estimada,
                asignado_a, centro_trabajo,
                costo_materiales, costo_mano_obra, costo_operaciones_externas, costo_total,
                notas_produccion
            ) VALUES (1, 1, ?, ?, ?, ?, ?, 0, 0, 'planificada', ?, ?, ?, ?, ?, ?, 0, 0, 0, 0, ?)
            """,
            (
                bom_id,
                producto_id,
                order_number,
                descripcion,
                cantidad,
                prioridad,
                now,
                now,
                now,
                asignado_a,
                centro_trabajo,
                f"Orden creada manualmente. BOM {bom_codigo}"
            ),
        )

        orden_id = cursor.lastrowid

        # Create operations from BOM
        cursor.execute(
            """
            SELECT id, secuencia, duracion_estimada, nombre, tipo_operacion, centro_trabajo
            FROM bom_operaciones
            WHERE bom_header_id = ? AND organization_id = 1
            ORDER BY secuencia
            """,
            (bom_id,),
        )
        for idx, bom_op in enumerate(cursor.fetchall(), 1):
            bom_op_id, seq, duracion, nombre_op, tipo_op, centro_bom = bom_op
            cursor.execute(
                """
                INSERT INTO operaciones_produccion (
                    organization_id, orden_produccion_id, bom_operacion_id,
                    secuencia, duracion_estimada, duracion_real,
                    estado, asignado_a, centro_trabajo,
                    fecha_inicio_estimada, fecha_fin_estimada,
                    inspecciones_realizadas, resultado_control_calidad
                ) VALUES (1, ?, ?, ?, ?, NULL, 'planificada', ?, ?, NULL, NULL, 0, NULL)
                """,
                (
                    orden_id,
                    bom_op_id,
                    seq or idx * 10,
                    duracion or 2.0,
                    asignado_a,
                    centro_bom or centro_trabajo,
                ),
            )

        # Operaciones específicas para vehículos (combustible y ruedas)
        if es_vehiculo:
            vehicle_ops = [
                (900, "Chequeo combustible (min 5L)", 0.2, "Verificar nivel y rellenar hasta 5L si es menor."),
                (910, "Inspección y sustitución de ruedas", 0.4, "Si una rueda está mal, sustituir su pareja del mismo eje."),
            ]
            for seq, nombre_op, duracion, nota in vehicle_ops:
                cursor.execute(
                    """
                    INSERT INTO operaciones_produccion (
                        organization_id, orden_produccion_id, bom_operacion_id,
                        secuencia, duracion_estimada, duracion_real,
                        estado, asignado_a, centro_trabajo,
                        fecha_inicio_estimada, fecha_fin_estimada,
                        inspecciones_realizadas, resultado_control_calidad
                    ) VALUES (1, ?, NULL, ?, ?, NULL, 'planificada', ?, ?, NULL, NULL, 0, ?)
                    """,
                    (
                        orden_id,
                        seq,
                        duracion,
                        asignado_a,
                        centro_trabajo,
                        nota,
                    ),
                )

            # Anotar en notas de producción para visibilidad
            cursor.execute(
                """
                UPDATE ordenes_produccion
                SET notas_produccion = COALESCE(notas_produccion, '') || '
Vehículo: añadir combustible hasta 5L y revisar ruedas (sustituir en pares).'
                WHERE id = ? AND organization_id = 1
                """,
                (orden_id,),
            )

        conn.commit()
        conn.close()
        return JSONResponse(status_code=200, content={"success": True, "orden_id": orden_id, "numero": order_number})

    except Exception as e:
        conn.rollback()
        conn.close()
        import traceback
        print(f"Error in create_orden_produccion_demo: {str(e)}")
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/seed-ordenes")
async def seed_ordenes_produccion_demo():
    """Seed production orders, operations, and demo movements."""
    if not DB_PATH.exists():
        return {"error": "Database not found. Run /api/demo/seed first."}
    conn = get_db()
    ensure_produccion_tables(conn)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM ordenes_produccion WHERE organization_id = 1")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return {"message": "Órdenes de producción ya existen"}

        now = datetime.utcnow()
        orders = [
            {"numero": "OP-2025-001", "producto_codigo": "BC-100-001", "cantidad": 2, "descripcion": "Orden para cliente Agrícola Los Pinos", "prioridad": "alta", "dias_inicio": 0, "dias_fin": 2},
            {"numero": "OP-2025-002", "producto_codigo": "BS-200-001", "cantidad": 1, "descripcion": "Orden para Sistemas de Riego Agrícola", "prioridad": "media", "dias_inicio": 1, "dias_fin": 5},
            {"numero": "OP-2025-003", "producto_codigo": "BA-150-001", "cantidad": 3, "descripcion": "Producción serie autoaspirantes", "prioridad": "media", "dias_inicio": 2, "dias_fin": 4},
            {"numero": "OP-2025-004", "producto_codigo": "BD-300-001", "cantidad": 1, "descripcion": "Bomba diésel minería", "prioridad": "alta", "dias_inicio": 0, "dias_fin": 3},
            {"numero": "OP-2025-005", "producto_codigo": "BP-180-001", "cantidad": 4, "descripcion": "Serie bombas de presión", "prioridad": "baja", "dias_inicio": 3, "dias_fin": 6},
            {"numero": "OP-2025-006", "producto_codigo": "BI-500-001", "cantidad": 1, "descripcion": "Bomba industrial gran capacidad", "prioridad": "urgente", "dias_inicio": 0, "dias_fin": 4},
        ]

        cursor.execute(
            """
            SELECT bom_headers.id, bom_headers.producto_id, productos.codigo, bom_headers.codigo
            FROM bom_headers
            LEFT JOIN productos ON bom_headers.producto_id = productos.id
            WHERE bom_headers.organization_id = 1
            """
        )
        bom_map = {row[2]: (row[0], row[1], row[3]) for row in cursor.fetchall()}
        if not bom_map:
            conn.close()
            return {"error": "No hay BOMs disponibles. Ejecuta /api/demo/seed-boms primero."}

        created_orders = 0
        created_ops = 0

        for order in orders:
            if order["producto_codigo"] not in bom_map:
                continue
            bom_id, producto_id, bom_codigo = bom_map[order["producto_codigo"]]
            fecha_inicio = now + timedelta(days=order["dias_inicio"])
            fecha_fin = now + timedelta(days=order["dias_fin"])

            cursor.execute(
                """
                INSERT INTO ordenes_produccion (
                    organization_id, venta_id, bom_id, producto_id, numero, descripcion,
                    cantidad_ordenada, cantidad_completada, cantidad_rechazada,
                    estado, prioridad,
                    fecha_creacion, fecha_inicio_estimada, fecha_fin_estimada,
                    asignado_a, centro_trabajo,
                    costo_materiales, costo_mano_obra, costo_operaciones_externas, costo_total,
                    notas_produccion
                ) VALUES (1, 1, ?, ?, ?, ?, ?, 0, 0, 'planificada', ?, ?, ?, ?, 'Supervisor Producción', 'Línea de Ensamblaje', 0, 0, 0, 0, ?)
                """,
                (
                    bom_id,
                    producto_id,
                    order["numero"],
                    order["descripcion"],
                    order["cantidad"],
                    order["prioridad"],
                    now,
                    fecha_inicio,
                    fecha_fin,
                    f"Orden creada automáticamente. BOM {bom_codigo}"
                ),
            )
            orden_id = cursor.lastrowid
            created_orders += 1

            cursor.execute(
                """
                SELECT id, secuencia, duracion_estimada, nombre, tipo_operacion, centro_trabajo
                FROM bom_operaciones
                WHERE bom_header_id = ? AND organization_id = 1
                ORDER BY secuencia
                """,
                (bom_id,),
            )
            for idx, bom_op in enumerate(cursor.fetchall(), 1):
                bom_op_id, seq, duracion, nombre_op, tipo_op, centro_bom = bom_op
                cursor.execute(
                    """
                    INSERT INTO operaciones_produccion (
                        organization_id, orden_produccion_id, bom_operacion_id,
                        secuencia, duracion_estimada, duracion_real,
                        estado, asignado_a, centro_trabajo,
                        fecha_inicio_estimada, fecha_fin_estimada,
                        inspecciones_realizadas, resultado_control_calidad
                    ) VALUES (1, ?, ?, ?, ?, NULL, 'planificada', ?, ?, NULL, NULL, 0, NULL)
                    """,
                    (
                        orden_id,
                        bom_op_id,
                        seq or idx * 10,
                        duracion or 2.0,
                        "Operario Turno A",
                        centro_bom or "Línea A",
                    ),
                )
                created_ops += 1

            # Simple demo movement (picking)
            cursor.execute(
                """
                INSERT INTO movimientos_almacen (
                    organization_id, orden_produccion_id, producto_id, tipo_movimiento, cantidad,
                    ubicacion_origen, ubicacion_destino, estado, fecha_creacion, responsable
                ) VALUES (1, ?, ?, 'picking', ?, 'Almacén A', 'Línea A', 'entregado', ?, 'Almacén')
                """,
                (
                    orden_id,
                    producto_id,
                    order["cantidad"],
                    now,
                ),
            )

        conn.commit()
        conn.close()
        return {
            "message": "Órdenes de producción creadas",
            "ordenes": created_orders,
            "operaciones": created_ops,
        }

    except Exception as e:
        conn.rollback()
        conn.close()
        return {"error": str(e)}


@router.post("/reset-produccion")
async def reset_produccion_demo():
    """Reset demo production data: deletes orders, operations, and movements for organization 1."""
    if not DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Database not found")

    conn = get_db()
    ensure_produccion_tables(conn)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM operaciones_produccion WHERE organization_id = 1")
        cursor.execute("DELETE FROM movimientos_almacen WHERE organization_id = 1")
        cursor.execute("DELETE FROM ordenes_produccion WHERE organization_id = 1")
        conn.commit()
        return {"success": True, "message": "Producción demo reiniciada"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.post("/reset-all")
async def reset_all_demo():
    """Reset ALL demo data relevant to factory setup: BOMs, production orders, operations, and movements for organization 1."""
    if not DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Database not found")

    conn = get_db()
    cursor = conn.cursor()
    try:
        # Clear production-related tables
        ensure_produccion_tables(conn)
        cursor.execute("DELETE FROM operaciones_produccion WHERE organization_id = 1")
        cursor.execute("DELETE FROM movimientos_almacen WHERE organization_id = 1")
        cursor.execute("DELETE FROM ordenes_produccion WHERE organization_id = 1")

        # Clear BOM-related tables
        cursor.execute("DELETE FROM bom_operaciones WHERE organization_id = 1")
        cursor.execute("DELETE FROM bom_lines WHERE organization_id = 1")
        cursor.execute("DELETE FROM bom_headers WHERE organization_id = 1")

        conn.commit()
        return {"success": True, "message": "Proyecto demo reiniciado: BOMs y Producción limpiados"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.post("/ventas-pos")
async def create_venta_pos_demo(payload: dict):
    """Create a new POS sale (no auth, direct DB insert)."""
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        org_id = 1
        cliente_id = payload.get("cliente_id")
        metodo_pago = payload.get("metodo_pago", "efectivo")
        descuento = payload.get("descuento", 0)
        monto_pagado = payload.get("monto_pagado", 0)
        observaciones = payload.get("observaciones", "")
        detalles = payload.get("detalles", [])
        
        # Calculate totals
        subtotal = 0
        for detalle in detalles:
            qty = detalle.get("cantidad", 0)
            price = detalle.get("precio_unitario", 0)
            desc = detalle.get("descuento", 0)
            item_sub = (qty * price) - desc
            subtotal += item_sub
        
        impuesto = (subtotal - descuento) * 0.18
        total = subtotal - descuento + impuesto
        cambio = monto_pagado - total
        
        # Generate transaction number
        cursor.execute("SELECT COUNT(*) as cnt FROM ventas_pos WHERE organization_id = ?", (org_id,))
        count = cursor.fetchone()["cnt"] + 1
        numero = f"POS-{org_id}-{count:06d}"
        
        # Insert sale
        cursor.execute(
            """INSERT INTO ventas_pos 
               (organization_id, numero, cliente_id, subtotal, descuento, impuesto, total, 
                metodo_pago, monto_pagado, cambio, estado, observaciones, creado_en)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (org_id, numero, cliente_id, subtotal, descuento, impuesto, total, 
             metodo_pago, monto_pagado, cambio, "pendiente_aprobacion", observaciones)
        )
        venta_id = cursor.lastrowid
        
        # Insert line items and update stock
        for detalle in detalles:
            producto_id = detalle.get("producto_id")
            qty = detalle.get("cantidad", 0)
            price = detalle.get("precio_unitario", 0)
            desc = detalle.get("descuento", 0)
            item_sub = (qty * price) - desc
            
            cursor.execute(
                """INSERT INTO ventas_pos_detalle 
                   (venta_pos_id, producto_id, cantidad, precio_unitario, descuento, subtotal)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (venta_id, producto_id, qty, price, desc, item_sub)
            )
            
            # Update stock
            cursor.execute(
                "UPDATE productos SET stock_actual = stock_actual - ? WHERE id = ? AND organization_id = ?",
                (qty, producto_id, org_id)
            )
        
        conn.commit()
        
        # Fetch created sale
        cursor.execute(
            "SELECT id, numero, total, estado FROM ventas_pos WHERE id = ?", (venta_id,)
        )
        result = cursor.fetchone()
        
        return {
            "id": result["id"],
            "numero": result["numero"],
            "total": result["total"],
            "estado": result["estado"]
        }
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.post("/seed-almacen")
async def seed_almacen_demo():
    """Create warehouse structure: 10 aisles, A-Z shelves, 6 levels, 3 positions (L/C/R)."""
    if not DB_PATH.exists():
        return JSONResponse(content={"success": False, "message": "Database not found"}, status_code=500)
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Create almacen_ubicaciones table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS almacen_ubicaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL DEFAULT 1,
                codigo VARCHAR(50) UNIQUE NOT NULL,
                pasillo INTEGER NOT NULL,
                estanteria VARCHAR(1) NOT NULL,
                altura INTEGER NOT NULL,
                parcela VARCHAR(10) NOT NULL,
                capacidad_max FLOAT DEFAULT 100.0,
                ocupado FLOAT DEFAULT 0.0,
                producto_id INTEGER,
                activo BOOLEAN DEFAULT 1,
                notas TEXT,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)
        
        # Create almacen_movimientos table for tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS almacen_movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL DEFAULT 1,
                tipo VARCHAR(50) NOT NULL,
                ubicacion_origen_id INTEGER,
                ubicacion_destino_id INTEGER,
                producto_id INTEGER NOT NULL,
                cantidad FLOAT NOT NULL,
                usuario VARCHAR(100),
                fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                referencia VARCHAR(100),
                notas TEXT,
                FOREIGN KEY (ubicacion_origen_id) REFERENCES almacen_ubicaciones(id),
                FOREIGN KEY (ubicacion_destino_id) REFERENCES almacen_ubicaciones(id),
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)
        
        # Clear existing locations
        cursor.execute("DELETE FROM almacen_ubicaciones WHERE organization_id = 1")
        
        # Generate all locations
        pasillos = range(1, 11)  # 1-10
        estanterias = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alturas = range(1, 7)  # 1-6
        parcelas = ["IZQ", "CEN", "DER"]
        
        ubicaciones_creadas = 0
        for pasillo in pasillos:
            for estanteria in estanterias:
                for altura in alturas:
                    for parcela in parcelas:
                        codigo = f"P{pasillo:02d}-{estanteria}{altura}-{parcela}"
                        cursor.execute("""
                            INSERT INTO almacen_ubicaciones 
                            (organization_id, codigo, pasillo, estanteria, altura, parcela, capacidad_max, ocupado, activo)
                            VALUES (1, ?, ?, ?, ?, ?, 100.0, 0.0, 1)
                        """, (codigo, pasillo, estanteria, altura, parcela))
                        ubicaciones_creadas += 1
        
        conn.commit()
        
        return JSONResponse(content={
            "success": True,
            "message": f"Almacén creado: {ubicaciones_creadas} ubicaciones",
            "pasillos": len(pasillos),
            "estanterias_por_pasillo": len(estanterias),
            "alturas": len(alturas),
            "parcelas": len(parcelas),
            "total_ubicaciones": ubicaciones_creadas
        })
        
    except Exception as e:
        conn.rollback()
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)
    finally:
        conn.close()


@router.get("/almacen/config")
async def get_almacen_config():
    """Return current warehouse configuration summary."""
    if not DB_PATH.exists():
        return {
            "pasillos": 0,
            "estanterias": 0,
            "alturas": 0,
            "parcelas": [],
            "capacidad_max": 100.0
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) as total FROM sqlite_master WHERE type='table' AND name='almacen_ubicaciones'")
        exists = cursor.fetchone()["total"]
        if not exists:
            return {
                "pasillos": 0,
                "estanterias": 0,
                "alturas": 0,
                "parcelas": [],
                "capacidad_max": 100.0
            }

        cursor.execute("SELECT COUNT(*) as total FROM almacen_ubicaciones WHERE organization_id = 1")
        total = cursor.fetchone()["total"]
        if total == 0:
            return {
                "pasillos": 0,
                "estanterias": 0,
                "alturas": 0,
                "parcelas": [],
                "capacidad_max": 100.0
            }

        cursor.execute("SELECT MAX(pasillo) as max_pasillo FROM almacen_ubicaciones WHERE organization_id = 1")
        pasillos = cursor.fetchone()["max_pasillo"] or 0

        cursor.execute("SELECT COUNT(DISTINCT estanteria) as cnt FROM almacen_ubicaciones WHERE organization_id = 1")
        estanterias = cursor.fetchone()["cnt"] or 0

        cursor.execute("SELECT MAX(altura) as max_altura FROM almacen_ubicaciones WHERE organization_id = 1")
        alturas = cursor.fetchone()["max_altura"] or 0

        cursor.execute("SELECT DISTINCT parcela FROM almacen_ubicaciones WHERE organization_id = 1")
        parcelas = [row["parcela"] for row in cursor.fetchall()]

        cursor.execute("SELECT capacidad_max FROM almacen_ubicaciones WHERE organization_id = 1 LIMIT 1")
        cap = cursor.fetchone()["capacidad_max"] if total > 0 else 100.0

        return {
            "pasillos": pasillos,
            "estanterias": estanterias,
            "alturas": alturas,
            "parcelas": parcelas,
            "capacidad_max": cap
        }
    except Exception:
        return {
            "pasillos": 0,
            "estanterias": 0,
            "alturas": 0,
            "parcelas": [],
            "capacidad_max": 100.0
        }
    finally:
        conn.close()


@router.post("/almacen/configurar")
async def configurar_almacen(payload: dict):
    """Rebuild warehouse with custom dimensions."""
    if not DB_PATH.exists():
        return JSONResponse(content={"success": False, "message": "Database not found"}, status_code=500)

    pasillos = int(payload.get("pasillos", 0))
    estanterias = int(payload.get("estanterias", 0))
    alturas = int(payload.get("alturas", 0))
    parcelas = payload.get("parcelas", []) or []
    capacidad_max = float(payload.get("capacidad_max", 100.0))

    if pasillos <= 0 or estanterias <= 0 or alturas <= 0:
        return JSONResponse(content={"success": False, "message": "Dimensiones inválidas"}, status_code=400)
    if estanterias > 26:
        return JSONResponse(content={"success": False, "message": "Máximo 26 estanterías (A-Z)"}, status_code=400)
    if not parcelas:
        return JSONResponse(content={"success": False, "message": "Debe indicar al menos una parcela"}, status_code=400)

    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    estanterias_list = list(letras[:estanterias])

    conn = get_db()
    cursor = conn.cursor()

    try:
        # Ensure tables exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS almacen_ubicaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL DEFAULT 1,
                codigo VARCHAR(50) UNIQUE NOT NULL,
                pasillo INTEGER NOT NULL,
                estanteria VARCHAR(1) NOT NULL,
                altura INTEGER NOT NULL,
                parcela VARCHAR(10) NOT NULL,
                capacidad_max FLOAT DEFAULT 100.0,
                ocupado FLOAT DEFAULT 0.0,
                producto_id INTEGER,
                activo BOOLEAN DEFAULT 1,
                notas TEXT,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS almacen_movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL DEFAULT 1,
                tipo VARCHAR(50) NOT NULL,
                ubicacion_origen_id INTEGER,
                ubicacion_destino_id INTEGER,
                producto_id INTEGER NOT NULL,
                cantidad FLOAT NOT NULL,
                usuario VARCHAR(100),
                fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                referencia VARCHAR(100),
                notas TEXT,
                FOREIGN KEY (ubicacion_origen_id) REFERENCES almacen_ubicaciones(id),
                FOREIGN KEY (ubicacion_destino_id) REFERENCES almacen_ubicaciones(id),
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)

        # Clear existing locations
        cursor.execute("DELETE FROM almacen_ubicaciones WHERE organization_id = 1")

        ubicaciones_creadas = 0
        for pasillo in range(1, pasillos + 1):
            for est in estanterias_list:
                for altura in range(1, alturas + 1):
                    for parcela in parcelas:
                        codigo = f"P{pasillo:02d}-{est}{altura}-{parcela.upper()}"
                        cursor.execute(
                            """
                            INSERT INTO almacen_ubicaciones 
                            (organization_id, codigo, pasillo, estanteria, altura, parcela, capacidad_max, ocupado, activo)
                            VALUES (1, ?, ?, ?, ?, ?, ?, 0.0, 1)
                            """,
                            (codigo, pasillo, est, altura, parcela.upper(), capacidad_max)
                        )
                        ubicaciones_creadas += 1

        conn.commit()

        return JSONResponse(content={
            "success": True,
            "message": f"Almacén reconfigurado: {ubicaciones_creadas} ubicaciones",
            "pasillos": pasillos,
            "estanterias": estanterias,
            "alturas": alturas,
            "parcelas": parcelas,
            "capacidad_max": capacidad_max,
            "total_ubicaciones": ubicaciones_creadas
        })
    except Exception as e:
        conn.rollback()
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)
    finally:
        conn.close()


@router.get("/almacen/catalogo")
async def catalogo_almacen():
    """Return available pasillos, estanterias y alturas for UI selectors."""
    if not DB_PATH.exists():
        return {"pasillos": [], "estanterias": [], "alturas": []}

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT pasillo FROM almacen_ubicaciones WHERE organization_id = 1 ORDER BY pasillo")
        pasillos = [row["pasillo"] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT estanteria FROM almacen_ubicaciones WHERE organization_id = 1 ORDER BY estanteria")
        estanterias = [row["estanteria"] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT altura FROM almacen_ubicaciones WHERE organization_id = 1 ORDER BY altura")
        alturas = [row["altura"] for row in cursor.fetchall()]

        return {"pasillos": pasillos, "estanterias": estanterias, "alturas": alturas}
    except Exception:
        return {"pasillos": [], "estanterias": [], "alturas": []}
    finally:
        conn.close()


@router.post("/almacen/editar-bloque")
async def editar_bloque_almacen(payload: dict):
    """Bulk edit locations by pasillo / estanteria / altura (optional filters)."""
    if not DB_PATH.exists():
        return JSONResponse(content={"success": False, "message": "Database not found"}, status_code=500)

    pasillo = payload.get("pasillo")
    estanteria = payload.get("estanteria")
    altura = payload.get("altura")
    capacidad_max = payload.get("capacidad_max")
    activo = payload.get("activo")

    if pasillo is None:
        return JSONResponse(content={"success": False, "message": "Pasillo es requerido"}, status_code=400)

    updates = []
    params = []
    if capacidad_max is not None:
        try:
            cap = float(capacidad_max)
        except Exception:
            return JSONResponse(content={"success": False, "message": "capacidad_max inválida"}, status_code=400)
        updates.append("capacidad_max = ?")
        params.append(cap)

    if activo is not None:
        act_val = 1 if bool(activo) else 0
        updates.append("activo = ?")
        params.append(act_val)

    if not updates:
        return JSONResponse(content={"success": False, "message": "Nada para actualizar"}, status_code=400)

    where_clauses = ["organization_id = 1", "pasillo = ?"]
    params.append(int(pasillo))

    if estanteria:
        where_clauses.append("estanteria = ?")
        params.append(estanteria)
    if altura:
        where_clauses.append("altura = ?")
        params.append(int(altura))

    query = f"UPDATE almacen_ubicaciones SET {', '.join(updates)} WHERE " + " AND ".join(where_clauses)

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return JSONResponse(content={
            "success": True,
            "message": "Ubicaciones actualizadas",
            "rows_affected": cursor.rowcount
        })
    except Exception as e:
        conn.rollback()
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)
    finally:
        conn.close()


@router.post("/inventario/reset-y-compras")
async def reset_stock_y_compras_demo():
    """Poner stock en 0 y generar orden de compra automática por stock mínimo + necesidades de OP abiertas."""
    if not DB_PATH.exists():
        return JSONResponse(content={"success": False, "message": "Database not found"}, status_code=500)

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Asegurar tablas de compras
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL,
                numero VARCHAR(50) UNIQUE NOT NULL,
                fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                proveedor_id INTEGER,
                proveedor_nombre VARCHAR(200) NOT NULL,
                proveedor_documento VARCHAR(50),
                proveedor_email VARCHAR(150),
                total NUMERIC(10,2) NOT NULL DEFAULT 0,
                estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
                notas TEXT,
                creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
                actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS compras_detalle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                compra_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad FLOAT NOT NULL,
                precio_unitario NUMERIC(10,2) NOT NULL DEFAULT 0,
                subtotal NUMERIC(10,2) NOT NULL DEFAULT 0
            )
            """
        )

        # Poner stock en 0
        cursor.execute("UPDATE productos SET stock_actual = 0 WHERE organization_id = 1")

        # Base shortages por stock mínimo
        cursor.execute(
            """
            SELECT id, codigo, nombre, COALESCE(stock_minimo, 0) AS stock_minimo, COALESCE(precio_compra, 0) AS precio_compra
            FROM productos
            WHERE organization_id = 1
            """
        )
        productos = cursor.fetchall()
        faltantes = {}
        precio_map = {}
        nombre_map = {}
        for p in productos:
            pid = p["id"]
            faltantes[pid] = max(p["stock_minimo"], 0)
            precio_map[pid] = float(p["precio_compra"] or 0)
            nombre_map[pid] = p["nombre"]

        # Necesidades por órdenes de producción abiertas
        cursor.execute(
            """
            SELECT bom_id, cantidad_ordenada
            FROM ordenes_produccion
            WHERE organization_id = 1 AND estado NOT IN ('completada', 'cancelada')
            """
        )
        ordenes = cursor.fetchall()
        if ordenes:
            bom_ids = list({row["bom_id"] for row in ordenes if row["bom_id"]})
            bom_componentes = {}
            for bom_id in bom_ids:
                cursor.execute(
                    """
                    SELECT componente_id, cantidad
                    FROM bom_lines
                    WHERE organization_id = 1 AND bom_header_id = ?
                    """,
                    (bom_id,),
                )
                bom_componentes[bom_id] = cursor.fetchall()

            for row in ordenes:
                bom_id = row["bom_id"]
                qty = row["cantidad_ordenada"] or 0
                for comp in bom_componentes.get(bom_id, []):
                    comp_id = comp["componente_id"]
                    comp_qty = comp["cantidad"] or 0
                    faltantes[comp_id] = faltantes.get(comp_id, 0) + comp_qty * qty

        # Crear compra si hay faltantes
        items = [(pid, qty) for pid, qty in faltantes.items() if qty and qty > 0]
        if not items:
            conn.commit()
            return JSONResponse(content={"success": True, "message": "Stock puesto en 0, sin faltantes"})

        # Generar número
        cursor.execute("SELECT COUNT(*) FROM compras WHERE organization_id = 1")
        count = cursor.fetchone()[0] or 0
        numero = f"PO-AUTO-{count + 1:05d}"

        total = 0
        for pid, qty in items:
            total += qty * precio_map.get(pid, 0)

        cursor.execute(
            """
            INSERT INTO compras (organization_id, numero, proveedor_nombre, total, estado, notas)
            VALUES (1, ?, 'Proveedor Automático', ?, 'pendiente', 'Generado por stock 0 y necesidades de OP abiertas')
            """,
            (numero, total),
        )
        compra_id = cursor.lastrowid

        for pid, qty in items:
            precio = precio_map.get(pid, 0)
            subtotal = qty * precio
            cursor.execute(
                """
                INSERT INTO compras_detalle (compra_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
                """,
                (compra_id, pid, qty, precio, subtotal),
            )

        conn.commit()
        return JSONResponse(content={
            "success": True,
            "message": "Stock puesto en 0 y compra generada",
            "compra_numero": numero,
            "items": [
                {"producto_id": pid, "nombre": nombre_map.get(pid), "cantidad": qty, "precio_unitario": precio_map.get(pid, 0)}
                for pid, qty in items
            ]
        })

    except Exception as e:
        conn.rollback()
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=500)
    finally:
        conn.close()


@router.get("/almacen/ubicaciones")
async def get_almacen_ubicaciones(
    pasillo: int = None,
    estanteria: str = None,
    ocupadas: bool = None
):
    """Get warehouse locations with optional filters."""
    if not DB_PATH.exists():
        return []
    
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        query = """
            SELECT 
                u.id, u.codigo, u.pasillo, u.estanteria, u.altura, u.parcela,
                u.capacidad_max, u.ocupado, u.producto_id, u.activo,
                p.nombre as producto_nombre, p.codigo as producto_codigo
            FROM almacen_ubicaciones u
            LEFT JOIN productos p ON u.producto_id = p.id
            WHERE u.organization_id = 1
        """
        params = []
        
        if pasillo is not None:
            query += " AND u.pasillo = ?"
            params.append(pasillo)
        
        if estanteria is not None:
            query += " AND u.estanteria = ?"
            params.append(estanteria)
        
        if ocupadas is not None:
            if ocupadas:
                query += " AND u.ocupado > 0"
            else:
                query += " AND u.ocupado = 0"
        
        query += " ORDER BY u.pasillo, u.estanteria, u.altura, u.parcela"
        
        cursor.execute(query, params)
        rows = [dict(r) for r in cursor.fetchall()]
        return rows
        
    except Exception:
        return []
    finally:
        conn.close()

