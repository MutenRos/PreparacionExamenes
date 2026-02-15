"""API routes for Oficina Técnica - BOM management."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List

from dario_app.core.auth import get_org_id, get_tenant_db
from dario_app.modules.oficina_tecnica.models import BOMHeader, BOMLine, BOMOperacion
from dario_app.modules.oficina_tecnica.schemas import (
    BOMHeaderCreate,
    BOMHeaderUpdate,
    BOMHeaderResponse,
    BOMSummary,
    BOMLineCreate,
    BOMLineResponse,
    BOMOperacionCreate,
    BOMOperacionResponse,
)
from dario_app.modules.inventario.models import Producto, Proveedor

router = APIRouter(prefix="/api/oficina-tecnica", tags=["oficina-tecnica"])


# ============ SEEDING ENDPOINT ============

@router.post("/seed-bombas", status_code=200)
async def seed_bom_bombas(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """
    Create BOMs for all 6 Bombas Omni pump types with operations and materials.
    Idempotent: returns error if BOMs already exist.
    """
    from decimal import Decimal
    
    # Check if BOMs already exist
    existing = await db.scalar(
        select(BOMHeader).where(BOMHeader.organization_id == org_id).limit(1)
    )
    if existing:
        raise HTTPException(status_code=400, detail="BOMs ya existen en el sistema")
    
    # Get all products to link as components
    todos_productos = await db.execute(
        select(Producto).where(Producto.organization_id == org_id)
    )
    productos = todos_productos.scalars().all()
    
    if not productos:
        raise HTTPException(status_code=400, detail="No hay productos en el sistema")
    
    # Map product codes to IDs for linking
    producto_map = {p.codigo: p.id for p in productos}
    
    # BOM definitions with inline operations and materials
    boms_definicion = [
        {
            "nombre": "BOM Bomba Centrífuga BC-100",
            "codigo": "BOM-BC100-001",
            "producto_codigo": "BC-100-001",
            "version": "1.0",
            "descripcion": "Bill of Materials para ensamblaje de Bomba Centrífuga BC-100",
            "notas": "Bomba de una etapa, impulsión lateral. Voltaje 220V/380V",
            "materiales": [
                {"seq": 10, "desc": "Motor Eléctrico 1 HP", "qty": 1},
                {"seq": 20, "desc": "Carcasa / Chassis", "qty": 1},
                {"seq": 30, "desc": "Manguera PVC", "qty": 2},
                {"seq": 40, "desc": "Impulsor acero", "qty": 1},
                {"seq": 50, "desc": "Sello mecánico", "qty": 1},
                {"seq": 60, "desc": "Rodamientos", "qty": 2},
            ],
            "operaciones": [
                {"seq": 10, "nombre": "Mecanizado eje", "tipo": "mecanizado_interno", "duracion": 1.5, "costo": "45.00"},
                {"seq": 20, "nombre": "Ensamblaje rodamiento", "tipo": "ensamblaje", "duracion": 0.5, "costo": "15.00"},
                {"seq": 30, "nombre": "Ensamblaje impulsor", "tipo": "ensamblaje", "duracion": 1.0, "costo": "25.00"},
                {"seq": 40, "nombre": "Ensamblaje motor-bomba", "tipo": "ensamblaje", "duracion": 2.0, "costo": "50.00"},
                {"seq": 50, "nombre": "Control de calidad", "tipo": "control_calidad", "duracion": 1.0, "costo": "20.00"},
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
                {"seq": 10, "desc": "Motor Eléctrico 2 HP", "qty": 1},
                {"seq": 20, "desc": "Carcasa sumergible", "qty": 1},
                {"seq": 30, "desc": "Manguera reforzada", "qty": 3},
                {"seq": 40, "desc": "Impulsor acero inox", "qty": 2},
                {"seq": 50, "desc": "Sello mecánico doble", "qty": 2},
                {"seq": 60, "desc": "Rodamientos especiales", "qty": 3},
            ],
            "operaciones": [
                {"seq": 10, "nombre": "Mecanizado eje largo", "tipo": "mecanizado_interno", "duracion": 2.5, "costo": "75.00"},
                {"seq": 20, "nombre": "Mecanizado externo", "tipo": "mecanizado_externo", "duracion": 3.0, "costo": "120.00"},
                {"seq": 30, "nombre": "Ensamblaje multiétapas", "tipo": "ensamblaje", "duracion": 3.0, "costo": "85.00"},
                {"seq": 40, "nombre": "Prueba estanqueidad", "tipo": "control_calidad", "duracion": 1.5, "costo": "40.00"},
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
                {"seq": 10, "desc": "Motor Eléctrico 1.5 HP", "qty": 1},
                {"seq": 20, "desc": "Carcasa estándar", "qty": 1},
                {"seq": 30, "desc": "Manguera PVC", "qty": 2},
                {"seq": 40, "desc": "Impulsor acero", "qty": 1},
                {"seq": 50, "desc": "Sello mecánico", "qty": 1},
                {"seq": 60, "desc": "Rodamientos", "qty": 2},
            ],
            "operaciones": [
                {"seq": 10, "nombre": "Mecanizado álabes", "tipo": "mecanizado_interno", "duracion": 2.0, "costo": "60.00"},
                {"seq": 20, "nombre": "Balanceo dinámico", "tipo": "control_calidad", "duracion": 1.5, "costo": "35.00"},
                {"seq": 30, "nombre": "Ensamblaje y prueba", "tipo": "ensamblaje", "duracion": 1.5, "costo": "40.00"},
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
                {"seq": 10, "desc": "Motor Diésel 3 HP", "qty": 1},
                {"seq": 20, "desc": "Carcasa reforzada", "qty": 1},
                {"seq": 30, "desc": "Tanque combustible", "qty": 1},
                {"seq": 40, "desc": "Manguera industrial", "qty": 3},
                {"seq": 50, "desc": "Impulsor acero inox", "qty": 1},
                {"seq": 60, "desc": "Sello mecánico reforzado", "qty": 2},
            ],
            "operaciones": [
                {"seq": 10, "nombre": "Ensamblaje motor-bomba", "tipo": "ensamblaje", "duracion": 3.0, "costo": "90.00"},
                {"seq": 20, "nombre": "Instalación combustible", "tipo": "ensamblaje", "duracion": 2.0, "costo": "70.00"},
                {"seq": 30, "nombre": "Prueba potencia", "tipo": "control_calidad", "duracion": 2.0, "costo": "60.00"},
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
                {"seq": 10, "desc": "Motor Eléctrico 2.5 HP", "qty": 1},
                {"seq": 20, "desc": "Carcasa compacta", "qty": 1},
                {"seq": 30, "desc": "Manguera presión", "qty": 2},
                {"seq": 40, "desc": "Impulsor acero", "qty": 1},
                {"seq": 50, "desc": "Válvula alivio", "qty": 1},
                {"seq": 60, "desc": "Rodamientos", "qty": 2},
            ],
            "operaciones": [
                {"seq": 10, "nombre": "Mecanizado eje y válvula", "tipo": "mecanizado_interno", "duracion": 2.0, "costo": "60.00"},
                {"seq": 20, "nombre": "Ensamblaje sistema presión", "tipo": "ensamblaje", "duracion": 1.5, "costo": "45.00"},
                {"seq": 30, "nombre": "Prueba presión", "tipo": "control_calidad", "duracion": 1.0, "costo": "30.00"},
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
                {"seq": 10, "desc": "Motor 5 HP trifásico", "qty": 1},
                {"seq": 20, "desc": "Carcasa industrial", "qty": 1},
                {"seq": 30, "desc": "Manguera industrial 2 pulgadas", "qty": 2},
                {"seq": 40, "desc": "Impulsor acero inox dúplex", "qty": 2},
                {"seq": 50, "desc": "Sello mecánico doble", "qty": 2},
                {"seq": 60, "desc": "Rodamientos especiales", "qty": 4},
            ],
            "operaciones": [
                {"seq": 10, "nombre": "Mecanizado multiétapas", "tipo": "mecanizado_interno", "duracion": 4.0, "costo": "120.00"},
                {"seq": 20, "nombre": "Subcontratación mecanizado", "tipo": "mecanizado_externo", "duracion": 5.0, "costo": "200.00"},
                {"seq": 30, "nombre": "Ensamblaje multiétapas", "tipo": "ensamblaje", "duracion": 4.0, "costo": "120.00"},
                {"seq": 40, "nombre": "Balanceo dinámico", "tipo": "control_calidad", "duracion": 2.5, "costo": "80.00"},
                {"seq": 50, "nombre": "Prueba bajo carga", "tipo": "control_calidad", "duracion": 3.0, "costo": "100.00"},
            ]
        },
    ]
    
    created_count = 0
    material_count = 0
    operation_count = 0
    
    # Create BOMs
    for bom_def in boms_definicion:
        # Get producto ID
        producto_id = producto_map.get(bom_def["producto_codigo"])
        if not producto_id:
            continue
        
        # Create BOM header
        bom = BOMHeader(
            organization_id=org_id,
            producto_id=producto_id,
            nombre=bom_def["nombre"],
            codigo=bom_def["codigo"],
            version=bom_def["version"],
            descripcion=bom_def["descripcion"],
            notas_tecnicas=bom_def.get("notas"),
            cantidad_producida=Decimal("1.0"),
            unidad_medida="unidad",
            activo=True,
            es_principal=True,
        )
        db.add(bom)
        await db.flush()
        created_count += 1
        
        # Add materials (BOM Lines)
        for mat in bom_def.get("materiales", []):
            # Use first product as component (for demo purposes)
            primer_producto = productos[0] if productos else None
            if primer_producto:
                line = BOMLine(
                    organization_id=org_id,
                    bom_header_id=bom.id,
                    componente_id=primer_producto.id,
                    cantidad=mat.get("qty", 1),
                    unidad_medida="unidad",
                    secuencia=mat.get("seq", 10),
                    es_opcional=False,
                    notas=mat.get("desc", ""),
                    factor_desperdicio=Decimal("0.05"),
                )
                db.add(line)
                material_count += 1
        
        # Add operations
        for op in bom_def.get("operaciones", []):
            operacion = BOMOperacion(
                organization_id=org_id,
                bom_header_id=bom.id,
                nombre=op.get("nombre"),
                codigo=f"OP-{bom_def['codigo']}-{op.get('seq')}",
                tipo_operacion=op.get("tipo", "ensamblaje"),
                secuencia=op.get("seq", 10),
                duracion_estimada=op.get("duracion", 1.0),
                centro_trabajo="Producción",
                proveedor_id=None,
                costo_operacion=Decimal(op.get("costo", "0")),
                descripcion=op.get("nombre"),
                instrucciones=op.get("nombre"),
            )
            db.add(operacion)
            operation_count += 1
    
    await db.commit()
    
    return {
        "message": "BOMs para bombas creadas exitosamente",
        "boms_creadas": created_count,
        "materiales_agregados": material_count,
        "operaciones_agregadas": operation_count,
    }


@router.get("/boms/", response_model=List[BOMSummary])
async def list_boms(
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
    activo: bool = Query(None),
    producto_id: int = Query(None),
):
    """List all BOMs with summary information."""
    query = (
        select(
            BOMHeader.id,
            BOMHeader.codigo,
            BOMHeader.nombre,
            BOMHeader.version,
            BOMHeader.activo,
            Producto.nombre.label("producto_nombre"),
            func.count(BOMLine.id).label("total_componentes"),
        )
        .join(Producto, BOMHeader.producto_id == Producto.id)
        .outerjoin(BOMLine, BOMHeader.id == BOMLine.bom_header_id)
        .where(BOMHeader.organization_id == org_id)
        .group_by(BOMHeader.id, Producto.nombre)
    )

    if activo is not None:
        query = query.where(BOMHeader.activo == activo)
    
    if producto_id:
        query = query.where(BOMHeader.producto_id == producto_id)

    result = await db.execute(query)
    boms = result.all()

    # Get operation counts separately
    summaries = []
    for bom in boms:
        op_count = await db.scalar(
            select(func.count(BOMOperacion.id)).where(BOMOperacion.bom_header_id == bom.id)
        )
        summaries.append(
            BOMSummary(
                id=bom.id,
                codigo=bom.codigo,
                nombre=bom.nombre,
                producto_nombre=bom.producto_nombre,
                version=bom.version,
                activo=bom.activo,
                total_componentes=bom.total_componentes or 0,
                total_operaciones=op_count or 0,
            )
        )

    return summaries


@router.get("/boms/{bom_id}", response_model=BOMHeaderResponse)
async def get_bom(
    bom_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Get BOM details with all lines and operations."""
    result = await db.execute(
        select(BOMHeader)
        .options(
            selectinload(BOMHeader.lineas).selectinload(BOMLine.componente),
            selectinload(BOMHeader.operaciones).selectinload(BOMOperacion.proveedor),
            selectinload(BOMHeader.producto),
        )
        .where(BOMHeader.id == bom_id, BOMHeader.organization_id == org_id)
    )
    bom = result.scalar_one_or_none()

    if not bom:
        raise HTTPException(status_code=404, detail="BOM no encontrado")

    # Prepare response
    response_data = {
        "id": bom.id,
        "organization_id": bom.organization_id,
        "producto_id": bom.producto_id,
        "producto_nombre": bom.producto.nombre if bom.producto else None,
        "producto_codigo": bom.producto.codigo if bom.producto else None,
        "nombre": bom.nombre,
        "codigo": bom.codigo,
        "version": bom.version,
        "cantidad_producida": bom.cantidad_producida,
        "unidad_medida": bom.unidad_medida.value if bom.unidad_medida else "unidad",
        "descripcion": bom.descripcion,
        "notas_tecnicas": bom.notas_tecnicas,
        "activo": bom.activo,
        "es_principal": bom.es_principal,
        "lineas": [
            {
                "id": linea.id,
                "bom_header_id": linea.bom_header_id,
                "organization_id": linea.organization_id,
                "componente_id": linea.componente_id,
                "componente_nombre": linea.componente.nombre if linea.componente else None,
                "componente_codigo": linea.componente.codigo if linea.componente else None,
                "cantidad": linea.cantidad,
                "unidad_medida": linea.unidad_medida.value if linea.unidad_medida else "unidad",
                "secuencia": linea.secuencia,
                "es_opcional": linea.es_opcional,
                "notas": linea.notas,
                "factor_desperdicio": linea.factor_desperdicio,
            }
            for linea in sorted(bom.lineas, key=lambda x: x.secuencia)
        ],
        "operaciones": [
            {
                "id": op.id,
                "bom_header_id": op.bom_header_id,
                "organization_id": op.organization_id,
                "nombre": op.nombre,
                "codigo": op.codigo,
                "tipo_operacion": op.tipo_operacion.value if op.tipo_operacion else None,
                "secuencia": op.secuencia,
                "duracion_estimada": op.duracion_estimada,
                "centro_trabajo": op.centro_trabajo,
                "proveedor_id": op.proveedor_id,
                "proveedor_nombre": op.proveedor.nombre if op.proveedor else None,
                "costo_operacion": op.costo_operacion,
                "descripcion": op.descripcion,
                "instrucciones": op.instrucciones,
            }
            for op in sorted(bom.operaciones, key=lambda x: x.secuencia)
        ],
    }

    return response_data


@router.post("/boms/", response_model=BOMHeaderResponse, status_code=status.HTTP_201_CREATED)
async def create_bom(
    bom_data: BOMHeaderCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Create a new BOM with lines and operations."""
    
    # Verify product exists
    producto = await db.get(Producto, bom_data.producto_id)
    if not producto or producto.organization_id != org_id:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Check if code already exists
    existing = await db.scalar(
        select(BOMHeader).where(BOMHeader.codigo == bom_data.codigo, BOMHeader.organization_id == org_id)
    )
    if existing:
        raise HTTPException(status_code=400, detail="El código de BOM ya existe")

    # Create BOM header
    bom = BOMHeader(
        organization_id=org_id,
        producto_id=bom_data.producto_id,
        nombre=bom_data.nombre,
        codigo=bom_data.codigo,
        version=bom_data.version,
        cantidad_producida=bom_data.cantidad_producida,
        unidad_medida=bom_data.unidad_medida,
        descripcion=bom_data.descripcion,
        notas_tecnicas=bom_data.notas_tecnicas,
        activo=bom_data.activo,
        es_principal=bom_data.es_principal,
    )
    db.add(bom)
    await db.flush()

    # Create lines
    for line_data in bom_data.lineas:
        line = BOMLine(
            organization_id=org_id,
            bom_header_id=bom.id,
            componente_id=line_data.componente_id,
            cantidad=line_data.cantidad,
            unidad_medida=line_data.unidad_medida,
            secuencia=line_data.secuencia,
            es_opcional=line_data.es_opcional,
            notas=line_data.notas,
            factor_desperdicio=line_data.factor_desperdicio,
        )
        db.add(line)

    # Create operations
    for op_data in bom_data.operaciones:
        operacion = BOMOperacion(
            organization_id=org_id,
            bom_header_id=bom.id,
            nombre=op_data.nombre,
            codigo=op_data.codigo,
            tipo_operacion=op_data.tipo_operacion,
            secuencia=op_data.secuencia,
            duracion_estimada=op_data.duracion_estimada,
            centro_trabajo=op_data.centro_trabajo,
            proveedor_id=op_data.proveedor_id,
            costo_operacion=op_data.costo_operacion,
            descripcion=op_data.descripcion,
            instrucciones=op_data.instrucciones,
        )
        db.add(operacion)

    await db.commit()
    await db.refresh(bom)

    # Return created BOM
    return await get_bom(bom.id, org_id, db)


@router.put("/boms/{bom_id}", response_model=BOMHeaderResponse)
async def update_bom(
    bom_id: int,
    bom_data: BOMHeaderUpdate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Update BOM header information."""
    bom = await db.scalar(
        select(BOMHeader).where(BOMHeader.id == bom_id, BOMHeader.organization_id == org_id)
    )

    if not bom:
        raise HTTPException(status_code=404, detail="BOM no encontrado")

    # Update fields
    update_data = bom_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bom, field, value)

    await db.commit()
    return await get_bom(bom_id, org_id, db)


@router.delete("/boms/{bom_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bom(
    bom_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a BOM (soft delete by setting activo=False)."""
    bom = await db.scalar(
        select(BOMHeader).where(BOMHeader.id == bom_id, BOMHeader.organization_id == org_id)
    )

    if not bom:
        raise HTTPException(status_code=404, detail="BOM no encontrado")

    bom.activo = False
    await db.commit()


# ===== BOM Lines endpoints =====

@router.post("/boms/{bom_id}/lineas/", response_model=BOMLineResponse, status_code=status.HTTP_201_CREATED)
async def add_bom_line(
    bom_id: int,
    line_data: BOMLineCreate,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Add a new line to an existing BOM."""
    bom = await db.scalar(
        select(BOMHeader).where(BOMHeader.id == bom_id, BOMHeader.organization_id == org_id)
    )
    if not bom:
        raise HTTPException(status_code=404, detail="BOM no encontrado")

    line = BOMLine(
        organization_id=org_id,
        bom_header_id=bom_id,
        **line_data.model_dump()
    )
    db.add(line)
    await db.commit()
    await db.refresh(line)

    # Get component name
    componente = await db.get(Producto, line.componente_id)
    
    return BOMLineResponse(
        id=line.id,
        bom_header_id=line.bom_header_id,
        organization_id=line.organization_id,
        componente_id=line.componente_id,
        componente_nombre=componente.nombre if componente else None,
        componente_codigo=componente.codigo if componente else None,
        cantidad=line.cantidad,
        unidad_medida=line.unidad_medida.value if line.unidad_medida else "unidad",
        secuencia=line.secuencia,
        es_opcional=line.es_opcional,
        notas=line.notas,
        factor_desperdicio=line.factor_desperdicio,
    )


@router.delete("/boms/lineas/{line_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bom_line(
    line_id: int,
    org_id: int = Depends(get_org_id),
    db: AsyncSession = Depends(get_tenant_db),
):
    """Delete a BOM line."""
    line = await db.scalar(
        select(BOMLine).where(BOMLine.id == line_id, BOMLine.organization_id == org_id)
    )
    if not line:
        raise HTTPException(status_code=404, detail="Línea de BOM no encontrada")

    await db.delete(line)
    await db.commit()
