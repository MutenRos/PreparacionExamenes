import { useState } from 'react'
import { useInvoice } from '../../contexts/InvoiceContext'
import { format } from 'date-fns'
import './VeriFactu.css'

export default function VeriFactu() {
  const { invoices, sendToVerifactu } = useInvoice()
  const [sending, setSending] = useState(null)

  const handleSendToVerifactu = async (invoiceId) => {
    setSending(invoiceId)
    await sendToVerifactu(invoiceId)
    setSending(null)
  }

  const pendingInvoices = invoices.filter(inv => inv.verifactuStatus === 'pendiente')
  const sentInvoices = invoices.filter(inv => inv.verifactuStatus === 'enviada')

  return (
    <div className="verifactu-page">
      <div className="page-header">
        <div>
          <h1>✅ Sistema VeriFactu</h1>
          <p>Integración con el sistema de facturación de la AEAT</p>
        </div>
      </div>

      <div className="verifactu-info">
        <div className="info-card">
          <h3>ℹ️ Sobre VeriFactu</h3>
          <p>VeriFactu es el sistema de la Agencia Tributaria española que garantiza la integridad y veracidad de las facturas electrónicas.</p>
          <ul>
            <li>✓ Envío automático de facturas</li>
            <li>✓ Validación y firma digital</li>
            <li>✓ Cumplimiento normativo</li>
            <li>✓ Trazabilidad completa</li>
          </ul>
        </div>

        <div className="stats-cards">
          <div className="verifactu-stat">
            <h3>{pendingInvoices.length}</h3>
            <p>Facturas Pendientes</p>
          </div>
          <div className="verifactu-stat success">
            <h3>{sentInvoices.length}</h3>
            <p>Facturas Enviadas</p>
          </div>
        </div>
      </div>

      <div className="verifactu-section">
        <h2>📤 Facturas Pendientes de Envío</h2>
        {pendingInvoices.length > 0 ? (
          <div className="invoices-list">
            {pendingInvoices.map(invoice => (
              <div key={invoice.id} className="verifactu-invoice-card">
                <div className="invoice-info">
                  <h3>Factura {invoice.number}</h3>
                  <p><strong>{invoice.customerName}</strong></p>
                  <p>Fecha: {format(new Date(invoice.date), 'dd/MM/yyyy')}</p>
                  <p>Total: <strong>€{invoice.total.toFixed(2)}</strong></p>
                </div>
                <div className="invoice-actions">
                  <button
                    onClick={() => handleSendToVerifactu(invoice.id)}
                    disabled={sending === invoice.id}
                    className="send-btn"
                  >
                    {sending === invoice.id ? '⏳ Enviando...' : '📤 Enviar a VeriFactu'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data">No hay facturas pendientes de envío</p>
        )}
      </div>

      <div className="verifactu-section">
        <h2>✅ Facturas Enviadas</h2>
        {sentInvoices.length > 0 ? (
          <div className="sent-invoices-grid">
            {sentInvoices.map(invoice => (
              <div key={invoice.id} className="sent-invoice-card">
                <div className="sent-badge">✅ Enviada</div>
                <h3>Factura {invoice.number}</h3>
                <p><strong>{invoice.customerName}</strong></p>
                <p className="verifactu-code">
                  Código VeriFactu: <code>{invoice.verifactuCode}</code>
                </p>
                <p className="sent-date">
                  Enviado: {format(new Date(invoice.verifactuDate), 'dd/MM/yyyy HH:mm')}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data">No hay facturas enviadas aún</p>
        )}
      </div>
    </div>
  )
}
