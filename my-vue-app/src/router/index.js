import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import DoctorDashboard from '../views/doctor/Dashboard.vue'
import DoctorAppointments from '../components/AppointmentCard.vue'
import DoctorConsultation from '../views/doctor/Consultation.vue'
import DoctorRecords from '../views/doctor/Records.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/doctor',
    name: 'DoctorDashboard',
    component: DoctorDashboard,
    meta: { requiresAuth: true, role: 'doctor' }
  },
  {
    path: '/doctor/appointments',
    name: 'DoctorAppointments',
    component: DoctorAppointments,
    meta: { requiresAuth: true, role: 'doctor' }
  },
  {
    path: '/doctor/consultation/:appointmentId',
    name: 'DoctorConsultation',
    component: DoctorConsultation,
    meta: { requiresAuth: true, role: 'doctor' }
  },
  {
    path: '/doctor/records',
    name: 'DoctorRecords',
    component: DoctorRecords,
    meta: { requiresAuth: true, role: 'doctor' }
  },
  {
    path: '/doctor/records/:appointmentId',
    name: 'PastRecordDetails',
    component: () => import('@/views/doctor/PastRecordDetails.vue'),
    meta: { requiresAuth: true, role: 'doctor' }

  }
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const userRole = localStorage.getItem('userRole')
  
  if (requiresAuth && !userRole) {
    next('/')
  } else if (requiresAuth && to.meta.role !== userRole) {
    next(`/${userRole}`)
  } else {
    next()
  }
})

export default router 