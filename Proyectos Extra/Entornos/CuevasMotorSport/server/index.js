import express from 'express'
import multer from 'multer'
import cors from 'cors'
import { v4 as uuidv4 } from 'uuid'
import path from 'path'
import fs from 'fs'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()
const PORT = 3001

// Crear carpeta de uploads si no existe
const uploadsDir = path.join(__dirname, '../public/uploads')
const vehiclesDir = path.join(uploadsDir, 'vehicles')

if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true })
}
if (!fs.existsSync(vehiclesDir)) {
  fs.mkdirSync(vehiclesDir, { recursive: true })
}

// Middleware
app.use(cors())
app.use(express.json())
app.use('/uploads', express.static(path.join(__dirname, '../public/uploads')))

// Configuración de Multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const vehicleId = req.params.vehicleId || 'temp'
    const vehicleDir = path.join(vehiclesDir, vehicleId)
    
    if (!fs.existsSync(vehicleDir)) {
      fs.mkdirSync(vehicleDir, { recursive: true })
    }
    
    cb(null, vehicleDir)
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = uuidv4()
    const ext = path.extname(file.originalname)
    const prefix = req.body.imageType === 'main' ? 'main_' : 'gallery_'
    cb(null, `${prefix}${uniqueSuffix}${ext}`)
  }
})

const fileFilter = (req, file, cb) => {
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true)
  } else {
    cb(new Error('Tipo de archivo no permitido. Solo imágenes JPG, PNG, WebP o GIF.'), false)
  }
}

const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB máximo
  }
})

// Rutas

// Subir imagen principal
app.post('/api/upload/:vehicleId/main', upload.single('image'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No se ha proporcionado ninguna imagen' })
    }
    
    const vehicleId = req.params.vehicleId
    const imageUrl = `/uploads/vehicles/${vehicleId}/${req.file.filename}`
    
    res.json({
      success: true,
      imageUrl,
      filename: req.file.filename
    })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

// Subir múltiples imágenes a la galería
app.post('/api/upload/:vehicleId/gallery', upload.array('images', 20), (req, res) => {
  try {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ error: 'No se han proporcionado imágenes' })
    }
    
    const vehicleId = req.params.vehicleId
    const images = req.files.map(file => ({
      url: `/uploads/vehicles/${vehicleId}/${file.filename}`,
      filename: file.filename
    }))
    
    res.json({
      success: true,
      images
    })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

// Obtener todas las imágenes de un vehículo
app.get('/api/images/:vehicleId', (req, res) => {
  try {
    const vehicleId = req.params.vehicleId
    const vehicleDir = path.join(vehiclesDir, vehicleId)
    
    if (!fs.existsSync(vehicleDir)) {
      return res.json({ mainImage: null, gallery: [] })
    }
    
    const files = fs.readdirSync(vehicleDir)
    let mainImage = null
    const gallery = []
    
    files.forEach(file => {
      const url = `/uploads/vehicles/${vehicleId}/${file}`
      if (file.startsWith('main_')) {
        mainImage = { url, filename: file }
      } else if (file.startsWith('gallery_')) {
        gallery.push({ url, filename: file })
      }
    })
    
    res.json({ mainImage, gallery })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

// Eliminar una imagen específica
app.delete('/api/images/:vehicleId/:filename', (req, res) => {
  try {
    const { vehicleId, filename } = req.params
    const filePath = path.join(vehiclesDir, vehicleId, filename)
    
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath)
      res.json({ success: true, message: 'Imagen eliminada' })
    } else {
      res.status(404).json({ error: 'Imagen no encontrada' })
    }
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

// Eliminar todas las imágenes de un vehículo
app.delete('/api/images/:vehicleId', (req, res) => {
  try {
    const vehicleId = req.params.vehicleId
    const vehicleDir = path.join(vehiclesDir, vehicleId)
    
    if (fs.existsSync(vehicleDir)) {
      fs.rmSync(vehicleDir, { recursive: true, force: true })
      res.json({ success: true, message: 'Todas las imágenes eliminadas' })
    } else {
      res.json({ success: true, message: 'No había imágenes que eliminar' })
    }
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

// Mover imágenes de temp a ID real
app.post('/api/images/move/:fromId/:toId', (req, res) => {
  try {
    const { fromId, toId } = req.params
    const fromDir = path.join(vehiclesDir, fromId)
    const toDir = path.join(vehiclesDir, toId)
    
    if (fs.existsSync(fromDir)) {
      if (!fs.existsSync(toDir)) {
        fs.mkdirSync(toDir, { recursive: true })
      }
      
      const files = fs.readdirSync(fromDir)
      files.forEach(file => {
        fs.renameSync(
          path.join(fromDir, file),
          path.join(toDir, file)
        )
      })
      
      fs.rmdirSync(fromDir)
      
      // Actualizar URLs
      const movedImages = files.map(file => ({
        oldUrl: `/uploads/vehicles/${fromId}/${file}`,
        newUrl: `/uploads/vehicles/${toId}/${file}`,
        filename: file
      }))
      
      res.json({ success: true, movedImages })
    } else {
      res.json({ success: true, movedImages: [] })
    }
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime(), timestamp: new Date().toISOString() })
})

app.listen(PORT, () => {
  console.log(`🖼️  Servidor de imágenes corriendo en http://localhost:${PORT}`)
  console.log(`📁 Imágenes guardadas en: ${uploadsDir}`)
})
