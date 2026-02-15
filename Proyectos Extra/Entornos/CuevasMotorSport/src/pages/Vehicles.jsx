import { useState } from 'react'
import { useInventory } from '../contexts/InventoryContext'
import { Link } from 'react-router-dom'
import { Icons } from '../components/Icons'
import './Vehicles.css'

const API_URL = 'http://localhost:3001'

export default function Vehicles() {
  const { vehicles } = useInventory()
  const [selectedVehicle, setSelectedVehicle] = useState(null)
  const [currentImageIndex, setCurrentImageIndex] = useState(0)
  const [filter, setFilter] = useState('todos')

  // Solo mostrar vehículos disponibles o reservados (no vendidos)
  const publicVehicles = vehicles.filter(v => 
    v.type === 'coche_deportivo' && v.status !== 'vendido'
  )

  const filteredVehicles = filter === 'todos' 
    ? publicVehicles 
    : publicVehicles.filter(v => v.status === filter)

  const openModal = (vehicle) => {
    setSelectedVehicle(vehicle)
    setCurrentImageIndex(0)
  }

  const closeModal = () => {
    setSelectedVehicle(null)
    setCurrentImageIndex(0)
  }

  const getAllImages = (vehicle) => {
    const images = []
    if (vehicle.mainImage) {
      images.push(vehicle.mainImage)
    }
    if (vehicle.gallery && vehicle.gallery.length > 0) {
      images.push(...vehicle.gallery)
    }
    return images
  }

  const nextImage = () => {
    const images = getAllImages(selectedVehicle)
    setCurrentImageIndex((prev) => (prev + 1) % images.length)
  }

  const prevImage = () => {
    const images = getAllImages(selectedVehicle)
    setCurrentImageIndex((prev) => (prev - 1 + images.length) % images.length)
  }

  return (
    <div className="vehicles-page">
      {/* Header */}
      <header className="vehicles-header">
        <nav className="vehicles-nav">
          <Link to="/" className="nav-logo">
            <span className="logo-icon"><Icons.Flag size={20} /></span>
            <span className="logo-text">Cuevas MotorSport</span>
          </Link>
          <div className="nav-links">
            <Link to="/">Inicio</Link>
            <Link to="/vehiculos" className="active">Vehículos</Link>
            <Link to="/servicios/grua">Servicios</Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="vehicles-hero">
        <div className="hero-content">
          <h1>Vehículos de Competición</h1>
          <p>Preparados para ganar. Listos para ti.</p>
        </div>
      </section>

      {/* Filters */}
      <section className="vehicles-filters">
        <div className="container">
          <div className="filter-buttons">
            <button 
              className={filter === 'todos' ? 'active' : ''} 
              onClick={() => setFilter('todos')}
            >
              Todos
            </button>
            <button 
              className={filter === 'disponible' ? 'active' : ''} 
              onClick={() => setFilter('disponible')}
            >
              Disponibles
            </button>
            <button 
              className={filter === 'reservado' ? 'active' : ''} 
              onClick={() => setFilter('reservado')}
            >
              Reservados
            </button>
          </div>
          <p className="results-count">{filteredVehicles.length} vehículos</p>
        </div>
      </section>

      {/* Vehicle Grid */}
      <section className="vehicles-grid-section">
        <div className="container">
          {filteredVehicles.length === 0 ? (
            <div className="no-vehicles">
              <span className="no-vehicles-icon"><Icons.Car size={48} /></span>
              <h3>No hay vehículos disponibles</h3>
              <p>Vuelve pronto, estamos preparando nuevas máquinas.</p>
            </div>
          ) : (
            <div className="vehicles-grid">
              {filteredVehicles.map(vehicle => (
                <article 
                  key={vehicle.id} 
                  className="vehicle-card"
                  onClick={() => openModal(vehicle)}
                >
                  <div className="card-image">
                    {vehicle.mainImage ? (
                      <img 
                        src={`${API_URL}${vehicle.mainImage.url}`} 
                        alt={`${vehicle.brand} ${vehicle.model}`}
                      />
                    ) : (
                      <div className="card-placeholder">
                        <span><Icons.Car size={32} /></span>
                      </div>
                    )}
                    <span className={`card-status ${vehicle.status}`}>
                      {vehicle.status === 'disponible' ? 'Disponible' : 'Reservado'}
                    </span>
                    {vehicle.gallery && vehicle.gallery.length > 0 && (
                      <span className="card-gallery-count">
                        <Icons.Camera size={14} /> +{vehicle.gallery.length}
                      </span>
                    )}
                  </div>
                  
                  <div className="card-content">
                    <div className="card-header">
                      <span className="card-year">{vehicle.year}</span>
                      {vehicle.categoria && (
                        <span className="card-category">{vehicle.categoria}</span>
                      )}
                    </div>
                    
                    <h3 className="card-title">{vehicle.brand} {vehicle.model}</h3>
                    
                    <div className="card-specs">
                      {vehicle.potenciaCv && (
                        <span className="spec"><Icons.Zap size={14} /> {vehicle.potenciaCv} CV</span>
                      )}
                      {vehicle.motor && (
                        <span className="spec"><Icons.Settings size={14} /> {vehicle.motor}</span>
                      )}
                      {vehicle.traccion && (
                        <span className="spec"><Icons.Wheel size={14} /> {vehicle.traccion}</span>
                      )}
                    </div>
                    
                    <div className="card-footer">
                      <span className="card-price">
                        {vehicle.price ? `${Number(vehicle.price).toLocaleString('es-ES')} €` : 'Consultar'}
                      </span>
                      <button className="card-btn">Ver más</button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Contact CTA */}
      <section className="vehicles-cta">
        <div className="container">
          <h2>¿Interesado en algún vehículo?</h2>
          <p>Contacta con nosotros para más información o concertar una visita.</p>
          <div className="cta-buttons">
            <a href="tel:+34600000000" className="cta-btn primary">
              <Icons.Phone size={18} /> Llamar ahora
            </a>
            <a href="mailto:info@cuevasmotorsport.com" className="cta-btn secondary">
              <Icons.Mail size={18} /> Enviar email
            </a>
          </div>
        </div>
      </section>

      {/* Vehicle Detail Modal */}
      {selectedVehicle && (
        <div className="vehicle-modal-overlay" onClick={closeModal}>
          <div className="vehicle-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeModal}><Icons.X size={20} /></button>
            
            {/* Image Gallery */}
            <div className="modal-gallery">
              {getAllImages(selectedVehicle).length > 0 ? (
                <>
                  <img 
                    src={`${API_URL}${getAllImages(selectedVehicle)[currentImageIndex]?.url}`}
                    alt={`${selectedVehicle.brand} ${selectedVehicle.model}`}
                    className="gallery-main-image"
                  />
                  {getAllImages(selectedVehicle).length > 1 && (
                    <>
                      <button className="gallery-nav prev" onClick={prevImage}>‹</button>
                      <button className="gallery-nav next" onClick={nextImage}>›</button>
                      <div className="gallery-dots">
                        {getAllImages(selectedVehicle).map((_, idx) => (
                          <button 
                            key={idx}
                            className={`dot ${idx === currentImageIndex ? 'active' : ''}`}
                            onClick={() => setCurrentImageIndex(idx)}
                          />
                        ))}
                      </div>
                    </>
                  )}
                </>
              ) : (
                <div className="gallery-placeholder">
                  <span><Icons.Car size={48} /></span>
                </div>
              )}
              <span className={`modal-status ${selectedVehicle.status}`}>
                {selectedVehicle.status === 'disponible' ? 'Disponible' : 'Reservado'}
              </span>
            </div>

            {/* Vehicle Info */}
            <div className="modal-info">
              <div className="modal-header">
                <div>
                  <span className="modal-year">{selectedVehicle.year}</span>
                  <h2>{selectedVehicle.brand} {selectedVehicle.model}</h2>
                </div>
                <div className="modal-price">
                  {selectedVehicle.price 
                    ? `${Number(selectedVehicle.price).toLocaleString('es-ES')} €` 
                    : 'Consultar precio'}
                </div>
              </div>

              {/* Specs Grid */}
              <div className="modal-specs-grid">
                {selectedVehicle.motor && (
                  <div className="modal-spec">
                    <span className="spec-label">Motor</span>
                    <span className="spec-value">{selectedVehicle.motor}</span>
                  </div>
                )}
                {selectedVehicle.potenciaCv && (
                  <div className="modal-spec">
                    <span className="spec-label">Potencia</span>
                    <span className="spec-value">{selectedVehicle.potenciaCv} CV</span>
                  </div>
                )}
                {selectedVehicle.cilindrada && (
                  <div className="modal-spec">
                    <span className="spec-label">Cilindrada</span>
                    <span className="spec-value">{selectedVehicle.cilindrada} cc</span>
                  </div>
                )}
                {selectedVehicle.par && (
                  <div className="modal-spec">
                    <span className="spec-label">Par Motor</span>
                    <span className="spec-value">{selectedVehicle.par} Nm</span>
                  </div>
                )}
                {selectedVehicle.traccion && (
                  <div className="modal-spec">
                    <span className="spec-label">Tracción</span>
                    <span className="spec-value">{selectedVehicle.traccion}</span>
                  </div>
                )}
                {selectedVehicle.transmision && (
                  <div className="modal-spec">
                    <span className="spec-label">Transmisión</span>
                    <span className="spec-value">{selectedVehicle.transmision}</span>
                  </div>
                )}
                {selectedVehicle.pesoKg && (
                  <div className="modal-spec">
                    <span className="spec-label">Peso</span>
                    <span className="spec-value">{selectedVehicle.pesoKg} kg</span>
                  </div>
                )}
                {selectedVehicle.velocidadMax && (
                  <div className="modal-spec">
                    <span className="spec-label">Vel. Máxima</span>
                    <span className="spec-value">{selectedVehicle.velocidadMax} km/h</span>
                  </div>
                )}
                {selectedVehicle.aceleracion0100 && (
                  <div className="modal-spec">
                    <span className="spec-label">0-100 km/h</span>
                    <span className="spec-value">{selectedVehicle.aceleracion0100} s</span>
                  </div>
                )}
                {selectedVehicle.combustible && (
                  <div className="modal-spec">
                    <span className="spec-label">Combustible</span>
                    <span className="spec-value">{selectedVehicle.combustible}</span>
                  </div>
                )}
                {selectedVehicle.kilometraje && (
                  <div className="modal-spec">
                    <span className="spec-label">Kilometraje</span>
                    <span className="spec-value">{Number(selectedVehicle.kilometraje).toLocaleString('es-ES')} km</span>
                  </div>
                )}
                {selectedVehicle.color && (
                  <div className="modal-spec">
                    <span className="spec-label">Color</span>
                    <span className="spec-value">{selectedVehicle.color}</span>
                  </div>
                )}
              </div>

              {/* Competition Section */}
              {(selectedVehicle.categoria || selectedVehicle.homologacion || 
                selectedVehicle.jaula || selectedVehicle.arnesCertificado || 
                selectedVehicle.extintor || selectedVehicle.cortacorrientes) && (
                <div className="modal-competition">
                  <h4><Icons.Flag size={18} /> Competición</h4>
                  <div className="competition-grid">
                    {selectedVehicle.categoria && (
                      <span className="competition-tag">{selectedVehicle.categoria}</span>
                    )}
                    {selectedVehicle.homologacion && (
                      <span className="competition-tag">{selectedVehicle.homologacion}</span>
                    )}
                    {selectedVehicle.jaula && (
                      <span className="competition-tag safety"><Icons.Check size={14} /> Jaula homologada</span>
                    )}
                    {selectedVehicle.arnesCertificado && (
                      <span className="competition-tag safety"><Icons.Check size={14} /> Arnés certificado</span>
                    )}
                    {selectedVehicle.extintor && (
                      <span className="competition-tag safety"><Icons.Check size={14} /> Extintor</span>
                    )}
                    {selectedVehicle.cortacorrientes && (
                      <span className="competition-tag safety"><Icons.Check size={14} /> Cortacorrientes</span>
                    )}
                  </div>
                </div>
              )}

              {/* History */}
              {selectedVehicle.historialCompeticion && (
                <div className="modal-history">
                  <h4><Icons.Trophy size={18} /> Historial de Competición</h4>
                  <p>{selectedVehicle.historialCompeticion}</p>
                </div>
              )}

              {/* Contact Actions */}
              <div className="modal-actions">
                <a href="tel:+34600000000" className="action-btn primary">
                  <Icons.Phone size={18} /> Llamar
                </a>
                <a 
                  href={`mailto:info@cuevasmotorsport.com?subject=Consulta: ${selectedVehicle.brand} ${selectedVehicle.model} ${selectedVehicle.year}`} 
                  className="action-btn secondary"
                >
                  <Icons.Mail size={18} /> Consultar
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="vehicles-footer">
        <div className="container">
          <p>© 2026 Cuevas MotorSport. Todos los derechos reservados.</p>
        </div>
      </footer>
    </div>
  )
}
