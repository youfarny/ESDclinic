<template>
    <div class="success-message">
      <h1>🎉 Payment Successful!</h1>
      <p>Your appointment has been confirmed.</p>
      <h1>
  <router-link to="/patient/dashboard" class="text-blue-600 hover:underline">
    Back to Dashboard
  </router-link>
</h1>

    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  
  onMounted(async () => {
    const appointmentId = route.query.appointment_id
    const sessionId = route.query.session_id
  
    if (appointmentId && sessionId) {
      await fetch("http://localhost:5105/payment/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          appointment_id: appointmentId,
          session_id: sessionId
        })
      })
    }
  })
  </script>
  
  <style scoped>
  .success-message {
    text-align: center;
    margin-top: 60px;
  }
  </style>
  