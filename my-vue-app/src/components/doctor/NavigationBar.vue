<!-- src/components/doctor/NavigationBar.vue -->
<template>
    <nav class="navbar">
      <div class="logo">
        <router-link to="/doctor/dashboard">SMUDOC</router-link>
      </div>
      
      <div class="nav-links">
        <router-link to="/doctor/dashboard" class="nav-link">Dashboard</router-link>
        <router-link to="/doctor/consultation" class="nav-link">Consultation</router-link>
      </div>
      
      <div class="user-menu">
        <span class="username">Dr. Sarah Chen</span>
        <button @click="logout" class="logout-btn">Logout</button>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'NavigationBar',
    methods: {
      logout() {
        localStorage.removeItem('userRole')
        localStorage.removeItem('isAuthenticated')
        this.$router.push('/')
      }
    }
  }
  </script>
  
  <style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  .logo a {
    font-size: 1.5rem;
    font-weight: 700;
    color: #4f46e5;
    text-decoration: none;
  }
  
  .nav-links {
    display: flex;
    gap: 1.5rem;
  }
  
  .nav-link {
    color: #1f2937;
    text-decoration: none;
    font-weight: 500;
    padding: 0.5rem 0;
  }
  
  .nav-link:hover {
    color: #4f46e5;
  }
  
  .user-menu {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .username {
    font-weight: 500;
  }
  
  .logout-btn {
    padding: 0.5rem 1rem;
    background-color: #ef4444;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>