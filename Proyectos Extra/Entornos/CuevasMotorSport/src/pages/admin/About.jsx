import { useState } from 'react'
import { useAbout } from '../../contexts/AboutContext'
import { Icons } from '../../components/Icons'
import './About.css'

export default function About() {
  const { about, updateAbout, updateMission, updateVision, updateValues, updateGallery, updateWorkGallery, updateGalleryTitle, updateGalleryDescription, updateWorkGalleryTitle, updateWorkGalleryDescription } = useAbout()
  const [editMode, setEditMode] = useState(false)
  const [formData, setFormData] = useState(about)
  const [missionText, setMissionText] = useState(about.mission.content)
  const [visionText, setVisionText] = useState(about.vision.content)
  const [galleryTitle, setGalleryTitle] = useState(about.galleryTitle)
  const [galleryDesc, setGalleryDesc] = useState(about.galleryDescription)
  const [workGalleryTitle, setWorkGalleryTitle] = useState(about.workGalleryTitle)
  const [workGalleryDesc, setWorkGalleryDesc] = useState(about.workGalleryDescription)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleValueChange = (idx, field, value) => {
    const newValues = [...formData.values]
    newValues[idx] = { ...newValues[idx], [field]: value }
    setFormData(prev => ({ ...prev, values: newValues }))
  }

  const handleGalleryChange = (idx, field, value) => {
    const newGallery = [...formData.gallery]
    newGallery[idx] = { ...newGallery[idx], [field]: value }
    setFormData(prev => ({ ...prev, gallery: newGallery }))
  }

  const handleGalleryImageUpload = (idx, file) => {
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        const newGallery = [...formData.gallery]
        newGallery[idx] = { ...newGallery[idx], src: e.target.result }
        setFormData(prev => ({ ...prev, gallery: newGallery }))
      }
      reader.readAsDataURL(file)
    }
  }

  const handleWorkGalleryImageUpload = (idx, file) => {
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        const newWorkGallery = [...formData.workGallery]
        newWorkGallery[idx] = { ...newWorkGallery[idx], src: e.target.result }
        setFormData(prev => ({ ...prev, workGallery: newWorkGallery }))
      }
      reader.readAsDataURL(file)
    }
  }

  const handleWorkGalleryChange = (idx, field, value) => {
    const newWorkGallery = [...formData.workGallery]
    newWorkGallery[idx] = { ...newWorkGallery[idx], [field]: value }
    setFormData(prev => ({ ...prev, workGallery: newWorkGallery }))
  }

  const removeGalleryImage = (idx) => {
    const newGallery = formData.gallery.filter((_, i) => i !== idx)
    setFormData(prev => ({ ...prev, gallery: newGallery }))
  }

  const removeWorkGalleryImage = (idx) => {
    const newWorkGallery = formData.workGallery.filter((_, i) => i !== idx)
    setFormData(prev => ({ ...prev, workGallery: newWorkGallery }))
  }

  const addGalleryImage = () => {
    setFormData(prev => ({
      ...prev,
      gallery: [...prev.gallery, { src: '', alt: 'Nueva imagen' }]
    }))
  }

  const addWorkGalleryImage = () => {
    setFormData(prev => ({
      ...prev,
      workGallery: [...prev.workGallery, { src: '', alt: 'Nuevo trabajo' }]
    }))
  }

  const handleSave = () => {
    updateAbout({
      title: formData.title,
      subtitle: formData.subtitle,
      description: formData.description,
      team: formData.team,
      experience: formData.experience
    })
    updateMission(missionText)
    updateVision(visionText)
    updateValues(formData.values)
    updateGallery(formData.gallery)
    updateWorkGallery(formData.workGallery)
    updateGalleryTitle(galleryTitle)
    updateGalleryDescription(galleryDesc)
    updateWorkGalleryTitle(workGalleryTitle)
    updateWorkGalleryDescription(workGalleryDesc)
    setEditMode(false)
  }

  return (
    <div className="admin-about">
      <div className="page-header">
        <h1><Icons.Info size={28} /> Sobre Nosotros</h1>
        <p>Edita la información pública sobre Cuevas MotorSport</p>
      </div>

      <div className="admin-actions">
        {!editMode ? (
          <button className="btn btn-primary" onClick={() => setEditMode(true)}>
            <Icons.Edit size={16} /> Editar Contenido
          </button>
        ) : (
          <div className="edit-actions">
            <button className="btn btn-primary" onClick={handleSave}>
              <Icons.Check size={16} /> Guardar Cambios
            </button>
            <button className="btn btn-secondary" onClick={() => {
              setEditMode(false)
              setFormData(about)
              setMissionText(about.mission.content)
              setVisionText(about.vision.content)
              setGalleryTitle(about.galleryTitle)
              setGalleryDesc(about.galleryDescription)
              setWorkGalleryTitle(about.workGalleryTitle)
              setWorkGalleryDesc(about.workGalleryDescription)
            }}>
              <Icons.X size={16} /> Cancelar
            </button>
          </div>
        )}
      </div>

      {editMode ? (
        <div className="admin-form">
          <div className="form-section">
            <h3>Encabezado Principal</h3>
            
            <div className="form-group">
              <label>Título</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Subtítulo</label>
              <input
                type="text"
                name="subtitle"
                value={formData.subtitle}
                onChange={handleInputChange}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Descripción Principal</label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                className="form-textarea"
                rows="4"
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Misión</h3>
            <div className="form-group">
              <label>Texto de Misión</label>
              <textarea
                value={missionText}
                onChange={(e) => setMissionText(e.target.value)}
                className="form-textarea"
                rows="3"
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Visión</h3>
            <div className="form-group">
              <label>Texto de Visión</label>
              <textarea
                value={visionText}
                onChange={(e) => setVisionText(e.target.value)}
                className="form-textarea"
                rows="3"
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Valores</h3>
            {formData.values.map((value, idx) => (
              <div key={idx} className="value-edit">
                <h4>Valor {idx + 1}</h4>
                <div className="form-group">
                  <label>Icono (emoji)</label>
                  <input
                    type="text"
                    value={value.icon}
                    onChange={(e) => handleValueChange(idx, 'icon', e.target.value)}
                    className="form-input"
                    maxLength="2"
                  />
                </div>
                <div className="form-group">
                  <label>Título</label>
                  <input
                    type="text"
                    value={value.title}
                    onChange={(e) => handleValueChange(idx, 'title', e.target.value)}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label>Descripción</label>
                  <textarea
                    value={value.description}
                    onChange={(e) => handleValueChange(idx, 'description', e.target.value)}
                    className="form-textarea"
                    rows="2"
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="form-section">
            <h3>Galería: Sobre Cuevas MotorSport</h3>
            
            <div className="form-group">
              <label>Título del Carrusel</label>
              <input
                type="text"
                value={galleryTitle}
                onChange={(e) => setGalleryTitle(e.target.value)}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Descripción del Carrusel</label>
              <textarea
                value={galleryDesc}
                onChange={(e) => setGalleryDesc(e.target.value)}
                className="form-textarea"
                rows="3"
              />
            </div>

            {formData.gallery && formData.gallery.map((image, idx) => (
              <div key={idx} className="gallery-edit">
                <h4>Imagen {idx + 1}</h4>
                <div className="form-group">
                  <label>Subir Imagen</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleGalleryImageUpload(idx, e.target.files[0])}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label>O Ruta de la imagen</label>
                  <input
                    type="text"
                    value={image.src}
                    onChange={(e) => handleGalleryChange(idx, 'src', e.target.value)}
                    className="form-input"
                    placeholder="/src/assets/images/..."
                  />
                </div>
                <div className="form-group">
                  <label>Descripción (alt)</label>
                  <input
                    type="text"
                    value={image.alt}
                    onChange={(e) => handleGalleryChange(idx, 'alt', e.target.value)}
                    className="form-input"
                  />
                </div>
                <button 
                  className="btn btn-danger"
                  onClick={() => removeGalleryImage(idx)}
                >
                  <Icons.Trash size={14} /> Eliminar imagen
                </button>
              </div>
            ))}
            <button 
              className="btn btn-secondary"
              onClick={addGalleryImage}
              style={{ marginTop: '1rem' }}
            >
              <Icons.Plus size={14} /> Agregar imagen
            </button>
          </div>

          <div className="form-section">
            <h3>Galería: Nuestro Trabajo</h3>
            
            <div className="form-group">
              <label>Título</label>
              <input
                type="text"
                value={workGalleryTitle}
                onChange={(e) => setWorkGalleryTitle(e.target.value)}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Descripción</label>
              <textarea
                value={workGalleryDesc}
                onChange={(e) => setWorkGalleryDesc(e.target.value)}
                className="form-textarea"
                rows="3"
              />
            </div>

            {formData.workGallery && formData.workGallery.map((image, idx) => (
              <div key={idx} className="gallery-edit">
                <h4>Trabajo {idx + 1}</h4>
                <div className="form-group">
                  <label>Subir Imagen</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleWorkGalleryImageUpload(idx, e.target.files[0])}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label>O Ruta de la imagen</label>
                  <input
                    type="text"
                    value={image.src}
                    onChange={(e) => handleWorkGalleryChange(idx, 'src', e.target.value)}
                    className="form-input"
                    placeholder="/src/assets/images/..."
                  />
                </div>
                <div className="form-group">
                  <label>Descripción (alt)</label>
                  <input
                    type="text"
                    value={image.alt}
                    onChange={(e) => handleWorkGalleryChange(idx, 'alt', e.target.value)}
                    className="form-input"
                  />
                </div>
                <button 
                  className="btn btn-danger"
                  onClick={() => removeWorkGalleryImage(idx)}
                >
                  <Icons.Trash size={14} /> Eliminar imagen
                </button>
              </div>
            ))}
            <button 
              className="btn btn-secondary"
              onClick={addWorkGalleryImage}
              style={{ marginTop: '1rem' }}
            >
              <Icons.Plus size={14} /> Agregar trabajo
            </button>
          </div>

          <div className="form-section">
            <h3>Información Adicional</h3>
            
            <div className="form-group">
              <label>Equipo</label>
              <input
                type="text"
                name="team"
                value={formData.team}
                onChange={handleInputChange}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Experiencia</label>
              <input
                type="text"
                name="experience"
                value={formData.experience}
                onChange={handleInputChange}
                className="form-input"
              />
            </div>
          </div>
        </div>
      ) : (
        <div className="about-preview">
          <div className="preview-section">
            <h3>{about.title}</h3>
            <p className="preview-subtitle">{about.subtitle}</p>
            <p className="preview-text">{about.description}</p>
          </div>

          {about.gallery && about.gallery.length > 0 && (
            <div className="preview-gallery">
              <h4>Sobre Cuevas MotorSport</h4>
              <div className="gallery-preview">
                {about.gallery.map((image, idx) => (
                  <div key={idx} className="gallery-preview-item">
                    <img src={image.src} alt={image.alt} />
                    <p>{image.alt}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="preview-grid">
            <div className="preview-card">
              <h4>{about.mission.title}</h4>
              <p>{about.mission.content}</p>
            </div>
            <div className="preview-card">
              <h4>{about.vision.title}</h4>
              <p>{about.vision.content}</p>
            </div>
          </div>

          {about.gallery && about.gallery.length > 0 && (
            <div className="preview-gallery">
              <h4>Sobre Cuevas MotorSport</h4>
              <div className="gallery-preview">
                {about.gallery.map((image, idx) => (
                  <div key={idx} className="gallery-preview-item">
                    <img src={image.src} alt={image.alt} />
                    <p>{image.alt}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="preview-values">
            <h4>Valores</h4>
            <div className="values-display">
              {about.values.map((value, idx) => (
                <div key={idx} className="value-display">
                  <span className="value-emoji">{value.icon}</span>
                  <strong>{value.title}</strong>
                  <p>{value.description}</p>
                </div>
              ))}
            </div>
          </div>

          {about.workGallery && about.workGallery.length > 0 && (
            <div className="preview-gallery">
              <h4>{about.workGalleryTitle}</h4>
              <div className="gallery-preview work">
                {about.workGallery.map((image, idx) => (
                  <div key={idx} className="gallery-preview-item work">
                    <img src={image.src} alt={image.alt} />
                    <p>{image.alt}</p>
                  </div>
                ))}
              </div>
              <p style={{ marginTop: '1rem', textAlign: 'center', color: 'var(--text-light)' }}>{about.workGalleryDescription}</p>
            </div>
          )}

          <div className="preview-footer">
            <p><strong>Equipo:</strong> {about.team}</p>
            <p><strong>Experiencia:</strong> {about.experience}</p>
          </div>
        </div>
      )}
    </div>
  )
}
