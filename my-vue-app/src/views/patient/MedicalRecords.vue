<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Medical Records</h1>

    <p v-if="error" class="text-red-600 mb-4">{{ error }}</p>
    <div v-if="loading" class="text-gray-500 mb-4">Loading your medical records...</div>
    
    <div v-if="records.length === 0 && !loading" class="text-gray-500 mb-4">
      No medical records found.
    </div>

    <div v-for="record in records" :key="record.appointment_id" class="border p-4 mb-4 rounded-md shadow-md bg-white">
      <div class="flex justify-between items-start mb-2">
        <h2 class="text-lg font-semibold">Appointment #{{ record.appointment_id }}</h2>
        <span :class="record.payment_status === 'Paid' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'" class="px-2 py-1 rounded-full text-sm font-medium">
          {{ record.payment_status }}
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <p class="mb-1"><span class="font-semibold">Doctor:</span> {{ record.doctor_name }}</p>
          <p class="mb-1"><span class="font-semibold">Start Time:</span> {{ formatDateTime(record.start_time) }}</p>
          <p class="mb-1"><span class="font-semibold">End Time:</span> {{ formatDateTime(record.end_time) }}</p>
          <p class="mb-1"><span class="font-semibold">Cost:</span> ${{ record.payment_amount || 'N/A' }}</p>
        </div>
        
        <div>
          <p class="mb-1"><span class="font-semibold">Diagnosis:</span> {{ record.diagnosis || 'Not provided' }}</p>
          <div class="mb-1">
            <span class="font-semibold">Symptoms:</span>
            <span v-if="record.symptoms && record.symptoms.length">
              {{ Array.isArray(record.symptoms) ? record.symptoms.join(', ') : record.symptoms }}
            </span>
            <span v-else>None reported</span>
          </div>
          <div>
            <span class="font-semibold">Prescribed Medications:</span>
            <span v-if="record.medicine && record.medicine.length">
              {{ Array.isArray(record.medicine) ? record.medicine.join(', ') : record.medicine }}
            </span>
            <span v-else>None prescribed</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const records = ref([])
const loading = ref(true)
const error = ref('')

// Get patient info from localStorage
let patient = {}
try {
  patient = JSON.parse(localStorage.getItem('patient')) || {}
} catch {
  patient = {}
}
const patientId = patient?.patient_id

// API URL for Kong Gateway
const API_URL = 'http://localhost:8000'
const API_KEY = 'admin' // API key required by Kong

// Format date and time for better display
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return 'N/A'
  const date = new Date(dateTimeStr)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

onMounted(async () => {
  if (!patientId) {
    error.value = 'Patient information not found. Please log in again.'
    loading.value = false
    return
  }

  await loadMedicalRecords()
})

const loadMedicalRecords = async () => {
  try {
    // Step 1: Get all appointments for this patient
    const appointmentsRes = await axios.get(`${API_URL}/appointment/records/${patientId}?apikey=${API_KEY}`)
    const allAppointments = appointmentsRes.data
    
    // Filter for completed appointments with diagnosis
    const completedAppointments = allAppointments.filter(appt => 
      appt.diagnosis && 
      appt.start_time && 
      appt.end_time
    )

    if (completedAppointments.length === 0) {
      loading.value = false
      return
    }

    // Step 2: Process each appointment to get full details
    const processedRecords = await Promise.all(completedAppointments.map(async (appt) => {
      try {
        // Default record with base appointment information
        let record = {
          appointment_id: appt.appointment_id,
          diagnosis: appt.diagnosis || 'Not recorded',
          doctor_id: appt.doctor_id,
          doctor_name: 'Unknown Doctor',
          symptoms: Array.isArray(appt.patient_symptoms) ? 
                  appt.patient_symptoms : 
                  (appt.patient_symptoms ? [appt.patient_symptoms] : []),
          medicine: [],
          start_time: appt.start_time,
          end_time: appt.end_time,
          payment_status: 'Pending',
          payment_amount: 'N/A'
        }

        // Step 3: Get payment details using process/calculate endpoint
        try {
          const paymentRes = await axios.post(`${API_URL}/process/calculate?apikey=${API_KEY}`, {
            appointment_id: appt.appointment_id
          })
          
          if (paymentRes.data && paymentRes.data.data) {
            const { payment_amount, payment_id } = paymentRes.data.data
            record.payment_amount = payment_amount || 'N/A'
            record.payment_status = payment_id ? 'Paid' : 'Pending'
          }
        } catch (err) {
          console.warn(`Failed to fetch payment for appointment ${appt.appointment_id}:`, err)
        }

        // Step 4: Get prescription details if available
        if (appt.prescription_id) {
          try {
            const presRes = await axios.get(`${API_URL}/prescription/${appt.prescription_id}?apikey=${API_KEY}`)
            
            if (presRes.data && presRes.data.prescription && presRes.data.prescription.medicine) {
              const medicineList = presRes.data.prescription.medicine
              record.medicine = Array.isArray(medicineList) ? 
                              medicineList : 
                              (typeof medicineList === 'string' ? JSON.parse(medicineList) : [])
            }
          } catch (err) {
            console.warn(`Failed to fetch prescription ${appt.prescription_id}:`, err)
          }
        }

        // Step 5: Get doctor details
        if (appt.doctor_id) {
          try {
            const doctorRes = await axios.get(`${API_URL}/doctor/byid?doctor_id=${appt.doctor_id}&apikey=${API_KEY}`)
            
            if (doctorRes.data && doctorRes.data.Doctor && doctorRes.data.Doctor[0]) {
              record.doctor_name = doctorRes.data.Doctor[0].doctor_name
            }
          } catch (err) {
            console.warn(`Failed to fetch doctor ${appt.doctor_id}:`, err)
          }
        }

        return record
      } catch (err) {
        console.error(`Error processing appointment ${appt.appointment_id}:`, err)
        return {
          appointment_id: appt.appointment_id,
          diagnosis: appt.diagnosis || 'Not recorded',
          doctor_name: 'Unknown Doctor',
          symptoms: [],
          medicine: [],
          start_time: appt.start_time,
          end_time: appt.end_time,
          payment_status: 'Unknown',
          payment_amount: 'N/A'
        }
      }
    }))

    // Sort by appointment date (most recent first)
    records.value = processedRecords.sort((a, b) => 
      new Date(b.start_time) - new Date(a.start_time)
    )
  } catch (err) {
    console.error('Failed to load medical records:', err)
    error.value = 'Failed to load medical records. Please try again later.'
  } finally {
    loading.value = false
  }
}
</script>