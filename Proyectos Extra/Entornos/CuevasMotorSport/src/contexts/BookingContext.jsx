import { createContext, useContext, useState, useEffect } from 'react'
import { format, parseISO, isAfter, isBefore, isEqual } from 'date-fns'

const BookingContext = createContext(null)

export function BookingProvider({ children }) {
  const [bookings, setBookings] = useState(() => {
    const stored = localStorage.getItem('bookings')
    return stored ? JSON.parse(stored) : []
  })

  useEffect(() => {
    localStorage.setItem('bookings', JSON.stringify(bookings))
  }, [bookings])

  const createBooking = (bookingData) => {
    const newBooking = {
      ...bookingData,
      id: Date.now(),
      status: 'pendiente',
      createdAt: new Date().toISOString(),
      paymentStatus: 'pendiente'
    }
    setBookings(prev => [...prev, newBooking])
    return newBooking
  }

  const updateBooking = (id, updates) => {
    setBookings(prev => prev.map(b => b.id === id ? { ...b, ...updates } : b))
  }

  const deleteBooking = (id) => {
    setBookings(prev => prev.filter(b => b.id !== id))
  }

  const getBookingsByVehicle = (vehicleId) => {
    return bookings.filter(b => b.vehicleId === vehicleId)
  }

  const getBookingsByDate = (date) => {
    const dateStr = format(new Date(date), 'yyyy-MM-dd')
    return bookings.filter(b => {
      const bookingDate = format(parseISO(b.startDate), 'yyyy-MM-dd')
      return bookingDate === dateStr
    })
  }

  const isVehicleAvailable = (vehicleId, startDate, endDate) => {
    const vehicleBookings = getBookingsByVehicle(vehicleId).filter(
      b => b.status !== 'cancelada'
    )
    
    const start = parseISO(startDate)
    const end = parseISO(endDate)

    for (const booking of vehicleBookings) {
      const bookingStart = parseISO(booking.startDate)
      const bookingEnd = parseISO(booking.endDate)

      // Check if dates overlap
      if (
        (isAfter(start, bookingStart) && isBefore(start, bookingEnd)) ||
        (isAfter(end, bookingStart) && isBefore(end, bookingEnd)) ||
        (isBefore(start, bookingStart) && isAfter(end, bookingEnd)) ||
        isEqual(start, bookingStart) ||
        isEqual(end, bookingEnd)
      ) {
        return false
      }
    }
    return true
  }

  const value = {
    bookings,
    createBooking,
    updateBooking,
    deleteBooking,
    getBookingsByVehicle,
    getBookingsByDate,
    isVehicleAvailable
  }

  return <BookingContext.Provider value={value}>{children}</BookingContext.Provider>
}

export function useBooking() {
  const context = useContext(BookingContext)
  if (!context) {
    throw new Error('useBooking must be used within BookingProvider')
  }
  return context
}
