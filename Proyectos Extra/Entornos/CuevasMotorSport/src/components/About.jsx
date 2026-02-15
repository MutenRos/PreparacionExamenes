import { useAbout } from '../contexts/AboutContext'
import Carousel from './Carousel'
import './About.css'

export default function About() {
  const { about } = useAbout()

  return (
    <section className="about">
      <div className="about-container">
        <div className="about-header">
          <h2 className="about-title">{about.title}</h2>
          <p className="about-subtitle">{about.subtitle}</p>
        </div>

        <div className="about-content">
          <p className="about-description">{about.description}</p>
        </div>

        {about.gallery && about.gallery.length > 0 && (
          <Carousel 
            images={about.gallery}
            title={about.galleryTitle}
            description={about.galleryDescription}
          />
        )}

        <div className="about-cards">
          <div className="about-card mission">
            <h3>{about.mission.title}</h3>
            <p>{about.mission.content}</p>
          </div>
          <div className="about-card vision">
            <h3>{about.vision.title}</h3>
            <p>{about.vision.content}</p>
          </div>
        </div>

        <div className="about-values">
          <h3>Nuestros Valores</h3>
          <div className="values-grid">
            {about.values.map((value, idx) => (
              <div key={idx} className="value-item">
                <div className="value-icon">{value.icon}</div>
                <h4>{value.title}</h4>
                <p>{value.description}</p>
              </div>
            ))}
          </div>
        </div>

        {about.workGallery && about.workGallery.length > 0 && (
          <div className="work-gallery">
            <h3>{about.workGalleryTitle}</h3>
            <div className="work-gallery-grid">
              {about.workGallery.map((image, idx) => (
                <div key={idx} className="work-gallery-item">
                  <img src={image.src} alt={image.alt || `Nuestro Trabajo ${idx + 1}`} />
                </div>
              ))}
            </div>
            <p className="work-gallery-description">{about.workGalleryDescription}</p>
          </div>
        )}

        <div className="about-footer">
          <div className="about-stat">
            <div className="stat-number">{about.team}</div>
          </div>
          <div className="about-stat">
            <div className="stat-number">{about.experience}</div>
          </div>
        </div>
      </div>
    </section>
  )
}
