import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useBooking } from '../contexts/BookingContext'
import { Icons } from '../components/Icons'
import './PlatformService.css'

export default function PlatformService() {
  const navigate = useNavigate()
  const { createBooking } = useBooking()
  const [selectedDate, setSelectedDate] = useState(null)
  const [selectedTime, setSelectedTime] = useState(null)
  const [currentMonthOffset, setCurrentMonthOffset] = useState(0)
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    duration: '1',
    description: ''
  })
  const [showConfirmation, setShowConfirmation] = useState(false)
  const [submitError, setSubmitError] = useState('')

  // Horarios disponibles para recogida
  const availableTimes = [
    '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'
  ]

  const getCurrentMonth = () => {
    const date = new Date()
    date.setDate(1)
    date.setMonth(date.getMonth() + currentMonthOffset)
    return date
  }

  const canPreviousMonth = () => currentMonthOffset > 0
  const canNextMonth = () => currentMonthOffset < 2

  const getDaysInMonth = (date) => {
    const year = date.getFullYear()
    const month = date.getMonth()
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const daysInMonth = lastDay.getDate()
    const startingDayOfWeek = firstDay.getDay()

    const days = []
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null)
    }
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(new Date(year, month, i))
    }
    return days
  }

  const getMonthName = (date) => {
    return date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' })
  }

  const isDatePast = (date) => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    return date < today
  }

  const handleDateSelect = (date) => {
    if (!isDatePast(date)) {
      setSelectedDate(date)
      setSelectedTime(null)
    }
  }

  const handleManualDateChange = (e) => {
    const dateValue = e.target.value
    if (dateValue) {
      const [year, month, day] = dateValue.split('-').map(Number)
      const date = new Date(year, month - 1, day)
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      if (date >= today) {
        setSelectedDate(date)
        setSelectedTime(null)
      }
    } else {
      setSelectedDate(null)
      setSelectedTime(null)
    }
  }

  const getDateInputValue = () => {
    if (!selectedDate) return ''
    const year = selectedDate.getFullYear()
    const month = String(selectedDate.getMonth() + 1).padStart(2, '0')
    const day = String(selectedDate.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }

  const handleTimeSelect = (time) => {
    setSelectedTime(time)
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!selectedDate || !selectedTime || !formData.name || !formData.phone || !formData.email) {
      setSubmitError('Completa todos los campos: día, hora y datos de contacto.')
      return
    }

    setSubmitError('')

    const startDate = `${selectedDate.toISOString().split('T')[0]}T${selectedTime}:00`
    const booking = {
      type: 'plataforma',
      service: 'Alquiler de Plataforma Portacoches',
      name: formData.name,
      phone: formData.phone,
      email: formData.email,
      duration: formData.duration,
      description: formData.description,
      startDate,
      endDate: startDate,
      vehicleId: null
    }

    createBooking(booking)
    setShowConfirmation(true)
    setTimeout(() => {
      navigate('/')
    }, 3000)
  }

  return (
    <div className="platform-service">
      {showConfirmation && (
        <div className="confirmation-modal">
          <div className="confirmation-content">
            <div className="confirmation-icon"><Icons.CheckCircle size={48} /></div>
            <h2>¡Solicitud de Plataforma Enviada!</h2>
            <p>Tu reserva de plataforma portacoches ha sido registrada.</p>
            <p className="small-text">Te contactaremos para confirmar disponibilidad y detalles.</p>
          </div>
        </div>
      )}

      <button className="back-btn" onClick={() => navigate('/')}>
        ← Volver
      </button>

      <div className="platform-container">
        <div className="platform-header">
          <div className="platform-icon-section">
            <div className="platform-big-icon"><Icons.Car size={64} /></div>
            <div className="platform-badge">Alquiler Profesional</div>
          </div>

          <div className="platform-info">
            <h1>Alquiler de Plataforma Portacoches</h1>
            <p className="platform-subtitle">Remolque especializado para transporte seguro de vehículos</p>

            <div className="platform-features">
              <div className="feature-item">
                <span className="feature-icon"><Icons.Lock size={24} /></span>
                <div>
                  <h4>Sistema de Sujeción Seguro</h4>
                  <p>Anclajes profesionales para todo tipo de vehículos</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon"><Icons.Ruler size={24} /></span>
                <div>
                  <h4>Capacidad Variable</h4>
                  <p>Adaptable a diferentes tamaños de vehículos</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon"><Icons.Shield size={24} /></span>
                <div>
                  <h4>Depósito de Garantía</h4>
                  <p>Condiciones flexibles de alquiler</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon"><Icons.MessageCircle size={24} /></span>
                <div>
                  <h4>Contacto WhatsApp</h4>
                  <p><a href="https://wa.me/34686531422" target="_blank" rel="noopener noreferrer" style={{color: '#25D366', textDecoration: 'none', fontWeight: 'bold'}}>686 531 422</a></p>
                </div>
              </div>
            </div>

            <div className="pricing-section">
              <h3><Icons.Euro size={20} /> Tarifas</h3>
              <div className="pricing-grid">
                <div className="price-item main">
                  <span className="price-value">60€</span>
                  <span className="price-label">/ día</span>
                </div>
                <div className="price-item">
                  <span className="price-value">3,50€</span>
                  <span className="price-label">/ hora extra</span>
                  <span className="price-note">(opcional*)</span>
                </div>
              </div>
              <p className="pricing-note">
                * La fracción horaria es opcional y puede ser anulada según el motivo del retraso.
                <br />Alquiler mínimo: 1 día.
              </p>
            </div>
          </div>
        </div>

        <div className="platform-content">
          <div className="platform-booking">
            <h2>Reservar Plataforma Portacoches</h2>
            
            <form onSubmit={handleSubmit} className="booking-form">
              <div className="form-section">
                <h3><Icons.ClipboardList size={20} /> Información de Contacto</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label>Nombre *</label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      placeholder="Tu nombre"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Teléfono *</label>
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      placeholder="Tu teléfono"
                      required
                    />
                  </div>
                </div>

                <div className="form-group full-width">
                  <label>Email *</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="Tu email"
                    required
                  />
                </div>
              </div>

              <div className="form-section">
                <h3><Icons.Package size={20} /> Detalles del Alquiler</h3>
                <p className="section-hint">La plataforma se recoge y entrega en nuestras instalaciones</p>

                <div className="pickup-info">
                  <div className="pickup-icon"><Icons.Home size={32} /></div>
                  <div className="pickup-details">
                    <h4>Punto de Recogida y Entrega</h4>
                    <p>Cuevas MotorSport - Nuestras instalaciones</p>
                    <p className="pickup-note">Ven a recoger la plataforma y devuélvela en el mismo punto dentro de las 24h contratadas.</p>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Duración del Alquiler</label>
                    <select
                      name="duration"
                      value={formData.duration}
                      onChange={handleInputChange}
                    >
                      <option value="1">1 día - 60€</option>
                      <option value="2">2 días - 120€</option>
                      <option value="3">3 días - 180€</option>
                      <option value="4">4 días - 240€</option>
                      <option value="5">5 días - 300€</option>
                      <option value="7">1 semana - 420€</option>
                      <option value="14">2 semanas - 840€</option>
                      <option value="custom">Personalizado (indicar en descripción)</option>
                    </select>
                  </div>
                  
                  {formData.duration !== 'custom' && (
                    <div className="price-estimate">
                      <span className="estimate-label">Precio estimado:</span>
                      <span className="estimate-value">{parseInt(formData.duration) * 60}€</span>
                      <span className="estimate-note">+ horas extra si aplica</span>
                    </div>
                  )}
                </div>

                <div className="form-group full-width">
                  <label>Detalles Adicionales</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Tipo de vehículo a transportar, peso aproximado, observaciones especiales..."
                    rows="3"
                  />
                </div>
              </div>

              <div className="form-section">
                <h3><Icons.Calendar size={20} /> Fecha y Hora de Recogida de la Plataforma</h3>
                <p className="section-hint">Selecciona cuándo vendrás a recoger la plataforma</p>

                <div className="manual-date-input">
                  <label>Introducir fecha manualmente:</label>
                  <input
                    type="date"
                    value={getDateInputValue()}
                    onChange={handleManualDateChange}
                    min={new Date().toISOString().split('T')[0]}
                    className="date-input"
                  />
                  {selectedDate && (
                    <span className="selected-date-display">
                      <Icons.Check size={16} /> {selectedDate.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                    </span>
                  )}
                </div>

                <div className="calendar-divider">
                  <span>o selecciona en el calendario</span>
                </div>

                <div className="calendar-section">
                  <div className="calendar-navigation">
                    <button 
                      type="button" 
                      className="nav-btn prev-btn"
                      onClick={() => setCurrentMonthOffset(currentMonthOffset - 1)}
                      disabled={!canPreviousMonth()}
                    >
                      ← Anterior
                    </button>
                    <h5>{getMonthName(getCurrentMonth())}</h5>
                    <button 
                      type="button" 
                      className="nav-btn next-btn"
                      onClick={() => setCurrentMonthOffset(currentMonthOffset + 1)}
                      disabled={!canNextMonth()}
                    >
                      Siguiente →
                    </button>
                  </div>

                  <div className="calendar-month">
                    <div className="month-grid">
                      <div className="weekday-header">L</div>
                      <div className="weekday-header">M</div>
                      <div className="weekday-header">M</div>
                      <div className="weekday-header">J</div>
                      <div className="weekday-header">V</div>
                      <div className="weekday-header">S</div>
                      <div className="weekday-header">D</div>
                      
                      {getDaysInMonth(getCurrentMonth()).map((date, dayIdx) => (
                        <div key={dayIdx} className="calendar-day-slot">
                          {date ? (
                            <button
                              type="button"
                              className={`calendar-day ${selectedDate?.toDateString() === date.toDateString() ? 'selected' : ''} ${isDatePast(date) ? 'past' : ''}`}
                              onClick={() => handleDateSelect(date)}
                              disabled={isDatePast(date)}
                            >
                              <span className="day-date">{date.getDate()}</span>
                            </button>
                          ) : (
                            <div className="empty-day"></div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {selectedDate && (
                  <div className="time-section">
                    <h4>Hora de entrega de la plataforma para {selectedDate.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}:</h4>
                    <div className="time-grid">
                      {availableTimes.map(time => (
                        <button
                          key={time}
                          type="button"
                          className={`time-slot ${selectedTime === time ? 'selected' : ''}`}
                          onClick={() => handleTimeSelect(time)}
                        >
                          {time}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="form-actions">
                <button type="button" className="cancel-btn" onClick={() => navigate('/')}>
                  Cancelar
                </button>
                {!selectedDate && (
                  <p className="validation-hint">Selecciona un día de recogida.</p>
                )}
                {selectedDate && !selectedTime && (
                  <p className="validation-hint">Selecciona una hora de recogida.</p>
                )}
                {(selectedDate && selectedTime && (!formData.name || !formData.phone || !formData.email)) && (
                  <p className="validation-hint">Completa todos los campos de contacto.</p>
                )}
                <button
                  type="submit"
                  className="submit-btn"
                  disabled={!selectedDate || !selectedTime || !formData.name || !formData.phone || !formData.email}
                >
                  Confirmar Reserva
                </button>
                {submitError && <p className="submit-error">{submitError}</p>}
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
