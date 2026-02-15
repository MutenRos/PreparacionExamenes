import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useBooking } from '../contexts/BookingContext'
import { Icons } from '../components/Icons'
import craneImg from '../assets/images/WhatsApp Image 2025-12-31 at 09.46.58.jpeg'
import './CraneService.css'

export default function CraneService() {
  const navigate = useNavigate()
  const { createBooking } = useBooking()
  const [selectedDate, setSelectedDate] = useState(null)
  const [selectedTime, setSelectedTime] = useState(null)
  const [currentMonthOffset, setCurrentMonthOffset] = useState(0)
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    locationOrigin: '',
    locationDestination: '',
    description: ''
  })
  const [activeMap, setActiveMap] = useState('origin') // 'origin' o 'destination'
  const mapQuery = activeMap === 'origin' 
    ? (formData.locationOrigin || '').trim() || 'España'
    : (formData.locationDestination || '').trim() || 'España'
  const mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(mapQuery)}&output=embed`
  const [showConfirmation, setShowConfirmation] = useState(false)
  const [submitError, setSubmitError] = useState('')

  // Días y horarios ocupados (vacío por defecto, se llenarán con reservas)
  const occupiedDates = []
  const occupiedTimes = []

  const isDateOccupied = (date) => {
    return occupiedDates.some(d => d.toDateString() === date.toDateString())
  }

  const isTimeOccupied = (time) => {
    return occupiedTimes.includes(time)
  }

  // Horarios disponibles
  const availableTimes = [
    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00',
    '20:00', '21:00', '22:00', '23:00'
  ]

  const getCurrentMonth = () => {
    const date = new Date()
    date.setDate(1) // Fijar a día 1 para evitar problemas con meses
    date.setMonth(date.getMonth() + currentMonthOffset)
    return date
  }

  const canPreviousMonth = () => {
    return currentMonthOffset > 0
  }

  const canNextMonth = () => {
    return currentMonthOffset < 2
  }

  const getDaysInMonth = (date) => {
    const year = date.getFullYear()
    const month = date.getMonth()
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const daysInMonth = lastDay.getDate()
    const startingDayOfWeek = firstDay.getDay()

    const days = []
    // Días vacíos del mes anterior
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null)
    }
    // Días del mes
    for (let i = 1; i <= daysInMonth; i++) {
      days.push(new Date(year, month, i))
    }
    return days
  }

  const getMonthName = (date) => {
    return date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' })
  }

  const handleDateSelect = (date) => {
    setSelectedDate(date)
    setSelectedTime(null)
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
    if (!selectedDate || !selectedTime || !formData.name || !formData.phone || !formData.email || !formData.locationOrigin || !formData.locationDestination) {
      setSubmitError('Completa todos los campos: día, hora, datos de contacto y ubicaciones.')
      return
    }

    setSubmitError('')

    const startDate = `${selectedDate.toISOString().split('T')[0]}T${selectedTime}:00`
    const booking = {
      type: 'portes',
      service: 'Servicio de Grúa/Portes',
      name: formData.name,
      phone: formData.phone,
      email: formData.email,
      locationOrigin: formData.locationOrigin,
      locationDestination: formData.locationDestination,
      recogidaDir: formData.locationOrigin,
      descargaDir: formData.locationDestination,
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
    <div className="crane-service">
      {showConfirmation && (
        <div className="confirmation-modal">
          <div className="confirmation-content">
            <div className="confirmation-icon"><Icons.CheckCircle size={48} /></div>
            <h2>¡Solicitud Enviada!</h2>
            <p>Tu solicitud de transporte ha sido registrada exitosamente.</p>
            <p className="small-text">Te contactaremos pronto para confirmar horarios y presupuesto.</p>
          </div>
        </div>
      )}

      <button className="back-btn" onClick={() => navigate('/')}>
        ← Volver
      </button>

      <div className="crane-container">
        <div className="crane-header">
          <div className="crane-image-section">
            <img src={craneImg} alt="Grúa Cuevas MotorSport" className="crane-image" />
            <div className="crane-badge">Portes Especializados</div>
          </div>

          <div className="crane-info">
            <h1>Servicio de Portes Especializados</h1>
            <p className="crane-subtitle">Transporte seguro de vehículos de proyecto, clásicos y deportivos</p>

            <div className="crane-features">
              <div className="feature-item">
                <span className="feature-icon"><Icons.Car size={24} /></span>
                <div>
                  <h4>Vehículos Especializados</h4>
                  <p>Proyectos, clásicos, deportivos y de competición</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon"><Icons.Tool size={24} /></span>
                <div>
                  <h4>Entre Talleres</h4>
                  <p>Transporte seguro entre talleres y ubicaciones</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon"><Icons.Users size={24} /></span>
                <div>
                  <h4>Personal Profesional</h4>
                  <p>Equipo experto en manejo de vehículos especiales</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">💬</span>
                <div>
                  <h4>Contacto WhatsApp</h4>
                  <p><a href="https://wa.me/34686531422" target="_blank" rel="noopener noreferrer" style={{color: '#25D366', textDecoration: 'none', fontWeight: 'bold'}}>686 531 422</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="crane-content">
          <div className="crane-booking">
            <h2>Solicitar Servicio de Portes</h2>
            
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
                <h3>📍 Ubicaciones del Transporte</h3>
                
                <div className="locations-grid">
                  <div className="location-input-group">
                    <label className={`location-label ${activeMap === 'origin' ? 'active' : ''}`}>
                      <span className="location-icon">🏠</span> Ubicación de ORIGEN (Recogida) *
                    </label>
                    <input
                      type="text"
                      name="locationOrigin"
                      value={formData.locationOrigin}
                      onChange={handleInputChange}
                      onFocus={() => setActiveMap('origin')}
                      placeholder="¿Dónde recogemos el vehículo?"
                      required
                      className={activeMap === 'origin' ? 'active-input' : ''}
                    />
                  </div>
                  
                  <div className="location-arrow">→</div>
                  
                  <div className="location-input-group">
                    <label className={`location-label ${activeMap === 'destination' ? 'active' : ''}`}>
                      <span className="location-icon">🎯</span> Ubicación de DESTINO (Entrega) *
                    </label>
                    <input
                      type="text"
                      name="locationDestination"
                      value={formData.locationDestination}
                      onChange={handleInputChange}
                      onFocus={() => setActiveMap('destination')}
                      placeholder="¿Dónde entregamos el vehículo?"
                      required
                      className={activeMap === 'destination' ? 'active-input' : ''}
                    />
                  </div>
                </div>

                <div className="map-picker">
                  <div className="map-header">
                    <div className="map-tabs">
                      <button 
                        type="button" 
                        className={`map-tab ${activeMap === 'origin' ? 'active' : ''}`}
                        onClick={() => setActiveMap('origin')}
                      >
                        🏠 Ver Origen
                      </button>
                      <button 
                        type="button" 
                        className={`map-tab ${activeMap === 'destination' ? 'active' : ''}`}
                        onClick={() => setActiveMap('destination')}
                      >
                        🎯 Ver Destino
                      </button>
                    </div>
                    <a
                      className="map-link"
                      href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(mapQuery)}`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Abrir en Google Maps ↗
                    </a>
                  </div>
                  <div className="map-frame">
                    <iframe
                      title={`Mapa de ${activeMap === 'origin' ? 'origen' : 'destino'}`}
                      src={mapUrl}
                      loading="lazy"
                      allowFullScreen
                      referrerPolicy="no-referrer-when-downgrade"
                    />
                  </div>
                  <p className="map-hint">
                    Mostrando: <strong>{activeMap === 'origin' ? 'ORIGEN' : 'DESTINO'}</strong> — 
                    Escribe la dirección arriba y verifica la posición en el mapa.
                  </p>
                </div>

                <div className="form-group full-width">
                  <label>Detalles del Vehículo</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Tipo de vehículo, marca, modelo, estado, destino..."
                    rows="3"
                  />
                </div>
              </div>

              <div className="form-section">
                <h3>📅 Selecciona Fecha Preferida</h3>

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
                  <h4>¿Cuándo necesitas el transporte?</h4>
                  
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
                              className={`calendar-day ${selectedDate?.toDateString() === date.toDateString() ? 'selected' : ''} ${isDateOccupied(date) ? 'occupied' : ''}`}
                              onClick={() => !isDateOccupied(date) && handleDateSelect(date)}
                              disabled={isDateOccupied(date)}
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
                    <h4>Horario preferido para {selectedDate.toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' })}:</h4>
                    <div className="time-grid">
                      {availableTimes.map(time => (
                        <button
                          key={time}
                          type="button"
                          className={`time-slot ${selectedTime === time ? 'selected' : ''} ${isTimeOccupied(time) ? 'occupied' : ''}`}
                          onClick={() => !isTimeOccupied(time) && handleTimeSelect(time)}
                          disabled={isTimeOccupied(time)}
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
                  <p className="validation-hint">Selecciona un día.</p>
                )}
                {selectedDate && !selectedTime && (
                  <p className="validation-hint">Selecciona una hora.</p>
                )}
                {(selectedDate && selectedTime && (!formData.name || !formData.phone || !formData.email || !formData.locationOrigin || !formData.locationDestination)) && (
                  <p className="validation-hint">Completa todos los campos de contacto y ubicaciones.</p>
                )}
                <button
                  type="submit"
                  className="submit-btn"
                  disabled={!selectedDate || !selectedTime || !formData.name || !formData.phone || !formData.email || !formData.locationOrigin || !formData.locationDestination}
                >
                  Confirmar Solicitud
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
