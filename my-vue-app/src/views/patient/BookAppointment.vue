<template>
  <div class="p-6 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Book an Appointment</h1>

    <div class="space-y-4">
      <!-- Doctor dropdown -->
      <select
        v-model="doctorId"
        class="w-full p-2 border rounded"
      >
        <option disabled value="">Select a Doctor</option>
        <option
          v-for="doc in doctors"
          :key="doc.id"
          :value="doc.id"
        >
          {{ doc.id }} - {{ doc.name }}
        </option>
      </select>

      <!-- Symptom input -->
      <textarea
        v-model="symptoms"
        placeholder="Describe your symptoms"
        class="w-full border p-2 rounded resize-y"
      ></textarea>

      <!-- Book button -->
      <button
        @click="bookAppointment"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Book Appointment
      </button>

      <p v-if="message" class="text-green-600 mt-4">{{ message }}</p>
      <p v-if="error" class="text-red-600 mt-4">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const doctorId = ref('');
const symptoms = ref('');
const doctors = ref([]);
const message = ref('');
const error = ref('');

// Manually try to fetch doctor IDs 1–3
onMounted(async () => {
  const tempDoctors = [];

  for (let id = 1; id <= 3; id++) {
    try {
      const res = await fetch(`http://localhost:8000/doctor/byid?doctor_id=${id}&apikey=admin`);
    //   const res = await fetch(`https://personal-73tajzpf.outsystemscloud.com/Doctor_service/rest/DoctorAPI/doctor/byid?doctor_id=${id}`);
      const data = await res.json();

      // Check if the data is valid and doctor exists
      if (data.Result.Success && data.Doctor.length > 0) {
        tempDoctors.push({
          id: data.Doctor[0].doctor_id,
          name: data.Doctor[0].doctor_name,
        });
      } else {
        console.error(`Failed to fetch doctor with ID: ${id}`);
      }
    } catch (e) {
      console.error('Error fetching doctor details:', e);
    }
  }

  doctors.value = tempDoctors;
});


const bookAppointment = async () => {
  const patient = JSON.parse(localStorage.getItem('patient'));
  const patientId = patient?.patient_id;

  if (!patientId) {
    error.value = 'You must be logged in as a patient to book an appointment.';
    return;
  }

  try {
    const res = await fetch('http://localhost:5100/appointment/new', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        patient_id: patientId,
        doctor_id: Number(doctorId.value),
        patient_symptoms: { description: symptoms.value },
      }),
    });

    if (!res.ok) throw new Error('Appointment creation failed');

    const data = await res.json();
    message.value = `Appointment created! ID: ${data.appointment_id}`;
    doctorId.value = '';
    symptoms.value = '';
    error.value = '';
  } catch (err) {
    error.value = err.message;
    message.value = '';
  }
};
</script>
