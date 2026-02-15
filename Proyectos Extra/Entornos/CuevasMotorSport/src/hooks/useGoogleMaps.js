import { useEffect, useState } from 'react'

let isLoading = false
let isLoaded = false
const callbacks = []

export function useGoogleMaps() {
  const [loaded, setLoaded] = useState(isLoaded)

  useEffect(() => {
    if (isLoaded) {
      setLoaded(true)
      return
    }

    callbacks.push(() => setLoaded(true))

    if (isLoading) return

    isLoading = true

    const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
    if (!apiKey || apiKey === 'your_google_maps_api_key_here') {
      console.warn('Google Maps API key not configured. Set VITE_GOOGLE_MAPS_API_KEY in .env file.')
      return
    }

    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`
    script.async = true
    script.defer = true
    script.onload = () => {
      isLoaded = true
      isLoading = false
      callbacks.forEach(cb => cb())
    }
    script.onerror = () => {
      console.error('Failed to load Google Maps API')
      isLoading = false
    }
    document.head.appendChild(script)
  }, [])

  return { loaded, google: loaded ? window.google : null }
}
