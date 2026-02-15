"""ERP Action Executor - Ejecuta operaciones reales en el ERP desde comandos de voz."""

import re
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from dario_app.modules.inventario.models import Producto, Proveedor
from dario_app.modules.clientes.models import Cliente
from dario_app.modules.ventas.models import Venta, VentaDetalle
from dario_app.modules.compras.models import Compra, CompraDetalle
from dario_app.modules.usuarios.models import Usuario


class ERPActionExecutor:
    """Ejecuta acciones complejas en el ERP basadas en comandos de voz."""
    
    @staticmethod
    async def search_products(
        db: AsyncSession, 
        org_id: int, 
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca productos por nombre, código o categoría.
        Soporta filtros: es_alquiler, categoria, stock_bajo
        """
        stmt = select(Producto).where(
            Producto.organization_id == org_id,
            Producto.activo == True
        )
        
        # Búsqueda por texto
        if query:
            search_pattern = f"%{query}%"
            stmt = stmt.where(
                or_(
                    Producto.nombre.ilike(search_pattern),
                    Producto.codigo.ilike(search_pattern),
                    Producto.categoria.ilike(search_pattern)
                )
            )
        
        # Filtros adicionales
        if filters:
            if filters.get("categoria"):
                stmt = stmt.where(Producto.categoria.ilike(f"%{filters['categoria']}%"))
            if filters.get("stock_bajo"):
                stmt = stmt.where(Producto.stock_actual <= Producto.stock_minimo)
            # es_alquiler solo si la columna existe
            if filters.get("es_alquiler"):
                try:
                    stmt = stmt.where(Producto.es_alquiler == True)
                except Exception:
                    pass  # Columna no existe en esta BD
        
        stmt = stmt.limit(10)
        result = await db.execute(stmt)
        productos = result.scalars().all()
        
        return [
            {
                "id": p.id,
                "codigo": p.codigo,
                "nombre": p.nombre,
                "categoria": p.categoria,
                "stock_actual": p.stock_actual,
                "stock_minimo": p.stock_minimo,
                "precio_venta": float(p.precio_venta or 0),
                "es_alquiler": getattr(p, 'es_alquiler', False),
                "activo": p.activo
            }
            for p in productos
        ]
    
    @staticmethod
    async def get_product_details(
        db: AsyncSession,
        org_id: int,
        identifier: str  # código o nombre parcial
    ) -> Optional[Dict[str, Any]]:
        """Obtiene detalles completos de un producto específico."""
        stmt = select(Producto).where(
            Producto.organization_id == org_id,
            or_(
                Producto.codigo == identifier,
                Producto.nombre.ilike(f"%{identifier}%")
            )
        ).limit(1)
        
        result = await db.execute(stmt)
        producto = result.scalar_one_or_none()
        
        if not producto:
            return None
        
        # Obtener proveedor si existe
        proveedor = None
        if producto.proveedor_id:
            prov_stmt = select(Proveedor).where(Proveedor.id == producto.proveedor_id)
            prov_result = await db.execute(prov_stmt)
            prov = prov_result.scalar_one_or_none()
            if prov:
                proveedor = {"id": prov.id, "nombre": prov.nombre}
        
        return {
            "id": producto.id,
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "categoria": producto.categoria,
            "sku": producto.sku,
            "stock_actual": producto.stock_actual,
            "stock_minimo": producto.stock_minimo,
            "precio_compra": float(producto.precio_compra or 0),
            "precio_venta": float(producto.precio_venta or 0),
            "margen_porcentaje": float(producto.margen_porcentaje or 0),
            "es_alquiler": getattr(producto, 'es_alquiler', False),
            "visible_en_pos": producto.visible_en_pos,
            "proveedor": proveedor,
            "activo": producto.activo
        }
    
    @staticmethod
    async def create_product(
        db: AsyncSession,
        org_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Crea un nuevo producto desde comando de voz."""
        # Generar código si no se proporciona
        if not data.get("codigo"):
            count = await db.scalar(
                select(func.count(Producto.id)).where(Producto.organization_id == org_id)
            )
            data["codigo"] = f"PROD-{count + 1:04d}"
        
        producto = Producto(
            organization_id=org_id,
            codigo=data["codigo"],
            nombre=data["nombre"],
            descripcion=data.get("descripcion", ""),
            categoria=data.get("categoria", "General"),
            unidad_medida=data.get("unidad_medida", "unidad"),
            precio_compra=data.get("precio_compra", 0),
            precio_venta=data.get("precio_venta", 0),
            stock_actual=data.get("stock_actual", 0),
            stock_minimo=data.get("stock_minimo", 0),
            es_alquiler=data.get("es_alquiler", False),
            visible_en_pos=data.get("visible_en_pos", True),
            activo=True
        )
        
        db.add(producto)
        await db.commit()
        await db.refresh(producto)
        
        return {
            "id": producto.id,
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "es_alquiler": producto.es_alquiler
        }
    
    @staticmethod
    async def update_product_stock(
        db: AsyncSession,
        org_id: int,
        identifier: str,
        new_stock: int
    ) -> Optional[Dict[str, Any]]:
        """Actualiza el stock de un producto."""
        stmt = select(Producto).where(
            Producto.organization_id == org_id,
            or_(
                Producto.codigo == identifier,
                Producto.nombre.ilike(f"%{identifier}%")
            )
        ).limit(1)
        
        result = await db.execute(stmt)
        producto = result.scalar_one_or_none()
        
        if not producto:
            return None
        
        old_stock = producto.stock_actual
        producto.stock_actual = new_stock
        await db.commit()
        
        return {
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "stock_anterior": old_stock,
            "stock_nuevo": new_stock
        }
    
    @staticmethod
    async def search_clients(
        db: AsyncSession,
        org_id: int,
        query: str
    ) -> List[Dict[str, Any]]:
        """Busca clientes por nombre, email o NIF."""
        search_pattern = f"%{query}%"
        stmt = select(Cliente).where(
            Cliente.organization_id == org_id,
            or_(
                Cliente.nombre.ilike(search_pattern),
                Cliente.email.ilike(search_pattern),
                Cliente.nif.ilike(search_pattern)
            )
        ).limit(10)
        
        result = await db.execute(stmt)
        clientes = result.scalars().all()
        
        return [
            {
                "id": c.id,
                "nombre": c.nombre,
                "email": c.email,
                "telefono": c.telefono,
                "nif": c.nif,
                "direccion": c.direccion
            }
            for c in clientes
        ]
    
    @staticmethod
    async def create_client(
        db: AsyncSession,
        org_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Crea un nuevo cliente."""
        cliente = Cliente(
            organization_id=org_id,
            nombre=data["nombre"],
            email=data.get("email", ""),
            telefono=data.get("telefono", ""),
            nif=data.get("nif", ""),
            direccion=data.get("direccion", "")
        )
        
        db.add(cliente)
        await db.commit()
        await db.refresh(cliente)
        
        return {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "email": cliente.email
        }
    
    @staticmethod
    async def get_sales_stats(
        db: AsyncSession,
        org_id: int,
        period: str = "week"  # week, month, today
    ) -> Dict[str, Any]:
        """Obtiene estadísticas de ventas."""
        now = datetime.utcnow()
        
        if period == "today":
            start_date = datetime(now.year, now.month, now.day)
        elif period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=7)
        
        # Ventas totales
        stmt = select(
            func.count(Venta.id).label("count"),
            func.sum(Venta.total).label("total"),
            func.avg(Venta.total).label("promedio")
        ).where(
            Venta.organization_id == org_id,
            Venta.fecha >= start_date
        )
        
        result = await db.execute(stmt)
        stats = result.first()
        
        return {
            "periodo": period,
            "cantidad_ventas": stats.count or 0,
            "total_vendido": float(stats.total or 0),
            "ticket_promedio": float(stats.promedio or 0)
        }
    
    @staticmethod
    async def create_simple_sale(
        db: AsyncSession,
        org_id: int,
        cliente_id: Optional[int],
        productos: List[Dict[str, Any]]  # [{"producto_id": 1, "cantidad": 2}]
    ) -> Dict[str, Any]:
        """
        Crea una venta simple desde comando de voz.
        productos: lista de {"producto_id": int, "cantidad": int}
        """
        # Calcular total
        total = 0
        detalles = []
        
        for item in productos:
            producto_id = item["producto_id"]
            cantidad = item["cantidad"]
            
            # Obtener producto
            prod_stmt = select(Producto).where(Producto.id == producto_id)
            prod_result = await db.execute(prod_stmt)
            producto = prod_result.scalar_one_or_none()
            
            if not producto:
                continue
            
            precio = float(producto.precio_venta or 0)
            subtotal = precio * cantidad
            total += subtotal
            
            detalles.append({
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio_unitario": precio,
                "subtotal": subtotal
            })
        
        # Crear venta
        venta = Venta(
            organization_id=org_id,
            cliente_id=cliente_id,
            fecha=datetime.utcnow(),
            subtotal=total,
            total=total,
            estado="completada"
        )
        
        db.add(venta)
        await db.flush()
        
        # Crear detalles
        for detalle_data in detalles:
            detalle = VentaDetalle(
                venta_id=venta.id,
                producto_id=detalle_data["producto_id"],
                cantidad=detalle_data["cantidad"],
                precio_unitario=detalle_data["precio_unitario"],
                subtotal=detalle_data["subtotal"]
            )
            db.add(detalle)
            
            # Actualizar stock
            producto = await db.get(Producto, detalle_data["producto_id"])
            if producto:
                producto.stock_actual -= detalle_data["cantidad"]
        
        await db.commit()
        await db.refresh(venta)
        
        return {
            "venta_id": venta.id,
            "total": float(venta.total),
            "productos": len(detalles),
            "fecha": venta.fecha.isoformat()
        }
    
    @staticmethod
    async def get_low_stock_products(
        db: AsyncSession,
        org_id: int,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Obtiene productos con stock bajo."""
        stmt = select(Producto).where(
            Producto.organization_id == org_id,
            Producto.stock_actual <= Producto.stock_minimo,
            Producto.activo == True
        ).limit(limit)
        
        result = await db.execute(stmt)
        productos = result.scalars().all()
        
        return [
            {
                "codigo": p.codigo,
                "nombre": p.nombre,
                "stock_actual": p.stock_actual,
                "stock_minimo": p.stock_minimo,
                "deficit": p.stock_minimo - p.stock_actual
            }
            for p in productos
        ]
    
    @staticmethod
    async def get_rental_products(
        db: AsyncSession,
        org_id: int
    ) -> List[Dict[str, Any]]:
        """Obtiene todos los productos de alquiler."""
        try:
            stmt = select(Producto).where(
                Producto.organization_id == org_id,
                Producto.es_alquiler == True,
                Producto.activo == True
            )
            
            result = await db.execute(stmt)
            productos = result.scalars().all()
            
            return [
                {
                    "id": p.id,
                    "codigo": p.codigo,
                    "nombre": p.nombre,
                    "categoria": p.categoria,
                    "disponible": p.stock_actual > 0,
                    "stock_actual": p.stock_actual,
                    "precio_venta": float(p.precio_venta or 0)
                }
                for p in productos
            ]
        except Exception:
            # Si la columna es_alquiler no existe, retornar lista vacía
            return []


from datetime import timedelta
