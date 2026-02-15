# OmniERP ⚡ — Sistema ERP Empresarial Completo

![OmniERP — 74 módulos, 775+ endpoints, paridad con Microsoft Dynamics 365](https://img.shields.io/badge/Stack-Python%20%7C%20FastAPI%20%7C%20SQLAlchemy%20%7C%20Jinja2-667eea?style=for-the-badge)

## Introducción

OmniERP es un sistema ERP empresarial completo desarrollado con **Python y FastAPI** que alcanza paridad funcional con Microsoft Dynamics 365. Integra **74 módulos** (inventario, ventas, compras, producción, RRHH, contabilidad, CRM, logística, POS y más), **775+ endpoints REST**, autenticación JWT con 2FA, arquitectura multi-tenant con bases de datos SQLite por organización y un frontend basado en plantillas Jinja2 con un design system CSS propio. Es un proyecto ambicioso que demuestra cómo construir una aplicación empresarial real desde cero.

---

## Desarrollo de las partes

### 1. Arquitectura FastAPI — Application Factory y Módulos

El punto de entrada es `src/dario_app/main.py` (12 líneas), que delega la creación de la aplicación a `create_app()` en `src/dario_app/api/__init__.py`. Esta función usa el patrón **Application Factory**: configura el lifespan (inicialización de BD), registra middleware CORS, monta archivos estáticos y registra más de 50 routers de forma ordenada.

```python
# src/dario_app/api/__init__.py, líneas 24-34
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name, 
        version=settings.version, 
        lifespan=lifespan,
        description="Enterprise ERP System - Microsoft Dynamics 365 Class",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )
```

Cada módulo (ventas, inventario, compras, etc.) se importa y registra como un router independiente, manteniendo la separación de responsabilidades. El proyecto tiene más de 50 módulos importados en esta factoría.

---

### 2. Base de Datos Multi-Tenant — SQLAlchemy Async + SQLite

El sistema implementa **multi-tenancy** con una base de datos maestra para organizaciones/usuarios y bases separadas por organización. Todo funciona con SQLAlchemy 2.0 async y aiosqlite.

```python
# src/dario_app/database/__init__.py, líneas 12-23
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MASTER_DB_PATH = DATA_DIR / "erp.db"
MASTER_DATABASE_URL = f"sqlite+aiosqlite:///{MASTER_DB_PATH}"

# Directorio para bases de datos por organización (tenant)
ORG_DB_DIR = DATA_DIR / "org_dbs"
```

La función `get_tenant_engine(org_id)` cachea los engines para evitar crearlos en cada petición, y `get_db()` decide automáticamente si usar la BD maestra o la del tenant según el contexto.

---

### 3. Modelos SQLAlchemy — Ejemplo: Producto e Inventario

Los modelos usan la sintaxis moderna de SQLAlchemy 2.0 con `Mapped` y `mapped_column`. El modelo `Producto` es central al sistema:

```python
# src/dario_app/modules/inventario/models.py, líneas 38-75
class Producto(Base):
    """Gestiona productos del inventario incluyendo precios, stock,
    ubicación en almacén y relación con proveedores."""
    
    __tablename__ = "productos"
    
    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    precio_compra: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    precio_venta: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    stock_actual: Mapped[int] = mapped_column(Integer, default=0)
    stock_minimo: Mapped[int] = mapped_column(Integer, default=0)
    
    @property
    def stock_bajo(self) -> bool:
        """Indica si el stock actual está por debajo del mínimo configurado."""
        return self.stock_actual < self.stock_minimo
```

Cada campo usa tipos estrictos (`Decimal` para precios, `Boolean` para flags) e incluye índices en las columnas de búsqueda frecuente (`codigo`, `sku`, `categoria`).

---

### 4. Validaciones Pydantic — Schemas con field_validator

Las rutas API usan modelos Pydantic v2 con validadores personalizados que aseguran la integridad de los datos antes de llegar a la base de datos:

```python
# src/dario_app/modules/ventas/routes.py, líneas 31-47
class VentaDetalleCreate(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    
    @field_validator('cantidad')
    @classmethod
    def validate_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v
    
    @field_validator('precio_unitario')
    @classmethod
    def validate_precio(cls, v):
        if v < 0:
            raise ValueError('El precio no puede ser negativo')
        return v
```

Los esquemas de inventario también validan precios y stock con el decorador `@field_validator`, rechazando valores negativos antes de cualquier operación de escritura.

---

### 5. Autenticación JWT con Sesión por Cookie

El módulo `auth` (`src/dario_app/modules/auth/routes.py`) implementa login/registro con JWT almacenado en cookies HttpOnly. La función `create_access_token()` genera tokens con expiración de 1 semana:

```python
# src/dario_app/modules/auth/routes.py, líneas 50-59
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
```

El sistema soporta registro con creación automática de organización (tenant), hash de contraseñas con bcrypt, y registro del cliente en la organización administradora.

---

### 6. Design System CSS — Variables y Componentes

OmniERP tiene un design system completo definido en `src/dario_app/static/css/variables.css` (127 líneas) con variables para colores de marca, semánticos, neutros, sombras, tipografía y spacing:

```css
/* src/dario_app/static/css/variables.css, líneas 6-13 */
:root {
    --brand-primary: #667eea;
    --brand-secondary: #764ba2;
    --brand-accent: #10b981;
    --color-success: #10b981;
    --color-danger: #ef4444;
    --color-warning: #f59e0b;
}
```

El archivo `global.css` (932 líneas) extiende este sistema con un segundo conjunto de variables (`--primary: #2563eb`), transiciones premium, y escala de z-index. El archivo `components.css` (548 líneas) define tarjetas de estadísticas, módulos, y elementos de navegación con gradientes y animaciones. Se incluye soporte a dark mode via `@media (prefers-color-scheme: dark)`.

---

### 7. Dashboard — Interfaz Principal con Módulos y Estadísticas

El dashboard (`src/dario_app/templates/dashboard.html`, 589 líneas) es la interfaz central. Muestra 4 stat-cards con datos del backend (productos, ventas del mes, usuarios, órdenes), una cuadrícula de 21 módulos con iconos emoji, y un panel asistente con acordeones de compras sugeridas y recordatorios.

```html
<!-- src/dario_app/templates/dashboard.html, líneas 325-345 -->
<div class="stats">
    <div class="stat-card">
        <div class="icon">📦</div>
        <div class="value" id="statProductos">—</div>
        <div class="label">Productos en inventario</div>
    </div>
    <!-- ... 3 más: Ventas, Usuarios, Órdenes -->
</div>
```

Las estadísticas se cargan dinámicamente con `fetch('/api/reportes/resumen-dashboard')` al cargar la página, formateando los valores monetarios en euros con `toLocaleString()`.

---

### 8. POS (Punto de Venta) — Terminal de Venta Interactivo

El módulo POS (`src/dario_app/templates/pos.html`, 494 líneas) implementa un terminal de punto de venta con diseño split (2/3 productos, 1/3 carrito). La sección de productos muestra un grid responsive con búsqueda en tiempo real, y el carrito maneja cantidades, impuestos y total con botón de "Confirmar Venta".

```html
<!-- src/dario_app/templates/pos.html, líneas 58-72 -->
<div class="pos-container">
    <!-- Grid: 2fr para productos, 1fr para carrito -->
    <div class="products-panel"><!-- Catálogo con búsqueda --></div>
    <div class="cart-panel"><!-- Carrito y checkout --></div>
</div>
```

El POS se conecta con el módulo de ventas: las ventas creadas desde POS quedan en estado `pendiente_aprobacion` y aparecen en la vista de Ventas para ser aprobadas por un supervisor.

---

### 9. Módulo de Ventas — Aprobaciones y Detalles Expandibles

La vista de ventas (`src/dario_app/templates/ventas.html`, 526 líneas) tiene dos secciones: ventas pendientes de aprobación (del POS) con botones de Aprobar/Rechazar, y el historial completo con filas expandibles mostrando los detalles de cada venta.

```javascript
// src/dario_app/templates/ventas.html, líneas ~250-260
async function cargarVentas() {
    let respPend = await fetch('/api/ventas/pendientes-aprobacion');
    // ... Renderiza tabla con botones de aprobación
    // Cada fila tiene un toggle ▶ que expande detalles (productos, cantidades, subtotales)
}
```

Las rutas Python en `src/dario_app/modules/ventas/routes.py` (867 líneas) gestionan el CRUD completo, incluyendo generación automática de facturas PDF, envío por email, y cumplimiento fiscal español (NIF/NIE, SII/TicketBAI).

---

### 10. Inventario — Tabs, Stock Bajo y Gestión Completa

La vista de inventario (`src/dario_app/templates/inventario.html`, 877 líneas) usa un sistema de tabs para separar productos, proveedores y movimientos de stock. Los productos con stock por debajo del mínimo se resaltan con la clase `.stock-bajo` (fondo amarillo).

```css
/* src/dario_app/templates/inventario.html, línea ~78 */
.stock-bajo {
    background: #fef3c7 !important;  /* Amarillo suave para stock bajo */
}
```

Las rutas de inventario (`src/dario_app/modules/inventario/routes.py`, 335 líneas) exponen endpoints para CRUD de productos y proveedores, con validators Pydantic que rechazan precios y stock negativos.

---

## Presentación del proyecto

OmniERP arranca con un login limpio centrado en pantalla con gradiente violeta-azul. Al autenticarse, el dashboard muestra 4 tarjetas resumen con datos en tiempo real: productos en inventario, ventas del mes, usuarios activos y órdenes pendientes. Debajo, una cuadrícula de 21 módulos con iconos emoji permite acceder a cualquier área del sistema.

El flujo típico de negocio comienza en el POS: el empleado busca productos, los añade al carrito y confirma la venta. La venta aparece automáticamente en la sección de Ventas como "Pendiente de Aprobación", donde el supervisor la revisa, ve los detalles expandibles y decide aprobar o rechazar. Al aprobar, se generan las órdenes de producción correspondientes.

Desde Inventario, el usuario gestiona productos con tabs para productos, proveedores y movimientos. Los productos con stock bajo se destacan en amarillo, y el asistente del dashboard sugiere compras automáticas basándose en el stock mínimo configurado.

El sistema detrás utiliza FastAPI con 775+ endpoints, SQLAlchemy async para máximo rendimiento, y una arquitectura multi-tenant donde cada organización tiene su propia base de datos SQLite, aislando completamente los datos entre clientes.

---

## Conclusión

OmniERP demuestra que es posible construir un sistema ERP de nivel empresarial usando Python moderno y herramientas de código abierto. Con 74 módulos que cubren desde el punto de venta hasta recursos humanos, pasando por logística, producción y CRM, el proyecto refleja la complejidad real de un software empresarial. La arquitectura está bien definida: FastAPI como framework web async, SQLAlchemy 2.0 con mapeo moderno `Mapped`, Pydantic v2 para validación, JWT para autenticación, y un design system CSS con variables consistentes. La separación en módulos independientes con sus propios modelos, rutas y plantillas permite escalar sin perder organización. Es un proyecto que va más allá de un ejercicio académico y se acerca a lo que se encuentra en la industria real.
