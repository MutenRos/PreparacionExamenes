import { useState, useRef } from 'react'
import { Icons } from './Icons'
import './ImageUpload.css'

const API_URL = 'http://localhost:3001'

export default function ImageUpload({ vehicleId, mainImage, gallery, onImagesChange }) {
  const [uploading, setUploading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const mainInputRef = useRef(null)
  const galleryInputRef = useRef(null)

  const handleMainImageUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('image', file)
    formData.append('imageType', 'main')

    try {
      const response = await fetch(`${API_URL}/api/upload/${vehicleId}/main`, {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      
      if (data.success) {
        onImagesChange({
          mainImage: { url: data.imageUrl, filename: data.filename },
          gallery
        })
      }
    } catch (error) {
      console.error('Error subiendo imagen principal:', error)
      alert('Error al subir la imagen')
    } finally {
      setUploading(false)
    }
  }

  const handleGalleryUpload = async (files) => {
    if (!files || files.length === 0) return

    setUploading(true)
    const formData = new FormData()
    Array.from(files).forEach(file => {
      formData.append('images', file)
    })

    try {
      const response = await fetch(`${API_URL}/api/upload/${vehicleId}/gallery`, {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      
      if (data.success) {
        onImagesChange({
          mainImage,
          gallery: [...gallery, ...data.images]
        })
      }
    } catch (error) {
      console.error('Error subiendo imágenes:', error)
      alert('Error al subir las imágenes')
    } finally {
      setUploading(false)
    }
  }

  const handleDeleteImage = async (filename, isMain = false) => {
    if (!confirm('¿Eliminar esta imagen?')) return

    try {
      await fetch(`${API_URL}/api/images/${vehicleId}/${filename}`, {
        method: 'DELETE'
      })

      if (isMain) {
        onImagesChange({ mainImage: null, gallery })
      } else {
        onImagesChange({
          mainImage,
          gallery: gallery.filter(img => img.filename !== filename)
        })
      }
    } catch (error) {
      console.error('Error eliminando imagen:', error)
    }
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleGalleryUpload(e.dataTransfer.files)
    }
  }

  return (
    <div className="image-upload-container">
      {/* Imagen Principal */}
      <div className="upload-section">
        <h4><Icons.Camera size={18} /> Imagen Principal</h4>
        <div className="main-image-upload">
          {mainImage ? (
            <div className="main-image-preview">
              <img src={`${API_URL}${mainImage.url}`} alt="Imagen principal" />
              <div className="image-overlay">
                <button 
                  type="button"
                  className="btn-delete-image"
                  onClick={() => handleDeleteImage(mainImage.filename, true)}
                >
                  <Icons.Trash size={18} />
                </button>
                <button 
                  type="button"
                  className="btn-change-image"
                  onClick={() => mainInputRef.current?.click()}
                >
                  <Icons.Camera size={16} /> Cambiar
                </button>
              </div>
            </div>
          ) : (
            <div 
              className="upload-placeholder main"
              onClick={() => mainInputRef.current?.click()}
            >
              <span className="upload-icon"><Icons.Camera size={32} /></span>
              <span>Subir imagen principal</span>
              <span className="upload-hint">JPG, PNG, WebP (máx. 10MB)</span>
            </div>
          )}
          <input
            ref={mainInputRef}
            type="file"
            accept="image/*"
            onChange={handleMainImageUpload}
            style={{ display: 'none' }}
          />
        </div>
      </div>

      {/* Galería */}
      <div className="upload-section">
        <h4><Icons.Images size={18} /> Galería <span className="gallery-count">({gallery.length} imágenes)</span></h4>
        
        <div 
          className={`gallery-drop-zone ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => galleryInputRef.current?.click()}
        >
          <span className="upload-icon"><Icons.Upload size={32} /></span>
          <span>Arrastra imágenes aquí o haz clic para seleccionar</span>
          <span className="upload-hint">Puedes subir varias a la vez</span>
        </div>
        
        <input
          ref={galleryInputRef}
          type="file"
          accept="image/*"
          multiple
          onChange={(e) => handleGalleryUpload(e.target.files)}
          style={{ display: 'none' }}
        />

        {gallery.length > 0 && (
          <div className="gallery-preview">
            {gallery.map((img, index) => (
              <div key={img.filename} className="gallery-item">
                <img src={`${API_URL}${img.url}`} alt={`Galería ${index + 1}`} />
                <button 
                  type="button"
                  className="btn-delete-gallery"
                  onClick={(e) => {
                    e.stopPropagation()
                    handleDeleteImage(img.filename)
                  }}
                >
                  <Icons.X size={14} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {uploading && (
        <div className="upload-overlay">
          <div className="upload-spinner"></div>
          <span>Subiendo imágenes...</span>
        </div>
      )}
    </div>
  )
}
