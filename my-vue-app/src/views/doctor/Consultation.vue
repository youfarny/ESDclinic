<template>
  <div class="container mx-auto p-4">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Consultation</h1>
      <div class="text-gray-600">
        Appointment #{{ appointment?.appointment_id }}
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

    <!-- Consultation Form -->
    <div v-else class="space-y-6">
      <!-- Patient Information -->
      <div class="bg-white rounded-lg shadow p-4">
        <h2 class="text-xl font-semibold mb-4">Patient Information</h2>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-gray-600">Patient ID</p>
            <p class="font-medium">{{ appointment?.patient_id }}</p>
          </div>
          <div>
            <p class="text-gray-600">Symptoms</p>
            <p class="font-medium">{{ appointment?.patient_symptoms }}</p>
          </div>
        </div>
      </div>

      <!-- Consultation Form -->
      <div class="bg-white rounded-lg shadow p-4">
        <h2 class="text-xl font-semibold mb-4">Consultation Details</h2>
        <form @submit.prevent="submitConsultation" class="space-y-4">
          <!-- Diagnosis -->
          <div>
            <label class="block text-gray-700 mb-2">Diagnosis</label>
            <textarea v-model="diagnosis" 
                      class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows="4"
                      required></textarea>
          </div>

          <!-- Prescription -->
          <div>
            <label class="block text-gray-700 mb-2">Prescription</label>
            <textarea v-model="prescription" 
                      class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows="4"
                      required></textarea>
          </div>

          <!-- Allergies -->
          <div>
            <label class="block text-gray-700 mb-2">Allergies</label>
            <textarea v-model="allergies" 
                      class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows="2"></textarea>
          </div>

          <!-- Submit Button -->
          <div class="flex justify-end">
            <button type="submit" 
                    class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
              Complete Consultation
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { processApi } from '@/services/api.js'


const store = useStore()
const route = useRoute()
const router = useRouter()

const doctorId = localStorage.getItem('doctor_id')
const appointment = ref(null)
const diagnosis = ref('')
const prescription = ref('')
const allergies = ref('')
const isLoading = ref(false)
const error = ref(null)

const handleStartAppointment = async () => {
  try {
    isStarting.value = true
    error.value = null
    const response = await processApi.startAppointment(doctorId)
    appointment.value = response
  } catch (err) {
    error.value = err.message || 'Failed to start appointment'
    console.error('Start error:', err)
  } finally {
    isStarting.value = false
  }
}

// Fetch appointment details
const fetchAppointment = async () => {
  try {
    isLoading.value = true
    error.value = null
    const appointmentId = route.params.appointmentId
    const response = await store.dispatch('fetchAppointment', appointmentId)
    appointment.value = response
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

// Submit consultation
const submitConsultation = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    await store.dispatch('completeConsultation', {
      appointmentId: appointment.value.appointment_id,
      endTime: new Date().toISOString(),
      diagnosis: diagnosis.value,
      prescriptionId: 1 // This should be replaced with actual prescription ID from prescription service
    })
    
    router.push('/doctor')
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchAppointment()
})
</script> 