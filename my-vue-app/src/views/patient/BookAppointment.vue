<!-- src/views/patient/BookAppointment.vue -->
<template>
  <div class="book-appointment-container">
  <navigation-bar />
  
  <div class="content">
  <h1>Book an Appointment</h1>
  
  <div class="appointment-type-selector">
  <div
  :class="['appointment-type', { active: appointmentType === 'any' }]"
  @click="appointmentType = 'any'"
  >
  <h3>Any Available Doctor</h3>
  <p>Get the earliest available appointment with any doctor</p>
  </div>
  
  <div
  :class="['appointment-type', { active: appointmentType === 'previous' }]"
  @click="appointmentType = 'previous'"
  >
  <h3>Previous Doctor</h3>
  <p>Book with the same doctor as your last consultation</p>
  </div>
  
  <div
  :class="['appointment-type', { active: appointmentType === 'specific' }]"
  @click="appointmentType = 'specific'"
  >
  <h3>Specific Doctor</h3>
  <p>Choose a specific doctor for your consultation</p>
  </div>
  </div>
  
  <div v-if="appointmentType === 'specific'" class="doctor-selector">
  <h3>Select a Doctor</h3>
  <div class="doctors-list">
  <div
  v-for="doctor in doctors"
  :key="doctor.id"
  :class="['doctor-card', { selected: selectedDoctor === doctor.id }]"
  @click="selectedDoctor = doctor.id"
  >
  <div class="doctor-avatar"></div>
  <h4>{{ doctor.name }}</h4>
  <p>{{ doctor.specialization }}</p>
  </div>
  </div>
  </div>
  
  <div v-if="appointmentType === 'previous'" class="previous-doctor">
  <h3>Your Previous Doctor</h3>
  <div class="doctor-card selected">
  <div class="doctor-avatar"></div>
  <h4>{{ previousDoctor.name }}</h4>
  <p>{{ previousDoctor.specialization }}</p>
  </div>
  </div>
  
  <div class="reason-section">
  <h3>Reason for Consultation</h3>
  <textarea
  v-model="consultationReason"
  placeholder="Please briefly describe your symptoms or reason for the consultation..."
  rows="4"
  ></textarea>
  </div>
  
  <div class="action-buttons">
  <button class="secondary-btn" @click="$router.push('/patient')">Cancel</button>
  <button class="primary-btn" @click="submitAppointment">Book Appointment</button>
  </div>
  
  <div v-if="showConfirmation" class="confirmation-message">
  <h3>Appointment Confirmed!</h3>
  <h4><p>Your queue number is: <strong>{{ queueNumber }}</strong></p>
  <p>You will receive an SMS notification when your turn is approaching.</p></h4>
  </div>
  </div>
  </div>
  </template>
  
  <script>
  import NavigationBar from '../../components/patient/NavigationBar.vue'
  
  export default {
  name: 'BookAppointment',
  components: {
  NavigationBar
  },
  data() {
  return {
  appointmentType: 'any', // 'any', 'previous', or 'specific'
  selectedDoctor: null,
  consultationReason: '',
  doctors: [
  { id: 1, name: 'Dr. Sarah Chen', specialization: 'General Practitioner' },
  { id: 2, name: 'Dr. Michael Wong', specialization: 'Pediatrician' },
  { id: 3, name: 'Dr. David Kumar', specialization: 'Family Medicine' },
  { id: 4, name: 'Dr. Emily Tan', specialization: 'Internal Medicine' }
  ],
  previousDoctor: { id: 2, name: 'Dr. Michael Wong', specialization: 'Pediatrician' },
  showConfirmation: false,
  queueNumber: 'A-127'
  }
  },
  methods: {
  submitAppointment() {
  // In a real app, you would submit this to your backend
  console.log('Appointment type:', this.appointmentType)
  console.log('Doctor:', this.appointmentType === 'specific' ? this.selectedDoctor :
  this.appointmentType === 'previous' ? this.previousDoctor.id : 'Any')
  console.log('Reason:', this.consultationReason)
  
  // Simulate queue number generation
  this.queueNumber = 'A-' + Math.floor(Math.random() * 900 + 100)
  this.showConfirmation = true
  
  // Scroll to confirmation message
  setTimeout(() => {
  window.scrollTo({
  top: document.body.scrollHeight,
  behavior: 'smooth'
  })
  }, 100)
  }
  }
  }
  </script>
  
  <style scoped>
  .book-appointment-container {
  min-height: 100vh;
  background-color: #d1eef3;
  }
  
  .content {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
  }
  
  .appointment-type-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
  }
  
  .appointment-type {
  background-color: #536b7b;
  border-radius: 8px;
  padding: 1.5rem;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  }
  
  .appointment-type.active {
  border-color: #4f46e5;
  box-shadow: 0 4px 8px rgba(79, 70, 229, 0.2);
  }
  
  .appointment-type h3 {
  margin-bottom: 0.5rem;
  color: #a0cbc5;
  }
  
  .doctor-selector, .previous-doctor, .reason-section {
  background-color: rgb(155, 123, 123);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  }
  
  .doctors-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
  }
  
  .doctor-card {
  border: 1px solid #607cb2;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  }
  
  .doctor-card.selected {
  border-color: #000000;
  background-color: #382b2b;
  }
  
  .doctor-avatar {
  width: 60px;
  height: 60px;
  background-color: #414c61;
  border-radius: 50%;
  margin: 0 auto 0.75rem;
  }
  
  .doctor-card h4 {
  margin-bottom: 0.25rem;
  }
  
  textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  resize: vertical;
  font-family: inherit;
  }
  
  .action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  }
  
  .primary-btn, .secondary-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  }
  
  .primary-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
  }
  
  .secondary-btn {
  background-color: white;
  color: #111827;
  border: 1px solid #e5e7eb;
  }
  
  .confirmation-message {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #ecfdf5;
  border: 1px solid #10b981;
  border-radius: 8px;
  }
  
  .confirmation-message h3 {
  color: #047857;
  margin-bottom: 0.5rem;
  }
  
  .confirmation-message h4 {
  color: #517d71;
  margin-bottom: 0.5rem;
  }
  </style>