import './Header.css'
import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="header">
      <div className="header-container">
        <div className="logo-section">
          <div className="logo-mark">
            <img src="/cuevas-logo.png" alt="Cuevas MotorSport" />
          </div>
          <div className="logo-copy">
            <h1 className="logo-text">Cuevas MotorSport</h1>
            <p className="tagline">S. Grúa y Alquiler Vehículos Competición</p>
          </div>
        </div>
        
        <nav className={`nav ${mobileMenuOpen ? 'active' : ''}`}>
          <Link to="/vehiculos" onClick={() => setMobileMenuOpen(false)}>Vehículos</Link>
          <a href="#servicios" onClick={() => setMobileMenuOpen(false)}>Servicios</a>
          <a href="#contacto" onClick={() => setMobileMenuOpen(false)}>Contacto</a>
          <button className="cta-button" onClick={() => {
            document.getElementById('contacto')?.scrollIntoView({ behavior: 'smooth' })
            setMobileMenuOpen(false)
          }}>
            Solicitar Servicio
          </button>
        </nav>

        <button className="mobile-menu-btn" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
          ☰
        </button>
      </div>
    </header>
  )
}
