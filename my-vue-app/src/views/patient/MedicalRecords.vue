<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Medical Records</h1>

    <div v-if="loading" class="text-gray-500">Loading records...</div>
    <div v-else-if="records.length === 0" class="text-gray-500">No complete records found.</div>
    <div v-else class="space-y-4">
      <div v-for="record in records" :key="record.appointment_id" class="p-4 border rounded bg-white shadow">
        <p><strong>Appointment ID:</strong> {{ record.appointment_id }}</p>
        <p><strong>Diagnosis:</strong> {{ record.diagnosis }}</p>
        <p><strong>Medicine:</strong> {{ record.medicine.join(', ') }}</p>
        <p><strong>Start Time:</strong> {{ record.start_time }}</p>
        <p><strong>End Time:</strong> {{ record.end_time }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const records = ref([])
const loading = ref(true)

const patient = JSON.parse(localStorage.getItem('patient'))
const patientId = patient?.patient_id

onMounted(async () => {
  if (!patientId) return

  try {
    const appointmentsRes = await axios.get(`http://127.0.0.1:8000/appointment/records/${patientId}?apikey=admin`)
    const appointments = appointmentsRes.data

    const filtered = appointments.filter(appt =>
      appt.diagnosis && appt.prescription_id && appt.start_time && appt.end_time
    )

    const fetchedRecords = await Promise.all(filtered.map(async appt => {
      try {
        const presRes = await axios.get(`http://116.15.73.191:5104/prescription/${appt.prescription_id}`)
        const medicine = presRes.data.prescription?.medicine || []
        return {
          appointment_id: appt.appointment_id,
          diagnosis: appt.diagnosis,
          medicine: Array.isArray(medicine) ? medicine : JSON.parse(medicine),
          start_time: appt.start_time,
          end_time: appt.end_time
        }
      } catch (err) {
        console.warn('Error fetching prescription:', err)
        return null
      }
    }))

    records.value = fetchedRecords.filter(r => r !== null)
  } catch (err) {
    console.error('Failed to load medical records:', err)
  } finally {
    loading.value = false
  }
})
</script>
