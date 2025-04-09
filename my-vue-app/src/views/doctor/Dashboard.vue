<script setup>
import { ref, onMounted } from 'vue'
import AppointmentCard from '@/components/AppointmentCard.vue'
import { appointmentApi, doctorApi } from '@/services/api.js'

const doctorId = localStorage.getItem('doctorId') || '1'

const user = ref(null)
const todayAppointments = ref([])
const pastAppointments = ref([])
const consultationAppointments = ref([])
const isLoading = ref(true)
const error = ref(null)

const diagnosis = ref('')
const prescription = ref('')
const allergies = ref('')

const activeTab = ref('appointments')

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
    const normalized = normalizeSymptoms(allAppointments)

    todayAppointments.value = normalized.filter(a => !a.start_time && !a.end_time)
    consultationAppointments.value = normalized.filter(a => a.start_time && !a.end_time)
    pastAppointments.value = normalized.filter(a => a.start_time && a.end_time)
  } catch (err) {
    error.value = err.message || 'Failed to load appointments.'
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

const startConsultation = async (appointmentId) => {
  try {
    const response = await appointmentApi.startAppointmentProcess({ doctor_id: doctorId })
    console.log('Appointment started via composite service:', response)
    await fetchAppointments()
    activeTab.value = 'consultation'
  } catch (err) {
    alert('Failed to start consultation: ' + (err.message || 'Unknown error'))
  }
}

onMounted(fetchAppointments)
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Doctor Dashboard</h1>
    <div class="text-gray-600 mb-4" v-if="user?.doctor">
      Welcome, {{ user.doctor.doctor_name }}
    </div>

    <!-- Manual Tabs -->
    <div class="flex space-x-4 border-b mb-4">
      <button
        class="px-4 py-2"
        :class="{ 'border-b-2 border-blue-600 font-semibold': activeTab === 'appointments' }"
        @click="activeTab = 'appointments'"
      >Today's Appointments</button>

      <button
        class="px-4 py-2"
        :class="{ 'border-b-2 border-blue-600 font-semibold': activeTab === 'consultation' }"
        @click="activeTab = 'consultation'"
      >Online Consultations</button>

      <button
        class="px-4 py-2"
        :class="{ 'border-b-2 border-blue-600 font-semibold': activeTab === 'records' }"
        @click="activeTab = 'records'"
      >Past Records</button>
    </div>

    <div v-if="activeTab === 'appointments'">
      <h2 class="text-xl font-semibold mt-4 mb-2">Today's Appointments</h2>
      <div v-if="todayAppointments.length === 0">No appointments today.</div>
      <AppointmentCard
        v-for="a in todayAppointments"
        :key="a.appointment_id"
        :appointment="a"
      >
        <template #actions>
          <button
            v-if="a.appointment_id === Math.min(...todayAppointments.map(appt => appt.appointment_id))"
            class="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            @click="startConsultation(a.appointment_id)"
          >Start Consultation</button>
        </template>
      </AppointmentCard>
    </div>

    <div v-else-if="activeTab === 'consultation'">
      <div v-if="consultationAppointments.length === 0">No active online consultations.</div>
      <div v-for="appointment in consultationAppointments" :key="appointment.appointment_id" class="space-y-4">
        <div class="bg-white p-4 rounded shadow">
          <h2 class="text-lg font-semibold mb-2">Patient Informati\on</h2>
          <p><strong>Name:</strong> {{ appointment.patient_name }}</p>
          <p><strong>ID:</strong> {{ appointment.patient_id }}</p>
          <p><strong>Age:</strong> {{ appointment.patient_age }}</p>
          <p><strong>Start Time:</strong> {{ appointment.start_time }}</p>
          <p><strong>Symptoms:</strong> {{ appointment.patient_symptoms.join(', ') }}</p>
        </div>

        <div class="aspect-video w-full mb-4">
          <iframe :src="appointment.zoom_link" width="100%" height="100%" allow="camera; microphone; fullscreen" class="rounded border"></iframe>
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
    </div>

    <div v-else-if="activeTab === 'records'">
      <h2 class="text-xl font-semibold mt-4 mb-2">Past Records</h2>
      <div v-if="pastAppointments.length === 0">No past records found.</div>
      <AppointmentCard v-for="a in pastAppointments" :key="a.appointment_id" :appointment="a" />
    </div>
  </div>
</template>
