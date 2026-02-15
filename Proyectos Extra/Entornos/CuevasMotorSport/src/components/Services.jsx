import './Services.css'
import ServiceCard from './ServiceCard'

export default function Services() {
  const services = [
    {
      id: 1,
      title: 'Portes de Vehículos',
      icon: 'truck',
      description: 'Servicio especializado de portes para vehículos de proyecto, clásicos y deportivos. Transporte seguro entre talleres, eventos y ubicaciones.',
      features: [
        'Vehículos de proyecto',
        'Clásicos y restauración',
        'Deportivos y de competición',
        'Entre talleres y ubicaciones'
      ],
      color: '#d62828'
    },
    {
      id: 2,
      title: 'Alquiler de Coches Deportivos',
      icon: 'flag',
      description: 'Flota de vehículos deportivos de alta performance para experiencias de conducción inolvidables y eventos especiales.',
      features: [
        'Variedad de modelos',
        'Mantenimiento incluido',
        'Seguros completos',
        'Precios competitivos'
      ],
      color: '#f6c452'
    },
    {
      id: 3,
      title: 'Alquiler de Plataforma Portacoches',
      icon: 'car',
      description: 'Plataforma remolque especializada para transportar vehículos con seguridad. Perfecta para traslados y logística.',
      features: [
        'Capacidad variable',
        'Sistema de sujeción seguro',
        'Conductor experimentado',
        'Seguimiento GPS'
      ],
      color: '#2b303a'
    }
  ]

  return (
    <section id="servicios" className="services">
      <div className="services-container">
        <div className="services-header">
          <span className="services-badge">Servicios Premium</span>
          <h2 className="services-title">
            Nuestros <span className="text-gold">Servicios</span>
          </h2>
          <p className="services-subtitle">
            Soluciones completas para todas tus necesidades en el mundo del motor. 
            Calidad y profesionalismo garantizado.
          </p>
        </div>
        
        <div className="services-grid">
          {services.map(service => (
            <ServiceCard key={service.id} service={service} />
          ))}
        </div>
      </div>
    </section>
  )
}
