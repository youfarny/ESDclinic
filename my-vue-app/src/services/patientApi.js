import axios from 'axios'

const patientApiInstance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auth + error handling interceptors
patientApiInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

patientApiInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error.response?.data || error)
  }
)

export const patientApi = {
  getAllergies: async (patientId) => {
    const response = await patientApiInstance.get(`/patient/allergies/${patientId}?apikey=admin`)
    return response.data
  },

  getPatientInfo: async (patientId) => {
    const response = await patientApiInstance.get(`/patient/${patientId}?apikey=admin`)
    return response.data
  },

  getPrescriptionDetails: async (prescriptionId) => {
    const response = await patientApiInstance.get(`/prescription/${prescriptionId}?apikey=admin`)
    return response.data
  }
}
