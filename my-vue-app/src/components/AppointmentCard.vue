<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-lg font-semibold mb-2">Appointment ID: #{{ appointment.appointment_id }}</h2>
    <p><strong>Patient ID:</strong> #{{ appointment.patient_id }}</p>
    <p><strong>Symptoms:</strong> {{ appointment.patient_symptoms?.join(', ') || 'None' }}</p>
    
    <!-- Show start and end time -->
    <p v-if="showTiming" class="text-gray-600">Start Time: {{ appointment.start_time ? formatDateTime(appointment.start_time) : 'N/A' }}</p>
    <p v-if="showTiming" class="text-gray-600">End Time: {{ appointment.end_time ? formatDateTime(appointment.end_time) : 'N/A' }}</p>


    <button
      :disabled="!isFirst"
      @click="$emit('start-consultation', appointment.appointment_id)"
      class="mt-4 px-4 py-2 rounded text-white"
      :class="isFirst ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-300 cursor-not-allowed'"
    >
      Start Consultation
    </button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  appointment: Object,
  isFirst: Boolean,
  showTiming: {
    type: Boolean,
    default: false
  }
})

const formatDateTime = (isoString) => {
  if (!isoString) return 'N/A'
  const date = new Date(isoString)
  return date.toLocaleString('en-SG', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  })
}


defineEmits(['start-consultation'])

</script>
