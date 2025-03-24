<template>
  <div class="navbar-container">
    <div class="navbar-brand" @click="navigateTo('/patient-dashboard')">
      <span class="brand-text">SMUDOC</span>
    </div>
    
    <div class="navbar-links">
      <div 
        class="nav-link" 
        @click="navigateTo('/patient-dashboard')"
        :class="{ active: isActive('/patient-dashboard') }"
      >
        Dashboard
      </div>
      <div 
        class="nav-link" 
        @click="navigateTo('/book-appointment')"
        :class="{ active: isActive('/book-appointment') }"
      >
        Book Appointment
      </div>
      <div 
        class="nav-link" 
        @click="navigateTo('/appointments')"
        :class="{ active: isActive('/appointments') }"
      >
        My Appointments
      </div>
      <div 
        class="nav-link" 
        @click="navigateTo('/medical-records')"
        :class="{ active: isActive('/medical-records') }"
      >
        Medical Records
      </div>
    </div>
    
    <div class="navbar-actions">
      <button class="logout-btn" @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavigationBar',
  methods: {
    navigateTo(route) {
      if (this.$route.path !== route) {
        this.$router.push(route);
      }
    },
    isActive(route) {
      return this.$route.path === route;
    },
    logout() {
      // In a real app, this would clear authentication tokens
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
  height: 60px;
}

.navbar-brand {
  cursor: pointer;
}

.brand-text {
  color: #4682b4;
  font-size: 24px;
  font-weight: bold;
}

.navbar-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  color: #333;
  transition: all 0.2s;
}

.nav-link:hover {
  background-color: #f5f5f5;
}

.nav-link.active {
  background-color: #4682b4;
  color: white;
}

.logout-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
}
</style>
