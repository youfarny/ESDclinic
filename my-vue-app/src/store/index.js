import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    appointments: [],
    consultations: [],
    prescriptions: []
  },
  getters: {
    getUser: state => state.user,
    getAppointments: state => state.appointments,
    getConsultations: state => state.consultations,
    getPrescriptions: state => state.prescriptions
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_APPOINTMENTS(state, appointments) {
      state.appointments = appointments
    },
    SET_CONSULTATIONS(state, consultations) {
      state.consultations = consultations
    },
    SET_PRESCRIPTIONS(state, prescriptions) {
      state.prescriptions = prescriptions
    }
  },
  actions: {
    login({ commit }, { username, password, role }) {
      return new Promise((resolve, reject) => {
        // Here you would make an API call to your backend
        // For demonstration, we're just setting a mock user
        setTimeout(() => {
          const user = {
            id: '123',
            username,
            role
          }
          commit('SET_USER', user)
          localStorage.setItem('userRole', user.role);
          resolve(user)
        }, 1000)
      })
    },
    logout({ commit }) {
      commit('SET_USER', null)
      localStorage.removeItem('user')
    }
  }
})