# Flujo End-to-End OmniERP

Objetivo: Implementar el flujo completo desde proyecto hasta salida de fábrica, con documentos imprimibles en cada hito y automatización de órdenes.

## Resumen de etapas y documentos

1. Proyecto (Project Ops)
   - Documento imprimible del proyecto (ficha, alcance, cronograma, recursos)
   - Estado: draft → active → completed → converted_to_sale

2. Presupuesto (Ventas: Presupuesto/Cotización)
   - Documento imprimible del presupuesto
   - Estado: borrador → enviado → aceptado → rechazado

3. Pedido de Venta (Ventas: Pedido)
   - Documento imprimible de pedido de venta
   - Dispara generación de Órdenes de Trabajo por producto/kit

4. Órdenes de Trabajo (Producción)
   - Documento imprimible de orden de trabajo
   - Asignación a sección de producción

5. Órdenes de Movimiento (Logística/Carretilleros)
   - Movimiento Almacén → Picking Sección Producción
   - Documento imprimible del movimiento
   - Si falta stock → disparar Pedido de Compra

6. Pedido de Compra (Compras)
   - Un proveedor por pedido
   - Documento imprimible del pedido de compra
   - Estado: borrador → aprobado → enviado

7. Recepción de Compra (Puertas de Entrada)
   - Registro de entrada, actualización de inventario
   - Movimientos: Playa Entrada → Picking de secciones (si vinculado) o Ubicación de almacén
   - Documento imprimible de recepción/albarán de compra

8. Producción (Manufactura)
   - Inicio, incidencias, solicitudes de material extra
   - Registro final de tiempos, consumo, incidencias
   - Transformación de materiales a producto final en inventario
   - Informe de Orden de Producción (imprimible)

9. Embalaje
   - Reunir productos del pedido, embalar, dimensiones/peso, tiempos
   - Movimiento: Embalaje → Playa de salida
   - Documento imprimible del packing list

10. Salida de Fábrica / Expedición
   - Generar Albarán de envío (imprimible)
   - Generar Factura (imprimible PDF usando PDFGenerator)
   - Solicitar recogida a agencia logística / flota propia

## Eventos y disparadores clave

- Proyecto → Presupuesto: botón "Convertir a Venta (Presupuesto)"
- Presupuesto aceptado → Pedido de Venta
- Pedido de Venta confirmado → Generar Órdenes de Trabajo
- Órdenes de Trabajo asignadas → Generar Movimientos de carretilleros
- Stock insuficiente → Generar Pedidos de Compra (1 proveedor por pedido)
- Pedido de Compra aprobado → Envío a proveedor
- Llegada de mercancía → Registro Entrada + Movimientos a Picking/Ubicación
- Termina Producción → Informe de Producción + Movimiento a Embalaje
- Fin Embalaje → Movimiento a Playa de Salida
- Pedido en salida → Generar Albarán + Factura

## Endpoints de impresión (propuestos)

- Project Ops: `GET /api/project-ops/projects/{id}/print`
- Ventas:
  - Presupuesto: `GET /api/ventas/presupuestos/{id}/print`
  - Pedido de venta: `GET /api/ventas/pedidos/{id}/print`
  - Albarán: `GET /api/ventas/albaranes/{id}/print`
  - Factura: `GET /api/ventas/facturas/{id}/print` (PDFGenerator)
- Compras: `GET /api/compras/pedidos/{id}/print`
- Producción:
  - Orden de trabajo: `GET /api/produccion/ordenes/{id}/print`
  - Informe de producción: `GET /api/produccion/ordenes/{id}/report/print`
- Logística:
  - Movimiento: `GET /api/logistica/movimientos/{id}/print`
  - Packing list: `GET /api/logistica/embalajes/{id}/print`

## Plantillas imprimibles (HTML)

Estructura en `templates/print/`:
- `base.html` → layout y estilos
- `project.html`
- `presupuesto.html`
- `pedido_venta.html`
- `pedido_compra.html`
- `orden_trabajo.html`
- `movimiento.html`
- `recepcion_compra.html`
- `informe_produccion.html`
- `packing_list.html`
- `albaran.html`
- `factura.html` (opcional HTML además de PDF)

CSS global para impresión en `/static/print.css`.

## Datos mínimos por documento

- Proyecto: código, nombre, cliente, presupuesto, fechas, tareas, recursos
- Presupuesto: número, cliente, items, totales, condiciones
- Pedido venta: número, cliente, items, totales, condiciones
- Pedido compra: número, proveedor, items, totales, condiciones
- Orden trabajo: código, producto, BOM, pasos, sección, tiempos planificados
- Movimiento: origen, destino, materiales, cantidades, responsable
- Recepción compra: pedido, bultos, cantidades, incidencias, ubicaciones
- Informe producción: tiempos, incidencias, consumos, scrap, output, responsable
- Packing list: pedido, bultos, dimensiones, peso, contenidos
- Albarán: pedido, consignatario, bultos, transporte
- Factura: venta, impuestos, totales, términos

## Consideraciones

- Multi-tenant: todos los documentos aislados por `organization_id`
- Permisos: endpoints protegidos por módulo/acción
- Auditoría: registrar eventos de generación/impresión
- PDF: para factura y albarán usar `PDFGenerator` + `DocumentTemplate`
- Idioma/branding: `DocumentTemplate` por organización

## Roadmap (fases)

Fase 1 (hoje):
- Proyecto imprimible (HTML)
- Presupuesto imprimible (HTML)
- Estándar de CSS y base layout

Fase 2:
- Pedido venta + compra imprimibles
- Órdenes de trabajo y movimientos imprimibles

Fase 3:
- Recepción compra + packing list + informe producción

Fase 4:
- Albarán + Factura (PDF y HTML)
- Integración con logística
