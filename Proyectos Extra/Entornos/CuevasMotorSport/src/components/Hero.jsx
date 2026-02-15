import { Icons } from './Icons'
import './Hero.css'

export default function Hero() {
  const handleCall = () => {
    window.location.href = 'tel:+34686531422'
  }

  const handleServices = () => {
    document.getElementById('servicios')?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <section className="hero">
      <div className="hero-content">
        <h2 className="hero-title">
          <span className="text-white">¿Necesitas Ayuda</span>
          <span className="text-gold">en la Carretera?</span>
        </h2>
        <p className="hero-subtitle">
          Servicio de grúa 24/7, alquiler de vehículos deportivos y plataformas de remolque. 
          Más de 8 años de experiencia a tu servicio.
        </p>
        <div className="hero-buttons">
          <button className="btn btn-primary" onClick={handleCall}>
            <Icons.Phone size={18} /> Llamar Ahora
          </button>
          <button className="btn btn-secondary" onClick={handleServices}>
            Conocer Servicios
          </button>
        </div>
        <div className="hero-stats">
          <div className="hero-stat">
            <span className="hero-stat-value">24/7</span>
            <span className="hero-stat-label">Disponibilidad</span>
          </div>
          <div className="hero-stat">
            <span className="hero-stat-value">8+</span>
            <span className="hero-stat-label">Años Experiencia</span>
          </div>
          <div className="hero-stat">
            <span className="hero-stat-value">500+</span>
            <span className="hero-stat-label">Servicios</span>
          </div>
        </div>
      </div>
      <div className="hero-image">
        <div className="hero-logo-card">
          <img src="/src/assets/WhatsApp Image 2025-12-31 at 09.13.47.jpeg" alt="Cuevas MotorSport" className="hero-logo" />
        </div>
      </div>
    </section>
  )
}
