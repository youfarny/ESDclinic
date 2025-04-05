<template>
  <div class="pending-appointments-container">
    <doctor-navigation />
    
    <div class="content">
      <h1>Pending Appointments</h1>
      
      <div class="appointments-list">
        <table class="appointment-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Patient</th>
              <th>Reason</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appointment in pendingAppointments" :key="appointment.id">
              <td>{{ appointment.date }}</td>
              <td>{{ appointment.time }}</td>
              <td>{{ appointment.patientName }}</td>
              <td>{{ appointment.reason }}</td>
              <td>
                <button class="action-btn" @click="acceptAppointment(appointment.id)">Accept</button>
                <button class="action-btn reschedule" @click="rescheduleAppointment(appointment.id)">Reschedule</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import DoctorNavigation from '../../components/doctor/DocNavigationBar.vue'

export default {
  name: 'PendingAppointments',
  components: {
    DoctorNavigation
  },
  data() {
    return {
      pendingAppointments: [
        { id: 1, date: '2025-04-05', time: '14:00', patientName: 'Emily Johnson', reason: 'Annual checkup' },
        { id: 2, date: '2025-04-06', time: '09:30', patientName: 'Michael Wong', reason: 'Persistent cough' },
        { id: 3, date: '2025-04-06', time: '11:15', patientName: 'Sarah Williams', reason: 'Allergy consultation' },
        { id: 4, date: '2025-04-07', time: '15:45', patientName: 'Robert Garcia', reason: 'Blood pressure check' },
        // Add more sample data as needed
      ]
    }
  },
  methods: {
    acceptAppointment(id) {
      // Logic to accept appointment
      alert(`Accepting appointment ${id}`)
    },
    rescheduleAppointment(id) {
      // Logic to reschedule appointment
      alert(`Rescheduling appointment ${id}`)
    }
  }
}
</script>

<style scoped>
.pending-appointments-container {
  min-height: 100vh;
  background-color: #d1eef3;
}

.content {
  padding: 2rem;
}

.appointments-list {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 1.5rem;
}

.appointment-table {
  width: 100%;
  border-collapse: collapse;
}

.appointment-table th, 
.appointment-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.action-btn {
  padding: 0.5rem 1rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
}

.action-btn.reschedule {
  background-color: #f59e0b;
}

.action-btn:hover {
  opacity: 0.9;
}
</style>