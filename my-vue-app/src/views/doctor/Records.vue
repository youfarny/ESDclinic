<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">Patient Records</h1>
    
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
      {{ error }}
    </div>

    <!-- Records List -->
    <div v-else class="space-y-4">
      <div v-for="record in records" :key="record.id" 
           class="bg-white rounded-lg shadow p-4">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="font-medium">Patient ID: {{ record.patient_id }}</h3>
            <p class="text-gray-600">Start Time: {{ formatTime(a.start_time) }}</p>
            <p class="text-gray-600">End Time: {{ formatTime(a.end_time) }}</p>
            <p class="text-gray-600">Diagnosis: {{ record.diagnosis }}</p>
            <p class="text-gray-600">Prescription: {{ record.prescription }}</p>
          </div>
          <button @click="viewRecordDetails(record)"
                  class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">
            View Details
          </button>
        </div>
      </div>

      <!-- No Records Message -->
      <div v-if="records.length === 0" class="text-center text-gray-500 py-8">
        No records found
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { format } from 'date-fns'

const store = useStore()
const router = useRouter()

const records = ref([])
const isLoading = ref(false)
const error = ref(null)

// Format date
const formatDate = (date) => {
  return format(new Date(date), 'PPP')
}

// Fetch records
const fetchRecords = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const doctorId = localStorage.getItem('doctorId')
    if (!doctorId) {
      throw new Error('Doctor ID not found')
    }
    
    // TODO: Implement record fetching from the store
    // For now, using dummy data
    records.value = [
      {
        id: 1,
        patient_id: 'P001',
        date: new Date(),
        diagnosis: 'Common cold',
        prescription: 'Rest and hydration'
      }
    ]
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}

// View record details
const viewRecordDetails = (record) => {
  router.push(`/doctor/records/${record.id}`)
}

onMounted(() => {
  fetchRecords()
})
</script> 
