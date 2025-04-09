<template>
  <div class="container mx-auto p-4">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Consultation</h1>
      <div class="text-gray-600">
        Appointment #{{ appointmentId }}
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
    </div>

    <!-- Error State
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
      {{ error }}
    </div> -->

    <!-- Consultation Form -->
    <div v-else class="space-y-6">
      <!-- Patient Information -->
      <div class="bg-white rounded-lg shadow p-4">
        <h2 class="text-xl font-semibold mb-4">Patient Information</h2>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-gray-600">Patient ID</p>
            <p class="font-medium">#{{ appointment?.patient_id }}</p>
          </div>
          <div>
            <p class="text-gray-600">Symptoms</p>
            <p class="font-medium"> 
              {{ appointment?.patient_symptoms.join(', ') || 'None'  }}
            </p>
          </div>
          <div>
            <p class="text-gray-600">Patient Name</p>
            <p class="font-medium">{{ patient?.patient_name }}</p>
          </div>
          <div>
            <p class="text-gray-600">Allergies</p>
            <ul class="list-disc list-inside text-red-600" v-if="patientAllergies.length">
              <li v-for="(allergy, index) in patientAllergies" :key="index">{{ allergy }}</li>
            </ul>
            <p v-else class="text-gray- 500">No known allergies</p>
            <!-- Allergy Warning -->
            <div v-if="warning" class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative mb-4">
              ⚠️ {{ warning }}
            </div>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-lg shadow p-4">
        <div v-if="appointment?.notes?.length">
          <h2 class="text-xl font-semibold mb-4">AI Recommendations:</h2>
          <ul class="list-disc list-inside text-sm text-gray-700">
            <li v-for="note in appointment.notes" :key="note.diagnosis">
              {{ note.diagnosis }} - Confidence: {{ note.confidence }}%
            </li>
          </ul>
        </div>
      </div>

      <!-- Consultation Form -->
      <div class="bg-white rounded-lg shadow p-4">
        <h2 class="text-xl font-semibold mb-4">Consultation Details</h2>
        <form @submit.prevent="submitConsultation" class="space-y-4">
        <!-- Diagnosis -->
        <div>
          <label class="block text-gray-700 mb-2">Diagnosis <span class="text-red-500">*</span></label>
          <textarea v-model="diagnosis" 
                    class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="3"
                    required></textarea>
        </div>

        <!-- Prescription -->
        <div>
          <label class="block text-gray-700 mb-2">Prescription (comma-separated) <span class="text-red-500">*</span></label>
          <textarea v-model="prescription" 
                    class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="2"
                    required></textarea>
          <p class="text-sm text-gray-500 mt-1">Example: Panadol, Ibuprofen</p>
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

      <!-- Success / Error Popup -->
      <div v-if="popupMessage" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg p-6 w-96 text-center">
          <h2 class="text-xl font-bold mb-4">Status</h2>
          <p class="text-gray-700 mb-6">{{ popupMessage }}</p>
          <button @click="closePopup"
                  class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Close
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { appointmentApi, patientApi } from '@/services/api.js'

const store = useStore()
const route = useRoute()
const router = useRouter()

const appointmentId = computed(() => route.params.appointmentId)
const doctorId = localStorage.getItem('doctorId')
const appointment = ref(null)
const diagnosis = ref('')
const prescription = ref('')
const allergies = ref('')
const patientAllergies = ref([])
const isLoading = ref(false)
const error = ref(null)
const warning = ref(null)
const popupMessage = ref('')
const patient = ref(null)


const closePopup = () => {
  popupMessage.value = ''
  error.value = null // Reset local error state
}


const fetchAppointment = async () => {
  try {
    isLoading.value = true
    error.value = null

    if (!appointmentId.value) {
      throw new Error('Appointment ID not found')
    }

    const response = await appointmentApi.getAppointment(appointmentId.value)
    appointment.value = response

    const allergyResponse = await patientApi.getAllergies(response.patient_id)
    patientAllergies.value = allergyResponse.allergies || []

    const patientData = await patientApi.getPatientInfo(response.patient_id)
    patient.value = patientData

  } catch (err) {
    error.value = err.message || 'Failed to fetch appointment details'
  } finally {
    isLoading.value = false
  }
}

const submitConsultation = async () => {
  try {
    isLoading.value = true
    error.value = null

    const response = await store.dispatch('completeConsultation', {
      appointmentId: appointmentId.value,
      patientId: appointment.value.patient_id,
      diagnosis: diagnosis.value,
      medicine: prescription.value.split(',').map(m => m.trim())
    })

    if (response.code === 200) {
      popupMessage.value = `✅ Appointment submitted successfully!\nPrescription ID: ${response.data.prescription_id}`
      
      // ✅ Wait a moment and then redirect
      setTimeout(() => {
        router.push('/doctor')  // ← make sure this route matches your actual dashboard route
      }, 1500) // Optional delay so user sees the popup
    } else {
      popupMessage.value = `❌ Submission failed: ${response.message}`
    }
  } catch (err) {
    popupMessage.value = `❌ Patient is allergic to medication!`
  } finally {
    isLoading.value = false
  }
}


onMounted(() => {
  fetchAppointment()
})

</script>