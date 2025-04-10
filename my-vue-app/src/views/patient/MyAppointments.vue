<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">My Appointments</h1>

    <p v-if="error" class="text-red-600 mb-4">{{ error }}</p>
    <p v-if="successMessage" class="text-green-600 mb-4">{{ successMessage }}</p>

<!-- Back button after successful payment -->
    <div v-if="successMessage">
      <button
        @click="goBack"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Go Back to My Appointments
      </button>
    </div>


    <div v-for="appt in appointments" :key="appt.appointment_id" class="border p-4 mb-4 rounded flex justify-between items-center">
      <div>
        <p><strong>Doctor ID:</strong> {{ appt.doctor_id }}</p>
        <p><strong>Start Time:</strong> {{ appt.start_time }}</p>
        <p><strong>End Time:</strong> {{ appt.end_time }}</p>
        <p><strong>Diagnosis:</strong> {{ appt.diagnosis }}</p>
        <p><strong>Total Cost:</strong> ${{ appt.total_cost }}</p>
        <p><strong>Status:</strong> {{ appt.payment_status === 0 ? 'Unpaid' : 'Paid' }}</p>
      </div>

      <div>
  <div
    v-if="appt.payment_status === 0"
    class="flex justify-end"
  >
    <button
      @click="goToStripe(appt)"
      class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
    >
      Pay Now
    </button>
  </div>
  <div
    v-else
    class="text-green-700 font-semibold"
  >
    ✅ Paid
  </div>
</div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const appointments = ref([])
const error = ref('')
const successMessage = ref('')
const goBack = () => {
  window.location.href = '/patient/my-appointments'
}


let patient = {}
try {
  patient = JSON.parse(localStorage.getItem('patient')) || {}
} catch {
  patient = {}
}
const patientId = patient?.patient_id

onMounted(async () => {
  const query = new URLSearchParams(window.location.search)
  const paymentSuccess = query.get('payment') === 'success'
  const paymentId = query.get('payment_id')
  const appointmentId = query.get('appointment_id')

  // 1. If returned from Stripe with success, finish payment process
  if (paymentSuccess && appointmentId && paymentId) {
    try {
      const finishRes = await axios.post('http://localhost:8000/process/finish?apikey=admin', {
        appointment_id: appointmentId,
        payment_id: paymentId
      })
      if (finishRes.data.code === 200) {
        successMessage.value = 'Payment completed successfully!'
      }
    } catch (finishErr) {
      console.error('Failed to finalize payment:', finishErr)
    }
  }

  // 2. Then load appointments
  await loadAppointments()
})

const loadAppointments = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/appointment/records/${patientId}?apikey=admin`)
    const allAppointments = res.data

    const enrichedAppointments = await Promise.all(
      allAppointments.map(async (appt) => {
        try {
          const calc = await axios.post(`http://localhost:8000/process/calculate?apikey=admin`, {
            appointment_id: appt.appointment_id,
          })

          const { payment_amount, payment_id, payment_status } = calc.data.data || {}

          return {
            ...appt,
            total_cost: payment_amount ?? 'N/A',
            payment_id: payment_id ?? null,
            payment_status: payment_status === true ? 1 : 0

          }
        } catch (calcErr) {
          console.error(`Failed to calculate payment for appointment ${appt.appointment_id}`, calcErr)
          return { ...appt, total_cost: 'N/A', payment_status: 0 }
        }
      })
    )

    appointments.value = enrichedAppointments
  } catch (err) {
    console.error('Error loading appointments:', err)
    error.value = 'Failed to load appointments'
  }
};
const goToStripe = async (appt) => {
  try {
    // Get the most updated payment info
    const res = await axios.post(`http://localhost:8000/process/calculate?apikey=admin`, {
      appointment_id: appt.appointment_id
    })
    const { payment_id, payment_amount } = res.data.data || {}

    if (!payment_id) {
      throw new Error("No payment_id returned from process/calculate")
    }

    // Save it in sessionStorage
    sessionStorage.setItem("last_payment", JSON.stringify({
      appointment_id: appt.appointment_id,
      payment_id: payment_id
    }))

    // Proceed to Stripe
    const stripeResponse = await fetch("https://personal-5nnqipga.outsystemscloud.com/Stripe/rest/payments/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mode: "payment",
        success_url: `http://localhost:5173/patient/my-appointments?payment=success`,
        cancel_url: `http://localhost:5173/patient/my-appointments`,
        currency: "usd",
        product_name: `Appointment #${appt.appointment_id}`,
        unit_amount: Math.abs(payment_amount),
        quantity: 1
      })
    })

    const stripeData = await stripeResponse.json()
    const redirectUrl = stripeData.url || stripeData.redirect_url || stripeData.checkout_url

    if (redirectUrl) {
      window.location.href = redirectUrl
    } else {
      throw new Error("Stripe did not return a redirect URL")
    }
  } catch (err) {
    console.error("Stripe error:", err)
    alert("Stripe error: " + err.message)
  }
}


</script>
