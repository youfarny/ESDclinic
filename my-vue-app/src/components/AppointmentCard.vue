<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  appointment: Object
})

const emit = defineEmits(['start-consultation'])
</script>

<template>
  <div class="bg-white shadow rounded-lg p-4 space-y-4">
    <div>
      <h3 class="text-lg font-semibold">Appointment</h3>
      <p class="text-sm text-gray-600">Patient ID: {{ appointment.patient_id }}</p>
      <p class="text-sm text-gray-600">Symptoms: {{ appointment.patient_symptoms }}</p>
    </div>

    <div class="flex justify-end">
      <button
        @click="() => emit('start-consultation')"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        Start Consultation
      </button>
    </div>
  </div>
</template>
