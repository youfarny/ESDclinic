<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">Appointments</h1>
    
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
      <div v-for="appointment in appointments" :key="appointment.appointment_id" 
           class="bg-white rounded-lg shadow p-4">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="font-medium">Appointment #{{ appointment.appointment_id }}</h3>
            <p class="text-gray-600">Patient ID: {{ appointment.patient_id }}</p>
            <p class="text-gray-600">Symptoms: {{ appointment.patient_symptoms }}</p>
            <p class="text-gray-600">Status: {{ appointment.status || 'Pending' }}</p>
          </div>
          <div class="flex space-x-2">
            <button v-if="!appointment.start_time" 
                    @click="startConsultation(appointment)"
                    class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
              Start Consultation
            </button>
            <button @click="viewAppointmentDetails(appointment)"
                    class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">
              View Details
            </button>
          </div>
        </div>
      </div>

      <!-- No Appointments Message -->
      <div v-if="appointments.length === 0" class="text-center text-gray-500 py-8">
        No appointments found
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const appointments = ref([])
const isLoading = ref(false)
const error = ref(null)

// Fetch appointments
const fetchAppointments = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const doctorId = localStorage.getItem('doctorId')
    if (!doctorId) {
      throw new Error('Doctor ID not found')
    }
    
    const allAppointments = await store.dispatch('fetchAppointments', doctorId)
    appointments.value = allAppointments
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

// Start consultation
const startConsultation = async (appointment) => {
  try {
    await store.dispatch('startConsultation', {
      appointmentId: appointment.appointment_id,
      notes: 'Initial consultation notes',
      startTime: new Date().toISOString()
    })
    router.push(`/doctor/consultation/${appointment.appointment_id}`)
  } catch (err) {
    error.value = err.message
  }
}

// View appointment details
const viewAppointmentDetails = (appointment) => {
  router.push(`/doctor/appointments/${appointment.appointment_id}`)
}

onMounted(() => {
  fetchAppointments()
})
</script> 