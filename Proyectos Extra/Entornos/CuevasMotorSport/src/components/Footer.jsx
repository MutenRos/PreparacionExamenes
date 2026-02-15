import { Icons } from './Icons'
import './Footer.css'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
            <div className="footer-brand">
              <img src="/cuevas-logo.png" alt="Cuevas MotorSport" />
              <h3>Cuevas MotorSport</h3>
            </div>
            <p>S. Grúa y alquiler vehículos competición. Siempre listos, también para remolques y asistencia.</p>
        </div>

        <div className="footer-section">
          <h4>Servicios</h4>
          <ul>
            <li><a href="#servicios">Portes de Vehículos</a></li>
            <li><a href="#servicios">Alquiler de Coches Deportivos</a></li>
            <li><a href="#servicios">Alquiler de Plataforma Portacoches</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Contacto</h4>
          <ul>
            <li><a href="tel:+34686531422"><Icons.Phone size={14} /> +34 686 531 422</a></li>
            <li><a href="https://wa.me/34686531422" target="_blank" rel="noopener noreferrer"><Icons.MessageCircle size={14} /> WhatsApp</a></li>
            <li><a href="mailto:info@cuevasmotorsport.es"><Icons.Mail size={14} /> info@cuevasmotorsport.es</a></li>
            <li><Icons.MapPin size={14} /> España</li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Redes Sociales</h4>
          <div className="social-links">
            <a href="#" title="Facebook">f</a>
            <a href="#" title="Instagram"><Icons.Camera size={16} /></a>
            <a href="#" title="Twitter">X</a>
            <a href="#" title="LinkedIn">in</a>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; {currentYear} Cuevas MotorSport. Todos los derechos reservados.</p>
        <button
          onClick={() => window.location.href = '/login'}
          className="footer-admin-btn"
          title="Acceso Admin"
          aria-label="Acceso al panel de administración"
        >
          <Icons.Lock size={14} />
        </button>
      </div>
    </footer>
  )
}
