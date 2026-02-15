import { createContext, useContext, useState, useEffect } from 'react'

const InventoryContext = createContext(null)

const initialVehicles = [
  {
    id: 1,
    type: 'coche_deportivo',
    brand: 'Ferrari',
    model: '488 GTB',
    year: 2020,
    price: 500,
    priceUnit: 'día',
    status: 'disponible',
    image: 'car',
    specs: { power: '670cv', speed: '330km/h' }
  },
  {
    id: 2,
    type: 'coche_deportivo',
    brand: 'Porsche',
    model: '911 GT3',
    year: 2021,
    price: 450,
    priceUnit: 'día',
    status: 'disponible',
    image: 'flag',
    specs: { power: '510cv', speed: '318km/h' }
  },
  {
    id: 3,
    type: 'remolque',
    brand: 'Brian James',
    model: 'Race Transporter',
    year: 2022,
    price: 150,
    priceUnit: 'día',
    status: 'disponible',
    image: 'truck',
    specs: { capacity: '2500kg', length: '5.5m' },
    platformSpecs: {
      weight: '1200',
      dimensionLength: '5.5',
      dimensionWidth: '2.4',
      dimensionHeight: '1.5',
      axles: '2'
    }
  },
  {
    id: 4,
    type: 'plataforma',
    brand: 'Turbo',
    model: 'Plataforma Estándar',
    year: 2021,
    price: 120,
    priceUnit: 'día',
    status: 'disponible',
    image: 'package',
    specs: {},
    platformSpecs: {
      weight: '1500',
      dimensionLength: '6.0',
      dimensionWidth: '2.5',
      dimensionHeight: '0.8',
      axles: '3'
    }
  },
  {
    id: 5,
    type: 'grua',
    brand: 'Mercedes',
    model: 'Atego 1530',
    year: 2019,
    price: 200,
    priceUnit: 'servicio',
    status: 'disponible',
    image: '🚒',
    specs: { capacity: '3500kg', winch: 'Sí' }
  }
]

export function InventoryProvider({ children }) {
  const [vehicles, setVehicles] = useState(() => {
    const stored = localStorage.getItem('inventory')
    return stored ? JSON.parse(stored) : initialVehicles
  })

  useEffect(() => {
    localStorage.setItem('inventory', JSON.stringify(vehicles))
  }, [vehicles])

  const addVehicle = (vehicle) => {
    const newVehicle = {
      ...vehicle,
      id: Date.now(),
      status: 'disponible'
    }
    setVehicles(prev => [...prev, newVehicle])
    return newVehicle
  }

  const updateVehicle = (id, updates) => {
    setVehicles(prev => prev.map(v => v.id === id ? { ...v, ...updates } : v))
  }

  const deleteVehicle = (id) => {
    setVehicles(prev => prev.filter(v => v.id !== id))
  }

  const getVehicleById = (id) => {
    return vehicles.find(v => v.id === Number(id))
  }

  const getAvailableVehicles = (type) => {
    return vehicles.filter(v => 
      v.status === 'disponible' && 
      (type ? v.type === type : true)
    )
  }

  const value = {
    vehicles,
    addVehicle,
    updateVehicle,
    deleteVehicle,
    getVehicleById,
    getAvailableVehicles
  }

  return <InventoryContext.Provider value={value}>{children}</InventoryContext.Provider>
}

export function useInventory() {
  const context = useContext(InventoryContext)
  if (!context) {
    throw new Error('useInventory must be used within InventoryProvider')
  }
  return context
}
