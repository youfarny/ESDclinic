<template>
  <div class="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
    <div class="font-semibold text-lg">Appointment #{{ appointment.appointment_id }}</div>
    <div class="text-gray-600">Patient ID: {{ appointment.patient_id }}</div>
    <div class="text-gray-600">
      Symptoms:
      {{
        Array.isArray(appointment.patient_symptoms)
          ? appointment.patient_symptoms.join(', ')
          : (appointment.patient_symptoms || 'None')
      }}
    </div>
    <div class="text-gray-500">Start: {{ formatTime(appointment.start_time) || 'Not started' }}</div>
    <div class="text-gray-500">End: {{ formatTime(appointment.end_time) || '-' }}</div>
    <button
      v-if="!appointment.start_time"
      class="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      @click="$emit('start')"
    >
      Start Consultation
    </button>
  </div>
</template>

<script setup>
defineProps({
  appointment: {
    type: Object,
    required: true,
  },
})

defineEmits(['start'])

const formatTime = (time) => {
  return time ? new Date(time).toLocaleString() : null
}
</script>
