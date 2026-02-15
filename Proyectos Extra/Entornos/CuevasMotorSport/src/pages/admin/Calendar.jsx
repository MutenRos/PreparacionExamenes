import { useState } from 'react'
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isToday, startOfWeek, endOfWeek } from 'date-fns'
import { es } from 'date-fns/locale'
import { useBooking } from '../../contexts/BookingContext'
import { useInventory } from '../../contexts/InventoryContext'
import './Calendar.css'

export default function Calendar() {
  const [currentDate, setCurrentDate] = useState(new Date())
  const [selectedDate, setSelectedDate] = useState(null)
  const { getBookingsByDate } = useBooking()
  const { vehicles } = useInventory()

  const monthStart = startOfMonth(currentDate)
  const monthEnd = endOfMonth(currentDate)
  const calendarStart = startOfWeek(monthStart, { weekStartsOn: 1 })
  const calendarEnd = endOfWeek(monthEnd, { weekStartsOn: 1 })
  const days = eachDayOfInterval({ start: calendarStart, end: calendarEnd })

  const dayBookings = selectedDate ? getBookingsByDate(selectedDate) : []

  return (
    <div className="calendar-page">
      <div className="page-header">
        <h1>📅 Agenda Interactiva</h1>
        <p>Gestión de disponibilidad y reservas</p>
      </div>

      <div className="calendar-container">
        <div className="calendar-header">
          <button onClick={() => setCurrentDate(new Date(currentDate.setMonth(currentDate.getMonth() - 1)))}>
            ←
          </button>
          <h2>{format(currentDate, 'MMMM yyyy', { locale: es })}</h2>
          <button onClick={() => setCurrentDate(new Date(currentDate.setMonth(currentDate.getMonth() + 1)))}>
            →
          </button>
        </div>

        <div className="calendar-grid">
          {['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'].map(day => (
            <div key={day} className="calendar-weekday">{day}</div>
          ))}
          
          {days.map(day => {
            const dayBookingsCount = getBookingsByDate(day).length
            return (
              <div
                key={day.toString()}
                className={`calendar-day ${!isSameMonth(day, currentDate) ? 'other-month' : ''} ${isToday(day) ? 'today' : ''} ${selectedDate && format(day, 'yyyy-MM-dd') === format(selectedDate, 'yyyy-MM-dd') ? 'selected' : ''}`}
                onClick={() => setSelectedDate(day)}
              >
                <span className="day-number">{format(day, 'd')}</span>
                {dayBookingsCount > 0 && (
                  <span className="booking-badge">{dayBookingsCount}</span>
                )}
              </div>
            )
          })}
        </div>
      </div>

      {selectedDate && (
        <div className="day-details">
          <h3>📋 Reservas para {format(selectedDate, 'dd/MM/yyyy', { locale: es })}</h3>
          {dayBookings.length > 0 ? (
            <div className="bookings-list">
              {dayBookings.map(booking => {
                const vehicle = vehicles.find(v => v.id === booking.vehicleId)
                return (
                  <div key={booking.id} className="booking-detail-card">
                    <div className="booking-vehicle">
                      <span className="vehicle-icon-small">{vehicle?.image}</span>
                      <div>
                        <strong>{vehicle?.brand} {vehicle?.model}</strong>
                        <p>{booking.service}</p>
                      </div>
                    </div>
                    <div className="booking-customer">
                      <p><strong>{booking.customerName}</strong></p>
                      <p>{booking.customerEmail}</p>
                    </div>
                    <span className={`status-badge ${booking.status}`}>
                      {booking.status}
                    </span>
                  </div>
                )
              })}
            </div>
          ) : (
            <p className="no-bookings">No hay reservas para este día</p>
          )}
        </div>
      )}
    </div>
  )
}
