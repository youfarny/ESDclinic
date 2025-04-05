<!-- src/views/doctor/Dashboard.vue -->
<template>
    <div class="dashboard-container">
      <doctor-navigation />
      
      <div class="content">
        <h1>Doctor Dashboard</h1>

        <div class="stats-row">
          <div class="stat-card" @click="navigateTo('/doctor/pending-appointments')">
            <h3>Pending Appointments</h3>
            <p class="stat-number">12</p>
          </div>
          
          <div class="stat-card" @click="navigateTo('/doctor/consultation-records')">
            <h3>Completed Consultation Records</h3>
            <p class="stat-number">8</p>
          </div>
          
    
        </div> 
        
        <div class="next-appointments">
          <h2>Next Appointments</h2>
          <table class="appointment-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Patient</th>
                <th>Reason</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>10:00 AM</td>
                <td>John Smith</td>
                <td>Fever, headache</td>
                <td>
                  <button class="start-btn" @click="startConsultation">Start</button>
                </td>
              </tr>
              <tr>
                <td>10:30 AM</td>
                <td>Maria Chen</td>
                <td>Follow-up appointment</td>
                <td>
                  <button class="start-btn" disabled>Upcoming</button>
                </td>
              </tr>
              <tr>
                <td>11:00 AM</td>
                <td>David Kumar</td>
                <td>Skin rash</td>
                <td>
                  <button class="start-btn" disabled>Upcoming</button>
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
    name: 'DoctorDashboard',
    components: {
      DoctorNavigation
    },
    methods: {
      startConsultation() {
        this.$router.push('/doctor/consultation')
      },
      navigateTo(route) {
        this.$router.push(route)
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
  
  .stats-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }
  
  .stat-card {
  background-color: #554e4e;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px #ffffff0d;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  }

  .stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #4137ff;
    margin-top: 0.5rem;
  }
  
  .next-appointments {
    background-color: #536b7b;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(255, 255, 255, 0.05);
  }
  
  .appointment-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
  }
  
  .appointment-table th, 
  .appointment-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .start-btn {
    padding: 0.5rem 1rem;
    background-color: #4f46e5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .start-btn:disabled {
    background-color: #e5e7eb;
    color: #6b7280;
    cursor: not-allowed;
  }
  </style>