import { useState } from 'react'
import './Carousel.css'

export default function Carousel({ images, title, description }) {
  const [currentSlide, setCurrentSlide] = useState(0)

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % images.length)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + images.length) % images.length)
  }

  const goToSlide = (idx) => {
    setCurrentSlide(idx)
  }

  if (!images || images.length === 0) return null

  return (
    <div className="carousel">
      <div className="carousel-container">
        <h3>{title}</h3>
        <div className="carousel-wrapper">
          <button className="carousel-btn carousel-btn-prev" onClick={prevSlide}>
            ❮
          </button>
          
          <div className="carousel-slide">
            <img src={images[currentSlide].src} alt={images[currentSlide].alt} />
          </div>
          
          <button className="carousel-btn carousel-btn-next" onClick={nextSlide}>
            ❯
          </button>
        </div>

        <div className="carousel-indicators">
          {images.map((_, idx) => (
            <button
              key={idx}
              className={`indicator ${idx === currentSlide ? 'active' : ''}`}
              onClick={() => goToSlide(idx)}
            />
          ))}
        </div>

        <p className="carousel-description">{description}</p>
      </div>
    </div>
  )
}
