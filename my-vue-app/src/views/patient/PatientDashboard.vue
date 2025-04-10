<template>
  <div class="min-h-screen p-8 bg-blue-50">
    <h1 class="text-3xl font-bold mb-6 text-blue-800">Welcome to Your Patient Dashboard</h1>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
      <div
        class="bg-white rounded shadow p-6 hover:shadow-lg cursor-pointer text-center"
        @click="$router.push('/patient/book-appointment')"
      >
        <h2 class="text-xl font-semibold mb-2">📅 Book Appointment</h2>
        <p>Schedule a consultation with a doctor.</p>
      </div>

      <div
        class="bg-white rounded shadow p-6 hover:shadow-lg cursor-pointer text-center"
        @click="$router.push('/patient/my-appointments')"
      >
        <h2 class="text-xl font-semibold mb-2">🗓 My Appointments</h2>
        <p>View and manage your upcoming appointments.</p>
      </div>

      <div
        class="bg-white rounded shadow p-6 hover:shadow-lg cursor-pointer text-center"
        @click="$router.push('/patient/medical-records')"
      >
        <h2 class="text-xl font-semibold mb-2">📖 Medical Records</h2>
        <p>Review your previous diagnoses and prescriptions.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// Optional: Check if patient is logged in
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  const patient = localStorage.getItem('patient')
  if (!patient) {
    router.push('/login') // redirect if not logged in
  }
})
</script>
