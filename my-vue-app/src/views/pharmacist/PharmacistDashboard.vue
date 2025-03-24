<!-- src/views/pharmacist/Dashboard.vue -->
<template>
    <div class="dashboard-container">
      <pharmacist-navigation />
      
      <div class="content">
        <h1>Pharmacist Dashboard</h1>
        
        <div class="stats-row">
          <div class="stat-card">
            <h3>Pending Prescriptions</h3>
            <p class="stat-number">7</p>
          </div>
          
          <div class="stat-card">
            <h3>Processed Today</h3>
            <p class="stat-number">12</p>
          </div>
          
          <div class="stat-card">
            <h3>Out of Stock Items</h3>
            <p class="stat-number">3</p>
          </div>
        </div>
        
        <div class="prescriptions-table">
          <h2>Pending Prescriptions</h2>
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Items</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>9:45 AM</td>
                <td>John Smith</td>
                <td>Dr. Sarah Chen</td>
                <td>3 items</td>
                <td>
                  <button class="process-btn" @click="processPrescription">Process</button>
                </td>
              </tr>
              <tr>
                <td>10:15 AM</td>
                <td>Maria Lopez</td>
                <td>Dr. David Kumar</td>
                <td>1 item</td>
                <td>
                  <button class="process-btn" @click="processPrescription">Process</button>
                </td>
              </tr>
              <tr>
                <td>11:00 AM</td>
                <td>Ahmed Ali</td>
                <td>Dr. Michael Wong</td>
                <td>5 items</td>
                <td>
                  <button class="process-btn" @click="processPrescription">Process</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import PharmacistNavigation from '../../components/pharmacist/NavigationBar.vue'
  
  export default {
    name: 'PharmacistDashboard',
    components: {
      PharmacistNavigation
    },
    methods: {
      processPrescription() {
        this.$router.push('/pharmacist/process')
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
    background-color: #536b7b;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  .stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #4f46e5;
    margin-top: 0.5rem;
  }
  
  .prescriptions-table {
    background-color: #555f67;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
  }
  
  th, td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .process-btn {
    padding: 0.5rem 1rem;
    background-color: #4f46e5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>