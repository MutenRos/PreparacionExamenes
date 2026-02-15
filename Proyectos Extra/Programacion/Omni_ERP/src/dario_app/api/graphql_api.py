"""GraphQL API implementation for advanced queries."""

import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from dario_app.core.auth import get_current_user_org


# GraphQL Types
@strawberry.type
class ProductoType:
    id: int
    nombre: str
    descripcion: Optional[str]
    sku: str
    precio_venta: float
    precio_compra: float
    stock_actual: int
    stock_minimo: int
    activo: bool


@strawberry.type
class ClienteType:
    id: int
    nombre: str
    email: Optional[str]
    telefono: Optional[str]
    tipo_cliente: str
    nivel_lealtad: str


@strawberry.type
class VentaType:
    id: int
    numero_venta: str
    fecha_venta: str
    total: float
    estado: str
    cliente: Optional[ClienteType]


@strawberry.type
class AnalyticsType:
    total_revenue: float
    total_orders: int
    average_order_value: float
    top_products: List[ProductoType]


# Queries
@strawberry.type
class Query:
    @strawberry.field
    async def productos(
        self,
        info,
        limit: int = 10,
        offset: int = 0,
        search: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> List[ProductoType]:
        """Get products with filters."""
        from sqlalchemy import select
        from dario_app.modules.inventario.models import Producto
        from dario_app.database import get_db
        
        # Get org_id from context
        request = info.context["request"]
        user_context = await get_current_user_org(request)
        
        if not user_context:
            return []
        
        org_id = user_context["org_id"]
        
        # Query products
        async for db in get_db(org_id):
            query = select(Producto).where(Producto.organization_id == org_id)
            
            if search:
                query = query.where(
                    Producto.nombre.contains(search) | Producto.sku.contains(search)
                )
            
            if activo is not None:
                query = query.where(Producto.activo == activo)
            
            query = query.limit(limit).offset(offset)
            result = await db.execute(query)
            productos = result.scalars().all()
            
            return [
                ProductoType(
                    id=p.id,
                    nombre=p.nombre,
                    descripcion=p.descripcion,
                    sku=p.sku,
                    precio_venta=float(p.precio_venta),
                    precio_compra=float(p.precio_compra),
                    stock_actual=p.stock_actual,
                    stock_minimo=p.stock_minimo,
                    activo=p.activo
                )
                for p in productos
            ]
        
        return []
    
    @strawberry.field
    async def ventas(
        self,
        info,
        limit: int = 10,
        estado: Optional[str] = None
    ) -> List[VentaType]:
        """Get sales with optional filters."""
        from sqlalchemy import select
        from dario_app.modules.ventas.models import Venta
        from dario_app.modules.clientes.models import Cliente
        from dario_app.database import get_db
        
        request = info.context["request"]
        user_context = await get_current_user_org(request)
        
        if not user_context:
            return []
        
        org_id = user_context["org_id"]
        
        async for db in get_db(org_id):
            query = select(Venta).where(Venta.organization_id == org_id)
            
            if estado:
                query = query.where(Venta.estado == estado)
            
            query = query.limit(limit)
            result = await db.execute(query)
            ventas = result.scalars().all()
            
            # Get clientes
            venta_list = []
            for v in ventas:
                cliente = None
                if v.cliente_id:
                    cliente_query = select(Cliente).where(Cliente.id == v.cliente_id)
                    cliente_result = await db.execute(cliente_query)
                    c = cliente_result.scalar_one_or_none()
                    if c:
                        cliente = ClienteType(
                            id=c.id,
                            nombre=c.nombre,
                            email=c.email,
                            telefono=c.telefono,
                            tipo_cliente=c.tipo_cliente,
                            nivel_lealtad=c.nivel_lealtad
                        )
                
                venta_list.append(
                    VentaType(
                        id=v.id,
                        numero_venta=v.numero_venta,
                        fecha_venta=v.fecha_venta.isoformat(),
                        total=float(v.total),
                        estado=v.estado,
                        cliente=cliente
                    )
                )
            
            return venta_list
        
        return []
    
    @strawberry.field
    async def analytics(self, info, days: int = 30) -> AnalyticsType:
        """Get analytics dashboard data."""
        from sqlalchemy import select, func
        from dario_app.modules.ventas.models import Venta, VentaDetalle
        from dario_app.modules.inventario.models import Producto
        from dario_app.database import get_db
        from datetime import timedelta
        
        request = info.context["request"]
        user_context = await get_current_user_org(request)
        
        if not user_context:
            return AnalyticsType(
                total_revenue=0.0,
                total_orders=0,
                average_order_value=0.0,
                top_products=[]
            )
        
        org_id = user_context["org_id"]
        start_date = datetime.utcnow() - timedelta(days=days)
        
        async for db in get_db(org_id):
            # Get sales metrics
            sales_query = select(
                func.sum(Venta.total).label('revenue'),
                func.count(Venta.id).label('orders'),
                func.avg(Venta.total).label('avg_value')
            ).where(
                Venta.organization_id == org_id,
                Venta.fecha_venta >= start_date
            )
            
            sales_result = await db.execute(sales_query)
            sales = sales_result.first()
            
            # Get top products
            top_query = select(
                Producto.id,
                Producto.nombre,
                Producto.sku,
                Producto.precio_venta,
                Producto.precio_compra,
                Producto.stock_actual,
                Producto.stock_minimo,
                Producto.activo,
                func.sum(VentaDetalle.cantidad).label('sold')
            ).join(
                VentaDetalle, VentaDetalle.producto_id == Producto.id
            ).join(
                Venta, Venta.id == VentaDetalle.venta_id
            ).where(
                Producto.organization_id == org_id,
                Venta.fecha_venta >= start_date
            ).group_by(
                Producto.id
            ).order_by(
                func.sum(VentaDetalle.cantidad).desc()
            ).limit(5)
            
            top_result = await db.execute(top_query)
            top_products = top_result.all()
            
            return AnalyticsType(
                total_revenue=float(sales.revenue or 0),
                total_orders=sales.orders or 0,
                average_order_value=float(sales.avg_value or 0),
                top_products=[
                    ProductoType(
                        id=p.id,
                        nombre=p.nombre,
                        descripcion=None,
                        sku=p.sku,
                        precio_venta=float(p.precio_venta),
                        precio_compra=float(p.precio_compra),
                        stock_actual=p.stock_actual,
                        stock_minimo=p.stock_minimo,
                        activo=p.activo
                    )
                    for p in top_products
                ]
            )
        
        return AnalyticsType(
            total_revenue=0.0,
            total_orders=0,
            average_order_value=0.0,
            top_products=[]
        )


# Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_producto(
        self,
        info,
        nombre: str,
        sku: str,
        precio_venta: float,
        precio_compra: float,
        stock_inicial: int = 0
    ) -> ProductoType:
        """Create a new product."""
        from dario_app.modules.inventario.models import Producto
        from dario_app.database import get_db
        
        request = info.context["request"]
        user_context = await get_current_user_org(request)
        
        if not user_context:
            raise Exception("Unauthorized")
        
        org_id = user_context["org_id"]
        
        async for db in get_db(org_id):
            producto = Producto(
                organization_id=org_id,
                nombre=nombre,
                sku=sku,
                precio_venta=Decimal(str(precio_venta)),
                precio_compra=Decimal(str(precio_compra)),
                stock_actual=stock_inicial,
                stock_minimo=10,
                activo=True
            )
            
            db.add(producto)
            await db.commit()
            await db.refresh(producto)
            
            return ProductoType(
                id=producto.id,
                nombre=producto.nombre,
                descripcion=producto.descripcion,
                sku=producto.sku,
                precio_venta=float(producto.precio_venta),
                precio_compra=float(producto.precio_compra),
                stock_actual=producto.stock_actual,
                stock_minimo=producto.stock_minimo,
                activo=producto.activo
            )


# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)


# Create GraphQL router
def create_graphql_router():
    """Create GraphQL router with context."""
    return GraphQLRouter(
        schema,
        context_getter=lambda request: {"request": request}
    )
