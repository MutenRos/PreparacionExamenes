import { useState, useEffect } from 'react'
import { useInventory } from '../../contexts/InventoryContext'
import ImageUpload from '../../components/ImageUpload'
import { Icons } from '../../components/Icons'
import '../../components/ImageUpload.css'
import './Inventory.css'

const API_URL = 'http://localhost:3001'

export default function Inventory() {
  const { vehicles, addVehicle, updateVehicle, deleteVehicle } = useInventory()
  const [showModal, setShowModal] = useState(false)
  const [editingVehicle, setEditingVehicle] = useState(null)
  const [tempVehicleId, setTempVehicleId] = useState(null)
  const [vehicleImages, setVehicleImages] = useState({ mainImage: null, gallery: [] })
  const [formData, setFormData] = useState({
    type: 'coche_deportivo',
    brand: '',
    model: '',
    year: new Date().getFullYear(),
    price: '',
    priceUnit: 'día',
    image: '🚗',
    status: 'disponible',
    // Datos generales del vehículo
    vin: '',
    matricula: '',
    color: '',
    kilometraje: '',
    combustible: 'gasolina',
    transmision: 'manual',
    // Especificaciones técnicas coche
    motor: '',
    cilindrada: '',
    potenciaCv: '',
    potenciaKw: '',
    par: '',
    traccion: '4x2',
    pesoKg: '',
    velocidadMax: '',
    aceleracion0100: '',
    // Competición
    categoria: '',
    homologacion: '',
    jaula: false,
    arnesCertificado: false,
    extintor: false,
    cortacorrientes: false,
    // Historial
    historialCompeticion: '',
    propietariosAnteriores: '',
    ultimaRevision: '',
    observaciones: '',
    specs: {},
    platformSpecs: {
      weight: '',
      dimensionLength: '',
      dimensionWidth: '',
      dimensionHeight: '',
      axles: ''
    }
  })

  const vehicleTypes = {
    coche_deportivo: { label: 'Coche Deportivo', icon: 'car' },
    remolque: { label: 'Remolque Portacoches', icon: 'truck' },
    plataforma: { label: 'Plataforma', icon: 'package' },
    grua: { label: 'Grúa', icon: 'truck' }
  }

  const handleOpenModal = async (vehicle = null) => {
    if (vehicle) {
      setEditingVehicle(vehicle)
      setFormData(vehicle)
      setTempVehicleId(vehicle.id)
      // Cargar imágenes existentes
      try {
        const response = await fetch(`${API_URL}/api/images/${vehicle.id}`)
        const images = await response.json()
        setVehicleImages(images)
      } catch {
        setVehicleImages({ mainImage: null, gallery: [] })
      }
    } else {
      setEditingVehicle(null)
      // Generar ID temporal para nuevos vehículos
      const newTempId = `temp_${Date.now()}`
      setTempVehicleId(newTempId)
      setVehicleImages({ mainImage: null, gallery: [] })
      setFormData({
        type: 'coche_deportivo',
        brand: '',
        model: '',
        year: new Date().getFullYear(),
        price: '',
        priceUnit: 'día',
        image: '🚗',
        status: 'disponible',
        vin: '',
        matricula: '',
        color: '',
        kilometraje: '',
        combustible: 'gasolina',
        transmision: 'manual',
        motor: '',
        cilindrada: '',
        potenciaCv: '',
        potenciaKw: '',
        par: '',
        traccion: '4x2',
        pesoKg: '',
        velocidadMax: '',
        aceleracion0100: '',
        categoria: '',
        homologacion: '',
        jaula: false,
        arnesCertificado: false,
        extintor: false,
        cortacorrientes: false,
        historialCompeticion: '',
        propietariosAnteriores: '',
        ultimaRevision: '',
        observaciones: '',
        specs: {},
        platformSpecs: {
          weight: '',
          dimensionLength: '',
          dimensionWidth: '',
          dimensionHeight: '',
          axles: ''
        }
      })
    }
    setShowModal(true)
  }

  const handleCloseModal = async () => {
    // Si es un vehículo nuevo que se cancela, limpiar imágenes temporales
    if (!editingVehicle && tempVehicleId?.startsWith('temp_')) {
      try {
        await fetch(`${API_URL}/api/images/${tempVehicleId}`, { method: 'DELETE' })
      } catch {
        // Ignorar errores de limpieza
      }
    }
    setShowModal(false)
    setEditingVehicle(null)
    setTempVehicleId(null)
    setVehicleImages({ mainImage: null, gallery: [] })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Preparar datos con imágenes
    const vehicleData = {
      ...formData,
      mainImage: vehicleImages.mainImage,
      gallery: vehicleImages.gallery
    }
    
    if (editingVehicle) {
      updateVehicle(editingVehicle.id, vehicleData)
    } else {
      // Para nuevo vehículo, necesitamos mover las imágenes del ID temporal al ID real
      const newVehicle = addVehicle(vehicleData)
      if (tempVehicleId?.startsWith('temp_') && newVehicle?.id) {
        try {
          await fetch(`${API_URL}/api/images/move/${tempVehicleId}/${newVehicle.id}`, {
            method: 'POST'
          })
        } catch {
          console.error('Error moviendo imágenes')
        }
      }
    }
    setShowModal(false)
    setEditingVehicle(null)
    setTempVehicleId(null)
    setVehicleImages({ mainImage: null, gallery: [] })
  }

  const handleDelete = async (id) => {
    if (confirm('¿Estás seguro de eliminar este vehículo?')) {
      // Eliminar imágenes del servidor
      try {
        await fetch(`${API_URL}/api/images/${id}`, { method: 'DELETE' })
      } catch {
        // Continuar aunque falle
      }
      deleteVehicle(id)
    }
  }

  const handleImagesChange = (images) => {
    setVehicleImages(images)
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    
    if (name.startsWith('platform_')) {
      const specKey = name.replace('platform_', '')
      setFormData(prev => ({
        ...prev,
        platformSpecs: {
          ...prev.platformSpecs,
          [specKey]: value
        }
      }))
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }))
    }
  }

  return (
    <div className="inventory-page">
      <div className="page-header">
        <div>
          <h1>🚗 Inventario</h1>
          <p>Gestión de vehículos y remolques</p>
        </div>
        <button onClick={() => handleOpenModal()} className="add-btn">
          ➕ Añadir Vehículo
        </button>
      </div>

      <div className="inventory-grid">
        {vehicles.map(vehicle => (
          <div key={vehicle.id} className="inventory-card">
            <div className="vehicle-image-section">
              {vehicle.mainImage ? (
                <img 
                  src={`${API_URL}${vehicle.mainImage.url}`} 
                  alt={`${vehicle.brand} ${vehicle.model}`}
                  className="vehicle-main-image"
                />
              ) : (
                <span className="vehicle-large-icon">{vehicle.image}</span>
              )}
              <span className={`status-badge ${vehicle.status}`}>
                {vehicle.status}
              </span>
              {vehicle.gallery && vehicle.gallery.length > 0 && (
                <span className="gallery-badge">
                  📷 {vehicle.gallery.length}
                </span>
              )}
            </div>
            
            <div className="vehicle-details">
              <span className="vehicle-type">{vehicleTypes[vehicle.type]?.label}</span>
              <h3>{vehicle.brand} {vehicle.model}</h3>
              <p className="vehicle-year">Año: {vehicle.year}</p>
              
              <div className="vehicle-specs">
                {Object.entries(vehicle.specs || {}).map(([key, value]) => (
                  <span key={key} className="spec-tag">
                    {key}: {value}
                  </span>
                ))}
                {vehicle.platformSpecs && (vehicle.platformSpecs.weight || vehicle.platformSpecs.axles) && (
                  <>
                    {vehicle.platformSpecs.weight && (
                      <span className="spec-tag">
                        Peso: {vehicle.platformSpecs.weight}kg
                      </span>
                    )}
                    {vehicle.platformSpecs.axles && (
                      <span className="spec-tag">
                        Ejes: {vehicle.platformSpecs.axles}
                      </span>
                    )}
                    {(vehicle.platformSpecs.dimensionLength || vehicle.platformSpecs.dimensionWidth || vehicle.platformSpecs.dimensionHeight) && (
                      <span className="spec-tag">
                        {vehicle.platformSpecs.dimensionLength && `${vehicle.platformSpecs.dimensionLength}m`}
                        {vehicle.platformSpecs.dimensionLength && vehicle.platformSpecs.dimensionWidth && ' × '}
                        {vehicle.platformSpecs.dimensionWidth && `${vehicle.platformSpecs.dimensionWidth}m`}
                        {(vehicle.platformSpecs.dimensionLength || vehicle.platformSpecs.dimensionWidth) && vehicle.platformSpecs.dimensionHeight && ' × '}
                        {vehicle.platformSpecs.dimensionHeight && `${vehicle.platformSpecs.dimensionHeight}m`}
                      </span>
                    )}
                  </>
                )}
              </div>

              <div className="vehicle-price">
                <strong>€{vehicle.price}</strong>
                <span>/{vehicle.priceUnit}</span>
              </div>
            </div>

            <div className="vehicle-actions">
              <button onClick={() => handleOpenModal(vehicle)} className="edit-btn">
                <Icons.Edit size={14} /> Editar
              </button>
              <button onClick={() => handleDelete(vehicle.id)} className="delete-btn">
                <Icons.Trash size={14} /> Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingVehicle ? 'Editar Vehículo' : 'Nuevo Vehículo'}</h2>
              <button onClick={handleCloseModal} className="close-btn"><Icons.X size={18} /></button>
            </div>

            <form onSubmit={handleSubmit} className="vehicle-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Tipo</label>
                  <select name="type" value={formData.type} onChange={handleChange} required>
                    {Object.entries(vehicleTypes).map(([key, value]) => (
                      <option key={key} value={key}>{value.label}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Icono</label>
                  <input
                    type="text"
                    name="image"
                    value={formData.image}
                    onChange={handleChange}
                    placeholder="🚗"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Marca</label>
                  <input
                    type="text"
                    name="brand"
                    value={formData.brand}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Modelo</label>
                  <input
                    type="text"
                    name="model"
                    value={formData.model}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Año</label>
                  <input
                    type="number"
                    name="year"
                    value={formData.year}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Precio</label>
                  <input
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Unidad</label>
                  <select name="priceUnit" value={formData.priceUnit} onChange={handleChange}>
                    <option value="día">día</option>
                    <option value="servicio">servicio</option>
                    <option value="hora">hora</option>
                    <option value="venta">venta (precio total)</option>
                  </select>
                </div>
              </div>

              {(formData.type === 'coche_deportivo') && (
                <>
                  {/* Identificación */}
                  <div className="specs-section">
                    <h4>🔖 Identificación</h4>
                    <div className="form-row">
                      <div className="form-group">
                        <label>VIN / Bastidor</label>
                        <input
                          type="text"
                          name="vin"
                          value={formData.vin || ''}
                          onChange={handleChange}
                          placeholder="WVWZZZ3CZWE123456"
                        />
                      </div>
                      <div className="form-group">
                        <label>Matrícula</label>
                        <input
                          type="text"
                          name="matricula"
                          value={formData.matricula || ''}
                          onChange={handleChange}
                          placeholder="1234 ABC"
                        />
                      </div>
                      <div className="form-group">
                        <label>Color</label>
                        <input
                          type="text"
                          name="color"
                          value={formData.color || ''}
                          onChange={handleChange}
                          placeholder="Rojo Racing"
                        />
                      </div>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Kilometraje</label>
                        <input
                          type="number"
                          name="kilometraje"
                          value={formData.kilometraje || ''}
                          onChange={handleChange}
                          placeholder="45000"
                        />
                      </div>
                      <div className="form-group">
                        <label>Combustible</label>
                        <select name="combustible" value={formData.combustible || 'gasolina'} onChange={handleChange}>
                          <option value="gasolina">Gasolina</option>
                          <option value="diesel">Diésel</option>
                          <option value="hibrido">Híbrido</option>
                          <option value="electrico">Eléctrico</option>
                          <option value="e85">E85 / Bioetanol</option>
                          <option value="racing_fuel">Combustible Racing</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Transmisión</label>
                        <select name="transmision" value={formData.transmision || 'manual'} onChange={handleChange}>
                          <option value="manual">Manual</option>
                          <option value="automatica">Automática</option>
                          <option value="secuencial">Secuencial</option>
                          <option value="dsg">DSG / PDK</option>
                          <option value="cvt">CVT</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  {/* Motor y Rendimiento */}
                  <div className="specs-section">
                    <h4>⚡ Motor y Rendimiento</h4>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Motor</label>
                        <input
                          type="text"
                          name="motor"
                          value={formData.motor || ''}
                          onChange={handleChange}
                          placeholder="2.0 TSI / V8 BiTurbo..."
                        />
                      </div>
                      <div className="form-group">
                        <label>Cilindrada (cc)</label>
                        <input
                          type="number"
                          name="cilindrada"
                          value={formData.cilindrada || ''}
                          onChange={handleChange}
                          placeholder="1984"
                        />
                      </div>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Potencia (CV)</label>
                        <input
                          type="number"
                          name="potenciaCv"
                          value={formData.potenciaCv || ''}
                          onChange={handleChange}
                          placeholder="310"
                        />
                      </div>
                      <div className="form-group">
                        <label>Potencia (kW)</label>
                        <input
                          type="number"
                          name="potenciaKw"
                          value={formData.potenciaKw || ''}
                          onChange={handleChange}
                          placeholder="228"
                        />
                      </div>
                      <div className="form-group">
                        <label>Par Motor (Nm)</label>
                        <input
                          type="number"
                          name="par"
                          value={formData.par || ''}
                          onChange={handleChange}
                          placeholder="400"
                        />
                      </div>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Tracción</label>
                        <select name="traccion" value={formData.traccion || '4x2'} onChange={handleChange}>
                          <option value="4x2">Tracción delantera (FWD)</option>
                          <option value="rwd">Tracción trasera (RWD)</option>
                          <option value="4x4">Tracción total (AWD/4x4)</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Peso (kg)</label>
                        <input
                          type="number"
                          name="pesoKg"
                          value={formData.pesoKg || ''}
                          onChange={handleChange}
                          placeholder="1350"
                        />
                      </div>
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Velocidad Máx (km/h)</label>
                        <input
                          type="number"
                          name="velocidadMax"
                          value={formData.velocidadMax || ''}
                          onChange={handleChange}
                          placeholder="250"
                        />
                      </div>
                      <div className="form-group">
                        <label>0-100 km/h (seg)</label>
                        <input
                          type="number"
                          step="0.1"
                          name="aceleracion0100"
                          value={formData.aceleracion0100 || ''}
                          onChange={handleChange}
                          placeholder="4.8"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Competición */}
                  <div className="specs-section">
                    <h4><Icons.Flag size={18} /> Competición</h4>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Categoría</label>
                        <input
                          type="text"
                          name="categoria"
                          value={formData.categoria || ''}
                          onChange={handleChange}
                          placeholder="Rally, Circuito, Drift, Hillclimb..."
                        />
                      </div>
                      <div className="form-group">
                        <label>Homologación</label>
                        <input
                          type="text"
                          name="homologacion"
                          value={formData.homologacion || ''}
                          onChange={handleChange}
                          placeholder="FIA N3, Grupo A, R5..."
                        />
                      </div>
                    </div>
                    <div className="form-row checkboxes-row">
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          name="jaula"
                          checked={formData.jaula || false}
                          onChange={(e) => setFormData(prev => ({ ...prev, jaula: e.target.checked }))}
                        />
                        <span>Jaula de Seguridad</span>
                      </label>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          name="arnesCertificado"
                          checked={formData.arnesCertificado || false}
                          onChange={(e) => setFormData(prev => ({ ...prev, arnesCertificado: e.target.checked }))}
                        />
                        <span>Arnés Certificado</span>
                      </label>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          name="extintor"
                          checked={formData.extintor || false}
                          onChange={(e) => setFormData(prev => ({ ...prev, extintor: e.target.checked }))}
                        />
                        <span>Extintor</span>
                      </label>
                      <label className="checkbox-label">
                        <input
                          type="checkbox"
                          name="cortacorrientes"
                          checked={formData.cortacorrientes || false}
                          onChange={(e) => setFormData(prev => ({ ...prev, cortacorrientes: e.target.checked }))}
                        />
                        <span>Cortacorrientes</span>
                      </label>
                    </div>
                  </div>

                  {/* Historial */}
                  <div className="specs-section">
                    <h4><Icons.ClipboardList size={18} /> Historial y Observaciones</h4>
                    <div className="form-group full-width">
                      <label>Historial de Competición</label>
                      <textarea
                        name="historialCompeticion"
                        value={formData.historialCompeticion || ''}
                        onChange={handleChange}
                        rows="3"
                        placeholder="Campeonatos, carreras, resultados destacados..."
                      />
                    </div>
                    <div className="form-row">
                      <div className="form-group">
                        <label>Propietarios Anteriores</label>
                        <input
                          type="text"
                          name="propietariosAnteriores"
                          value={formData.propietariosAnteriores || ''}
                          onChange={handleChange}
                          placeholder="1, 2, 3..."
                        />
                      </div>
                      <div className="form-group">
                        <label>Última Revisión</label>
                        <input
                          type="date"
                          name="ultimaRevision"
                          value={formData.ultimaRevision || ''}
                          onChange={handleChange}
                        />
                      </div>
                    </div>
                    <div className="form-group full-width">
                      <label>Observaciones</label>
                      <textarea
                        name="observaciones"
                        value={formData.observaciones || ''}
                        onChange={handleChange}
                        rows="3"
                        placeholder="Estado general, modificaciones, notas importantes..."
                      />
                    </div>
                  </div>
                </>
              )}

              {(formData.type === 'plataforma' || formData.type === 'remolque') && (
                <div className="platform-specs-section">
                  <h4><Icons.Settings size={18} /> Especificaciones de Plataforma</h4>
                  
                  <div className="form-row">
                    <div className="form-group">
                      <label>Peso (kg)</label>
                      <input
                        type="number"
                        name="platform_weight"
                        value={formData.platformSpecs?.weight || ''}
                        onChange={handleChange}
                        placeholder="1200"
                      />
                    </div>

                    <div className="form-group">
                      <label>Ejes</label>
                      <input
                        type="number"
                        name="platform_axles"
                        value={formData.platformSpecs?.axles || ''}
                        onChange={handleChange}
                        placeholder="2"
                      />
                    </div>
                  </div>

                  <h5>Dimensiones (metros)</h5>
                  
                  <div className="form-row">
                    <div className="form-group">
                      <label>Largo (m)</label>
                      <input
                        type="number"
                        step="0.1"
                        name="platform_dimensionLength"
                        value={formData.platformSpecs?.dimensionLength || ''}
                        onChange={handleChange}
                        placeholder="5.5"
                      />
                    </div>

                    <div className="form-group">
                      <label>Ancho (m)</label>
                      <input
                        type="number"
                        step="0.1"
                        name="platform_dimensionWidth"
                        value={formData.platformSpecs?.dimensionWidth || ''}
                        onChange={handleChange}
                        placeholder="2.4"
                      />
                    </div>

                    <div className="form-group">
                      <label>Alto (m)</label>
                      <input
                        type="number"
                        step="0.1"
                        name="platform_dimensionHeight"
                        value={formData.platformSpecs?.dimensionHeight || ''}
                        onChange={handleChange}
                        placeholder="1.5"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Sección de Imágenes */}
              <ImageUpload
                vehicleId={tempVehicleId}
                mainImage={vehicleImages.mainImage}
                gallery={vehicleImages.gallery}
                onImagesChange={handleImagesChange}
              />

              <div className="form-actions">
                <button type="button" onClick={handleCloseModal} className="cancel-btn">
                  Cancelar
                </button>
                <button type="submit" className="submit-btn">
                  {editingVehicle ? 'Guardar Cambios' : 'Añadir Vehículo'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
