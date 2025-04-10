import axios from 'axios'

const appointmentApiInstance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auth + error handling interceptors
appointmentApiInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

appointmentApiInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error.response?.data || error)
  }
)

export const appointmentApi = {
  getAppointment: async (appointmentId) => {
    const response = await appointmentApiInstance.get(`/appointment/${appointmentId}?apikey=admin`)
    return response.data
  },

  getPatientAppointments: async (patientId) => {
    const response = await appointmentApiInstance.get(`/appointment/records/${patientId}?apikey=admin`)
    return response.data
  },
  
  getAppointmentsForDoctor: async (doctorId) => {
    const response = await appointmentApiInstance.get(`/appointment/doctor/${doctorId}?apikey=admin`)
    return response.data
  },

  getDoctorQueueAppointments: async (doctorId) => {
    const response = await appointmentApiInstance.get(`/queue/doctor/${doctorId}?apikey=admin`)
    return response.data
  },

  markPaymentSuccess: async (appointmentId, paymentId) => {
    const response = await appointmentApiInstance.patch('/appointment/payment?apikey=admin', {
      appointment_id: appointmentId,
      payment_id: paymentId,
    })
    return response.data
  }
  
}
