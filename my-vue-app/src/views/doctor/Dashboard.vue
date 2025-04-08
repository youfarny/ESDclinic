<template>
  <div class="container mx-auto p-4">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Doctor Dashboard</h1>
      <div class="text-gray-600" v-if="user?.doctor">
        Welcome, {{ user.doctor.doctor_name }}
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
      {{ error }}
    </div>

    <!-- Appointments List -->
    <div v-else class="space-y-4">
      <h2 class="text-xl font-semibold mb-4">Today's Appointments</h2>

      <div v-for="appointment in appointments" :key="appointment.appointment_id"
           class="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
        <div class="font-semibold text-lg">Appointment #{{ appointment.appointment_id }}</div>
        <div class="text-gray-600">Patient ID: {{ appointment.patient_id }}</div>
        <div class="text-gray-600">Symptoms: {{ appointment.patient_symptoms.join(', ') }}</div>
        <div class="text-gray-500">Start: {{ formatTime(appointment.start_time) || 'Not started' }}</div>
        <div class="text-gray-500">End: {{ formatTime(appointment.end_time) || 'In progress' }}</div>
        <button
          class="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          @click="startConsultation(appointment.appointment_id)"
        >
          Start Consultation
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { doctorApi, appointmentApi } from '@/services/api.js'

const router = useRouter()
const doctorId = localStorage.getItem('doctorId') || '1'

const user = ref(null)
const appointments = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchDashboardData = async () => {
  try {
    const [doctorData, patientAppointments] = await Promise.all([
      doctorApi.getDoctor(doctorId),
      appointmentApi.getAppointmentsForDoctor(doctorId)
    ])

    user.value = doctorData

    // console.log("Set user to:", user.value)

    appointments.value = patientAppointments.map(app => ({
      ...app,
      patient_symptoms: Array.isArray(app.patient_symptoms)
        ? app.patient_symptoms
        : (app.patient_symptoms ? [app.patient_symptoms] : [])
    }))
  } catch (err) {
    error.value = err.message || 'Something went wrong.'
  } finally {
    isLoading.value = false
  }
}

const formatTime = (timeStr) => {
  if (!timeStr) return null
  return new Date(timeStr).toLocaleString()
}

const startConsultation = (appointmentId) => {
  router.push(`/doctor/consultation/${appointmentId}`)
}

onMounted(fetchDashboardData)
</script>
