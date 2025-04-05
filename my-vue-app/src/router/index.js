import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import PatientDashboard from '../views/patient/PatientDashboard.vue'
import BookAppointment from '../views/patient/BookAppointment.vue'
import MyAppointments from '../views/patient/MyAppointments.vue'
import MedicalRecords from '../views/patient/MedicalRecords.vue'
import DoctorDashboard from '../views/doctor/DoctorDashboard.vue'
import DoctorConsultation from '../views/doctor/Consultation.vue'
import PendingAppointments from '../views/doctor/PendingAppointments.vue'
import ConsultationRecords from '../views/doctor/ConsultationRecords.vue'


const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  // Patient routes
  
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

  // Doctor routes
  {
    path: '/doctor',
    name: 'DoctorDashboard',
    component: DoctorDashboard,
    meta: { requiresAuth: true, role: 'doctor' }
  },
  {
    path: '/doctor/consultation',
    name: 'DoctorConsultation',
    component: DoctorConsultation,
    meta: { requiresAuth: true, role: 'doctor' }
  },
  {
    path: '/doctor/pending-appointments',
    name: 'PendingAppointments',
    component: PendingAppointments
  },
  {
    path: '/doctor/consultation-records',
    name: 'ConsultationRecords',
    component: ConsultationRecords,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard to protect routes
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const userRole = localStorage.getItem('userRole')
  
  if (requiresAuth && !userRole) {
    next('/')
  } else if (requiresAuth && to.meta.role !== userRole) {
    // Redirect to the appropriate dashboard based on role
    next(`/${userRole}`)
  } else {
    next()
  }
})

export default router