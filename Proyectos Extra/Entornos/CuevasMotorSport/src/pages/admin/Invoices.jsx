import { useState } from 'react'
import { useInvoice } from '../../contexts/InvoiceContext'
import { format } from 'date-fns'
import { Icons } from '../../components/Icons'
import './Invoices.css'

export default function Invoices() {
  const { invoices, deliveryNotes, createInvoice, createDeliveryNote } = useInvoice()
  const [showModal, setShowModal] = useState(false)
  const [docType, setDocType] = useState('factura')
  const [selectedBooking, setSelectedBooking] = useState(null)

  const handleCreateDocument = (type) => {
    setDocType(type)
    setShowModal(true)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const formData = new FormData(e.target)
    
    const docData = {
      bookingId: selectedBooking,
      customerName: formData.get('customerName'),
      customerNIF: formData.get('customerNIF'),
      customerAddress: formData.get('customerAddress'),
      items: [
        {
          description: formData.get('description'),
          quantity: Number(formData.get('quantity')),
          price: Number(formData.get('price')),
          total: Number(formData.get('quantity')) * Number(formData.get('price'))
        }
      ],
      subtotal: Number(formData.get('quantity')) * Number(formData.get('price')),
      iva: Number(formData.get('quantity')) * Number(formData.get('price')) * 0.21,
      total: Number(formData.get('quantity')) * Number(formData.get('price')) * 1.21
    }

    if (docType === 'factura') {
      createInvoice(docData)
    } else {
      createDeliveryNote(docData)
    }

    setShowModal(false)
    setSelectedBooking(null)
  }

  return (
    <div className="invoices-page">
      <div className="page-header">
        <h1><Icons.Euro size={28} /> Facturas y Albaranes</h1>
        <div className="header-actions">
          <button onClick={() => handleCreateDocument('factura')} className="create-btn">
            <Icons.Plus size={16} /> Nueva Factura
          </button>
          <button onClick={() => handleCreateDocument('albaran')} className="create-btn secondary">
            <Icons.Plus size={16} /> Nuevo Albarán
          </button>
        </div>
      </div>

      <div className="documents-grid">
        <div className="documents-section">
          <h2><Icons.Receipt size={20} /> Facturas</h2>
          {invoices.length > 0 ? (
            <div className="documents-list">
              {invoices.map(invoice => (
                <div key={invoice.id} className="document-card">
                  <div className="document-header">
                    <h3>Factura {invoice.number}</h3>
                    <span className={`doc-status ${invoice.status}`}>{invoice.status}</span>
                  </div>
                  <div className="document-details">
                    <p><strong>{invoice.customerName}</strong></p>
                    <p>NIF: {invoice.customerNIF}</p>
                    <p>Fecha: {format(new Date(invoice.date), 'dd/MM/yyyy')}</p>
                    <p className="document-total">Total: €{invoice.total.toFixed(2)}</p>
                  </div>
                  <div className="document-actions">
                    <button className="view-btn"><Icons.Eye size={14} /> Ver</button>
                    <button className="download-btn"><Icons.Download size={14} /> PDF</button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-docs">No hay facturas</p>
          )}
        </div>

        <div className="documents-section">
          <h2><Icons.ClipboardList size={20} /> Albaranes</h2>
          {deliveryNotes.length > 0 ? (
            <div className="documents-list">
              {deliveryNotes.map(note => (
                <div key={note.id} className="document-card">
                  <div className="document-header">
                    <h3>Albarán {note.number}</h3>
                    <span className={`doc-status ${note.status}`}>{note.status}</span>
                  </div>
                  <div className="document-details">
                    <p><strong>{note.customerName}</strong></p>
                    <p>Fecha: {format(new Date(note.date), 'dd/MM/yyyy')}</p>
                  </div>
                  <div className="document-actions">
                    <button className="view-btn"><Icons.Eye size={14} /> Ver</button>
                    <button className="download-btn"><Icons.Download size={14} /> PDF</button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-docs">No hay albaranes</p>
          )}
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Crear {docType === 'factura' ? 'Factura' : 'Albarán'}</h2>
              <button onClick={() => setShowModal(false)} className="close-btn"><Icons.X size={18} /></button>
            </div>

            <form onSubmit={handleSubmit} className="invoice-form">
              <div className="form-section">
                <h3>Datos del Cliente</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label>Nombre / Razón Social</label>
                    <input type="text" name="customerName" required />
                  </div>
                  <div className="form-group">
                    <label>NIF/CIF</label>
                    <input type="text" name="customerNIF" required />
                  </div>
                </div>
                <div className="form-group">
                  <label>Dirección</label>
                  <input type="text" name="customerAddress" required />
                </div>
              </div>

              <div className="form-section">
                <h3>Líneas de Servicio</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label>Descripción</label>
                    <input type="text" name="description" required />
                  </div>
                  <div className="form-group">
                    <label>Cantidad</label>
                    <input type="number" name="quantity" defaultValue="1" required />
                  </div>
                  <div className="form-group">
                    <label>Precio €</label>
                    <input type="number" step="0.01" name="price" required />
                  </div>
                </div>
              </div>

              <div className="form-actions">
                <button type="button" onClick={() => setShowModal(false)} className="cancel-btn">
                  Cancelar
                </button>
                <button type="submit" className="submit-btn">
                  Generar {docType === 'factura' ? 'Factura' : 'Albarán'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
