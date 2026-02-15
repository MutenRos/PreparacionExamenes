import { useState } from 'react'
import { Icons } from './Icons'
import './Contact.css'

export default function Contact() {
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: '',
    servicio: 'grua',
    mensaje: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const validatePhone = (phone) => {
    if (!phone) return true // optional field
    return /^[+]?[\d\s()-]{6,15}$/.test(phone)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!validatePhone(formData.telefono)) {
      alert('Por favor, introduce un número de teléfono válido.')
      return
    }
    setIsSubmitting(true)
    // Simulate network delay
    setTimeout(() => {
      console.log('Formulario enviado:', formData)
      setIsSubmitting(false)
      setSubmitSuccess(true)
      setFormData({ nombre: '', email: '', telefono: '', servicio: 'grua', mensaje: '' })
      setTimeout(() => setSubmitSuccess(false), 4000)
    }, 800)
  }

  return (
    <section id="contacto" className="contact">
      <div className="contact-container">
        <div className="contact-info">
          <h2>Contacta con Nosotros</h2>
          <p className="contact-subtitle">Responderemos tu solicitud en el menor tiempo posible</p>
          
          <div className="contact-details">
            <div className="detail-item">
              <span className="detail-icon"><Icons.Phone size={20} /></span>
              <div>
                <h4>Teléfono</h4>
                <p><a href="tel:+34686531422" style={{color: 'inherit', textDecoration: 'none'}}>+34 686 531 422</a></p>
              </div>
            </div>
            
            <div className="detail-item">
              <span className="detail-icon"><Icons.MessageCircle size={20} /></span>
              <div>
                <h4>WhatsApp</h4>
                <p><a href="https://wa.me/34686531422" target="_blank" rel="noopener noreferrer" style={{color: '#25D366', textDecoration: 'none', fontWeight: 'bold'}}>Enviar mensaje</a></p>
              </div>
            </div>
            
            <div className="detail-item">
              <span className="detail-icon"><Icons.Mail size={20} /></span>
              <div>
                <h4>Email</h4>
                <p>info@cuevasmotorsport.es</p>
              </div>
            </div>
            
            <div className="detail-item">
              <span className="detail-icon"><Icons.MapPin size={20} /></span>
              <div>
                <h4>Ubicación</h4>
                <p>Tu Ciudad, España</p>
              </div>
            </div>

            <div className="detail-item">
              <span className="detail-icon"><Icons.Clock size={20} /></span>
              <div>
                <h4>Horario</h4>
                <p>24/7 - Servicio de grúa disponible</p>
              </div>
            </div>
          </div>
        </div>

        <form className="contact-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="nombre">Nombre *</label>
            <input
              type="text"
              id="nombre"
              name="nombre"
              value={formData.nombre}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="telefono">Teléfono</label>
            <input
              type="tel"
              id="telefono"
              name="telefono"
              value={formData.telefono}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="servicio">Servicio *</label>
            <select
              id="servicio"
              name="servicio"
              value={formData.servicio}
              onChange={handleChange}
              required
            >
              <option value="grua">Servicio de Grúa</option>
              <option value="alquiler-coches">Alquiler de Coches Deportivos</option>
              <option value="plataforma">Alquiler de Plataforma Portacoches</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="mensaje">Mensaje *</label>
            <textarea
              id="mensaje"
              name="mensaje"
              rows="5"
              value={formData.mensaje}
              onChange={handleChange}
              required
            ></textarea>
          </div>

          <button type="submit" className="submit-btn" disabled={isSubmitting}>
            {isSubmitting ? 'Enviando...' : 'Enviar Solicitud'}
          </button>
          {submitSuccess && (
            <p className="success-message" role="status">¡Gracias! Nos pondremos en contacto pronto.</p>
          )}
        </form>
      </div>
    </section>
  )
}
