<template>
  <div class="appointments-container">
  <h1>My Appointments</h1>
  
  <div v-if="appointments.length === 0" class="no-appointments">
  <p>You don't have any upcoming appointments.</p>
  <button class="btn-primary" @click="$router.push('/book-appointment')">Book an Appointment</button>
  </div>
  
  <div v-else class="appointments-list">
  <div v-for="(appointment, index) in appointments" :key="index" class="appointment-card">
  <div class="appointment-date">
  <div class="month">{{ getMonthName(appointment.date) }}</div>
  <div class="day">{{ getDayOfMonth(appointment.date) }}</div>
  </div>
  <div class="appointment-details">
  <h3>{{ appointment.doctorName }}</h3>
  <p>{{ appointment.specialty }}</p>
  <p>Time: {{ formatTime(appointment.time) }}</p>
  <p>Location: {{ appointment.location }}</p>
  </div>
  <div class="appointment-actions">
  <button class="btn-secondary" @click="rescheduleAppointment(index)">Reschedule</button>
  <button class="btn-danger" @click="cancelAppointment(index)">Cancel</button>
  </div>
  </div>
  </div>
  </div>
  </template>
  
  <script>
  export default {
  name: 'MyAppointments',
  data() {
  return {
  appointments: [
  {
  doctorName: 'Dr. Sarah Johnson',
  specialty: 'General Practitioner',
  date: '2025-03-22',
  time: '10:30',
  location: 'Main Clinic, Room 204'
  },
  {
  doctorName: 'Dr. Robert Chen',
  specialty: 'Dermatologist',
  date: '2025-04-05',
  time: '14:15',
  location: 'Specialist Wing, Room 118'
  }
  ]
  }
  },
  methods: {
  getMonthName(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('default', { month: 'short' });
  },
  getDayOfMonth(dateString) {
  const date = new Date(dateString);
  return date.getDate();
  },
  formatTime(timeString) {
  const [hours, minutes] = timeString.split(':');
  const period = hours >= 12 ? 'PM' : 'AM';
  const formattedHours = hours % 12 || 12;
  return `${formattedHours}:${minutes} ${period}`;
  },
  rescheduleAppointment(index) {
  alert(`Rescheduling appointment with ${this.appointments[index].doctorName}`);
  // Implement rescheduling logic here
  },
  cancelAppointment(index) {
  if (confirm(`Are you sure you want to cancel your appointment with ${this.appointments[index].doctorName}?`)) {
  this.appointments.splice(index, 1);
  }
  }
  }
  }
  </script>
  
  <style scoped>
  .appointments-container {
  padding: 20px;
  background-color: #d1eef3;
  min-height: 80vh;
  }
  
  .no-appointments {
  text-align: center;
  padding: 40px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .appointments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  }
  
  .appointment-card {
  display: flex;
  background-color: #536b7b;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .appointment-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #4682b4;
  color: white;
  padding: 15px;
  min-width: 80px;
  }
  
  .month {
  font-size: 0.9rem;
  text-transform: uppercase;
  }
  
  .day {
  font-size: 1.8rem;
  font-weight: bold;
  }
  
  .appointment-details {
  flex-grow: 1;
  padding: 15px;
  }
  
  .appointment-details h3 {
  margin-top: 0;
  color: #333;
  }
  
  .appointment-actions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 10px;
  padding: 15px;
  }
  
  .btn-primary {
  background-color: #4682b4;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  }
  
  .btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  }
  
  .btn-danger {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  }
  </style>