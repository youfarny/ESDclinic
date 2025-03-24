import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import PatientDashboard from '../views/patient/Dashboard.vue'
import DoctorDashboard from '../views/doctor/Dashboard.vue'
import PharmacistDashboard from '../views/pharmacist/PharmacistDashboard.vue'
import BookAppointment from '../views/patient/BookAppointment.vue'
import DoctorConsultation from '../views/doctor/Consultation.vue'
import PharmacistInventory from '../views/pharmacist/Inventory.vue'
import PharmacistAbout from '../views/pharmacist/About.vue'
import ProcessPrescription from '../views/pharmacist/ProcessPrescription.vue'
import MyAppointments from '../views/patient/MyAppointments.vue'
import MedicalRecords from '../views/patient/MedicalRecords.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  // Patient routes
  {
    path: '/patient',
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
  // Pharmacist routes
  {
    path: '/pharmacist',
    name: 'PharmacistDashboard',
    component: PharmacistDashboard,
    meta: { requiresAuth: true, role: 'pharmacist' }
  },
  {
    path: '/pharmacist/about',
    name: 'PharmacistAbout',
    component: PharmacistAbout,
    meta: { requiresAuth: true, role: 'pharmacist' }
  },
  {
    path: '/pharmacist/inventory',
    name: 'PharmacistInventory',
    component: PharmacistInventory,
    meta: { requiresAuth: true, role: 'pharmacist' }
  },
  {
    path: '/pharmacist/process',
    name: 'ProcessPrescription',
    component: ProcessPrescription,
    meta: { requiresAuth: true, role: 'pharmacist' }
  }
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