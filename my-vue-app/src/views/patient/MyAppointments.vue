<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">My Appointments</h1>

    <p v-if="error" class="text-red-600 mb-4">{{ error }}</p>
    <p v-if="successMessage" class="text-green-600 mb-4">{{ successMessage }}</p>

  
  <template v-for="appt in appointments"
  :key="appt.appointment_id" >
  
  <div v-if="appt.end_time != null"
  class="border p-4 mb-4 rounded flex justify-between items-center"
>
  <div>
    <p><strong>Doctor ID:</strong> {{ appt.doctor_id }}</p>
    <p><strong>Start Time:</strong> {{ appt.start_time || 'N/A' }}</p>
    <p><strong>End Time:</strong> {{ appt.end_time || 'N/A' }}</p>
    <p><strong>Diagnosis:</strong> {{ appt.diagnosis || 'N/A' }}</p>
    <p><strong>Total Cost:</strong> ${{ appt.total_cost }}</p>
    <p><strong>Status:</strong> {{ appt.payment_id === null ? 'Unpaid' : 'Paid' }}</p>
  </div>

  <div v-if="appt.payment_id === null">
    <button
      @click="goToStripe(appt)"
      class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
    >
      Pay Now
    </button>
  </div>

  <div v-else="appt.payment_status !== 0" class="text-green-600 font-bold">
    ✅ Paid
  </div>
  
</div>
</template>



  

  
</div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const appointments = ref([])
const error = ref('')
const successMessage = ref('')

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
  console.log("💡 Query Params:", { paymentSuccess, paymentId, appointmentId })

  if (paymentSuccess && appointmentId && paymentId) {
    
    try {
      const finishRes = await axios.post('http://localhost:8000/process/finish', {
        apikey: "admin",
        appointment_id: appointmentId,
        payment_id: paymentId,
        // payment_status: true
      })

      if (finishRes.data.code === 200) {
        console.log("✅ Payment finish succeeded:", finishRes.data)
        successMessage.value = 'Payment completed successfully!'
        await loadAppointments()
      } else {
        console.warn("⚠️ Payment finish did not return code 200:", finishRes.data)
      }
    } catch (finishErr) {
      console.error('❌ Failed to finalize payment:', finishErr?.response?.data || finishErr)
    }
  } else {
    await loadAppointments()
  }
})
const loadAppointments = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/appointment/records/${patientId}?apikey=admin`)
    const allAppointments = res.data

    console.log("📥 Raw Appointments Retrieved:", allAppointments)

    const enrichedAppointments = await Promise.all(
      allAppointments.map(async (appt) => {
        if (!appt.start_time || !appt.end_time) {
          console.warn("⏭ Skipping appointment due to missing time:", appt)
          return { ...appt, total_cost: 'N/A', payment_status: 0 }
        }

        try {
          const calc = await axios.post(`http://localhost:8000/process/calculate?apikey=admin`, {
            appointment_id: appt.appointment_id,
          })

          const { payment_amount, payment_id, payment_status } = calc.data.data || {}

          const enriched = {
            ...appt,
            total_cost: payment_amount ?? 'N/A',
            payment_id: payment_id ?? null,
            payment_status: payment_status ?? 0,
          }

          console.log(`✅ Enriched appointment ${appt.appointment_id}:`, enriched)
          return enriched
        } catch (calcErr) {
          console.error(`❌ Failed to calculate payment for appointment ${appt.appointment_id}`, calcErr?.response?.data || calcErr)
          return { ...appt, total_cost: 'N/A', payment_status: 0 }
        }
      })
    )

    console.log("📦 Final Enriched Appointments:", enrichedAppointments)
    appointments.value = enrichedAppointments
  } catch (err) {
    console.error('❌ Error loading appointments:', err?.response?.data || err)
    error.value = 'Failed to load appointments'
  }
}


const goToStripe = async (appt) => {
  console.log("🔁 Stripe success_url being sent:", `http://localhost:5173/patient/my-appointments?payment=success&appointment_id=${appt.appointment_id}&payment_id=${appt.payment_id}`);

  try {
    const payload = {
      mode: "payment",
      success_url: `http://localhost:5173/patient/my-appointments?payment=success&appointment_id=${appt.appointment_id}&payment_id=${appt.payment_id}`,
      cancel_url: `http://localhost:5173/patient/my-appointments`,
      currency: "usd",
      product_name: `Appointment #${appt.appointment_id}`,
      unit_amount: Math.round(Math.abs(appt.total_cost * 100)),
      quantity: 1
    }

    console.log("🧾 Stripe Payload:", payload)

    const response = await fetch("https://personal-5nnqipga.outsystemscloud.com/Stripe/rest/payments/checkout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    })

    const data = await response.json()

    if (response.ok && (data.checkout_url || data.url || data.redirect_url)) {
      window.location.href = data.checkout_url || data.url || data.redirect_url
    } else {
      console.error("❌ Stripe Error Response:", data)
      throw new Error("Failed to get Stripe checkout link")
    }

  } catch (err) {
    alert("Stripe error: " + err.message)
    console.error("❌ Stripe redirect error:", err)
  }
}
</script>
