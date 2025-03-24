<template>
  <div class="medical-records-container">
    <navigation-bar />

    <div class="content">
      <h1>Medical Records - Allergies</h1>

      <div class="allergies-list">
        <div v-for="(allergy, index) in allergies" :key="index" class="record-item">
          <div class="record-header">
            <h3>{{ allergy.name }}</h3>
            <span class="severity" :class="allergy.severity.toLowerCase()">{{ allergy.severity }}</span>
          </div>
          <p>{{ allergy.reaction }}</p>
        </div>
      </div>

    
    </div>
  </div>
</template>

<script>
import NavigationBar from '../../components/patient/NavigationBar.vue'

export default {
  name: 'MedicalRecords',
  components: {
    NavigationBar
  },
  data() {
    return {
      allergies: [
        {
          name: 'Penicillin',
          severity: 'High',
          reaction: 'Hives, difficulty breathing'
        },
        {
          name: 'Peanuts',
          severity: 'Medium',
          reaction: 'Skin rash, itchiness'
        }
      ]
    }
  },
  methods: {
    navigateToDashboard() {
      this.$router.push('/patient/dashboard')
    }
  }
}
</script>

<style scoped>
.medical-records-container {
  min-height: 100vh;
  background-color: #d1eef3;
}

.content {
  padding: 2rem;
}

h1 {
  color: white;
  margin-bottom: 2rem;
}

.allergies-list {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.record-item {
  background-color: #536b7b;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.record-header h3 {
  margin: 0;
}

.severity {
  padding: 5px 10px;
  border-radius: 20px;
}

.severity.high {
  background-color: #ff6b6b;
}

.severity.medium {
  background-color: #ffd166;
}

.navigation-buttons {
  margin-top: 20px;
}

.navigation-buttons button {
  background-color: #382b2b;
  color: white;
  border-radius: 8px;
  padding: 10px;
}
</style>
