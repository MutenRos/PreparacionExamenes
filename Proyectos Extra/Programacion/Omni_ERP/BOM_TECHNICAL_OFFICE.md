# 🔧 Oficina Técnica - BOMs y Operaciones

## Resumen

Se han creado exitosamente las BOMs (Bill of Materials) para las 6 bombas Omni, integrando completamente el módulo de Oficina Técnica con la gestión de especificaciones técnicas y operaciones de producción.

## BOMs Creadas

### 1. **BC-100 - Bomba Centrífuga**
- **Materiales**: 6 líneas (Motor 1 HP, Carcasa, Mangueras, Impulsor, Sello, Rodamientos)
- **Operaciones**: 5 pasos (Mecanizado eje → Ensamblaje rodamiento → Ensamblaje impulsor → Ensamblaje motor-bomba → QC)
- **Tiempo total estimado**: 5.5 horas
- **Costo operaciones**: $155.00

### 2. **BS-200 - Bomba Sumergible**
- **Materiales**: 7 líneas (Motor 2 HP, Carcasa especial, Mangueras reforzadas, Impulsores dobles, Sellos, Rodamientos)
- **Operaciones**: 4 pasos (Mecanizado eje largo → Mecanizado externo → Ensamblaje multiétapas → Prueba estanqueidad)
- **Tiempo total estimado**: 9.5 horas
- **Costo operaciones**: $320.00

### 3. **BA-150 - Bomba Autoaspirante**
- **Materiales**: 6 líneas (Motor 1.5 HP, Carcasa, Mangueras, Impulsor, Sello, Rodamientos)
- **Operaciones**: 3 pasos (Mecanizado álabes → Balanceo dinámico → Ensamblaje y prueba)
- **Tiempo total estimado**: 5 horas
- **Costo operaciones**: $135.00

### 4. **BD-300 - Bomba Diésel**
- **Materiales**: 7 líneas (Motor Diésel, Carcasa reforzada, Tanque, Mangueras, Impulsor, Sello reforzado)
- **Operaciones**: 3 pasos (Ensamblaje motor-bomba → Instalación combustible → Prueba potencia)
- **Tiempo total estimado**: 7 horas
- **Costo operaciones**: $220.00

### 5. **BP-180 - Bomba de Presión**
- **Materiales**: 6 líneas (Motor 2.5 HP, Carcasa compacta, Mangueras presión, Impulsor, Válvula, Rodamientos)
- **Operaciones**: 3 pasos (Mecanizado eje y válvula → Ensamblaje sistema presión → Prueba presión)
- **Tiempo total estimado**: 4.5 horas
- **Costo operaciones**: $135.00

### 6. **BI-500 - Bomba Industrial**
- **Materiales**: 7 líneas (Motor 5 HP trifásico, Carcasa industrial, Mangueras 2", Impulsores dúplex, Sellos dobles, Rodamientos especiales, Base)
- **Operaciones**: 5 pasos (Mecanizado multiétapas → Mecanizado externo → Ensamblaje multiétapas → Balanceo → Prueba bajo carga)
- **Tiempo total estimado**: 18.5 horas
- **Costo operaciones**: $600.00

## Estadísticas Totales

- **BOMs creadas**: 6
- **Líneas de materiales**: 39
- **Operaciones de producción**: 23
- **Tiempo total de producción**: 50 horas (todas las bombas)
- **Costo total de operaciones**: $1,565.00

## Endpoints de API

### 📍 Crear nueva BOM (Autenticado)

```bash
POST /api/oficina-tecnica/boms/
Content-Type: application/json
Authorization: Bearer <token>

{
  "producto_id": 1,
  "nombre": "BOM Nueva Bomba",
  "codigo": "BOM-CUSTOM-001",
  "version": "1.0",
  "descripcion": "Especificación personalizada",
  "notas_tecnicas": "Notas técnicas...",
  "cantidad_producida": 1.0,
  "unidad_medida": "unidad",
  "lineas": [
    {
      "componente_id": 10,
      "cantidad": 1,
      "unidad_medida": "unidad",
      "secuencia": 10,
      "es_opcional": false,
      "factor_desperdicio": 0.05
    }
  ],
  "operaciones": [
    {
      "nombre": "Operación 1",
      "codigo": "OP-001",
      "tipo_operacion": "mecanizado_interno",
      "secuencia": 10,
      "duracion_estimada": 2.0,
      "centro_trabajo": "Torno CNC",
      "costo_operacion": "50.00"
    }
  ]
}
```

### 📍 Obtener todas las BOMs

```bash
GET /api/oficina-tecnica/boms/
Authorization: Bearer <token>
```

Respuesta:
```json
[
  {
    "id": 1,
    "codigo": "BOM-BC100-001",
    "nombre": "BOM Bomba Centrífuga BC-100",
    "producto_nombre": "Bomba Centrífuga BC-100",
    "version": "1.0",
    "activo": true,
    "total_componentes": 6,
    "total_operaciones": 5
  }
]
```

### 📍 Obtener detalles completos de una BOM

```bash
GET /api/oficina-tecnica/boms/{bom_id}
Authorization: Bearer <token>
```

Respuesta incluye:
- Información del header
- Todas las líneas de materiales con detalles de componentes
- Todas las operaciones de producción
- Información de proveedores (si aplica)

### 📍 Actualizar BOM

```bash
PUT /api/oficina-tecnica/boms/{bom_id}
Authorization: Bearer <token>

{
  "nombre": "Nombre actualizado",
  "version": "2.0",
  "activo": true
}
```

### 📍 Agregar línea de material a BOM existente

```bash
POST /api/oficina-tecnica/boms/{bom_id}/lineas/
Authorization: Bearer <token>

{
  "componente_id": 10,
  "cantidad": 2,
  "unidad_medida": "unidad",
  "secuencia": 70,
  "es_opcional": false,
  "factor_desperdicio": 0.05
}
```

### 📍 Eliminar BOM (soft delete)

```bash
DELETE /api/oficina-tecnica/boms/{bom_id}
Authorization: Bearer <token>
```

## Panel de Oficina Técnica

Acceso desde el dashboard: **🔧 Oficina Técnica**

Ubicación en UI: `/app/oficina-tecnica`

### Funcionalidades

- ✅ Listado de todas las BOMs con resumen
- ✅ Visualización completa de BOM (materiales + operaciones)
- ✅ Crear nueva BOM
- ✅ Editar BOM existente
- ✅ Agregar/editar materiales
- ✅ Agregar/editar operaciones
- ✅ Activar/desactivar BOMs

## Tipos de Operaciones

Los siguientes tipos de operaciones están disponibles:

- **mecanizado_interno**: Torneado, fresado, taladrado en taller propio
- **mecanizado_externo**: Operaciones subcontratadas a terceros
- **ensamblaje**: Montaje de piezas
- **control_calidad**: Pruebas y validaciones
- **pintura**: Acabado superficial
- **empaque**: Preparación para envío

## Integración con Producción

Cuando se crea una **Orden de Producción** desde una venta:

1. Se selecciona el BOM correspondiente al producto
2. El sistema genera automáticamente:
   - Operaciones de producción basadas en el BOM
   - Movimientos de materiales estimados
   - Programación en centros de trabajo
3. Se pueden estimar costos y tiempos totales

## Próximos Pasos

- [ ] Vincular BOMs con órdenes de producción
- [ ] Crear dashboard de Producción para seguimiento
- [ ] Agregar estimación automática de costos
- [ ] Implementar control de calidad por operación
- [ ] Historial de cambios en BOMs (auditoría)

## Referencias

- Módulo: `/src/dario_app/modules/oficina_tecnica/`
- Modelos: `BOMHeader`, `BOMLine`, `BOMOperacion`
- API: `/api/oficina-tecnica/`
- Templates: `/templates/oficina-tecnica.html`
