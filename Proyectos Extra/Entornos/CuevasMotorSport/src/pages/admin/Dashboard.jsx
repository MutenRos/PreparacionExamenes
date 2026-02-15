import { useInventory } from '../../contexts/InventoryContext'
import { useBooking } from '../../contexts/BookingContext'
import { useInvoice } from '../../contexts/InvoiceContext'
import { Icons } from '../../components/Icons'
import './Dashboard.css'

export default function Dashboard() {
  const { vehicles } = useInventory()
  const { bookings } = useBooking()
  const { invoices } = useInvoice()

  const stats = {
    totalVehicles: vehicles.length,
    availableVehicles: vehicles.filter(v => v.status === 'disponible').length,
    activeBookings: bookings.filter(b => b.status === 'confirmada').length,
    pendingBookings: bookings.filter(b => b.status === 'pendiente').length,
    totalInvoices: invoices.length,
    pendingInvoices: invoices.filter(i => i.status === 'pendiente').length
  }

  const recentBookings = bookings.slice(-5).reverse()

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1><Icons.BarChart size={28} /> Dashboard</h1>
        <p>Resumen general de Cuevas MotorSport</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon"><Icons.Car size={28} /></div>
          <div className="stat-info">
            <h3>{stats.totalVehicles}</h3>
            <p>Vehículos Totales</p>
            <small>{stats.availableVehicles} disponibles</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon"><Icons.ClipboardList size={28} /></div>
          <div className="stat-info">
            <h3>{stats.activeBookings}</h3>
            <p>Reservas Activas</p>
            <small>{stats.pendingBookings} pendientes</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon"><Icons.Euro size={28} /></div>
          <div className="stat-info">
            <h3>{stats.totalInvoices}</h3>
            <p>Facturas</p>
            <small>{stats.pendingInvoices} pendientes</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon"><Icons.BarChart size={28} /></div>
          <div className="stat-info">
            <h3>€{(stats.activeBookings * 350).toFixed(0)}</h3>
            <p>Ingresos Est.</p>
            <small>Este mes</small>
          </div>
        </div>
      </div>

      <div className="dashboard-section">
        <h2><Icons.Calendar size={22} /> Últimas Reservas</h2>
        {recentBookings.length > 0 ? (
          <div className="recent-bookings">
            {recentBookings.map(booking => (
              <div key={booking.id} className="booking-item">
                <div className="booking-info">
                  <strong>{booking.customerName}</strong>
                  <p>{booking.service}</p>
                </div>
                <div className="booking-status">
                  <span className={`status-badge ${booking.status}`}>
                    {booking.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-data">No hay reservas recientes</p>
        )}
      </div>

      <div className="dashboard-section">
        <h2><Icons.Car size={22} /> Estado del Inventario</h2>
        <div className="inventory-overview">
          {vehicles.map(vehicle => (
            <div key={vehicle.id} className="vehicle-mini-card">
              <span className="vehicle-icon">{vehicle.image}</span>
              <div className="vehicle-mini-info">
                <strong>{vehicle.brand} {vehicle.model}</strong>
                <span className={`mini-status ${vehicle.status}`}>
                  {vehicle.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
