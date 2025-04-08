import axios from 'axios'

const doctorApiInstance = axios.create({
  baseURL: 'http://localhost:5101',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auth + error handling interceptors
doctorApiInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

doctorApiInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error.response?.data || error)
  }
)

export const doctorApi = {
  getDoctor: async (doctorId) => {
    const response = await doctorApiInstance.get(`/doctor/${doctorId}`)
    return response.data
  },

  getDoctorName: async (doctorName) => {
    const response = await doctorApiInstance.get(`/doctor/${doctorName}`)
    return response.data
  },

  getAllDoctors: async () => {
    const response = await doctorApiInstance.get('/doctors')
    return response.data
  },

  updateDoctor: async (doctorId, data) => {
    const response = await doctorApiInstance.put(`/doctor/${doctorId}`, data)
    return response.data
  },

  deleteDoctor: async (doctorId) => {
    const response = await doctorApiInstance.delete(`/doctor/${doctorId}`)
    return response.data
  },
}
