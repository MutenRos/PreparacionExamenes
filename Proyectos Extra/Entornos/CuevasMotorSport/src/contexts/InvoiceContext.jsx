import { createContext, useContext, useState, useEffect } from 'react'

const InvoiceContext = createContext(null)

export function InvoiceProvider({ children }) {
  const [invoices, setInvoices] = useState(() => {
    const stored = localStorage.getItem('invoices')
    return stored ? JSON.parse(stored) : []
  })

  const [deliveryNotes, setDeliveryNotes] = useState(() => {
    const stored = localStorage.getItem('deliveryNotes')
    return stored ? JSON.parse(stored) : []
  })

  useEffect(() => {
    localStorage.setItem('invoices', JSON.stringify(invoices))
  }, [invoices])

  useEffect(() => {
    localStorage.setItem('deliveryNotes', JSON.stringify(deliveryNotes))
  }, [deliveryNotes])

  const generateInvoiceNumber = () => {
    const year = new Date().getFullYear()
    const count = invoices.filter(inv => inv.number.startsWith(`${year}`)).length + 1
    return `${year}${String(count).padStart(4, '0')}`
  }

  const generateDeliveryNoteNumber = () => {
    const year = new Date().getFullYear()
    const count = deliveryNotes.filter(dn => dn.number.startsWith(`ALB-${year}`)).length + 1
    return `ALB-${year}${String(count).padStart(4, '0')}`
  }

  const createInvoice = (invoiceData) => {
    const newInvoice = {
      ...invoiceData,
      id: Date.now(),
      number: generateInvoiceNumber(),
      date: new Date().toISOString(),
      status: 'emitida',
      verifactuStatus: 'pendiente'
    }
    setInvoices(prev => [...prev, newInvoice])
    return newInvoice
  }

  const createDeliveryNote = (noteData) => {
    const newNote = {
      ...noteData,
      id: Date.now(),
      number: generateDeliveryNoteNumber(),
      date: new Date().toISOString(),
      status: 'emitido'
    }
    setDeliveryNotes(prev => [...prev, newNote])
    return newNote
  }

  const updateInvoice = (id, updates) => {
    setInvoices(prev => prev.map(inv => inv.id === id ? { ...inv, ...updates } : inv))
  }

  const sendToVerifactu = async (invoiceId) => {
    // Simulación de envío a VeriFactu
    return new Promise((resolve) => {
      setTimeout(() => {
        updateInvoice(invoiceId, { 
          verifactuStatus: 'enviada',
          verifactuDate: new Date().toISOString(),
          verifactuCode: `VF-${Math.random().toString(36).substr(2, 9).toUpperCase()}`
        })
        resolve({ success: true })
      }, 1500)
    })
  }

  const value = {
    invoices,
    deliveryNotes,
    createInvoice,
    createDeliveryNote,
    updateInvoice,
    sendToVerifactu
  }

  return <InvoiceContext.Provider value={value}>{children}</InvoiceContext.Provider>
}

export function useInvoice() {
  const context = useContext(InvoiceContext)
  if (!context) {
    throw new Error('useInvoice must be used within InvoiceProvider')
  }
  return context
}
