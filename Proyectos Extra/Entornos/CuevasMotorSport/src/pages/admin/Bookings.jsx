import { useBooking } from '../../contexts/BookingContext'
import { useInventory } from '../../contexts/InventoryContext'
import { format, parseISO } from 'date-fns'
import { useState } from 'react'
import { Icons } from '../../components/Icons'
import './Bookings.css'
import {
  generateSolicitudReserva,
  generateConfirmacionReserva,
  generateAlbaranRecogida,
  generateAlbaranEntrega,
  generateFactura,
  downloadPDF,
  printPDF,
  previewPDF
} from '../../services/DocumentGenerator'

// Flujo de documentos: solicitud → confirmacion → albaran_recogida → albaran_entrega → factura
const DOCUMENT_FLOW = [
  { key: 'solicitud', label: 'Solicitud de Reserva', icon: <Icons.FileText size={16} />, statusChange: null },
  { key: 'confirmacion', label: 'Confirmación de Reserva', icon: <Icons.CheckCircle size={16} />, statusChange: 'confirmada' },
  { key: 'albaran_recogida', label: 'Albarán de Recogida', icon: <Icons.Package size={16} />, statusChange: 'en_curso' },
  { key: 'albaran_entrega', label: 'Albarán de Entrega', icon: <Icons.Truck size={16} />, statusChange: null },
  { key: 'factura', label: 'Factura', icon: <Icons.Euro size={16} />, statusChange: 'completada' }
]

export default function Bookings() {
  const { bookings, updateBooking, deleteBooking } = useBooking()
  const { vehicles } = useInventory()
  const [calculatingDistances, setCalculatingDistances] = useState({})
  const [showDocModal, setShowDocModal] = useState(null)

  // Obtener documentos generados de una reserva
  const getGeneratedDocs = (booking) => {
    return booking.generatedDocs || {}
  }

  // Verificar si un documento puede generarse (el anterior debe estar generado)
  const canGenerateDoc = (booking, docKey) => {
    const docs = getGeneratedDocs(booking)
    const docIndex = DOCUMENT_FLOW.findIndex(d => d.key === docKey)
    
    // El primer documento siempre se puede generar
    if (docIndex === 0) return true
    
    // Los demás requieren que el anterior esté generado
    const prevDocKey = DOCUMENT_FLOW[docIndex - 1].key
    return !!docs[prevDocKey]
  }

  // Obtener el siguiente documento a generar
  const getNextDoc = (booking) => {
    const docs = getGeneratedDocs(booking)
    for (const doc of DOCUMENT_FLOW) {
      if (!docs[doc.key]) return doc
    }
    return null // Todos generados
  }

  // Marcar documento como generado
  const markDocGenerated = (bookingId, docKey, docNumber) => {
    const booking = bookings.find(b => b.id === bookingId)
    const currentDocs = getGeneratedDocs(booking)
    const docInfo = DOCUMENT_FLOW.find(d => d.key === docKey)
    
    const updates = {
      generatedDocs: {
        ...currentDocs,
        [docKey]: {
          number: docNumber,
          date: new Date().toISOString()
        }
      }
    }
    
    // Cambiar estado si corresponde
    if (docInfo?.statusChange) {
      updates.status = docInfo.statusChange
    }
    
    updateBooking(bookingId, updates)
  }

  const handleStatusChange = (id, newStatus) => {
    updateBooking(id, { status: newStatus })
  }

  const handleDelete = (id) => {
    if (confirm('¿Eliminar esta reserva?')) {
      deleteBooking(id)
    }
  }

  const statusOptions = ['pendiente', 'confirmada', 'en_curso', 'completada', 'cancelada']

  const handleBudgetChange = (id, field, value) => {
    updateBooking(id, { [field]: value })
  }

  const handleLocationChange = (id, field, value) => {
    updateBooking(id, { [field]: value })
  }

  // Funciones de documentos
  const handleGenerateDocument = (type, booking, action = 'preview') => {
    const vehicle = vehicles.find(v => v.id === booking.vehicleId)
    const docs = getGeneratedDocs(booking)
    let result
    let filename

    switch (type) {
      case 'solicitud':
        result = generateSolicitudReserva(booking, vehicle)
        filename = `Solicitud_${booking.id}.pdf`
        break
      case 'confirmacion':
        // Pasar datos de la solicitud si existe
        result = generateConfirmacionReserva(booking, vehicle, docs.solicitud)
        filename = `Confirmacion_${booking.id}.pdf`
        break
      case 'albaran_recogida':
        // Pasar datos de la confirmación
        result = generateAlbaranRecogida(booking, vehicle, docs.confirmacion)
        filename = `Albaran_Recogida_${booking.id}.pdf`
        break
      case 'albaran_entrega':
        // Pasar datos del albarán de recogida
        result = generateAlbaranEntrega(booking, vehicle, docs.albaran_recogida)
        filename = `Albaran_Entrega_${booking.id}.pdf`
        break
      case 'factura':
        const total = calcTotal(booking)
        // Pasar datos del albarán de entrega
        result = generateFactura(booking, vehicle, { 
          total,
          paymentMethod: 'Transferencia bancaria / Efectivo',
          albaranEntrega: docs.albaran_entrega
        })
        filename = `Factura_${result.docNumber}.pdf`
        break
      default:
        return
    }

    // Si es descarga o impresión, marcar como generado
    if (action === 'download' || action === 'print') {
      markDocGenerated(booking.id, type, result.docNumber)
    }

    switch (action) {
      case 'download':
        downloadPDF(result.doc, filename)
        break
      case 'print':
        printPDF(result.doc)
        break
      case 'preview':
      default:
        previewPDF(result.doc)
        break
    }
  }

  const calculateDistances = async (id, origen, recogida, descarga) => {
    if (!origen || !recogida || !descarga) {
      alert('Por favor, complete todas las ubicaciones')
      return
    }

    setCalculatingDistances(prev => ({ ...prev, [id]: true }))

    try {
      const service = new window.google.maps.DistanceMatrixService()
      
      const calculateLeg = (origin, destination) => {
        return new Promise((resolve, reject) => {
          service.getDistanceMatrix(
            {
              origins: [origin],
              destinations: [destination],
              travelMode: window.google.maps.TravelMode.DRIVING,
              unitSystem: window.google.maps.UnitSystem.METRIC
            },
            (response, status) => {
              if (status === 'OK' && response.rows[0]?.elements[0]?.status === 'OK') {
                const distanceMeters = response.rows[0].elements[0].distance.value
                const distanceKm = (distanceMeters / 1000).toFixed(1)
                resolve(parseFloat(distanceKm))
              } else {
                reject(new Error(`Error calculando distancia: ${status}`))
              }
            }
          )
        })
      }

      const [km1, km2, km3] = await Promise.all([
        calculateLeg(origen, recogida),
        calculateLeg(recogida, descarga),
        calculateLeg(descarga, origen)
      ])

      const kmTotal = km1 + km2 + km3

      updateBooking(id, {
        origenDir: origen,
        recogidaDir: recogida,
        descargaDir: descarga,
        kmOrigenRecogida: km1,
        kmRecogidaDescarga: km2,
        kmDescargaOrigen: km3,
        kmDist: kmTotal
      })

      alert(`Distancias calculadas:\n• Origen → Recogida: ${km1} km\n• Recogida → Descarga: ${km2} km\n• Descarga → Origen: ${km3} km\n• TOTAL: ${kmTotal.toFixed(1)} km`)
    } catch (error) {
      console.error('Error calculando distancias:', error)
      alert('Error al calcular las distancias. Verifique las direcciones.')
    } finally {
      setCalculatingDistances(prev => ({ ...prev, [id]: false }))
    }
  }

  const calcTotal = (booking) => {
    const porte = parseFloat(booking.porteImporte || 0) || 0
    const kmPrecio = parseFloat(booking.kmPrecio || 0) || 0
    const kmDist = parseFloat(booking.kmDist || 0) || 0
    return porte + kmPrecio * kmDist
  }

  const getStatusLabel = (status) => {
    const labels = {
      pendiente: 'Pendiente',
      confirmada: 'Confirmada',
      en_curso: 'En Curso',
      completada: 'Completada',
      cancelada: 'Cancelada'
    }
    return labels[status] || status
  }

  return (
    <div className="bookings-page">
      <div className="page-header">
        <h1><Icons.ClipboardList size={28} /> Reservas</h1>
        <p>Gestión de reservas de clientes</p>
      </div>

      <div className="bookings-container">
        {bookings.length > 0 ? (
          <table className="bookings-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Cliente</th>
                <th>Contacto</th>
                <th>Servicio</th>
                <th>Fecha</th>
                <th>Estado</th>
                <th>Ubicaciones & Distancias</th>
                <th>Presupuesto</th>
                <th>Total</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {bookings.map(booking => {
                const vehicle = vehicles.find(v => v.id === booking.vehicleId)
                const total = calcTotal(booking)
                const phone = (booking.phone || booking.customerPhone || '').replace(/\s+/g, '')
                const waLink = phone ? `https://wa.me/34${phone.startsWith('34') ? phone.slice(2) : phone}` : null
                const email = booking.email || booking.customerEmail || ''
                const cliente = booking.name || booking.customerName || 'Cliente'
                const service = booking.type || booking.service || 'Portes'
                const dateStr = booking.startDate ? format(parseISO(booking.startDate), 'dd/MM/yyyy') : '-'
                return (
                  <tr key={booking.id}>
                    <td>#{booking.id.toString().slice(-4)}</td>
                    <td>
                      <strong>{cliente}</strong>
                      <br />
                      <small>{email}</small>
                    </td>
                    <td className="contact-cell">
                      {phone ? <span>{phone}</span> : <span className="muted">Sin teléfono</span>}
                      {waLink && (
                        <a className="wa-btn" href={waLink} target="_blank" rel="noopener noreferrer">WhatsApp</a>
                      )}
                      {email && (
                        <a className="mail-btn" href={`mailto:${email}`}>Email</a>
                      )}
                    </td>
                    <td>
                      <span className="vehicle-icon-tiny">{vehicle?.image}</span>
                      {service}
                    </td>
                    <td>{dateStr}</td>
                    <td>
                      <select
                        value={booking.status}
                        onChange={(e) => handleStatusChange(booking.id, e.target.value)}
                        className={`status-select ${booking.status}`}
                      >
                        {statusOptions.map(status => (
                          <option key={status} value={status}>{status}</option>
                        ))}
                      </select>
                    </td>
                    <td className="locations-cell">
                      <div className="location-inputs">
                        <label><Icons.Home size={14} /> Origen (Base)
                          <input
                            type="text"
                            placeholder="Dirección de origen"
                            value={booking.origenDir || ''}
                            onChange={(e) => handleLocationChange(booking.id, 'origenDir', e.target.value)}
                          />
                        </label>
                        <label><Icons.MapPin size={14} /> Recogida
                          <input
                            type="text"
                            placeholder="Donde está el vehículo"
                            value={booking.recogidaDir || ''}
                            onChange={(e) => handleLocationChange(booking.id, 'recogidaDir', e.target.value)}
                          />
                        </label>
                        <label><Icons.Target size={14} /> Descarga
                          <input
                            type="text"
                            placeholder="Destino final"
                            value={booking.descargaDir || ''}
                            onChange={(e) => handleLocationChange(booking.id, 'descargaDir', e.target.value)}
                          />
                        </label>
                      </div>
                      <button 
                        className="calc-dist-btn"
                        onClick={() => calculateDistances(
                          booking.id, 
                          booking.origenDir, 
                          booking.recogidaDir, 
                          booking.descargaDir
                        )}
                        disabled={calculatingDistances[booking.id]}
                      >
                        {calculatingDistances[booking.id] ? 'Calculando...' : <><Icons.Ruler size={14} /> Calcular distancias</>}
                      </button>
                      {booking.kmDist && (
                        <div className="distances-summary">
                          <small>
                            <strong>Origen → Recogida:</strong> {booking.kmOrigenRecogida || 0} km<br />
                            <strong>Recogida → Descarga:</strong> {booking.kmRecogidaDescarga || 0} km<br />
                            <strong>Descarga → Origen:</strong> {booking.kmDescargaOrigen || 0} km<br />
                            <strong className="total-km">TOTAL: {booking.kmDist} km</strong>
                          </small>
                        </div>
                      )}
                    </td>
                    <td className="budget-cell">
                      <label>Servicio (€)
                        <input
                          type="number"
                          min="0"
                          step="0.01"
                          value={booking.porteImporte || ''}
                          onChange={(e) => handleBudgetChange(booking.id, 'porteImporte', e.target.value)}
                        />
                      </label>
                      <label>€/km
                        <input
                          type="number"
                          min="0"
                          step="0.01"
                          value={booking.kmPrecio || ''}
                          onChange={(e) => handleBudgetChange(booking.id, 'kmPrecio', e.target.value)}
                        />
                      </label>
                      <label>Km (auto)
                        <input
                          type="number"
                          min="0"
                          step="0.1"
                          value={booking.kmDist || ''}
                          readOnly
                          title="Calculado automáticamente"
                        />
                      </label>
                    </td>
                    <td className="total-cell">€ {total.toFixed(2)}</td>
                    <td className="actions-cell">
                      <div className="docs-buttons">
                        {DOCUMENT_FLOW.map((doc, idx) => {
                          const docs = getGeneratedDocs(booking)
                          const isGenerated = !!docs[doc.key]
                          const canGenerate = canGenerateDoc(booking, doc.key)
                          const isNext = !isGenerated && canGenerate
                          
                          return (
                            <button
                              key={doc.key}
                              className={`doc-btn ${doc.key} ${isGenerated ? 'generated' : ''} ${isNext ? 'next-doc' : ''} ${!canGenerate ? 'disabled' : ''}`}
                              onClick={() => canGenerate && setShowDocModal({ booking, type: doc.key })}
                              disabled={!canGenerate}
                              title={isGenerated ? `${doc.label} - Generado el ${format(parseISO(docs[doc.key].date), 'dd/MM/yyyy HH:mm')}` : canGenerate ? doc.label : `Genera primero: ${DOCUMENT_FLOW[idx - 1]?.label}`}
                            >
                              {doc.icon} {isGenerated ? '✓' : ''} {doc.label.split(' ')[0]}
                            </button>
                          )
                        })}
                      </div>
                      <div className="doc-progress">
                        <span className="progress-text">
                          {Object.keys(getGeneratedDocs(booking)).length}/{DOCUMENT_FLOW.length} docs
                        </span>
                        <div className="progress-bar">
                          <div 
                            className="progress-fill" 
                            style={{ width: `${(Object.keys(getGeneratedDocs(booking)).length / DOCUMENT_FLOW.length) * 100}%` }}
                          />
                        </div>
                      </div>
                      <button onClick={() => handleDelete(booking.id)} className="delete-btn-small">
                        <Icons.Trash size={16} />
                      </button>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        ) : (
          <div className="no-data-message">
            <p>No hay reservas registradas</p>
          </div>
        )}
      </div>

      {/* Modal de documentos */}
      {showDocModal && (
        <div className="doc-modal-overlay" onClick={() => setShowDocModal(null)}>
          <div className="doc-modal" onClick={(e) => e.stopPropagation()}>
            <div className="doc-modal-header">
              <h3>
                {DOCUMENT_FLOW.find(d => d.key === showDocModal.type)?.icon} {DOCUMENT_FLOW.find(d => d.key === showDocModal.type)?.label}
              </h3>
              <button className="close-btn" onClick={() => setShowDocModal(null)}><Icons.X size={18} /></button>
            </div>
            
            {/* Flujo de documentos visual */}
            <div className="doc-flow-indicator">
              {DOCUMENT_FLOW.map((doc, idx) => {
                const docs = getGeneratedDocs(showDocModal.booking)
                const isGenerated = !!docs[doc.key]
                const isCurrent = doc.key === showDocModal.type
                return (
                  <div key={doc.key} className={`flow-step ${isGenerated ? 'done' : ''} ${isCurrent ? 'current' : ''}`}>
                    <span className="flow-icon">{isGenerated ? '✓' : doc.icon}</span>
                    {idx < DOCUMENT_FLOW.length - 1 && <span className="flow-arrow">→</span>}
                  </div>
                )
              })}
            </div>

            <div className="doc-modal-info">
              <p><strong>Cliente:</strong> {showDocModal.booking.name || showDocModal.booking.customerName}</p>
              <p><strong>Servicio:</strong> {showDocModal.booking.type || showDocModal.booking.service}</p>
              <p><strong>Total:</strong> € {calcTotal(showDocModal.booking).toFixed(2)}</p>
              
              {/* Mostrar documento origen si existe */}
              {(() => {
                const docIndex = DOCUMENT_FLOW.findIndex(d => d.key === showDocModal.type)
                if (docIndex > 0) {
                  const prevDoc = DOCUMENT_FLOW[docIndex - 1]
                  const docs = getGeneratedDocs(showDocModal.booking)
                  if (docs[prevDoc.key]) {
                    return (
                      <p className="doc-origin">
                        <strong>Generado desde:</strong> {prevDoc.label} ({docs[prevDoc.key].number})
                      </p>
                    )
                  }
                }
                return null
              })()}
            </div>

            <div className="doc-modal-actions">
              <button 
                className="doc-action-btn preview"
                onClick={() => {
                  handleGenerateDocument(showDocModal.type, showDocModal.booking, 'preview')
                }}
              >
                <Icons.Eye size={16} /> Vista Previa
              </button>
              <button 
                className="doc-action-btn download"
                onClick={() => {
                  handleGenerateDocument(showDocModal.type, showDocModal.booking, 'download')
                  setShowDocModal(null)
                }}
              >
                <Icons.Download size={16} /> Descargar y Registrar
              </button>
              <button 
                className="doc-action-btn print"
                onClick={() => {
                  handleGenerateDocument(showDocModal.type, showDocModal.booking, 'print')
                  setShowDocModal(null)
                }}
              >
                <Icons.Printer size={16} /> Imprimir y Registrar
              </button>
            </div>

            {/* Notas según el documento */}
            {(() => {
              const docInfo = DOCUMENT_FLOW.find(d => d.key === showDocModal.type)
              const docIndex = DOCUMENT_FLOW.findIndex(d => d.key === showDocModal.type)
              const nextDoc = DOCUMENT_FLOW[docIndex + 1]
              
              return (
                <div className="doc-modal-notes">
                  {docInfo?.statusChange && (
                    <p className="doc-modal-note warning">
                      <Icons.AlertTriangle size={14} /> Al descargar/imprimir, el estado cambiará a "{docInfo.statusChange}"
                    </p>
                  )}
                  {nextDoc && (
                    <p className="doc-modal-note info">
                      <Icons.Info size={14} /> Después podrás generar: {nextDoc.icon} {nextDoc.label}
                    </p>
                  )}
                  {!nextDoc && (
                    <p className="doc-modal-note success">
                      <Icons.CheckCircle size={14} /> Este es el último documento del flujo
                    </p>
                  )}
                </div>
              )
            })()}
          </div>
        </div>
      )}
    </div>
  )
}
