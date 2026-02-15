# Cuevas MotorSport - Sistema Completo de Gestión

Aplicación web profesional para **Cuevas MotorSport**, con sistema de gestión administrativa, inventario, agenda de reservas, facturación e integración con VeriFactu.

## 🚀 Características Principales

### 🌐 Web Pública
- **Servicio de Grúa 24/7**: Remolques de emergencia con personal profesional
- **Alquiler de Coches Deportivos**: Vehículos de alta performance para experiencias únicas
- **Alquiler de Plataforma Portacoches**: Transporte seguro de vehículos con GPS
- **Formulario de Contacto**: Sistema de consultas directo

### 🔐 Panel de Administración
- **Sistema de Login**: Acceso seguro solo para administradores
  - Usuario: `admin`
  - Contraseña: `admin123`

### 📊 Módulos Administrativos

#### 1. Dashboard
- Resumen general de estadísticas
- Vehículos disponibles/ocupados
- Reservas activas y pendientes
- Ingresos estimados

#### 2. Gestión de Inventario
- CRUD completo de vehículos y remolques
- Estados: Disponible, Ocupado, Mantenimiento
- Especificaciones técnicas
- Precios por día/servicio/hora

#### 3. Agenda Interactiva
- Calendario mensual con reservas
- Vista de disponibilidad diaria
- Marcadores visuales de ocupación
- Gestión de horarios

#### 4. Sistema de Reservas
- Listado completo de reservas
- Estados: Pendiente, Confirmada, Completada, Cancelada
- Información de clientes
- Gestión de fechas y vehículos

#### 5. Generador de Facturas y Albaranes
- Creación de facturas profesionales
- Albaranes de entrega
- Cálculo automático de IVA (21%)
- Datos de cliente completos
- Numeración automática

#### 6. Integración VeriFactu
- Envío de facturas al sistema de la AEAT
- Validación y firma digital
- Códigos de verificación
- Cumplimiento normativo español
- Trazabilidad completa

## 📋 Tecnologías Utilizadas

- **Frontend**: React 18 + Vite
- **Routing**: React Router DOM v6
- **Gestión de Fechas**: date-fns
- **Estado**: Context API
- **Almacenamiento**: LocalStorage
- **Estilos**: CSS Moderno y Responsive

## 🛠️ Instalación y Uso

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build

# Vista previa de producción
npm run preview
```

El servidor estará disponible en `http://localhost:5173`

## 📁 Estructura del Proyecto

```
src/
├── contexts/           # Gestión de estado global
│   ├── AuthContext.jsx         - Autenticación
│   ├── InventoryContext.jsx    - Inventario
│   ├── BookingContext.jsx      - Reservas
│   └── InvoiceContext.jsx      - Facturas
├── pages/
│   ├── Login.jsx              - Login admin
│   └── admin/
│       ├── Dashboard.jsx      - Panel principal
│       ├── Inventory.jsx      - Gestión inventario
│       ├── Calendar.jsx       - Agenda
│       ├── Bookings.jsx       - Reservas
│       ├── Invoices.jsx       - Facturas/Albaranes
│       └── VeriFactu.jsx      - Integración AEAT
├── components/
│   ├── Header.jsx            - Navegación pública
│   ├── Hero.jsx              - Sección principal
│   ├── Services.jsx          - Servicios
│   ├── ServiceCard.jsx       - Tarjeta servicio
│   ├── Contact.jsx           - Formulario contacto
│   ├── Footer.jsx            - Pie de página
│   ├── AdminLayout.jsx       - Layout administración
│   └── ProtectedRoute.jsx    - Rutas protegidas
├── App.jsx                   - Componente principal
└── main.jsx                  - Punto de entrada
```

## 🎨 Diseño

- **Primario**: Rojo (#d32f2f) - Brand color
- **Secundario**: Negro (#1a1a1a) - Fondos oscuros
- **Acento**: Naranja (#ffa500) - Destacados
- **Responsive**: Optimizado para mobile, tablet y desktop

## 🔑 Credenciales de Prueba

**Panel de Administración:**
- Usuario: `admin`
- Contraseña: `admin123`

## 📊 Funcionalidades de Datos

Todos los datos se almacenan en LocalStorage para demo:
- Inventario de vehículos
- Reservas de clientes
- Facturas y albaranes
- Estado de VeriFactu

## 🚀 Próximas Mejoras

- [ ] Backend con Node.js/Express
- [ ] Base de datos (PostgreSQL/MongoDB)
- [ ] Integración real con VeriFactu API
- [ ] Sistema de pagos online (Stripe/PayPal)
- [ ] Notificaciones por email
- [ ] Chat en vivo
- [ ] Aplicación móvil
- [ ] Reportes y estadísticas avanzadas
- [ ] Multi-idioma

## 📞 Información de Contacto

- **Email**: info@cuevasmotorsport.es
- **Teléfono**: +34 XXX XXX XXX
- **Ubicación**: Tu Ciudad, España
- **Disponibilidad**: 24/7

## 📄 Licencia

Todos los derechos reservados © 2025 Cuevas MotorSport
