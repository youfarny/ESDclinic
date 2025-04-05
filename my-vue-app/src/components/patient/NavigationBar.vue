<template>
  <div class="navbar-container">
    <!-- Brand Section -->
    <div class="navbar-brand">
      <router-link to="/patient/dashboard" class="brand-text">SMUDOC</router-link>
    </div>

    <!-- Navigation Links -->
    <div class="navbar-links">
      <router-link 
        to="/patient/dashboard" 
        class="nav-link" 
        :class="{ active: isActive('/patient/dashboard') }"
      >
        Dashboard
      </router-link>
      <router-link 
        to="/patient/book-appointment" 
        class="nav-link" 
        :class="{ active: isActive('/patient/book-appointment') }"
      >
        Book Appointment
      </router-link>
      <router-link 
        to="/patient/appointments" 
        class="nav-link" 
        :class="{ active: isActive('/patient/appointments') }"
      >
        My Appointments
      </router-link>
      <router-link 
        to="/patient/medical-records" 
        class="nav-link" 
        :class="{ active: isActive('/patient/medical-records') }"
      >
        Medical Records
      </router-link>
    </div>

    <!-- Logout Button -->
    <div class="navbar-actions">
      <button class="logout-btn" @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavigationBar',
  methods: {
    // Method to check if a route is active
    isActive(route) {
      return this.$route.path === route;
    },
    
    // Logout method
    logout() {
      // Clear user session (e.g., tokens or role)
      localStorage.removeItem('userRole'); // Example: Clear user role
      this.$router.push('/'); // Redirect to login page
    }
  }
};
</script>

<style scoped>
/* Navbar Container */
.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  padding: 10px 20px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

/* Brand Section */
.navbar-brand .brand-text {
  font-size: 24px;
  font-weight: bold;
  color: #007bff;
  text-decoration: none;
}

/* Navigation Links */
.navbar-links {
  display: flex;
  gap: 15px;
}

.navbar-links .nav-link {
  font-size: 16px;
  color: #333333;
  text-decoration: none;
}

.navbar-links .nav-link:hover {
  color: #007bff;
}

.navbar-links .nav-link.active {
  font-weight: bold;
  color: #007bff;
}

/* Logout Button */
.navbar-actions .logout-btn {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.navbar-actions .logout-btn:hover {
  background-color: #ff7875;
}
</style>





<!-- <template>
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
</style> -->
