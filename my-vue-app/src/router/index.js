import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import DoctorDashboard from '../views/doctor/Dashboard.vue'
import DoctorAppointments from '../views/doctor/Appointments.vue'
import DoctorConsultation from '../views/doctor/Consultation.vue'
import DoctorRecords from '../views/doctor/Records.vue'

import PatientDashboard from '../views/patient/PatientDashboard.vue'
import BookAppointment from '../views/patient/BookAppointment.vue'
import MyAppointments from '../views/patient/MyAppointments.vue'
import MedicalRecords from '../views/patient/MedicalRecords.vue'

// Define your routes
const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  // patient routes
  { path: '/patient', component: PatientDashboard },
  {
    path: '/patient/dashboard',
    name: 'PatientDashboard',
    component: PatientDashboard,
    meta: { requiresAuth: true, role: 'patient' }
  },
  {
    path: '/patient/book-appointment',
    name: 'BookAppointment',
    component: BookAppointment,
    meta: { requiresAuth: true, role: 'patient' }
  },
  {
    path: '/patient/appointments',
    name: 'MyAppointments',
    component: MyAppointments,
    meta: { requiresAuth: true, role: 'patient' }
  },
  {
    path: '/patient/medical-records',
    name: 'MedicalRecords',
    component: MedicalRecords,
    meta: { requiresAuth: true, role: 'patient' }
  },
  {
    path: '/patient/payment-success',
    name: 'PaymentSuccess',
    component: () => import('../views/patient/PaymentSuccess.vue')
  },

  // doctor routes
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
  }
]

// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const userRole = localStorage.getItem('userRole')
  
  // If the route requires authentication but no userRole exists in localStorage, redirect to login
  if (requiresAuth && !userRole) {
    next('/')
  } else if (requiresAuth && to.meta.role !== userRole) {
    // If the role doesn't match, redirect to the dashboard of the logged-in user
    next(`/${userRole}`)
  } else {
    // Allow the navigation
    next()
  }
})

export default router
