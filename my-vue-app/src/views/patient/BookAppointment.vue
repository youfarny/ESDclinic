<template>
  <div class="p-6 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Book an Appointment</h1>

    <!-- Selection Type -->
    <div class="mb-4">
      <label class="font-semibold block mb-2">Choose a Doctor:</label>
      <label class="block">
        <input type="radio" value="shortest" v-model="selection" /> Shortest Queue Doctor
      </label>
      <label class="block">
        <input type="radio" value="previous" v-model="selection" /> Previous Doctor
      </label>
      <label class="block">
        <input type="radio" value="custom" v-model="selection" /> Choose Specific Doctor
      </label>
    </div>

    <!-- Display Selected Doctor Info -->
    <div v-if="selectedDoctorName" class="mb-2 text-sm text-gray-600">
      Selected Doctor: <strong>{{ selectedDoctorName }}</strong>
    </div>

    <!-- Doctor Dropdown -->
    <div v-if="selection === 'custom'" class="mb-4">
      <select v-model="doctorId" class="w-full p-2 border rounded">
        <option disabled value="">Select a Doctor</option>
        <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
          {{ doc.id }} - {{ doc.name }}
        </option>
      </select>
    </div>

    <!-- Symptoms -->
    <textarea
      v-model="symptoms"
      placeholder='Enter symptoms like ["Fever", "Headache"]'
      class="w-full border p-2 rounded resize-y font-mono text-sm mb-4"
    ></textarea>

    <!-- Book Button -->
    <button @click="bookAppointment" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
      Book Appointment
    </button>

    <p v-if="message" class="text-green-600 mt-4">{{ message }}</p>
    <p v-if="error" class="text-red-600 mt-4">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const selection = ref('custom');
const doctorId = ref('');
const doctors = ref([]);
const symptoms = ref('');
const message = ref('');
const error = ref('');
const selectedDoctorName = ref('');

let patient = {};
try {
  patient = JSON.parse(localStorage.getItem('patient')) || {};
} catch {
  patient = {};
}
const patientId = patient?.patient_id;

// Fetch all doctors for custom dropdown
onMounted(async () => {
  const temp = [];
  for (let id = 1; id <= 3; id++) {
    try {
      const res = await fetch(`http://localhost:8000/doctor/byid?doctor_id=${id}&apikey=admin`);
      const data = await res.json();
      if (data.Doctor?.length > 0) {
        temp.push({ id: data.Doctor[0].doctor_id, name: data.Doctor[0].doctor_name });
      }
    } catch (err) {
      console.error(`Error fetching doctor ${id}:`, err);
    }
  }
  doctors.value = temp;
});

// Show doctor name based on selected option
watch([selection, doctorId], async () => {
  error.value = '';
  selectedDoctorName.value = '';

  if (selection.value === 'shortest') {
    try {
      const res = await fetch('http://127.0.0.1:8000/queue/shortest?apikey=admin');
      const data = await res.json();
      doctorId.value = data.doctor_id;

      const doc = doctors.value.find(d => d.id === data.doctor_id);
      selectedDoctorName.value = doc ? `${doc.id} - ${doc.name}` : `Doctor ID ${data.doctor_id}`;
    } catch {
      error.value = 'Failed to fetch shortest queue doctor';
    }
  }

  if (selection.value === 'previous') {
    try {
      const res = await fetch(`http://127.0.0.1:8000/appointment/records/${patientId}?apikey=admin`);
      const data = await res.json();
      if (data.length > 0) {
        doctorId.value = data[data.length - 1].doctor_id;
        const doc = doctors.value.find(d => d.id === doctorId.value);
        selectedDoctorName.value = doc ? `${doc.id} - ${doc.name}` : `Doctor ID ${doctorId.value}`;
      } else {
        error.value = 'No previous appointments found';
      }
    } catch {
      error.value = 'Failed to fetch previous doctor';
    }
  }

  if (selection.value === 'custom') {
    const doc = doctors.value.find(d => d.id === doctorId.value);
    selectedDoctorName.value = doc ? `${doc.id} - ${doc.name}` : '';
  }
});

const bookAppointment = async () => {
  error.value = '';
  message.value = '';

  let parsedSymptoms;
  try {
    parsedSymptoms = JSON.parse(symptoms.value);
    if (!Array.isArray(parsedSymptoms)) throw new Error();
  } catch {
    error.value = 'Invalid symptom format. Use ["Fever", "Headache"]';
    return;
  }

  try {
    const res = await fetch('http://116.15.73.191:5100/appointment/new', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        patient_id: Number(patientId),
        doctor_id: Number(doctorId.value),
        patient_symptoms: JSON.stringify(parsedSymptoms),
      }),
    });

    const text = await res.text();
    const data = text ? JSON.parse(text) : {};
    if (!res.ok) throw new Error(data.error || 'Failed to create appointment');

    message.value = `Appointment created! ID: ${data.appointment_id}`;
    doctorId.value = '';
    symptoms.value = '';
    selectedDoctorName.value = '';
  } catch (err) {
    error.value = err.message || 'Unexpected error';
  }
};
</script>
