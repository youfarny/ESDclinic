<template>
  <div class="min-h-screen bg-gray-50">
    <div class="container mx-auto p-6">
      <!-- Dashboard Header -->
      <div class="flex justify-between items-center mb-6 bg-white p-4 rounded-lg shadow">
        <div class="flex items-center">
          <div class="bg-blue-500 p-2 rounded-lg mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-800">Doctor Dashboard</h1>
            <p class="text-gray-600" v-if="user?.doctor">Dr. {{ user.doctor.doctor_name }}</p>
          </div>
        </div>
        <div class="hidden md:block">
          <div class="bg-blue-100 px-4 py-2 rounded-full text-blue-800 font-medium">
            {{ new Date().toLocaleString('en-SG', { 
              weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
            }) }}
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex flex-col justify-center items-center h-64 bg-white rounded-lg shadow p-8">
        <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 mb-4"></div>
        <p class="text-gray-600 font-medium">Loading appointment data...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="bg-white rounded-lg shadow overflow-hidden mb-6">
        <div class="bg-red-500 px-4 py-2">
          <h2 class="text-white font-medium">Error</h2>
        </div>
        <div class="p-4 bg-red-50 border-l-4 border-red-500">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-red-700">{{ error }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Section -->
      <div v-else>
        <!-- Tabs -->
        <div class="bg-white rounded-lg shadow mb-6">
          <div class="flex overflow-x-auto">
            <button
              class="px-6 py-3 flex items-center font-medium text-sm border-b-2 transition-colors duration-200"
              :class="activeTab === 'appointments' 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              @click="activeTab = 'appointments'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Today's Appointments
              <span v-if="sortedTodayAppointments.length > 0" class="ml-2 bg-blue-100 text-blue-800 rounded-full px-2.5 py-0.5 text-xs font-medium">
                {{ sortedTodayAppointments.length }}
              </span>
            </button>

            <button
              class="px-6 py-3 flex items-center font-medium text-sm border-b-2 transition-colors duration-200"
              :class="activeTab === 'records' 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              @click="activeTab = 'records'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Past Records
              <span v-if="pastAppointments.length > 0" class="ml-2 bg-gray-100 text-gray-800 rounded-full px-2.5 py-0.5 text-xs font-medium">
                {{ pastAppointments.length }}
              </span>
            </button>
          </div>
        </div>

        <!-- Appointments Tab -->
        <div v-if="activeTab === 'appointments'">
          <div v-if="sortedTodayAppointments.length === 0" class="bg-white rounded-lg shadow p-8 text-center">
            <svg class="h-16 w-16 text-gray-300 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <h3 class="text-lg font-medium text-gray-600 mb-1">No appointments for today</h3>
            <p class="text-gray-500">Your schedule is clear for the day.</p>
          </div>
          
          <div v-else class="space-y-4">
            <AppointmentCard
              v-for="(appointment, index) in sortedTodayAppointments"
              :key="appointment.appointment_id"
              :appointment="appointment"
              :isFirst="index === 0"
              :showTiming="false"
              @start-consultation="handleStartConsultation"
            />
          </div>
        </div>

        <!-- Past Records Tab -->
        <div v-else-if="activeTab === 'records'">
          <div v-if="pastAppointments.length === 0" class="bg-white rounded-lg shadow p-8 text-center">
            <svg class="h-16 w-16 text-gray-300 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 class="text-lg font-medium text-gray-600 mb-1">No past records found</h3>
            <p class="text-gray-500">Previous consultation records will appear here.</p>
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="a in pastAppointments"
              :key="a.appointment_id"
              class="bg-white rounded-lg shadow overflow-hidden hover:shadow-md transition-shadow duration-200 cursor-pointer"
              @click="viewPastRecord(a.appointment_id)"
            >
              <div class="bg-gradient-to-r from-green-500 to-green-600 px-4 py-2">
                <h3 class="font-medium text-white">Appointment ID: #{{ a.appointment_id }}</h3>
              </div>
              <div class="p-4">
                <div class="flex justify-between items-start mb-3">
                  <div>
                    <p class="text-gray-600 text-sm">Patient ID</p>
                    <p class="font-medium">#{{ a.patient_id }}</p>
                  </div>
                  <div class="bg-green-100 text-green-800 text-xs rounded-full px-3 py-1 font-medium">
                    Completed
                  </div>
                </div>
                
                <div class="space-y-2">
                  <div class="flex items-start">
                    <svg class="h-5 w-5 text-gray-400 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span class="text-gray-700">{{ formatDateTime(a.start_time) }}</span>
                  </div>
                  
                  <div class="flex items-start">
                    <svg class="h-5 w-5 text-gray-400 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span class="text-gray-700">{{ formatDateTime(a.end_time) }}</span>
                  </div>
                  
                  <div class="flex items-start">
                    <svg class="h-5 w-5 text-gray-400 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span class="text-gray-700 truncate">
                      Symptoms: {{ Array.isArray(a.patient_symptoms) ? a.patient_symptoms.join(', ') : a.patient_symptoms || 'None' }}
                    </span>
                  </div>
                </div>
                
                <div class="mt-4 flex justify-end">
                  <span class="text-blue-600 font-medium text-sm flex items-center">
                    View Details
                    <svg class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppointmentCard from '@/components/AppointmentCard.vue'
import { appointmentApi, doctorApi, processApi } from '@/services/api.js'

const router = useRouter()
const doctorId = localStorage.getItem('doctorId') || '1'

const user = ref(null)
const todayAppointments = ref([])
const pastAppointments = ref([])
const isLoading = ref(true)
const error = ref(null)

const diagnosis = ref('')
const prescription = ref('')
const allergies = ref('')

const activeTab = ref('appointments')

const viewPastRecord = (appointmentId) => {
  router.push(`/doctor/records/${appointmentId}`)
}

// Sort today's appointments by queue number
const sortedTodayAppointments = computed(() => {
  return [...todayAppointments.value].sort((a, b) => {
    const queueA = a.queue_number || Number.MAX_SAFE_INTEGER
    const queueB = b.queue_number || Number.MAX_SAFE_INTEGER
    return queueA - queueB
  })
})

// Check if appointment is the first in queue
const isFirstInQueue = (appointment) => {
  const firstAppointment = sortedTodayAppointments.value[0]
  return firstAppointment && firstAppointment.appointment_id === appointment.appointment_id
}

const normalizeSymptoms = (list) =>
  list.map(app => ({
    ...app,
    patient_symptoms: Array.isArray(app.patient_symptoms)
      ? app.patient_symptoms
      : (app.patient_symptoms ? [app.patient_symptoms] : [])
  }))

const fetchAppointments = async () => {
  try {
    const [doctorData, allAppointments] = await Promise.all([
      doctorApi.getDoctor(doctorId),
      appointmentApi.getAppointmentsForDoctor(doctorId)
    ])

    user.value = doctorData

    let queueEntries = []

    try {
      queueEntries = await appointmentApi.getDoctorQueueAppointments(doctorId)
    } catch (queueErr) {
      if (queueErr?.error === 'No appointments in queue for this doctor') {
        queueEntries = [] // Gracefully handle 404 from queue
      } else {
        throw queueErr // Re-throw other errors
      }
    }

    const queueAppointmentIds = queueEntries.map(q => q.appointment_id)
    const normalized = normalizeSymptoms(allAppointments)

    todayAppointments.value = normalized.filter(a =>
      queueAppointmentIds.includes(a.appointment_id)
    )
    pastAppointments.value = normalized.filter(
      a => a.start_time && a.end_time
    )
  } catch (err) {
    error.value = err.message || 'Failed to load appointments.'
  } finally {
    isLoading.value = false
  }
}

const handleStartConsultation = async (appointmentId) => {
  try {
    isLoading.value = true
    error.value = null
    
    // Call the processApi to start appointment
    const response = await processApi.startAppointment(doctorId)
    console.log('Appointment started:', response)
    
    // Redirect to consultation page with appointment ID
    router.push(`/doctor/consultation/${appointmentId}`)
  } catch (err) {
    error.value = err.message || 'Failed to start consultation'
    console.error('Start error:', err)
  } finally {
    isLoading.value = false
  }
}

const formatDateTime = (isoString) => {
  if (!isoString) return 'N/A'
  const date = new Date(isoString)
  return date.toLocaleString('en-SG', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  })
}

onMounted(() => {
  fetchAppointments().then(() => {
    console.log('Today Appointments:', todayAppointments.value)
    console.log('Past Appointments:', pastAppointments.value)
  })
})
</script>
