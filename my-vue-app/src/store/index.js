import { createStore } from 'vuex'
import { doctorApi, appointmentApi } from '../services/api'

export default createStore({
  state: {
    user: null,
    appointments: [],
    currentAppointment: null,
    loading: false,
    error: null
  },
  getters: {
    getUser: state => state.user,
    getAppointments: state => state.appointments,
    getCurrentAppointment: state => state.currentAppointment,
    isLoading: state => state.loading,
    getError: state => state.error
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_APPOINTMENTS(state, appointments) {
      state.appointments = appointments
    },
    SET_CURRENT_APPOINTMENT(state, appointment) {
      state.currentAppointment = appointment
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    // Doctor actions
    async fetchDoctor({ commit }, doctorId) {
      try {
        commit('SET_LOADING', true)
        const response = await doctorApi.getDoctor(doctorId)
        commit('SET_USER', response.doctor)
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    // Appointment actions
    async fetchAppointments({ commit }, patientId) {
      try {
        commit('SET_LOADING', true)
        const response = await appointmentApi.getPatientAppointments(patientId)
        commit('SET_APPOINTMENTS', response)
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async createAppointment({ commit }, appointmentData) {
      try {
        commit('SET_LOADING', true)
        const response = await appointmentApi.createAppointment(appointmentData)
        return response
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async startConsultation({ commit }, { appointmentId, notes, startTime }) {
      try {
        commit('SET_LOADING', true)
        const response = await appointmentApi.startAppointment(appointmentId, notes, startTime)
        const appointment = await appointmentApi.getAppointment(appointmentId)
        commit('SET_CURRENT_APPOINTMENT', appointment)
        return response
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async completeConsultation({ commit }, { appointmentId, endTime, diagnosis, prescriptionId }) {
      try {
        commit('SET_LOADING', true)
        const response = await appointmentApi.endAppointment(appointmentId, endTime, diagnosis, prescriptionId)
        commit('SET_CURRENT_APPOINTMENT', null)
        return response
      } catch (error) {
        commit('SET_ERROR', error.message)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },

    logout({ commit }) {
      commit('SET_USER', null)
      commit('SET_APPOINTMENTS', [])
      commit('SET_CURRENT_APPOINTMENT', null)
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')
    }
  }
}) 