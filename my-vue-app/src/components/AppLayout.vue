<!-- src/components/AppLayout.vue -->
<template>
  <div class="page-container">
    <nav class="navbar">
      <div class="logo" @click="goToHome">SMUDOC</div>
      <div class="links">
        <!-- Render different navigation links based on user role -->
        <template v-if="isAuthenticated && userRole === 'patient'">
          <router-link to="/patient/dashboard">Dashboard</router-link>
          <router-link to="/patient/book-appointment">Book Appointment</router-link>
          <router-link to="/patient/my-appointments">My Appointments</router-link>
          <router-link to="/patient/medical-records">Medical Records</router-link>
          <router-link to="/patient/about">About</router-link>
        </template>

        <template v-else-if="isAuthenticated && userRole === 'doctor'">
          <router-link to="/doctor/dashboard">Dashboard</router-link>
          <router-link to="/doctor/consultation">Consultations</router-link>
          <router-link to="/doctor/about">About</router-link>
        </template>

        <!-- <template v-else-if="isAuthenticated && userRole === 'pharmacist'">
          <router-link to="/pharmacist/dashboard">Dashboard</router-link>
          <router-link to="/pharmacist/inventory">Inventory</router-link>
          <router-link to="/pharmacist/prescriptions">Prescriptions</router-link>
          <router-link to="/pharmacist/about">About</router-link>
        </template> -->

        <template v-else>
          <router-link to="/">Home</router-link>
          <router-link to="/about">About</router-link>
        </template>

        <button v-if="isAuthenticated" class="logout-btn" @click="logout">Logout</button>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="content-card">
      <slot></slot>
    </div>

    <!-- Footer -->
    <footer class="app-footer">
      <p>&copy; {{ currentYear }} SMUDOC Online Consultation. All rights reserved.</p>
      <div class="footer-links">
        <router-link to="/about">About</router-link>
        <router-link to="/contact">Contact</router-link>
        <router-link to="/">Home</router-link>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentYear: new Date().getFullYear()
    };
  },
  computed: {
    isAuthenticated() {
      return localStorage.getItem('isAuthenticated') === 'true';
    },
    userRole() {
      return localStorage.getItem('userRole') || '';
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userRole');
      this.$router.push('/');
    },
    goToHome() {
      if (this.isAuthenticated) {
        this.$router.push(`/${this.userRole}/dashboard`);
      } else {
        this.$router.push('/');
      }
    }
  }
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* Ensures full height of viewport */
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #ffffff;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
}

.links {
  display: flex;
  gap: 1rem;
}

.links a {
  text-decoration: none;
  color: #333;
}

.logout-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.content-card {
  flex-grow: 1; /* Fills remaining space between navbar and footer */
  display: flex;
  justify-content: center; /* Centers content horizontally */
  align-items: center; /* Centers content vertically */
}

.app-footer {
  text-align: center;
  padding: 1rem;
  background-color: #34495e;
  color: white;
}

.footer-links {
  display: flex;
  justify-content: center;
}
.footer-links a {
  color: #ddd;
}
.footer-links a:hover {
  color: white;
}
</style>
