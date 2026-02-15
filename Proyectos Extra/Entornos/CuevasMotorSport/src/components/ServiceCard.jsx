import { useNavigate } from 'react-router-dom'
import { Icons } from './Icons'
import './ServiceCard.css'

const iconMap = {
  truck: Icons.Truck,
  flag: Icons.Flag,
  car: Icons.Car
}

export default function ServiceCard({ service }) {
  const navigate = useNavigate()

  const handleSolicitar = () => {
    if (service.id === 1) {
      navigate('/servicios/grua')
    } else if (service.id === 3) {
      navigate('/servicios/plataforma')
    }
  }

  const IconComponent = iconMap[service.icon] || Icons.Car

  return (
    <div className="service-card" style={{ '--card-color': service.color }}>
      <div className="service-icon"><IconComponent size={48} /></div>
      <h3 className="service-title">{service.title}</h3>
      <p className="service-description">{service.description}</p>
      
      <div className="service-features">
        <h4>Características:</h4>
        <ul>
          {service.features.map((feature, idx) => (
            <li key={idx}><Icons.Check size={16} className="feature-check" /> {feature}</li>
          ))}
        </ul>
      </div>
      
      <button className="service-btn" onClick={handleSolicitar}>Solicitar</button>
    </div>
  )
}
