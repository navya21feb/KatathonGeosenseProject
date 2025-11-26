import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Traffic Insights
export const getTrafficData = async (location) => {
  const response = await api.get('/insights/traffic', {
    params: { lat: location.lat, lon: location.lon }
  })
  return response.data
}

export const getBusiestHours = async (location) => {
  const response = await api.get('/insights/busiest-hours', {
    params: { lat: location.lat, lon: location.lon }
  })
  return response.data
}

// Routes
export const compareRoutes = async (origin, destination) => {
  const response = await api.post('/routing/compare', {
    origin,
    destination
  })
  return response.data
}

// Reports
export const generateReport = async (params) => {
  const response = await api.post('/reports/generate', params)
  return response.data
}

export default api

