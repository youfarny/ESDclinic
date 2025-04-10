<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto p-6 max-w-4xl">
      <!-- Header with back button -->
      <div class="flex justify-between items-center mb-6 bg-white p-4 rounded-lg shadow">
        <div class="flex items-center">
          <div class="bg-blue-500 p-2 rounded-lg mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-gray-800">Past Appointment Details</h1>
        </div>
        <button @click="router.push('/doctor')" class="flex items-center text-blue-600 hover:text-blue-800">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Dashboard
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex flex-col justify-center items-center h-64 bg-white rounded-lg shadow p-8">
        <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 mb-4"></div>
        <p class="text-gray-600 font-medium">Loading record details...</p>
      </div>

      <!-- Content -->
      <div v-else class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Patient Information Card -->
          <div class="bg-white rounded-lg shadow overflow-hidden">
            <div class="bg-gradient-to-r from-blue-500 to-blue-600 px-4 py-3">
              <h2 class="text-xl font-semibold text-white flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Patient Information
              </h2>
            </div>
            <div class="p-5 space-y-4">
              <div class="flex items-center">
                <div class="bg-blue-100 p-2 rounded-full mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Patient ID</p>
                  <p class="font-medium">{{ appointment.patient_id }}</p>
                </div>
              </div>
              
              <div class="flex items-center">
                <div class="bg-blue-100 p-2 rounded-full mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Patient Name</p>
                  <p class="font-medium">{{ patient?.patient_name || 'N/A' }}</p>
                </div>
              </div>
              
              <div>
                <p class="text-sm text-gray-500 mb-2">Symptoms</p>
                <div class="flex flex-wrap gap-2">
                  <span v-for="(symptom, idx) in appointment.patient_symptoms" :key="idx" 
                        class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                    {{ symptom }}
                  </span>
                  <span v-if="!appointment.patient_symptoms || appointment.patient_symptoms.length === 0" 
                        class="text-gray-500">None reported</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Allergies Card -->
          <div class="bg-white rounded-lg shadow overflow-hidden">
            <div class="bg-gradient-to-r from-red-500 to-red-600 px-4 py-3">
              <h2 class="text-xl font-semibold text-white flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Allergies
              </h2>
            </div>
            <div class="p-5">
              <div v-if="patientAllergies.length" class="flex flex-wrap gap-2">
                <span v-for="(a, i) in patientAllergies" :key="i" 
                      class="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">
                  {{ a }}
                </span>
              </div>
              <div v-else class="p-4 bg-green-50 rounded-lg">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div class="ml-3">
                    <p class="text-green-700 font-medium">No known allergies</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Appointment Info Card -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <div class="bg-gradient-to-r from-green-500 to-green-600 px-4 py-3">
            <h2 class="text-xl font-semibold text-white flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Appointment Information
            </h2>
          </div>
          <div class="p-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <div class="flex items-center mb-4">
                  <div class="bg-green-100 p-2 rounded-full mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Start Time</p>
                    <p class="font-medium">{{ formatDateTime(appointment.start_time) }}</p>
                  </div>
                </div>
                
                <div class="flex items-center">
                  <div class="bg-green-100 p-2 rounded-full mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">End Time</p>
                    <p class="font-medium">{{ formatDateTime(appointment.end_time) }}</p>
                  </div>
                </div>
              </div>
              
              <div>
                <div class="flex items-center mb-4">
                  <div class="bg-green-100 p-2 rounded-full mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Diagnosis</p>
                    <p class="font-medium">{{ appointment.diagnosis || 'N/A' }}</p>
                  </div>
                </div>
                
                <div class="flex items-center">
                  <div class="bg-green-100 p-2 rounded-full mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Prescription ID: {{ appointment.prescription_id }}</p>
                    <p class="font-medium">{{ Array.isArray(prescription) ? prescription.join(', ') : prescription || 'None' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI Notes -->
        <div v-if="appointment.notes?.length" class="bg-white rounded-lg shadow overflow-hidden">
          <div class="bg-gradient-to-r from-purple-500 to-purple-600 px-4 py-3">
            <h2 class="text-xl font-semibold text-white flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              AI Recommendations
            </h2>
          </div>
          <div class="p-5">
            <div class="space-y-3">
              <div v-for="(note, index) in appointment.notes" :key="index" 
                   class="p-3 border-l-4 border-purple-500 bg-purple-50 rounded-r">
                <div class="flex justify-between items-start">
                  <p class="text-purple-800 font-medium">{{ note.diagnosis }}</p>
                  <span class="px-2 py-1 bg-purple-200 text-purple-800 rounded-lg text-xs font-medium">
                    {{ note.confidence }}% confidence
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { appointmentApi, patientApi } from '@/services/api'

const route = useRoute()
const router = useRouter()
const appointmentId = route.params.appointmentId

const appointment = ref({})
const patient = ref(null)
const patientAllergies = ref([])
const prescription = ref(null)
const isLoading = ref(true)

const formatDateTime = (iso) => {
  if (!iso) return 'N/A'
  return new Date(iso).toLocaleString('en-SG', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit', hour12: true
  })
}

onMounted(async () => {
  try {
    const data = await appointmentApi.getAppointment(appointmentId)
    appointment.value = data

    const patientInfo = await patientApi.getPatientInfo(data.patient_id)
    patient.value = patientInfo

    const allergyRes = await patientApi.getAllergies(data.patient_id)
    patientAllergies.value = allergyRes.allergies || []

    if (data.prescription_id) {
      const prescriptionData = await patientApi.getPrescriptionDetails(data.prescription_id)
      prescription.value = prescriptionData.prescription?.medicine || []
    }

  } catch (err) {
    console.error('Failed to load past record:', err)
  } finally {
    isLoading.value = false
  }
})
</script>