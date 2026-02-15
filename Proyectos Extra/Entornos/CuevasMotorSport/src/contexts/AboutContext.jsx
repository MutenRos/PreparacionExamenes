import { createContext, useContext, useState, useEffect } from 'react'

// Importar imágenes
import img1 from '../assets/images/WhatsApp Image 2025-12-31 at 09.29.30 (1).jpeg'
import img2 from '../assets/images/WhatsApp Image 2025-12-31 at 09.29.30 (2).jpeg'
import img3 from '../assets/images/WhatsApp Image 2025-12-31 at 09.29.30 (3).jpeg'
import img4 from '../assets/images/WhatsApp Image 2025-12-31 at 09.29.30.jpeg'
import img5 from '../assets/images/WhatsApp Image 2025-12-31 at 09.29.31 (1).jpeg'
import img6 from '../assets/images/WhatsApp Image 2025-12-31 at 09.29.31 (2).jpeg'
import img7 from '../assets/images/WhatsApp Image 2025-12-31 at 09.29.31 (3).jpeg'
import img8 from '../assets/images/WhatsApp Image 2025-12-31 at 09.29.31.jpeg'
import imgGrua from '../assets/images/WhatsApp Image 2025-12-31 at 09.46.58.jpeg'

const AboutContext = createContext(null)

const initialAbout = {
  title: 'Sobre Cuevas MotorSport',
  subtitle: 'Tu aliado en la carretera desde 2015',
  description: 'Somos una empresa de servicios automotriz especializada en grúa 24/7, alquiler de vehículos deportivos y plataformas de remolque. Contamos con más de 8 años de experiencia y un equipo profesional comprometido con la excelencia.',
  mission: {
    title: 'Nuestra Misión',
    content: 'Proporcionar servicios automotrices de calidad superior con atención personalizada, garantizando la confianza de nuestros clientes en cada intervención.'
  },
  vision: {
    title: 'Nuestra Visión',
    content: 'Ser la empresa líder en servicios automotrices en la región, reconocida por nuestra profesionalismo, rapidez y compromiso con el cliente.'
  },
  values: [
    { title: 'Profesionalismo', icon: 'settings', description: 'Técnicos capacitados y certificados' },
    { title: 'Disponibilidad', icon: '24', description: 'Servicio 24/7 todos los días' },
    { title: 'Confianza', icon: 'shield', description: 'Comprometidos con tu satisfacción' },
    { title: 'Rapidez', icon: 'zap', description: 'Respuesta inmediata garantizada' }
  ],
  gallery: [
    { src: img1, alt: 'Cuevas MotorSport' },
    { src: img2, alt: 'Cuevas MotorSport' },
    { src: img3, alt: 'Cuevas MotorSport' },
    { src: img4, alt: 'Cuevas MotorSport' },
    { src: img5, alt: 'Cuevas MotorSport' },
    { src: img6, alt: 'Cuevas MotorSport' },
    { src: img7, alt: 'Cuevas MotorSport' },
    { src: img8, alt: 'Cuevas MotorSport' }
  ],
  workGallery: [
    { src: imgGrua, alt: 'Servicio de Grúa en Acción' }
  ],
  galleryTitle: 'Galería de Servicios',
  galleryDescription: 'Conoce nuestros servicios y equipos profesionales',
  workGalleryTitle: 'Nuestro Trabajo',
  workGalleryDescription: 'Vea cómo trabajamos para nuestros clientes',
  team: 'Equipo de 15+ profesionales dedicados',
  experience: 'Más de 8 años sirviendo a la región'
}

export function AboutProvider({ children }) {
  const [about, setAbout] = useState(() => {
    const stored = localStorage.getItem('about')
    if (stored) {
      try {
        const parsed = JSON.parse(stored)
        // Si no tiene workGallery, combinar con datos por defecto
        if (!parsed.workGallery) {
          return { ...parsed, workGallery: initialAbout.workGallery }
        }
        return parsed
      } catch {
        return initialAbout
      }
    }
    return initialAbout
  })

  useEffect(() => {
    localStorage.setItem('about', JSON.stringify(about))
  }, [about])

  const updateAbout = (updates) => {
    setAbout(prev => ({ ...prev, ...updates }))
  }

  const updateMission = (content) => {
    setAbout(prev => ({
      ...prev,
      mission: { ...prev.mission, content }
    }))
  }

  const updateVision = (content) => {
    setAbout(prev => ({
      ...prev,
      vision: { ...prev.vision, content }
    }))
  }

  const updateValues = (values) => {
    setAbout(prev => ({ ...prev, values }))
  }

  const updateGallery = (gallery) => {
    setAbout(prev => ({ ...prev, gallery }))
  }

  const updateWorkGallery = (workGallery) => {
    setAbout(prev => ({ ...prev, workGallery }))
  }

  const updateGalleryTitle = (galleryTitle) => {
    setAbout(prev => ({ ...prev, galleryTitle }))
  }

  const updateGalleryDescription = (galleryDescription) => {
    setAbout(prev => ({ ...prev, galleryDescription }))
  }

  const updateWorkGalleryTitle = (workGalleryTitle) => {
    setAbout(prev => ({ ...prev, workGalleryTitle }))
  }

  const updateWorkGalleryDescription = (workGalleryDescription) => {
    setAbout(prev => ({ ...prev, workGalleryDescription }))
  }

  const value = {
    about,
    updateAbout,
    updateMission,
    updateVision,
    updateValues,
    updateGallery,
    updateWorkGallery,
    updateGalleryTitle,
    updateGalleryDescription,
    updateWorkGalleryTitle,
    updateWorkGalleryDescription
  }

  return (
    <AboutContext.Provider value={value}>
      {children}
    </AboutContext.Provider>
  )
}

export function useAbout() {
  const context = useContext(AboutContext)
  if (!context) {
    throw new Error('useAbout must be used within AboutProvider')
  }
  return context
}
