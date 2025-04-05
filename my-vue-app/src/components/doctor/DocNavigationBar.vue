<template>
  <nav class="navbar">
    <!-- Logo Section -->
    <div class="logo">
      <router-link to="/doctor/dashboard" class="logo-text">SMUDOC</router-link>
    </div>
    
    <!-- Navigation Links -->
    <div class="nav-links">
      <router-link to="/doctor/dashboard" class="nav-link" active-class="active">Dashboard</router-link>
      <router-link to="/doctor/consultation" class="nav-link" active-class="active">Consultation</router-link>
      <router-link to="/doctor/pending-appointments" class="nav-link" active-class="active">Appointments</router-link>
      <router-link to="/doctor/consultation-records" class="nav-link" active-class="active">Records</router-link>

    </div>
    
    <!-- User Menu -->
    <div class="user-menu">
      <span class="username">{{ doctorName }}</span>
      <button @click="logout" class="logout-btn">Logout</button>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'DoctorNavigationBar',
  data() {
    return {
      doctorName: 'Dr. Sarah Chen' // You can dynamically fetch this from Vuex or localStorage
    };
  },
  methods: {
    // Check if a route is active
    isActive(route) {
      return this.$route.path === route;
    },
    
    // Logout method
    logout() {
      localStorage.removeItem('userRole'); // Clear user role
      localStorage.removeItem('isAuthenticated'); // Clear authentication status
      this.$router.push('/'); // Redirect to login page
    }
  }
};
</script>

<style scoped>
/* Navbar Container */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  padding: 10px 20px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

/* Logo Section */
.logo .logo-text {
  font-size: 24px;
  font-weight: bold;
  color: #007bff;
  text-decoration: none;
}

/* Navigation Links */
.nav-links {
  display: flex;
  gap: 15px;
}

.nav-links .nav-link {
  font-size: 16px;
  color: #333333;
  text-decoration: none;
}

.nav-links .nav-link:hover {
  color: #007bff;
}

.nav-links .nav-link.active {
  font-weight: bold;
  color: #007bff;
}

/* User Menu */
.user-menu {
  display: flex;
  align-items: center;
}

.user-menu .username {
  margin-right: 15px;
}

.logout-btn {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
}

.logout-btn:hover {
  background-color: #ff7875;
}
</style>



<!-- src/components/doctor/NavigationBar.vue
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
  </style> -->

