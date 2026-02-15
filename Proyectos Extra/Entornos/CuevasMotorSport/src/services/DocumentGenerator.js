import jsPDF from 'jspdf'
import 'jspdf-autotable'

// Configuración de la empresa
const COMPANY_INFO = {
  name: 'Cuevas MotorSport',
  address: 'C/ Ejemplo, 123',
  city: '28001 Madrid',
  phone: '+34 600 000 000',
  email: 'info@cuevasmotorsport.com',
  cif: 'B12345678',
  web: 'www.cuevasmotorsport.com'
}

// Colores corporativos
const COLORS = {
  gold: [212, 175, 55],
  black: [10, 10, 10],
  gray: [100, 100, 100],
  lightGray: [240, 240, 240]
}

// Función auxiliar para formatear fecha
const formatDate = (date) => {
  if (!date) return new Date().toLocaleDateString('es-ES')
  return new Date(date).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

// Función auxiliar para formatear precio
const formatPrice = (price) => {
  if (!price) return '0,00 €'
  return Number(price).toLocaleString('es-ES', {
    style: 'currency',
    currency: 'EUR'
  })
}

// Función para añadir cabecera común
const addHeader = (doc, title, docNumber) => {
  // Logo/Nombre empresa
  doc.setFillColor(...COLORS.black)
  doc.rect(0, 0, 210, 40, 'F')
  
  doc.setTextColor(...COLORS.gold)
  doc.setFontSize(24)
  doc.setFont('helvetica', 'bold')
  doc.text(COMPANY_INFO.name, 20, 25)
  
  // Tipo de documento
  doc.setFontSize(12)
  doc.setTextColor(255, 255, 255)
  doc.text(title, 210 - 20, 18, { align: 'right' })
  
  // Número de documento
  doc.setFontSize(10)
  doc.text(docNumber, 210 - 20, 28, { align: 'right' })
  
  // Datos empresa
  doc.setTextColor(...COLORS.gray)
  doc.setFontSize(8)
  doc.setFont('helvetica', 'normal')
  doc.text(`${COMPANY_INFO.address} | ${COMPANY_INFO.city}`, 20, 50)
  doc.text(`Tel: ${COMPANY_INFO.phone} | Email: ${COMPANY_INFO.email} | CIF: ${COMPANY_INFO.cif}`, 20, 55)
  
  return 65 // Posición Y después de la cabecera
}

// Función para añadir pie de página
const addFooter = (doc, pageNum = 1, totalPages = 1) => {
  const pageHeight = doc.internal.pageSize.height
  
  doc.setDrawColor(...COLORS.gold)
  doc.setLineWidth(0.5)
  doc.line(20, pageHeight - 25, 190, pageHeight - 25)
  
  doc.setFontSize(8)
  doc.setTextColor(...COLORS.gray)
  doc.text(COMPANY_INFO.web, 20, pageHeight - 15)
  doc.text(`Página ${pageNum} de ${totalPages}`, 190, pageHeight - 15, { align: 'right' })
  doc.text('Documento generado electrónicamente - Cuevas MotorSport', 105, pageHeight - 10, { align: 'center' })
}

// Función para añadir sección de cliente
const addClientSection = (doc, startY, booking) => {
  doc.setFillColor(...COLORS.lightGray)
  doc.rect(20, startY, 170, 30, 'F')
  
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.setFont('helvetica', 'bold')
  doc.text('DATOS DEL CLIENTE', 25, startY + 8)
  
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(9)
  doc.text(`Nombre: ${booking.customerName || booking.name || 'N/A'}`, 25, startY + 16)
  doc.text(`Teléfono: ${booking.customerPhone || booking.phone || 'N/A'}`, 25, startY + 22)
  doc.text(`Email: ${booking.customerEmail || booking.email || 'N/A'}`, 110, startY + 16)
  
  return startY + 38
}

// Función para añadir sección de vehículo
const addVehicleSection = (doc, startY, vehicle) => {
  if (!vehicle) return startY
  
  doc.setFillColor(...COLORS.lightGray)
  doc.rect(20, startY, 170, 25, 'F')
  
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.setFont('helvetica', 'bold')
  doc.text('DATOS DEL VEHÍCULO', 25, startY + 8)
  
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(9)
  doc.text(`Vehículo: ${vehicle.brand || ''} ${vehicle.model || ''} (${vehicle.year || ''})`, 25, startY + 16)
  doc.text(`Matrícula: ${vehicle.matricula || 'N/A'}`, 25, startY + 22)
  doc.text(`Color: ${vehicle.color || 'N/A'}`, 110, startY + 16)
  doc.text(`KM: ${vehicle.kilometraje || 'N/A'}`, 110, startY + 22)
  
  return startY + 33
}

// ==========================================
// DOCUMENTO: SOLICITUD DE RESERVA
// ==========================================
export const generateSolicitudReserva = (booking, vehicle = null) => {
  const doc = new jsPDF()
  const docNumber = `SOL-${Date.now().toString().slice(-8)}`
  
  let y = addHeader(doc, 'SOLICITUD DE RESERVA', docNumber)
  
  // Fecha de solicitud
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.text(`Fecha de solicitud: ${formatDate(booking.createdAt || new Date())}`, 20, y)
  y += 10
  
  // Datos del cliente
  y = addClientSection(doc, y, booking)
  
  // Datos del vehículo si aplica
  if (vehicle) {
    y = addVehicleSection(doc, y, vehicle)
  }
  
  // Detalles de la reserva
  doc.setFillColor(...COLORS.gold)
  doc.rect(20, y, 170, 8, 'F')
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.setFont('helvetica', 'bold')
  doc.text('DETALLES DE LA SOLICITUD', 25, y + 6)
  y += 15
  
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(9)
  
  const details = [
    ['Servicio:', booking.service || booking.type || 'Alquiler de vehículo'],
    ['Fecha inicio:', formatDate(booking.startDate || booking.date)],
    ['Fecha fin:', formatDate(booking.endDate || booking.date)],
    ['Estado:', 'PENDIENTE DE CONFIRMACIÓN']
  ]
  
  details.forEach(([label, value]) => {
    doc.setFont('helvetica', 'bold')
    doc.text(label, 25, y)
    doc.setFont('helvetica', 'normal')
    doc.text(value, 70, y)
    y += 7
  })
  
  // Descripción/Notas
  if (booking.description || booking.notes) {
    y += 5
    doc.setFont('helvetica', 'bold')
    doc.text('Observaciones:', 25, y)
    y += 7
    doc.setFont('helvetica', 'normal')
    const notes = doc.splitTextToSize(booking.description || booking.notes, 160)
    doc.text(notes, 25, y)
    y += notes.length * 5
  }
  
  // Aviso legal
  y += 20
  doc.setFillColor(...COLORS.lightGray)
  doc.rect(20, y, 170, 25, 'F')
  doc.setFontSize(8)
  doc.setTextColor(...COLORS.gray)
  doc.text('AVISO IMPORTANTE', 25, y + 6)
  doc.setFont('helvetica', 'normal')
  const aviso = 'Esta solicitud está pendiente de confirmación por parte de Cuevas MotorSport. ' +
    'Recibirá una confirmación con los términos definitivos de la reserva. ' +
    'Este documento no tiene validez contractual hasta su confirmación.'
  const avisoLines = doc.splitTextToSize(aviso, 160)
  doc.text(avisoLines, 25, y + 12)
  
  addFooter(doc)
  
  return { doc, docNumber }
}

// ==========================================
// DOCUMENTO: CONFIRMACIÓN DE RESERVA
// ==========================================
export const generateConfirmacionReserva = (booking, vehicle = null, prevDoc = null) => {
  const doc = new jsPDF()
  const docNumber = `CONF-${booking.id || Date.now().toString().slice(-8)}`
  
  let y = addHeader(doc, 'CONFIRMACIÓN DE RESERVA', docNumber)
  
  // Fechas
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.text(`Fecha confirmación: ${formatDate(new Date())}`, 20, y)
  doc.text(`Nº Reserva: ${booking.id || docNumber}`, 130, y)
  y += 8
  
  // Referencia al documento origen
  if (prevDoc?.number) {
    doc.setFontSize(8)
    doc.setTextColor(...COLORS.gray)
    doc.text(`Referencia Solicitud: ${prevDoc.number}`, 20, y)
    y += 8
  } else {
    y += 2
  }
  
  // Datos del cliente
  y = addClientSection(doc, y, booking)
  
  // Datos del vehículo
  if (vehicle) {
    y = addVehicleSection(doc, y, vehicle)
  }
  
  // Detalles confirmados
  doc.setFillColor(...COLORS.gold)
  doc.rect(20, y, 170, 8, 'F')
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.setFont('helvetica', 'bold')
  doc.text('RESERVA CONFIRMADA', 25, y + 6)
  y += 15
  
  // Tabla de detalles
  doc.autoTable({
    startY: y,
    head: [['Concepto', 'Detalle']],
    body: [
      ['Servicio', booking.service || booking.type || 'Alquiler de vehículo'],
      ['Fecha de recogida', formatDate(booking.startDate || booking.date)],
      ['Fecha de devolución', formatDate(booking.endDate || booking.date)],
      ['Lugar de recogida', 'Instalaciones Cuevas MotorSport'],
      ['Estado', '✓ CONFIRMADA']
    ],
    theme: 'striped',
    headStyles: { fillColor: COLORS.gold, textColor: COLORS.black },
    styles: { fontSize: 9 },
    margin: { left: 20, right: 20 }
  })
  
  y = doc.lastAutoTable.finalY + 15
  
  // Precio si existe
  if (booking.price || booking.total) {
    doc.setFillColor(...COLORS.black)
    doc.rect(110, y, 80, 20, 'F')
    doc.setTextColor(...COLORS.gold)
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.text('TOTAL:', 115, y + 10)
    doc.text(formatPrice(booking.price || booking.total), 185, y + 10, { align: 'right' })
    y += 30
  }
  
  // Condiciones
  y += 10
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(9)
  doc.setFont('helvetica', 'bold')
  doc.text('CONDICIONES DE LA RESERVA:', 20, y)
  y += 7
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(8)
  const condiciones = [
    '• La reserva queda confirmada con este documento.',
    '• El vehículo debe recogerse en la fecha indicada.',
    '• Se requiere presentar DNI/Pasaporte y carnet de conducir vigente.',
    '• El cliente es responsable del vehículo durante el período de alquiler.',
    '• Cualquier daño será valorado y facturado según peritaje.'
  ]
  condiciones.forEach(cond => {
    doc.text(cond, 25, y)
    y += 5
  })
  
  addFooter(doc)
  
  return { doc, docNumber }
}

// ==========================================
// DOCUMENTO: ALBARÁN DE RECOGIDA
// ==========================================
export const generateAlbaranRecogida = (booking, vehicle = null, prevDoc = null) => {
  const doc = new jsPDF()
  const docNumber = `ALB-REC-${Date.now().toString().slice(-8)}`
  
  let y = addHeader(doc, 'ALBARÁN DE RECOGIDA', docNumber)
  
  // Fecha y hora
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  const now = new Date()
  doc.text(`Fecha: ${formatDate(now)}`, 20, y)
  doc.text(`Hora: ${now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}`, 80, y)
  doc.text(`Nº Reserva: ${booking.id || 'N/A'}`, 130, y)
  y += 8
  
  // Referencia al documento origen
  if (prevDoc?.number) {
    doc.setFontSize(8)
    doc.setTextColor(...COLORS.gray)
    doc.text(`Referencia Confirmación: ${prevDoc.number}`, 20, y)
    y += 8
  } else {
    y += 2
  }
  
  // Cliente
  y = addClientSection(doc, y, booking)
  
  // Vehículo
  if (vehicle) {
    y = addVehicleSection(doc, y, vehicle)
  }
  
  // Estado del vehículo
  y += 5
  doc.setFillColor(...COLORS.gold)
  doc.rect(20, y, 170, 8, 'F')
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.setFont('helvetica', 'bold')
  doc.text('ESTADO DEL VEHÍCULO EN LA RECOGIDA', 25, y + 6)
  y += 15
  
  // Tabla de checklist
  doc.autoTable({
    startY: y,
    head: [['Elemento', 'Estado', 'Observaciones']],
    body: [
      ['Carrocería exterior', '☐ Correcto  ☐ Incidencias', ''],
      ['Interior / Tapicería', '☐ Correcto  ☐ Incidencias', ''],
      ['Neumáticos', '☐ Correcto  ☐ Incidencias', ''],
      ['Luces y señalización', '☐ Correcto  ☐ Incidencias', ''],
      ['Nivel de combustible', '☐ Lleno  ☐ 3/4  ☐ 1/2  ☐ 1/4', ''],
      ['Kilometraje actual', vehicle?.kilometraje || '________', 'km'],
      ['Documentación vehículo', '☐ Entregada', ''],
      ['Herramientas/Repuestos', '☐ Completo  ☐ Incidencias', '']
    ],
    theme: 'grid',
    headStyles: { fillColor: COLORS.gold, textColor: COLORS.black },
    styles: { fontSize: 8 },
    columnStyles: {
      0: { cellWidth: 50 },
      1: { cellWidth: 60 },
      2: { cellWidth: 60 }
    },
    margin: { left: 20, right: 20 }
  })
  
  y = doc.lastAutoTable.finalY + 15
  
  // Zona de observaciones
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(9)
  doc.text('OBSERVACIONES ADICIONALES:', 20, y)
  y += 5
  doc.setDrawColor(...COLORS.gray)
  doc.rect(20, y, 170, 25)
  y += 35
  
  // Firmas
  doc.setFont('helvetica', 'bold')
  doc.text('FIRMA CLIENTE:', 30, y)
  doc.text('FIRMA EMPRESA:', 120, y)
  y += 5
  doc.rect(25, y, 60, 25)
  doc.rect(115, y, 60, 25)
  
  y += 30
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(8)
  doc.text(`${booking.customerName || booking.name || ''}`, 55, y, { align: 'center' })
  doc.text('Cuevas MotorSport', 145, y, { align: 'center' })
  
  addFooter(doc)
  
  return { doc, docNumber }
}

// ==========================================
// DOCUMENTO: ALBARÁN DE ENTREGA/DEVOLUCIÓN
// ==========================================
export const generateAlbaranEntrega = (booking, vehicle = null, prevDoc = null) => {
  const doc = new jsPDF()
  const docNumber = `ALB-ENT-${Date.now().toString().slice(-8)}`
  
  let y = addHeader(doc, 'ALBARÁN DE DEVOLUCIÓN', docNumber)
  
  // Fecha y hora
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  const now = new Date()
  doc.text(`Fecha: ${formatDate(now)}`, 20, y)
  doc.text(`Hora: ${now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}`, 80, y)
  doc.text(`Nº Reserva: ${booking.id || 'N/A'}`, 130, y)
  y += 8
  
  // Referencia al documento origen
  if (prevDoc?.number) {
    doc.setFontSize(8)
    doc.setTextColor(...COLORS.gray)
    doc.text(`Referencia Albarán Recogida: ${prevDoc.number}`, 20, y)
    y += 8
  } else {
    y += 2
  }
  
  // Cliente
  y = addClientSection(doc, y, booking)
  
  // Vehículo
  if (vehicle) {
    y = addVehicleSection(doc, y, vehicle)
  }
  
  // Estado del vehículo
  y += 5
  doc.setFillColor(...COLORS.gold)
  doc.rect(20, y, 170, 8, 'F')
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.setFont('helvetica', 'bold')
  doc.text('ESTADO DEL VEHÍCULO EN LA DEVOLUCIÓN', 25, y + 6)
  y += 15
  
  // Tabla de checklist
  doc.autoTable({
    startY: y,
    head: [['Elemento', 'Estado', 'Observaciones']],
    body: [
      ['Carrocería exterior', '☐ Correcto  ☐ Incidencias', ''],
      ['Interior / Tapicería', '☐ Correcto  ☐ Incidencias', ''],
      ['Neumáticos', '☐ Correcto  ☐ Incidencias', ''],
      ['Luces y señalización', '☐ Correcto  ☐ Incidencias', ''],
      ['Nivel de combustible', '☐ Lleno  ☐ 3/4  ☐ 1/2  ☐ 1/4', ''],
      ['Kilometraje final', '________', 'km'],
      ['Documentación vehículo', '☐ Devuelta', ''],
      ['Limpieza', '☐ Correcto  ☐ Cargo adicional', '']
    ],
    theme: 'grid',
    headStyles: { fillColor: COLORS.gold, textColor: COLORS.black },
    styles: { fontSize: 8 },
    columnStyles: {
      0: { cellWidth: 50 },
      1: { cellWidth: 60 },
      2: { cellWidth: 60 }
    },
    margin: { left: 20, right: 20 }
  })
  
  y = doc.lastAutoTable.finalY + 10
  
  // Resumen de uso
  doc.setFillColor(...COLORS.lightGray)
  doc.rect(20, y, 170, 20, 'F')
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(9)
  doc.text('RESUMEN DE USO:', 25, y + 7)
  doc.setFont('helvetica', 'normal')
  doc.text(`Días de alquiler: ____    |    KM recorridos: ____    |    Cargos adicionales: ____€`, 25, y + 14)
  y += 28
  
  // Observaciones
  doc.setFont('helvetica', 'bold')
  doc.text('INCIDENCIAS/DAÑOS DETECTADOS:', 20, y)
  y += 5
  doc.rect(20, y, 170, 20)
  y += 28
  
  // Firmas
  doc.setFont('helvetica', 'bold')
  doc.text('FIRMA CLIENTE:', 30, y)
  doc.text('FIRMA EMPRESA:', 120, y)
  y += 5
  doc.rect(25, y, 60, 20)
  doc.rect(115, y, 60, 20)
  
  y += 25
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(8)
  doc.text(`${booking.customerName || booking.name || ''}`, 55, y, { align: 'center' })
  doc.text('Cuevas MotorSport', 145, y, { align: 'center' })
  
  addFooter(doc)
  
  return { doc, docNumber }
}

// ==========================================
// DOCUMENTO: FACTURA
// ==========================================
export const generateFactura = (booking, vehicle = null, invoiceData = {}) => {
  const doc = new jsPDF()
  const docNumber = invoiceData.number || `FAC-${new Date().getFullYear()}-${Date.now().toString().slice(-6)}`
  
  let y = addHeader(doc, 'FACTURA', docNumber)
  
  // Fechas
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.text(`Fecha factura: ${formatDate(invoiceData.date || new Date())}`, 20, y)
  doc.text(`Nº Reserva: ${booking.id || 'N/A'}`, 130, y)
  y += 8
  
  // Referencia al albarán de entrega
  if (invoiceData.albaranEntrega?.number) {
    doc.setFontSize(8)
    doc.setTextColor(...COLORS.gray)
    doc.text(`Referencia Albarán Entrega: ${invoiceData.albaranEntrega.number}`, 20, y)
    y += 8
  } else {
    y += 2
  }
  
  // Datos fiscales cliente
  doc.setFillColor(...COLORS.lightGray)
  doc.rect(20, y, 170, 35, 'F')
  
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(10)
  doc.setFont('helvetica', 'bold')
  doc.text('DATOS DE FACTURACIÓN', 25, y + 8)
  
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(9)
  doc.text(`Cliente: ${booking.customerName || booking.name || 'N/A'}`, 25, y + 16)
  doc.text(`NIF/CIF: ${invoiceData.clientCif || 'N/A'}`, 25, y + 22)
  doc.text(`Dirección: ${invoiceData.clientAddress || 'N/A'}`, 25, y + 28)
  doc.text(`Email: ${booking.customerEmail || booking.email || 'N/A'}`, 110, y + 16)
  doc.text(`Teléfono: ${booking.customerPhone || booking.phone || 'N/A'}`, 110, y + 22)
  
  y += 45
  
  // Conceptos facturados
  const basePrice = Number(booking.price || booking.total || 0)
  const iva = basePrice * 0.21
  const total = basePrice + iva
  
  const items = [
    [
      booking.service || booking.type || 'Alquiler de vehículo',
      vehicle ? `${vehicle.brand} ${vehicle.model}` : '',
      `${formatDate(booking.startDate || booking.date)} - ${formatDate(booking.endDate || booking.date)}`,
      formatPrice(basePrice)
    ]
  ]
  
  // Añadir extras si existen
  if (invoiceData.extras && invoiceData.extras.length > 0) {
    invoiceData.extras.forEach(extra => {
      items.push([extra.concept, '', '', formatPrice(extra.amount)])
    })
  }
  
  doc.autoTable({
    startY: y,
    head: [['Concepto', 'Vehículo', 'Período', 'Importe']],
    body: items,
    theme: 'striped',
    headStyles: { fillColor: COLORS.gold, textColor: COLORS.black, fontStyle: 'bold' },
    styles: { fontSize: 9 },
    columnStyles: {
      0: { cellWidth: 60 },
      1: { cellWidth: 40 },
      2: { cellWidth: 40 },
      3: { cellWidth: 30, halign: 'right' }
    },
    margin: { left: 20, right: 20 }
  })
  
  y = doc.lastAutoTable.finalY + 10
  
  // Totales
  doc.autoTable({
    startY: y,
    body: [
      ['', '', 'Base imponible:', formatPrice(basePrice)],
      ['', '', 'IVA (21%):', formatPrice(iva)],
      ['', '', 'TOTAL:', formatPrice(total)]
    ],
    theme: 'plain',
    styles: { fontSize: 10 },
    columnStyles: {
      2: { fontStyle: 'bold', halign: 'right' },
      3: { halign: 'right' }
    },
    margin: { left: 20, right: 20 }
  })
  
  y = doc.lastAutoTable.finalY + 5
  
  // Destacar total
  doc.setFillColor(...COLORS.black)
  doc.rect(120, y, 70, 15, 'F')
  doc.setTextColor(...COLORS.gold)
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text('TOTAL: ' + formatPrice(total), 155, y + 10, { align: 'center' })
  
  y += 25
  
  // Forma de pago
  doc.setTextColor(...COLORS.black)
  doc.setFontSize(9)
  doc.setFont('helvetica', 'bold')
  doc.text('FORMA DE PAGO:', 20, y)
  doc.setFont('helvetica', 'normal')
  doc.text(invoiceData.paymentMethod || 'Transferencia bancaria / Efectivo', 60, y)
  y += 7
  
  if (invoiceData.bankAccount) {
    doc.setFont('helvetica', 'bold')
    doc.text('CUENTA BANCARIA:', 20, y)
    doc.setFont('helvetica', 'normal')
    doc.text(invoiceData.bankAccount, 60, y)
  }
  
  // Aviso legal
  y += 20
  doc.setFontSize(7)
  doc.setTextColor(...COLORS.gray)
  doc.text('Factura emitida conforme a la normativa fiscal vigente.', 20, y)
  doc.text(`${COMPANY_INFO.name} - CIF: ${COMPANY_INFO.cif} - ${COMPANY_INFO.address}, ${COMPANY_INFO.city}`, 20, y + 5)
  
  addFooter(doc)
  
  return { doc, docNumber, total }
}

// ==========================================
// FUNCIONES DE UTILIDAD
// ==========================================

// Descargar PDF
export const downloadPDF = (doc, filename) => {
  doc.save(filename)
}

// Abrir PDF para imprimir
export const printPDF = (doc) => {
  const blob = doc.output('blob')
  const url = URL.createObjectURL(blob)
  const printWindow = window.open(url)
  if (printWindow) {
    printWindow.onload = () => {
      printWindow.print()
    }
  }
}

// Previsualizar PDF en nueva pestaña
export const previewPDF = (doc) => {
  const blob = doc.output('blob')
  const url = URL.createObjectURL(blob)
  window.open(url, '_blank')
}
