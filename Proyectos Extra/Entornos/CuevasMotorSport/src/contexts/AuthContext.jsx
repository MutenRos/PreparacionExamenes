import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

function getInitialUser() {
  try {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      const parsed = JSON.parse(storedUser)
      // Validate stored user structure
      if (parsed && parsed.id && parsed.username && parsed.role) {
        return parsed
      }
      localStorage.removeItem('user')
    }
  } catch {
    localStorage.removeItem('user')
  }
  return null
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getInitialUser)
  const loading = false

  const login = (username, password) => {
    // Credenciales de administrador
    if (username === 'info@cuevasmotorsport.com' && password === 'admin123') {
      const userData = {
        id: 1,
        username: 'info@cuevasmotorsport.com',
        role: 'admin',
        name: 'Administrador'
      }
      setUser(userData)
      localStorage.setItem('user', JSON.stringify(userData))
      return { success: true }
    }
    return { success: false, error: 'Credenciales incorrectas' }
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('user')
  }

  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'admin'
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
