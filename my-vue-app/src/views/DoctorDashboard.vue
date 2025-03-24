<!-- src/views/DoctorDashboard.vue
<template>
    <div class="dashboard">
      <h1>Doctor Dashboard</h1>
      <p>Welcome to your doctor dashboard!</p>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      logout() {
        this.$store.dispatch('logout')
        this.$router.push('/login')
      }
    }
  }
  </script> -->