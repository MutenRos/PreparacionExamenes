import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Icons } from './Icons'
import './AdminLayout.css'

export default function AdminLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="sidebar-header">
          <div className="admin-logo">
            <img src="/cuevas-logo.png" alt="Cuevas MotorSport" />
            <div>
              <h2>Admin Cuevas</h2>
              <p>{user?.name}</p>
            </div>
          </div>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/admin" end className={({ isActive }) => isActive ? 'active' : ''}>
            <Icons.BarChart size={18} /> Dashboard
          </NavLink>
          <NavLink to="/admin/about" className={({ isActive }) => isActive ? 'active' : ''}>
            <Icons.Info size={18} /> Sobre Nosotros
          </NavLink>
          <NavLink to="/admin/inventory" className={({ isActive }) => isActive ? 'active' : ''}>
            <Icons.Car size={18} /> Inventario
          </NavLink>
          <NavLink to="/admin/calendar" className={({ isActive }) => isActive ? 'active' : ''}>
            <Icons.Calendar size={18} /> Agenda
          </NavLink>
          <NavLink to="/admin/bookings" className={({ isActive }) => isActive ? 'active' : ''}>
            <Icons.ClipboardList size={18} /> Reservas
          </NavLink>
          <NavLink to="/admin/invoices" className={({ isActive }) => isActive ? 'active' : ''}>
            <Icons.Euro size={18} /> Facturas
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <button onClick={handleLogout} className="logout-btn">
            <Icons.LogOut size={18} /> Cerrar Sesión
          </button>
        </div>
      </aside>

      <main className="admin-content">
        <Outlet />
      </main>
    </div>
  )
}
