"""Inventario API routes."""

from datetime import datetime
from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.core.auth import get_org_id, get_tenant_db

from .models import Producto, Proveedor

router = APIRouter(prefix="/api/inventario", tags=["inventario"])


# ============ PROVEEDOR SCHEMAS ============
class ProveedorCreate(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str | None = None
    contacto_nombre: str | None = None
    direccion: str | None = None
    terminos_pago: str | None = "30 días"
    descuento_volumen: Decimal | None = Decimal("0")
    dias_entrega_promedio: int | None = 7
    documento_proveedor: str | None = None
    notas: str | None = None
    es_activo: bool = True


class ProveedorResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str | None
    contacto_nombre: str | None
    direccion: str | None
    terminos_pago: str | None
    descuento_volumen: Decimal | None
    dias_entrega_promedio: int | None
    documento_proveedor: str | None
    es_activo: bool

    class Config:
        from_attributes = True


# ============ PRODUCTO SCHEMAS ============
class ProductoCreate(BaseModel):
    codigo: str
    nombre: str
    sku: str | None = None
    descripcion: str | None = None
    categoria: str | None = None
    ubicacion_almacen: str | None = None
    precio_compra: Decimal = Decimal("0.00")
    precio_venta: Decimal = Decimal("0.00")
    margen_porcentaje: Decimal | None = Decimal("20")
    stock_actual: int = 0
    stock_minimo: int = 0
    cantidad_minima_compra: int | None = 1
    unidad_medida: str = "unidad"
    proveedor_id: int | None = None
    activo: bool = True
    visible_en_pos: bool = True
    es_alquiler: bool = False

    @field_validator("precio_compra", "precio_venta", "margen_porcentaje")
    @classmethod
    def validate_precio(cls, v):
        if v is not None and v < 0:
            raise ValueError("Los precios no pueden ser negativos")
        return v

    @field_validator("stock_actual", "stock_minimo", "cantidad_minima_compra")
    @classmethod
    def validate_stock(cls, v):
        if v is not None and v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v


class ProductoResponse(BaseModel):
    id: int
    codigo: str
    sku: str | None
    nombre: str
    descripcion: str | None
    categoria: str | None
    ubicacion_almacen: str | None
    precio_compra: Decimal
    precio_venta: Decimal
    margen_porcentaje: Decimal | None
    stock_actual: int
    stock_minimo: int
    cantidad_minima_compra: int | None
    unidad_medida: str
    proveedor_id: int | None
    precio_ultima_compra: Decimal | None
    activo: bool
    visible_en_pos: bool
    es_alquiler: bool

    class Config:
        from_attributes = True


# ============ PROVEEDOR ROUTES ============
@router.get("/proveedores/", response_model=List[ProveedorResponse])
async def list_proveedores(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """List all suppliers for the organization."""
    result = await db.execute(select(Proveedor).where(Proveedor.organization_id == org_id))
    return result.scalars().all()


@router.post("/proveedores/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
async def create_proveedor(
    proveedor: ProveedorCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new supplier."""
    db_proveedor = Proveedor(**proveedor.model_dump(), organization_id=org_id)
    db.add(db_proveedor)
    await db.commit()
    await db.refresh(db_proveedor)
    return db_proveedor


@router.get("/proveedores/{proveedor_id}", response_model=ProveedorResponse)
async def get_proveedor(
    proveedor_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Get a supplier by ID."""
    result = await db.execute(
        select(Proveedor).where(Proveedor.id == proveedor_id, Proveedor.organization_id == org_id)
    )
    proveedor = result.scalar_one_or_none()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor


@router.put("/proveedores/{proveedor_id}", response_model=ProveedorResponse)
async def update_proveedor(
    proveedor_id: int,
    proveedor_update: ProveedorCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a supplier."""
    result = await db.execute(
        select(Proveedor).where(Proveedor.id == proveedor_id, Proveedor.organization_id == org_id)
    )
    db_proveedor = result.scalar_one_or_none()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    for key, value in proveedor_update.model_dump(exclude_unset=True).items():
        setattr(db_proveedor, key, value)

    await db.commit()
    await db.refresh(db_proveedor)
    return db_proveedor


# ============ PRODUCTO ROUTES ============
@router.get("/", response_model=List[ProductoResponse])
async def list_productos(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
):
    """List products with simple pagination."""
    offset = (page - 1) * limit
    result = await db.execute(
        select(Producto)
        .where(Producto.organization_id == org_id, Producto.activo == True)
        .order_by(Producto.id.desc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("", response_model=List[ProductoResponse], include_in_schema=False)
async def list_productos_no_slash(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000),
):
    """Alias sin slash final para evitar redirects."""
    return await list_productos(org_id=org_id, db=db, page=page, limit=limit)


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def create_producto(
    producto: ProductoCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new product."""
    # Generate auto-incremental codigo PROD/0000000
    max_result = await db.execute(
        select(func.max(Producto.id)).where(Producto.organization_id == org_id)
    )
    max_id = max_result.scalar() or 0
    next_id = max_id + 1
    codigo = f"PROD/{next_id:07d}"
    
    data = producto.model_dump()
    data["codigo"] = codigo
    db_producto = Producto(**data, organization_id=org_id)
    db.add(db_producto)
    await db.commit()
    await db.refresh(db_producto)
    return db_producto


@router.put("/{producto_id}", response_model=ProductoResponse)
async def update_producto(
    producto_id: int,
    producto_update: ProductoCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update an existing product. If stock falls below minimum, auto-generate purchase order."""
    result = await db.execute(
        select(Producto).where(Producto.id == producto_id, Producto.organization_id == org_id)
    )
    db_producto = result.scalar_one_or_none()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Check if stock_actual is being updated and will fall below minimum
    old_stock = db_producto.stock_actual
    updated_data = producto_update.model_dump(exclude_unset=True)
    new_stock = updated_data.get('stock_actual', old_stock)
    
    for key, value in updated_data.items():
        setattr(db_producto, key, value)
    
    db_producto.actualizado_en = datetime.utcnow()
    await db.commit()
    await db.refresh(db_producto)
    
    # Check if stock is now below minimum and trigger auto-purchase if needed
    if new_stock < db_producto.stock_minimo and old_stock >= db_producto.stock_minimo:
        # Stock just fell below minimum - auto-generate purchase order
        from dario_app.modules.compras.routes import _generar_compra_automatica
        try:
            result = await _generar_compra_automatica(org_id, db)
            if result:
                print(f"✓ Auto purchase order created: {result.numero}")
        except Exception as e:
            # Log but don't fail the update if purchase order generation has issues
            print(f"Warning: Failed to auto-generate purchase order: {str(e)}")
    
    return db_producto


@router.get("/{producto_id}", response_model=ProductoResponse)
async def get_producto(
    producto_id: int, org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """Get a product by ID."""
    result = await db.execute(
        select(Producto).where(Producto.id == producto_id, Producto.organization_id == org_id)
    )
    producto = result.scalar_one_or_none()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=ProductoResponse)
async def update_producto(
    producto_id: int,
    producto_update: ProductoCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update a product. If stock falls below minimum, auto-generate purchase order."""
    result = await db.execute(
        select(Producto).where(Producto.id == producto_id, Producto.organization_id == org_id)
    )
    db_producto = result.scalar_one_or_none()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Check if stock_actual is being updated and will fall below minimum
    old_stock = db_producto.stock_actual
    new_stock = producto_update.stock_actual if hasattr(producto_update, 'stock_actual') and producto_update.stock_actual is not None else old_stock
    
    for key, value in producto_update.model_dump(exclude_unset=True).items():
        setattr(db_producto, key, value)

    db_producto.actualizado_en = datetime.utcnow()
    await db.commit()
    await db.refresh(db_producto)
    
    # Check if stock is now below minimum and trigger auto-purchase if needed
    if new_stock < db_producto.stock_minimo and old_stock >= db_producto.stock_minimo:
        # Stock just fell below minimum - auto-generate purchase order
        from dario_app.modules.compras.routes import _generar_compra_automatica
        try:
            await _generar_compra_automatica(org_id, db)
        except Exception as e:
            # Log but don't fail the update if purchase order generation has issues
            print(f"Warning: Failed to auto-generate purchase order: {str(e)}")
    
    return db_producto


@router.get("/bajo-stock/", response_model=List[ProductoResponse])
async def list_bajo_stock(
    org_id: int = Depends(get_org_id), db: AsyncSession = Depends(get_tenant_db)
):
    """List products with low stock that may need auto-purchase."""
    result = await db.execute(
        select(Producto).where(
            Producto.stock_actual <= Producto.stock_minimo,
            Producto.organization_id == org_id,
            Producto.activo == True,
        )
    )
    return result.scalars().all()
