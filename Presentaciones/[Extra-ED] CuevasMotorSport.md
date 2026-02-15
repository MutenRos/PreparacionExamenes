# Cuevas MotorSport — Web Empresarial con Panel de Administración

![Cuevas MotorSport](public/cuevas-logo.png)

## Introducción

Cuevas MotorSport es una aplicación web completa desarrollada para una empresa real de servicios automotrices que ofrece portes de vehículos, alquiler de coches deportivos y alquiler de plataformas portacoches. La web combina una presencia pública atractiva y optimizada para SEO con un potente panel de administración que permite gestionar inventario, reservas, facturación y documentación profesional en PDF. Construida con React 19, Vite y un servidor Express dedicado para la gestión de imágenes, esta solución demuestra cómo crear un ecosistema frontend-backend completo para un negocio real.

---

## Desarrollo de las partes

### 1. Arquitectura de la Aplicación y Routing

La aplicación utiliza React Router 7 para gestionar la navegación entre las secciones públicas y el panel de administración protegido. Se implementan 5 Context Providers anidados que proporcionan estado global para autenticación, inventario, reservas, facturación y contenido "Sobre nosotros".

```jsx
// App.jsx — Estructura de rutas y context providers
<AuthProvider>
  <AboutProvider>
    <InventoryProvider>
      <BookingProvider>
        <InvoiceProvider>
          <BrowserRouter basename="/CuevasMotorSport">
            <Routes>
              <Route path="/" element={<PublicSite />} />
              <Route path="/vehiculos" element={<Vehicles />} />
              <Route path="/login" element={<Login />} />
              <Route path="/admin" element={
                <ProtectedRoute><AdminLayout /></ProtectedRoute>
              }>
                <Route index element={<Dashboard />} />
                <Route path="inventory" element={<Inventory />} />
                <Route path="calendar" element={<Calendar />} />
                <Route path="bookings" element={<Bookings />} />
                <Route path="invoices" element={<Invoices />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </InvoiceProvider>
      </BookingProvider>
    </InventoryProvider>
  </AboutProvider>
</AuthProvider>
```

La ruta `/admin` está protegida por `ProtectedRoute`, que verifica la autenticación del usuario antes de renderizar. Cada sección admin se renderiza dentro de `AdminLayout` usando `<Outlet />` de React Router.

### 2. Sistema de Gestión de Inventario con Galería de Imágenes

El inventario gestiona vehículos de múltiples tipos (coches deportivos, remolques, plataformas, grúas) con especificaciones técnicas detalladas, incluyendo datos de competición como homologación, jaula de seguridad y cortacorrientes. Un servidor Express dedicado gestiona la subida de imágenes con Multer.

```javascript
// server/index.js — Upload de imágenes con Multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const vehicleId = req.params.vehicleId
    const vehicleDir = path.join(vehiclesDir, vehicleId)
    if (!fs.existsSync(vehicleDir)) {
      fs.mkdirSync(vehicleDir, { recursive: true })
    }
    cb(null, vehicleDir)
  },
  filename: (req, file, cb) => {
    const prefix = req.path.includes('/main') ? 'main_' : 'gallery_'
    const uniqueName = `${prefix}${uuidv4()}${path.extname(file.originalname)}`
    cb(null, uniqueName)
  }
})
```

Cada vehículo puede tener una imagen principal y hasta 20 imágenes de galería. El sistema soporta un ID temporal para vehículos nuevos que se reubica al ID definitivo tras guardar.

```jsx
// InventoryContext.jsx — CRUD de vehículos con persistencia localStorage
const addVehicle = (vehicle) => {
  const newVehicle = {
    ...vehicle,
    id: Date.now(),
    status: 'disponible'
  }
  setVehicles(prev => [...prev, newVehicle])
  return newVehicle
}
```

### 3. Sistema de Reservas con Calendario Interactivo y Detección de Conflictos

El sistema de reservas incluye un calendario visual mensual construido con `date-fns` y un algoritmo de detección de solapamientos que verifica disponibilidad de vehículos en rangos de fechas.

```jsx
// BookingContext.jsx — Verificación de disponibilidad temporal
const isVehicleAvailable = (vehicleId, startDate, endDate) => {
  const vehicleBookings = getBookingsByVehicle(vehicleId).filter(
    b => b.status !== 'cancelada'
  )
  const start = parseISO(startDate)
  const end = parseISO(endDate)

  for (const booking of vehicleBookings) {
    const bookingStart = parseISO(booking.startDate)
    const bookingEnd = parseISO(booking.endDate)
    if (
      (isAfter(start, bookingStart) && isBefore(start, bookingEnd)) ||
      (isAfter(end, bookingStart) && isBefore(end, bookingEnd)) ||
      (isBefore(start, bookingStart) && isAfter(end, bookingEnd)) ||
      isEqual(start, bookingStart) || isEqual(end, bookingEnd)
    ) {
      return false
    }
  }
  return true
}
```

El calendario muestra badges con el número de reservas por día y permite navegar entre meses. Al seleccionar un día, se despliegan las reservas detalladas con vehículo, cliente y estado.

```jsx
// Calendar.jsx — Calendario interactivo con date-fns
const monthStart = startOfMonth(currentDate)
const monthEnd = endOfMonth(currentDate)
const calendarStart = startOfWeek(monthStart, { weekStartsOn: 1 })
const calendarEnd = endOfWeek(monthEnd, { weekStartsOn: 1 })
const days = eachDayOfInterval({ start: calendarStart, end: calendarEnd })
```

### 4. Generación de Documentos PDF con jsPDF

El sistema implementa un flujo documental completo: Solicitud → Confirmación → Albarán de Recogida → Albarán de Entrega → Factura. Cada documento PDF se genera con cabecera corporativa (negro y dorado), datos de empresa, cliente y vehículo, y pie de página estandarizado.

```javascript
// DocumentGenerator.js — Cabecera corporativa PDF
const addHeader = (doc, title, docNumber) => {
  doc.setFillColor(...COLORS.black)
  doc.rect(0, 0, 210, 40, 'F')
  doc.setTextColor(...COLORS.gold)
  doc.setFontSize(24)
  doc.setFont('helvetica', 'bold')
  doc.text(COMPANY_INFO.name, 20, 25)
  doc.setFontSize(12)
  doc.setTextColor(255, 255, 255)
  doc.text(title, 210 - 20, 18, { align: 'right' })
  doc.text(docNumber, 210 - 20, 28, { align: 'right' })
  return 65
}
```

El flujo de documentos está encadenado: cada paso solo se habilita cuando el anterior se ha generado, y ciertos documentos (Confirmación, Albarán de Entrega, Factura) cambian automáticamente el estado de la reserva.

```jsx
// Bookings.jsx — Flujo de documentos encadenado
const DOCUMENT_FLOW = [
  { key: 'solicitud', label: 'Solicitud de Reserva', statusChange: null },
  { key: 'confirmacion', label: 'Confirmación de Reserva', statusChange: 'confirmada' },
  { key: 'albaran_recogida', label: 'Albarán de Recogida', statusChange: 'en_curso' },
  { key: 'albaran_entrega', label: 'Albarán de Entrega', statusChange: null },
  { key: 'factura', label: 'Factura', statusChange: 'completada' }
]
```

### 5. Página Pública de Vehículos con Galería Modal

La página de vehículos muestra solo los coches deportivos disponibles o reservados, con filtros, conteo de resultados y un modal de detalle con galería de imágenes navegable.

```jsx
// Vehicles.jsx — Filtros y galería modal
const publicVehicles = vehicles.filter(v =>
  v.type === 'coche_deportivo' && v.status !== 'vendido'
)

const getAllImages = (vehicle) => {
  const images = []
  if (vehicle.mainImage) images.push(vehicle.mainImage)
  if (vehicle.gallery && vehicle.gallery.length > 0) images.push(...vehicle.gallery)
  return images
}
```

La página incluye su propio header de navegación, hero section con título impactante y una cuadrícula responsive con tarjetas de vehículo que muestran imagen principal, estado, contador de galería, especificaciones técnicas y precio.

### 6. Servicio de Grúa con Reserva Online y Mapas

La sección de servicio de grúa integra un formulario completo con selección de fecha/hora en calendario visual, campos de origen y destino con vista de Google Maps embebida, y cálculo de presupuesto.

```jsx
// CraneService.jsx — Integración de mapas para origen/destino
const [activeMap, setActiveMap] = useState('origin')
const mapQuery = activeMap === 'origin'
  ? (formData.locationOrigin || '').trim() || 'España'
  : (formData.locationDestination || '').trim() || 'España'
const mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(mapQuery)}&output=embed`
```

### 7. SEO, Schema.org y Accesibilidad

La aplicación implementa meta tags completos (Open Graph, Twitter Cards), datos estructurados Schema.org para `LocalBusiness` con catálogo de servicios, sitemap.xml, robots.txt y un manejador SPA 404.html. Se han añadido atributos ARIA para accesibilidad en elementos interactivos clave.

```html
<!-- index.html — Schema.org LocalBusiness -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Cuevas MotorSport",
  "telephone": "+34686531422",
  "openingHoursSpecification": {
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00", "closes": "23:59"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "itemListElement": [...]
  }
}
</script>
```

### 8. Iconografía SVG Personalizada

En lugar de depender de librerías externas como Lucide o FontAwesome, se ha creado un sistema completo de iconos SVG personalizados (475+ líneas) con diseño consistente stroke-based de 24x24 viewBox, soportando tamaños y clases CSS personalizables.

```jsx
// Icons.jsx — Sistema de iconos SVG consistente
Car: ({ className = '', size = 24 }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24"
    fill="none" stroke="currentColor" strokeWidth="2"
    strokeLinecap="round" strokeLinejoin="round">
    <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9..."/>
    <circle cx="7" cy="17" r="2"/>
    <circle cx="17" cy="17" r="2"/>
  </svg>
)
```

---

## Presentación del proyecto

Cuevas MotorSport presenta dos caras perfectamente integradas: una web pública profesional y un panel de administración completo.

**La parte pública** recibe al visitante con un hero impactante que destaca el servicio 24/7 y la experiencia de más de 8 años, seguido de las tres líneas de negocio (portes de vehículos, coches deportivos y plataformas portacoches), una sección "Sobre nosotros" con galería de imágenes del trabajo real y un formulario de contacto con validación. La página de vehículos ofrece un catálogo visual con filtros y galerías modales, y las páginas de servicios individuales (grúa y plataforma) permiten reservar directamente con selección de fecha y mapa interactivo.

**El panel de administración**, accesible vía login protegido, proporciona un dashboard con estadísticas en tiempo real (vehículos, reservas activas, facturas, ingresos estimados). Desde aquí se gestiona todo: el inventario completo de vehículos con galería fotográfica (subida vía servidor Express), una agenda visual tipo calendario, un sistema de reservas con flujo documental completo (solicitud → confirmación → albaranes → factura en PDF) y la facturación con albaranes de entrega.

El diseño visual mantiene una estética premium con paleta negro/dorado corporativa, tipografía Inter/Space Grotesk, scrollbar personalizada y transiciones suaves. Todo funciona como SPA con React Router y persiste datos en localStorage, mientras que las imágenes se gestionan mediante servidor Express con Multer.

---

## Conclusión

Cuevas MotorSport demuestra cómo una solución web moderna puede cubrir todas las necesidades de un negocio de servicios automotrices: desde captar clientes con una presencia web optimizada para SEO hasta gestionar la operativa diaria con reservas, inventario y documentación. La arquitectura React con Context API permite un estado global limpio y predecible, mientras que la generación de PDFs profesionales con jsPDF transforma la gestión administrativa. El proyecto combina tecnologías actuales (React 19, Vite, Express 5) con buenas prácticas de desarrollo web: accesibilidad, responsive design, datos estructurados Schema.org y separación clara entre frontend y backend para la gestión multimedia.
