import axios from 'axios'

const processApiInstance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auth + error handling interceptors
processApiInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

processApiInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error.response?.data || error)
  }
)

export const processApi = {
  startAppointment: async (doctorId) => {
    try {
      const response = await processApiInstance.post('/process/start', {
        apikey: 'admin',
        doctor_id: doctorId,
      })
      return response.data
    } catch (error) {
      console.error('Error starting appointment process:', error)
      throw error
    }
  },

  submitAppointment: async (data) => {
    try {
      const response = await processApiInstance.post('/process/end', {
        apikey: 'admin',
        ...data
      })
      return response.data
    } catch (error) {
      console.error('Error submitting appointment:', error)
      throw error
    }
  },

  endAppointment: async (data) => {
    try {
      const response = await processApiInstance.post('/process/end', {
        apikey: 'admin',
        ...data
      })
      return response.data
    } catch (error) {
      console.error('Error ending appointment:', error)
      throw error
    }
  }
  
}   