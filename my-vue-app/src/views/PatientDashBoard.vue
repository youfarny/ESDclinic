<!-- src/views/PatientDashboard.vue -->
<!-- <template>
    <div class="dashboard-container">
      <h1>Patient Dashboard</h1>
      <p>Welcome, {{ user ? user.username : 'Patient' }}!</p>
      
      <div class="dashboard-cards">
        <div class="card">
          <h2>My Appointments</h2>
          <div v-if="appointments.length === 0" class="no-data">
            You don't have any upcoming appointments.
          </div>
          <div v-else class="appointment-list">
            <div v-for="appointment in appointments" :key="appointment.id" class="appointment-item">
              <div class="appointment-details">
                <strong>{{ appointment.doctorName }}</strong>
                <div>{{ formatDate(appointment.date) }}</div>
                <div>Queue number: {{ appointment.queueNumber }}</div>
              </div>
              <div class="appointment-status" :class="appointment.status">
                {{ appointment.status }}
              </div>
            </div>
          </div>
          <router-link to="/patient/appointment" class="action-button">Book New Appointment</router-link>
        </div>
        
        <div class="card">
          <h2>Appointment Options</h2>
          <div class="appointment-options">
            <div class="option-item">
              <h3>Any Available Doctor</h3>
              <p>Get the fastest service with the next available doctor</p>
              <div class="option-indicator">Quick</div>
            </div>
            <div class="option-item">
              <h3>Previous Doctor</h3>
              <p>Continue care with a doctor you've seen before</p>
              <div class="option-indicator">Familiar</div>
            </div>
            <div class="option-item">
              <h3>Specific Doctor</h3>
              <p>Choose a specific doctor based on your preferences</p>
              <div class="option-indicator">Personalized</div>
            </div>
          </div>
          <router-link to="/patient/about" class="info-link">Learn more about appointment options</router-link>
        </div>
        
        <div class="card">
          <h2>Recent Consultations</h2>
          <div v-if="consultations.length === 0" class="no-data">
            You don't have any recent consultations.
          </div>
          <div v-else class="consultation-list">
            <div v-for="consultation in consultations" :key="consultation.id" class="consultation-item">
              <div class="consultation-details">
                <strong>{{ consultation.doctorName }}</strong>
                <div>{{ formatDate(consultation.date) }}</div>
                <div>{{ consultation.diagnosis }}</div>
              </div>
              <button class="view-button">View Details</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        appointments: [
          { id: 1, doctorName: 'Dr. Smith', date: '2025-03-20', queueNumber: 'A42', status: 'scheduled' }
        ],
        consultations: [
          { id: 1, doctorName: 'Dr. Johnson', date: '2025-03-01', diagnosis: 'Common cold' }
        ]
      }
    },
    computed: {
      user() {
        return this.$store.getters.getUser;
      }
    },
    methods: {
      formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      }
    }
  }
  </script>
  
  <style scoped>
  .dashboard-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  .dashboard-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }
  .card {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  .no-data {
    color: #666;
    font-style: italic;
    margin: 20px 0;
  }
  .appointment-list, .consultation-list {
    margin: 15px 0;
  }
  .appointment-item, .consultation-item {
    border-bottom: 1px solid #eee;
    padding: 10px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .appointment-item:last-child, .consultation-item:last-child {
    border-bottom: none;
  }
  .appointment-status {
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 0.9em;
    font-weight: bold;
  }
  .appointment-status.scheduled {
    background-color: #e3f2fd;
    color: #1976d2;
  }
  .appointment-status.completed {
    background-color: #e8f5e9;
    color: #388e3c;
  }
  .appointment-status.canceled {
    background-color: #ffebee;
    color: #d32f2f;
  }
  .action-button {
    display: block;
    background-color: #42b883;
    color: white;
    text-decoration: none;
    text-align: center;
    padding: 10px;
    border-radius: 4px;
    margin-top: 15px;
  }
  .info-link {
    display: block;
    text-align: center;
    margin-top: 15px;
    color: #42b883;
    text-decoration: none;
  }
  .option-item {
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px solid #eee;
  }
  .option-item:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
  }
  .option-indicator {
    display: inline-block;
    background-color: #f0f0f0;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.8em;
    color: #666;
  }
  .view-button {
    background-color: transparent;
    border: 1px solid #42b883;
    color: #42b883;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
  }
  .view-button:hover {
    background-color: #42b883;
    color: white;
  }
  </style> -->