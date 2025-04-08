import axios from 'axios'

const appointmentApiInstance = axios.create({
  baseURL: 'http://localhost:5100',
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
    const response = await appointmentApiInstance.get(`/appointment/${appointmentId}`)
    return response.data
  },

  getPatientAppointments: async (patientId) => {
    const response = await appointmentApiInstance.get(`/appointment/records/${patientId}`)
    return response.data
  },

  getAppointmentsForDoctor: async (doctorId) => {
    const response = await appointmentApiInstance.get(`/appointment/doctor/${doctorId}`)
    return response.data
  },

  createAppointment: async (appointmentData) => {
    const response = await appointmentApiInstance.post('/appointment/new', appointmentData)
    return response.data
  },

  startAppointment: async (appointmentId, notes, startTime) => {
    const response = await appointmentApiInstance.patch('/appointment/appointment_start', {
      appointment_id: appointmentId,
      notes,
      startTime,
    })
    return response.data
  },

  endAppointment: async (appointmentId, endTime, diagnosis, prescriptionId) => {
    const response = await appointmentApiInstance.patch('/appointment/appointment_end', {
      appointment_id: appointmentId,
      end_time: endTime,
      diagnosis,
      prescription_id: prescriptionId,
    })
    return response.data
  },

  markPaymentSuccess: async (appointmentId, paymentId) => {
    const response = await appointmentApiInstance.patch('/appointment/payment', {
      appointment_id: appointmentId,
      payment_id: paymentId,
    })
    return response.data
  },
}
