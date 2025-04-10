<template>
  <div class="p-6 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Book an Appointment</h1>

    <!-- Doctor Selection -->
    <div class="mb-4">
      <label class="font-semibold block mb-2">Choose a Doctor:</label>
      <label class="block"><input type="radio" value="shortest" v-model="selection" /> Shortest Queue Doctor</label>
      <label class="block"><input type="radio" value="previous" v-model="selection" /> Previous Doctor</label>
      <label class="block"><input type="radio" value="custom" v-model="selection" /> Choose Specific Doctor</label>
    </div>

    <!-- Display Selected Doctor Info -->
    <div v-if="selectedDoctorName" class="mb-2 text-sm text-gray-600">
      Selected Doctor: <strong>{{ selectedDoctorName }}</strong>
    </div>

    <!-- Doctor Dropdown -->
    <div v-if="selection === 'custom'" class="mb-4">
      <select v-model="doctorId" class="w-full p-2 border rounded">
        <option disabled value="">Select a Doctor</option>
        <option v-for="doc in doctors" :key="doc.id" :value="doc.name">
          {{ doc.id }} - {{ doc.name }}
        </option>
      </select>
    </div>

    <!-- Symptoms Input -->
    <textarea
      v-model="symptoms"
      placeholder='Enter symptoms like: Fever, Headache'
      class="w-full border p-2 rounded resize-y font-mono text-sm mb-4"
    ></textarea>

    <!-- Submit -->
    <button @click="bookAppointment" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
      Book Appointment
    </button>

    <p v-if="message" class="text-green-600 mt-4">{{ message }}</p>
    <p v-if="error" class="text-red-600 mt-4">{{ error }}</p>
  </div>
</template><script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const selection = ref('')
const doctorId = ref('')
const doctors = ref([])
const symptoms = ref('')
const message = ref('')
const error = ref('')
const selectedDoctorName = ref('')

let patient = {}
try {
  patient = JSON.parse(localStorage.getItem('patient')) || {}
} catch {
  patient = {}
}
const patientId = patient?.patient_id
const patientContact = "97208453"  // Set default contact number

// Fetch doctor list
onMounted(async () => {
  const temp = []
  for (let id = 1; id <= 3; id++) {
    try {
      const res = await fetch(`http://localhost:8000/doctor/byid?doctor_id=${id}&apikey=admin`)
      const data = await res.json()
      if (data.Doctor?.length > 0) {
        temp.push({ id: data.Doctor[0].doctor_id, name: data.Doctor[0].doctor_name })
      }
    } catch (err) {
      console.error(`Error fetching doctor ${id}:`, err)
    }
  }
  doctors.value = temp
})

// Handle doctor name display logic
watch([selection, doctorId], async () => {
  error.value = ''
  selectedDoctorName.value = ''
  
  if (!selection.value) {
    return  // Don't show any doctor if no selection made
  }

  if (selection.value === 'shortest') {
    try {
      const res = await fetch('http://127.0.0.1:8000/queue/shortest?apikey=admin')
      const data = await res.json()
      if (data.doctor_id) {
        const doc = doctors.value.find(d => d.id === data.doctor_id)
        doctorId.value = doc?.name || ''
        selectedDoctorName.value = doc ? `${doc.id} - ${doc.name}` : `Doctor ID ${data.doctor_id}`
      }
    } catch {
      error.value = 'Failed to fetch shortest queue doctor'
    }
  } else if (selection.value === 'previous') {
    try {
      const res = await fetch(`http://127.0.0.1:8000/appointment/records/${patientId}?apikey=admin`)
      const data = await res.json()
      if (data && data.length > 0) {
        // Sort appointments by date in descending order, using created_time as fallback
        const sortedAppointments = data.sort((a, b) => {
  const idA = a.appointment_id || 0
  const idB = b.appointment_id || 0
  return idB - idA // sort by appointment_id descending
})

       

        const lastAppointment = sortedAppointments[0]
        const lastDoctorId = lastAppointment.doctor_id
        
        // Fetch doctor name for the last appointment
        try {
          const doctorRes = await fetch(`http://localhost:8000/doctor/byid?doctor_id=${lastDoctorId}&apikey=admin`)
          const doctorData = await doctorRes.json()
          if (doctorData.Doctor?.length > 0) {
            const doctor = doctorData.Doctor[0]
            doctorId.value = doctor.doctor_id
            selectedDoctorName.value = `${doctor.doctor_id} - ${doctor.doctor_name}`
          }
        } catch (err) {
          console.error('Error fetching doctor details:', err)
          error.value = 'Failed to fetch previous doctor details'
        }
      } else {
        error.value = 'No previous appointments found'
      }
    } catch (err) {
      console.error('Error fetching previous appointments:', err)
      error.value = 'Failed to fetch previous doctor'
    }
  } else if (selection.value === 'custom') {
    if (doctorId.value) {
      const selectedDoctor = doctors.value.find(d => d.name === doctorId.value)
      if (selectedDoctor) {
        selectedDoctorName.value = `${selectedDoctor.id} - ${selectedDoctor.name}`
      }
    }
  }
})

// Add this new function after the watch block
const refreshDoctorSelection = async () => {
  if (selection.value === 'previous') {
    try {
      const res = await fetch(`http://127.0.0.1:8000/appointment/records/${patientId}?apikey=admin`)
      const data = await res.json()
      if (data.length > 0) {
        // Sort appointments by date in descending order
        const sortedAppointments = data.sort((a, b) => new Date(b.start_time) - new Date(a.start_time))
        const lastAppointment = sortedAppointments[0]
        doctorId.value = lastAppointment.doctor_id
        
        // Fetch doctor name for the last appointment
        try {
          const doctorRes = await fetch(`http://localhost:8000/doctor/byid?doctor_id=${doctorId.value}&apikey=admin`)
          const doctorData = await doctorRes.json()
          if (doctorData.Doctor?.length > 0) {
            selectedDoctorName.value = `${doctorId.value} - ${doctorData.Doctor[0].doctor_name}`
          } else {
            selectedDoctorName.value = `Doctor ID ${doctorId.value}`
          }
        } catch (err) {
          console.error('Error fetching doctor details:', err)
          selectedDoctorName.value = `Doctor ID ${doctorId.value}`
        }
      }
    } catch (err) {
      console.error('Error refreshing doctor selection:', err)
    }
  }
}

const bookAppointment = async () => {
  error.value = ''
  message.value = ''

  if (!selection.value) {
    error.value = 'Please select a doctor option'
    return
  }

  let parsedSymptoms
try {
  // Try JSON parsing first
  parsedSymptoms = JSON.parse(symptoms.value)

  if (!Array.isArray(parsedSymptoms)) throw new Error()
} catch {
  // If not valid JSON array, fallback to splitting by comma
  parsedSymptoms = symptoms.value.split(',').map(s => s.trim()).filter(s => s)
  if (parsedSymptoms.length === 0) {
    error.value = 'Please enter at least one symptom.'
    return
  }
}


  // Determine request_doctor value for composite service
  let requestDoctor = ''
  if (selection.value === 'previous') {
    requestDoctor = 'same'
  } else if (selection.value === 'custom') {
    requestDoctor = doctorId.value // Use the selected doctor name directly
  }

  try {
    console.log('Sending appointment request:', {
      patient_id: patientId,
      request_doctor: requestDoctor,
      patient_symptoms: parsedSymptoms,
      patient_contact: "97208453"
    })

    const res = await axios.post('http://localhost:8000/process/new', {
      apikey: 'admin',
      patient_id: patientId,
      request_doctor: requestDoctor,
      patient_symptoms: parsedSymptoms,
      patient_contact: "97208453"
    })

    const data = res.data.data
    message.value = `Appointment #${data.appointment_id} created with ${data.doctor_name} (Queue length: ${data.queue_length})`
    doctorId.value = ''
    symptoms.value = ''
    selection.value = ''  // Reset selection after booking

    // Add a small delay to ensure the appointment is properly saved
    await new Promise(resolve => setTimeout(resolve, 1000))
    // Refresh the doctor selection to show the most recent appointment
    await refreshDoctorSelection()
  } catch (err) {
    console.error('Error booking appointment:', err)
    error.value = err.message || 'Failed to book appointment'
  }
}
</script>
