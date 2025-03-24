<template>
  <div class="dashboard-container">
    <navigation-bar />

    <div class="content">
      <h1>Welcome to SMUDOC, {{ patientName }}</h1>
      <div class="action-cards">
        <div class="card" @click="navigateToBookAppointment">
          <h2>Book New Appointment</h2>
          <p>Schedule a consultation with one of our doctors</p>
        </div>

        <div class="card" @click="navigateToAppointments">
          <h2>My Appointments</h2>
          <p>View and manage your upcoming appointments</p>
        </div>

        <div class="card" @click="navigateToMedicalRecords">
          <h2>Medical Records</h2>
          <p>Access your medical history and prescriptions</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavigationBar from '../../components/patient/NavigationBar.vue'

export default {
  name: 'PatientDashboard',
  components: {
    NavigationBar
  },
  data() {
    return {
      patientName: 'John Doe'
    }
  },
  methods: {
    navigateToBookAppointment() {
      this.$router.push('/patient/book-appointment')
    },
    navigateToAppointments() {
      this.$router.push('/patient/appointments')
    },
    navigateToMedicalRecords() {
      this.$router.push('/patient/medical-records')
    }
  }
}
</script>

<style scoped>
.dashboard-container {
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

.action-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.card {
  background-color: #536b7b;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  color: white;
  text-align: center;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.card h2 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.card p {
  color: #e0e0e0;
  font-size: 0.9rem;
}
</style>