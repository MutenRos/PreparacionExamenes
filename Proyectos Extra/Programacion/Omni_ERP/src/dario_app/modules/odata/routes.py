"""OData V4 endpoints for Power BI integration - like Dynamics 365."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Any, Dict, List, Optional
from datetime import datetime
import json

from dario_app.core.auth import get_org_id, get_tenant_db
from dario_app.modules.ventas.models import Venta, VentaDetalle
from dario_app.modules.compras.models import Compra, CompraDetalle
from dario_app.modules.inventario.models import Producto
from dario_app.modules.clientes.models import Cliente


router = APIRouter(prefix="/odata/v4", tags=["odata"])


def odata_response(data: List[Dict], count: Optional[int] = None) -> Dict[str, Any]:
    """Format OData V4 response."""
    response = {
        "@odata.context": "$metadata",
        "value": data
    }
    if count is not None:
        response["@odata.count"] = count
    return response


@router.get("/")
async def odata_service_root():
    """OData V4 service root - list available entity sets."""
    return {
        "@odata.context": "$metadata",
        "value": [
            {"name": "Products", "kind": "EntitySet", "url": "Products"},
            {"name": "Sales", "kind": "EntitySet", "url": "Sales"},
            {"name": "SalesDetails", "kind": "EntitySet", "url": "SalesDetails"},
            {"name": "Purchases", "kind": "EntitySet", "url": "Purchases"},
            {"name": "Customers", "kind": "EntitySet", "url": "Customers"},
            {"name": "Suppliers", "kind": "EntitySet", "url": "Suppliers"},
            {"name": "Analytics", "kind": "EntitySet", "url": "Analytics"}
        ]
    }


@router.get("/$metadata")
async def odata_metadata():
    """OData V4 metadata document (EDMX)."""
    metadata = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema Namespace="OmniERP" xmlns="http://docs.oasis-open.org/odata/ns/edm">
      <EntityType Name="Product">
        <Key>
          <PropertyRef Name="id"/>
        </Key>
        <Property Name="id" Type="Edm.Int32" Nullable="false"/>
        <Property Name="nombre" Type="Edm.String"/>
        <Property Name="sku" Type="Edm.String"/>
        <Property Name="precio_venta" Type="Edm.Decimal"/>
        <Property Name="precio_compra" Type="Edm.Decimal"/>
        <Property Name="stock_actual" Type="Edm.Int32"/>
        <Property Name="stock_minimo" Type="Edm.Int32"/>
        <Property Name="activo" Type="Edm.Boolean"/>
      </EntityType>
      
      <EntityType Name="Sale">
        <Key>
          <PropertyRef Name="id"/>
        </Key>
        <Property Name="id" Type="Edm.Int32" Nullable="false"/>
        <Property Name="numero_venta" Type="Edm.String"/>
        <Property Name="fecha_venta" Type="Edm.DateTimeOffset"/>
        <Property Name="cliente_id" Type="Edm.Int32"/>
        <Property Name="total" Type="Edm.Decimal"/>
        <Property Name="pagado" Type="Edm.Decimal"/>
        <Property Name="estado" Type="Edm.String"/>
      </EntityType>
      
      <EntityType Name="Customer">
        <Key>
          <PropertyRef Name="id"/>
        </Key>
        <Property Name="id" Type="Edm.Int32" Nullable="false"/>
        <Property Name="nombre" Type="Edm.String"/>
        <Property Name="email" Type="Edm.String"/>
        <Property Name="telefono" Type="Edm.String"/>
        <Property Name="tipo_cliente" Type="Edm.String"/>
      </EntityType>
      
      <EntityContainer Name="Container">
        <EntitySet Name="Products" EntityType="OmniERP.Product"/>
        <EntitySet Name="Sales" EntityType="OmniERP.Sale"/>
        <EntitySet Name="Customers" EntityType="OmniERP.Customer"/>
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>"""
    
    from fastapi.responses import Response
    return Response(content=metadata, media_type="application/xml")


# ================== ENTITIES ==================

@router.get("/Products")
async def get_products(
    top: int = Query(100, alias="$top", le=1000),
    skip: int = Query(0, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    orderby: Optional[str] = Query(None, alias="$orderby"),
    count: bool = Query(False, alias="$count"),
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """OData V4 Products entity set."""
    
    # Build query
    query = select(Producto).where(Producto.organization_id == org_id)
    
    # Apply filter (simplified - real OData parser would be more complex)
    if filter:
        if "activo eq true" in filter.lower():
            query = query.where(Producto.activo == True)
        if "stock_actual gt" in filter.lower():
            try:
                value = int(filter.split("gt")[1].strip())
                query = query.where(Producto.stock_actual > value)
            except:
                pass
    
    # Apply orderby
    if orderby:
        if "nombre" in orderby:
            query = query.order_by(Producto.nombre.desc() if "desc" in orderby else Producto.nombre)
        elif "precio_venta" in orderby:
            query = query.order_by(Producto.precio_venta.desc() if "desc" in orderby else Producto.precio_venta)
    
    # Get count if requested
    total_count = None
    if count:
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await db.execute(count_query)
        total_count = count_result.scalar()
    
    # Apply pagination
    query = query.limit(top).offset(skip)
    
    # Execute query
    result = await db.execute(query)
    products = result.scalars().all()
    
    # Format response
    data = []
    for product in products:
        item = {
            "id": product.id,
            "nombre": product.nombre,
            "sku": product.sku,
            "precio_venta": float(product.precio_venta) if product.precio_venta else 0,
            "precio_compra": float(product.precio_compra) if product.precio_compra else 0,
            "stock_actual": product.stock_actual,
            "stock_minimo": product.stock_minimo,
            "activo": product.activo
        }
        
        # Apply select
        if select:
            fields = [f.strip() for f in select.split(",")]
            item = {k: v for k, v in item.items() if k in fields}
        
        data.append(item)
    
    return odata_response(data, total_count)


@router.get("/Sales")
async def get_sales(
    top: int = Query(100, alias="$top", le=1000),
    skip: int = Query(0, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    count: bool = Query(False, alias="$count"),
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """OData V4 Sales entity set."""
    
    query = select(Venta).where(Venta.organization_id == org_id)
    
    # Apply filter
    if filter:
        if "estado eq" in filter.lower():
            estado = filter.split("eq")[1].strip().strip("'")
            query = query.where(Venta.estado == estado)
    
    # Get count
    total_count = None
    if count:
        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total_count = count_result.scalar()
    
    # Pagination
    query = query.limit(top).offset(skip)
    
    result = await db.execute(query)
    sales = result.scalars().all()
    
    data = []
    for sale in sales:
        item = {
            "id": sale.id,
            "numero_venta": sale.numero_venta,
            "fecha_venta": sale.fecha_venta.isoformat() if sale.fecha_venta else None,
            "cliente_id": sale.cliente_id,
            "total": float(sale.total) if sale.total else 0,
            "pagado": float(sale.pagado) if sale.pagado else 0,
            "estado": sale.estado
        }
        
        if select:
            fields = [f.strip() for f in select.split(",")]
            item = {k: v for k, v in item.items() if k in fields}
        
        data.append(item)
    
    return odata_response(data, total_count)


@router.get("/Customers")
async def get_customers(
    top: int = Query(100, alias="$top", le=1000),
    skip: int = Query(0, alias="$skip"),
    filter: Optional[str] = Query(None, alias="$filter"),
    select: Optional[str] = Query(None, alias="$select"),
    count: bool = Query(False, alias="$count"),
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """OData V4 Customers entity set."""
    
    query = select(Cliente).where(Cliente.organization_id == org_id)
    
    # Get count
    total_count = None
    if count:
        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total_count = count_result.scalar()
    
    # Pagination
    query = query.limit(top).offset(skip)
    
    result = await db.execute(query)
    customers = result.scalars().all()
    
    data = []
    for customer in customers:
        item = {
            "id": customer.id,
            "nombre": customer.nombre,
            "email": customer.email if hasattr(customer, 'email') else None,
            "telefono": customer.telefono if hasattr(customer, 'telefono') else None,
            "tipo_cliente": customer.tipo_cliente if hasattr(customer, 'tipo_cliente') else "particular"
        }
        
        if select:
            fields = [f.strip() for f in select.split(",")]
            item = {k: v for k, v in item.items() if k in fields}
        
        data.append(item)
    
    return odata_response(data, total_count)


@router.get("/Analytics")
async def get_analytics_odata(
    top: int = Query(100, alias="$top"),
    skip: int = Query(0, alias="$skip"),
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """OData V4 Analytics entity set - aggregated KPIs."""
    
    from datetime import timedelta
    
    # Get various time periods
    periods = [7, 30, 90, 365]
    data = []
    
    for days in periods:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Revenue
        revenue_query = select(
            func.count(Venta.id).label('order_count'),
            func.sum(Venta.total).label('revenue'),
            func.avg(Venta.total).label('avg_order_value')
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha_venta >= start_date
        )
        revenue_result = await db.execute(revenue_query)
        revenue_data = revenue_result.first()
        
        # Products sold
        products_query = select(
            func.sum(VentaDetalle.cantidad).label('units_sold')
        ).join(
            Venta, Venta.id == VentaDetalle.venta_id
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha_venta >= start_date
        )
        products_result = await db.execute(products_query)
        units_sold = products_result.scalar() or 0
        
        data.append({
            "period_days": days,
            "period_label": f"Last {days} days",
            "order_count": revenue_data.order_count or 0,
            "total_revenue": float(revenue_data.revenue or 0),
            "avg_order_value": float(revenue_data.avg_order_value or 0),
            "units_sold": units_sold,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    return odata_response(data)


@router.get("/Products({id})")
async def get_product_by_id(
    id: int,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get single product by ID."""
    query = select(Producto).where(
        Producto.id == id,
        Producto.organization_id == org_id
    )
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "@odata.context": "$metadata#Products/$entity",
        "id": product.id,
        "nombre": product.nombre,
        "sku": product.sku,
        "precio_venta": float(product.precio_venta) if product.precio_venta else 0,
        "precio_compra": float(product.precio_compra) if product.precio_compra else 0,
        "stock_actual": product.stock_actual,
        "stock_minimo": product.stock_minimo,
        "activo": product.activo
    }


@router.get("/Sales({id})")
async def get_sale_by_id(
    id: int,
    db: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id)
):
    """Get single sale by ID."""
    query = select(Venta).where(
        Venta.id == id,
        Venta.organization_id == org_id
    )
    result = await db.execute(query)
    sale = result.scalar_one_or_none()
    
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    return {
        "@odata.context": "$metadata#Sales/$entity",
        "id": sale.id,
        "numero_venta": sale.numero_venta,
        "fecha_venta": sale.fecha_venta.isoformat() if sale.fecha_venta else None,
        "cliente_id": sale.cliente_id,
        "total": float(sale.total) if sale.total else 0,
        "pagado": float(sale.pagado) if sale.pagado else 0,
        "estado": sale.estado
    }
