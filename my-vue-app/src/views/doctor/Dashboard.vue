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
    const [doctorData, allAppointments, queueEntries] = await Promise.all([
      doctorApi.getDoctor(doctorId),
      appointmentApi.getAppointmentsForDoctor(doctorId),
      appointmentApi.getDoctorQueueAppointments(doctorId)
    ])

    user.value = doctorData

    // Get all appointment IDs in queue
    const queueAppointmentIds = queueEntries.map(q => q.appointment_id)

    const normalized = normalizeSymptoms(allAppointments)

    todayAppointments.value = normalized.filter(
      a => queueAppointmentIds.includes(a.appointment_id)
    )

    pastAppointments.value = normalized.filter(
      a => a.start_time || a.end_time
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

const submitConsultation = async (appointmentId) => {
  try {
    await appointmentApi.endAppointment(appointmentId, new Date().toISOString(), diagnosis.value, 1)
    diagnosis.value = ''
    prescription.value = ''
    allergies.value = ''
    alert('Consultation submitted successfully')
    await fetchAppointments()
  } catch (err) {
    alert('Failed to submit consultation: ' + (err.message || 'Unknown error'))
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


// onMounted(fetchAppointments)
onMounted(() => {
  fetchAppointments().then(() => {
    console.log('Today Appointments:', todayAppointments.value)
    console.log('Past Appointments:', pastAppointments.value)
  })
})

</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Doctor Dashboard</h1>
    <div class="text-gray-600 mb-4" v-if="user?.doctor">
      Welcome, {{ user.doctor.doctor_name }}
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
      {{ error }}
    </div>

    <!-- Manual Tabs -->
    <div v-else>
      <div class="flex space-x-4 border-b mb-4">
        <button
          class="px-4 py-2"
          :class="{ 'border-b-2 border-blue-600 font-semibold': activeTab === 'appointments' }"
          @click="activeTab = 'appointments'"
        >Today's Appointments</button>

        <button
          class="px-4 py-2"
          :class="{ 'border-b-2 border-blue-600 font-semibold': activeTab === 'records' }"
          @click="activeTab = 'records'"
        >Past Records</button>
      </div>

      <!-- Appointments Tab -->
      <div v-if="activeTab === 'appointments'" class="space-y-4">
        <div v-if="sortedTodayAppointments.length === 0" class="text-center text-gray-500 py-8">
          No appointments scheduled for today
        </div>
        <AppointmentCard
          v-for="(appointment, index) in sortedTodayAppointments"
          :key="appointment.appointment_id"
          :appointment="appointment"
          :isFirst="index === 0"
          :showTiming="false"
          @start-consultation="handleStartConsultation"
        />
      </div>

      <!-- <div v-else-if="activeTab === 'consultation'">
        <div v-if="consultationAppointments.length === 0" class="text-center text-gray-500 py-8">
          No active online consultations.
        </div>
        <div v-for="appointment in consultationAppointments" :key="appointment.appointment_id" class="space-y-4">
          <div class="bg-white p-4 rounded shadow">
            <h2 class="text-lg font-semibold mb-2">Patient Information</h2>
            <p><strong>ID:</strong> {{ appointment.patient_id }}</p>
            <p><strong>Symptoms:</strong> {{ Array.isArray(appointment.patient_symptoms) ? 
              appointment.patient_symptoms.join(', ') : appointment.patient_symptoms }}</p>
            <p><strong>Start Time:</strong> {{ appointment.start_time }}</p>
          </div>

          <div class="bg-white p-4 rounded shadow">
            <h2 class="text-lg font-semibold mb-2">Consultation Form</h2>
            <form @submit.prevent="submitConsultation(appointment.appointment_id)">
              <label class="block mb-2 font-medium">Diagnosis</label>
              <textarea v-model="diagnosis" class="w-full border rounded p-2 mb-4"></textarea>

              <label class="block mb-2 font-medium">Prescription</label>
              <textarea v-model="prescription" class="w-full border rounded p-2 mb-4"></textarea>

              <label class="block mb-2 font-medium">Allergies</label>
              <textarea v-model="allergies" class="w-full border rounded p-2 mb-4"></textarea>

              <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Submit</button>
            </form>
          </div>
        </div>
      </div> -->

      <div v-else-if="activeTab === 'records'">
        <!-- <h2 class="text-xl font-semibold mt-4 mb-2">Past Records</h2> -->
        <div v-if="pastAppointments.length === 0" class="text-center text-gray-500 py-8">No past records found.</div>
        <div v-for="a in pastAppointments" :key="a.appointment_id" class="bg-white p-4 rounded shadow mb-4">
          <h3 class="font-medium">Appointment ID: #{{ a.appointment_id }}</h3>
          <h3 class="font-medium">Patient ID: #{{ a.patient_id }}</h3>
          <p class="text-gray-600">Appointment Date: {{ formatDateTime(a.start_time) }}</p>
          <p class="text-gray-600">Start Time: {{ formatDateTime(a.start_time) }}</p>
          <p class="text-gray-600">End Time: {{ formatDateTime(a.end_time) }}</p>
          <p class="text-gray-600">Symptoms: {{ Array.isArray(a.patient_symptoms) ? 
            a.patient_symptoms.join(', ') : a.patient_symptoms }}</p>
        </div>
      </div>
    </div>
  </div>
</template>