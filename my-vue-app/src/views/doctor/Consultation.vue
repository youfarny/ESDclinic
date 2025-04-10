<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto p-6">
      <!-- Header with improved styling -->
      <div class="flex justify-between items-center mb-6 bg-white p-4 rounded-lg shadow">
        <div class="flex items-center">
          <div class="bg-blue-500 p-2 rounded-lg mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-gray-800">Consultation</h1>
        </div>  
        <div class="flex items-center">
          <!-- Zoom Button - toggles the video interface -->
          <button @click="toggleZoomInterface" 
                  class="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg mr-3 hover:bg-blue-700 transition-colors duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
            </svg>
            {{ showZoomInterface ? 'Hide Video Call' : 'Start Video Consultation' }}
          </button>
          <div class="bg-blue-100 px-4 py-2 rounded-full text-blue-800 font-medium">
            Appointment #{{ appointmentId }}
          </div>
        </div>
      </div>

      <!-- Loading State with improved animation -->
      <div v-if="isLoading" class="flex flex-col justify-center items-center h-64 bg-white rounded-lg shadow p-8">
        <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 mb-4"></div>
        <p class="text-gray-600 font-medium">Loading patient data...</p>
      </div>

      <!-- Side-by-side layout for Zoom + Patient Info -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <!-- Left Column: Patient Info + AI Recommendations -->
        <div class="space-y-6">
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
            <div class="p-4">
              <div class="grid grid-cols-1 gap-4">
                <div class="bg-gray-50 p-3 rounded-lg">
                  <p class="text-gray-500 text-sm mb-1">Patient ID</p>
                  <p class="font-medium text-gray-800">{{ appointment?.patient_id }}</p>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg">
                  <p class="text-gray-500 text-sm mb-1">Patient Name</p>
                  <p class="font-medium text-gray-800">{{ patient?.patient_name }}</p>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg">
                  <p class="text-gray-500 text-sm mb-1">Symptoms</p>
                  <div class="flex flex-wrap gap-1 mt-1">
                    <span v-for="(symptom, idx) in appointment?.patient_symptoms" :key="idx" 
                          class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                      {{ symptom }}
                    </span>
                    <span v-if="!appointment?.patient_symptoms || appointment?.patient_symptoms.length === 0" 
                          class="text-gray-500">None reported</span>
                  </div>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg">
                  <p class="text-gray-500 text-sm mb-1">Allergies</p>
                  <div v-if="patientAllergies.length" class="flex flex-wrap gap-1 mt-1">
                    <span v-for="(allergy, index) in patientAllergies" :key="index" 
                          class="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs">
                      {{ allergy }}
                    </span>
                  </div>
                  <p v-else class="text-green-600 font-medium">No known allergies</p>
                </div>
              </div>
            </div>
            <!-- Allergy Warning with improved styling -->
            <div v-if="warning" class="mx-4 mb-4 bg-yellow-50 border-l-4 border-yellow-400 p-3 rounded">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-yellow-700 text-sm">{{ warning }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- AI Recommendations with improved styling -->
          <div v-if="appointment?.notes?.length" class="bg-white rounded-lg shadow overflow-hidden">
            <div class="bg-gradient-to-r from-purple-500 to-purple-600 px-4 py-3">
              <h2 class="text-xl font-semibold text-white flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                AI Recommendations
              </h2>
            </div>
            <div class="p-4">
              <div class="space-y-2">
                <div v-for="note in appointment.notes" :key="note.diagnosis" 
                     class="flex justify-between items-center p-2 bg-gray-50 rounded-lg">
                  <span class="font-medium text-gray-800 text-sm">{{ note.diagnosis }}</span>
                  <div class="flex items-center">
                    <div class="w-24 bg-gray-200 rounded-full h-2 mr-2">
                      <div class="bg-purple-600 h-2 rounded-full" :style="`width: ${note.confidence}%`"></div>
                    </div>
                    <span class="text-xs font-medium text-gray-600">{{ note.confidence }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Column: Embedded Zoom Interface -->
        <div v-if="showZoomInterface && zoomMeeting?.join_url" class="h-full">
          <div class="bg-white rounded-lg shadow overflow-hidden h-full flex flex-col">
            <div class="bg-gradient-to-r from-blue-500 to-indigo-600 px-4 py-3 flex justify-between items-center">
              <h2 class="text-xl font-semibold text-white flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                  <line x1="8" y1="21" x2="16" y2="21"></line>
                  <line x1="12" y1="17" x2="12" y2="21"></line>
                </svg>
                Video Consultation
              </h2>
              <button @click="toggleZoomInterface" class="bg-white bg-opacity-20 text-white px-2 py-1 rounded text-sm flex items-center hover:bg-opacity-30">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                Close
              </button>
            </div>
            <div class="flex-grow p-0">
              <!-- Updated Zoom iframe with enhanced permissions -->
              <iframe 
                :src="zoomEmbedUrl" 
                allow="camera; microphone; fullscreen; display-capture; autoplay; clipboard-write; clipboard-read"
                sandbox="allow-forms allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"
                class="w-full h-full border-0"
                style="min-height: 400px;" 
                referrerpolicy="origin"
                frameborder="0">
              </iframe>
              
              <!-- Fallback option for Zoom meetings -->
              <div class="p-2 bg-gray-100 text-sm text-center">
                <p>Having trouble with audio or video?</p>
                <a :href="zoomMeeting?.join_url" target="_blank" class="text-blue-600 hover:underline font-medium">
                  Open in new tab
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              </div>
            </div>
            <!-- Simple meeting info display -->
            <div class="p-3 bg-gray-50 text-sm border-t">
              <div class="flex flex-wrap gap-4">
                <div>
                  <span class="text-gray-600">Meeting ID:</span>
                  <span class="font-mono ml-1">{{ formatZoomId(zoomMeeting?.id) }}</span>
                </div>
                <div>
                  <span class="text-gray-600">Password:</span>
                  <span class="font-mono ml-1">{{ zoomMeeting?.password }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Placeholder for when Zoom is not shown -->
        <div v-if="!showZoomInterface" class="bg-white rounded-lg shadow overflow-hidden flex items-center justify-center p-6">
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-blue-300 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            <h3 class="text-lg font-medium text-gray-700 mb-2">Video Consultation</h3>
            <p class="text-gray-500 mb-4">Click the "Start Video Consultation" button to begin video call with the patient.</p>
            <button @click="toggleZoomInterface" 
                    class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200">
              Start Video Call
            </button>
          </div>
        </div>
      </div>

      <!-- Consultation Form (Full Width Below) -->
      <div class="bg-white rounded-lg shadow overflow-hidden mb-6">
        <div class="bg-gradient-to-r from-green-500 to-green-600 px-4 py-3">
          <h2 class="text-xl font-semibold text-white flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Consultation Details
          </h2>
        </div>
        <div class="p-5">
          <form @submit.prevent="submitConsultation" class="space-y-5">
            <!-- Diagnosis with improved styling -->
            <div>
              <label class="block text-gray-700 font-medium mb-2">
                Diagnosis <span class="text-red-500">*</span>
              </label>
              <textarea v-model="diagnosis" 
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        rows="3"
                        placeholder="Enter your diagnosis"
                        required></textarea>
            </div>

            <!-- Prescription with improved styling -->
            <div>
              <label class="block text-gray-700 font-medium mb-2">
                Prescription (comma-separated) <span class="text-red-500">*</span>
              </label>
              <textarea v-model="prescription" 
                        class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        rows="2"
                        placeholder="e.g., Panadol, Ibuprofen"
                        required></textarea>
              <p class="text-sm text-gray-500 mt-1 italic">Example: Panadol, Ibuprofen</p>
            </div>

            <!-- Submit Button with improved styling -->
            <div class="flex justify-end pt-3">
              <button type="submit" 
                      class="bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-3 rounded-lg hover:from-green-600 hover:to-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Complete Consultation
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Success / Error Popup -->
      <div v-if="popupMessage" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-xl p-6 w-96 text-center max-w-md mx-auto">
          <h2 class="text-xl font-bold mb-4">Status</h2>
          <p class="text-gray-700 mb-6">{{ popupMessage }}</p>
          <button @click="closePopup"
                  class="bg-blue-500 text-white px-5 py-2 rounded-lg hover:bg-blue-600 transition-colors duration-200">
            Close
          </button>
        </div>
      </div>

      <!-- Leave Confirmation Modal -->
      <div v-if="showLeaveModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg shadow-xl w-96 max-w-md mx-auto">
          <div class="text-center mb-4">
            <svg class="mx-auto h-12 w-12 text-yellow-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h2 class="text-xl font-semibold mb-3 text-center">Leave Consultation?</h2>
          <p class="text-gray-600 mb-6 text-center">You haven't finished this consultation yet. Are you sure you want to leave?</p>
          <div class="flex justify-center space-x-4">
            <button @click="confirmLeave" class="px-5 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors duration-200">Leave</button>
            <button @click="cancelLeave" class="px-5 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors duration-200">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { appointmentApi, patientApi, zoomApi } from '@/services/api.js'

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
const consultationFinished = ref(false) // ✅ track if doctor finished
const showLeaveModal = ref(false)
let leaveNext = null // hold the next() function if user confirms

// Zoom integration
const zoomMeeting = ref(null)
const showZoomInterface = ref(false)

// Updated computed property for proper Zoom embedding
const zoomEmbedUrl = computed(() => {
  if (!zoomMeeting.value?.join_url) return '';
  
  // Extract the meeting ID and add necessary parameters
  let meetingId = '';
  if (zoomMeeting.value.id) {
    meetingId = zoomMeeting.value.id;
  } else if (zoomMeeting.value.join_url) {
    // Extract meeting ID from join URL if needed
    const matches = zoomMeeting.value.join_url.match(/\/j\/(\d+)/);
    if (matches && matches[1]) {
      meetingId = matches[1];
    }
  }
  
  // Use web client embedding with full parameters
  return `https://zoom.us/wc/join/${meetingId}?pwd=${zoomMeeting.value.password}&browser=chrome&embedded=true&enableAudioLabelForBrowserConnect=true&zc=true`;
});

const handleBeforeUnload = (event) => {
  if (!consultationFinished.value) {
    event.preventDefault()
    event.returnValue = '' // This triggers browser native confirm
  }
}

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
    
    // Initialize Zoom meeting for demo
    createZoomMeeting()

  } catch (err) {
    error.value = err.message || 'Failed to fetch appointment details'
  } finally {
    isLoading.value = false
  }
}

const toggleZoomInterface = () => {
  if (!zoomMeeting.value && !showZoomInterface.value) {
    createZoomMeeting().then(() => {
      showZoomInterface.value = true
    })
  } else {
    showZoomInterface.value = !showZoomInterface.value
  }
}

const createZoomMeeting = async () => {
  try {
    const meeting = await zoomApi.createZoomMeeting({
      patientName: patient.value?.patient_name || 'Patient',
      id: appointmentId.value,
      appointmentDate: appointment.value?.date || new Date().toISOString()
    })
    
    zoomMeeting.value = meeting
    return meeting
  } catch (error) {
    console.error('Error creating Zoom meeting:', error)
    popupMessage.value = 'Failed to create video call. Please try again.'
  }
}

// Format Zoom ID with spaces for readability
const formatZoomId = (id) => {
  if (!id) return ''
  return id.replace(/(\d{3})(\d{3})(\d{4})/, '$1 $2 $3')
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
      popupMessage.value = `✅ Consultation Complete!\nPrescription ID: ${response.data.prescription_id}`
      consultationFinished.value = true
      
      // Wait a moment and then redirect
      setTimeout(() => {
        router.push('/doctor')
      }, 2000)
    } else {
      popupMessage.value = `❌ Submission failed: ${response.message}`
    }
  } catch (err) {
    popupMessage.value = `❌ Patient is allergic to medication!`
  } finally {
    isLoading.value = false
  }
}

onBeforeRouteLeave((to, from, next) => {
  if (!consultationFinished.value) {
    showLeaveModal.value = true
    leaveNext = next // Save for later use
  } else {
    next()
  }
})

const confirmLeave = () => {
  showLeaveModal.value = false
  consultationFinished.value = true
  if (leaveNext) leaveNext()
}

const cancelLeave = () => {
  showLeaveModal.value = false
  if (leaveNext) leaveNext(false)
}

onMounted(() => {
  fetchAppointment()
  window.addEventListener('beforeunload', handleBeforeUnload)
})

// Clean up when component unmounts
onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
})
</script>