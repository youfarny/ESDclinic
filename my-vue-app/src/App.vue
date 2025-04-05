<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';

const store = useStore();
const router = useRouter();
const route = useRoute();

const user = computed(() => store.getters.getUser);
const isLoggedIn = computed(() => !!user.value);
const userRole = computed(() => user.value?.role || localStorage.getItem('userRole') || '');

function logout() {
  store.dispatch('logout');
  localStorage.removeItem('userRole');
  router.push('/');
}

// Check if a route is active or not
const isActive = (path) => {
  return route.path === path || route.path.startsWith(`${path}/`);
};
</script>

<template>
  <div id="app">
    <!-- Navigation Bar - shows different links based on role -->
    <nav v-if="isLoggedIn" class="navigation-bar">
      <div class="logo">SMUDOC</div>
      
      <!-- Patient Navigation -->
      <div v-if="userRole === 'patient'" class="nav-links">
        <router-link to="/patient" class="nav-link" :class="{ active: isActive('/patient') && route.path === '/patient' }">
          Dashboard
        </router-link>
        <router-link to="/patient/book-appointment" class="nav-link" :class="{ active: isActive('/patient/book-appointment') }">
          Book Appointment
        </router-link>
        <router-link to="/patient/appointments" class="nav-link" :class="{ active: isActive('/patient/appointments') }">
          My Appointments
        </router-link>
        <router-link to="/patient/medical-records" class="nav-link" :class="{ active: isActive('/patient/medical-records') }">
          Medical Records
        </router-link>
        <router-link to="/patient/about" class="nav-link" :class="{ active: isActive('/patient/about') }">
          About
        </router-link>
      </div>
      
      <!-- Doctor Navigation -->
      <div v-else-if="userRole === 'doctor'" class="nav-links">
        <router-link to="/doctor" class="nav-link" :class="{ active: isActive('/doctor') && route.path === '/doctor' }">
          Dashboard
        </router-link>
        <router-link to="/doctor/consultation" class="nav-link" :class="{ active: isActive('/doctor/consultation') }">
          Consultation
        </router-link>
      </div>
      
      <!-- Pharmacist Navigation
      <div v-else-if="userRole === 'pharmacist'" class="nav-links">
        <router-link to="/pharmacist" class="nav-link" :class="{ active: isActive('/pharmacist') && route.path === '/pharmacist' }">
          Dashboard
        </router-link>
        <router-link to="/pharmacist/inventory" class="nav-link" :class="{ active: isActive('/pharmacist/inventory') }">
          Inventory
        </router-link>
        <router-link to="/pharmacist/process" class="nav-link" :class="{ active: isActive('/pharmacist/process') }">
          Process Prescriptions
        </router-link>
        <router-link to="/pharmacist/about" class="nav-link" :class="{ active: isActive('/pharmacist/about') }">
          About
        </router-link>
      </div> -->
      
      <button @click="logout" class="logout-btn">Logout</button>
    </nav>

    <!-- Dynamic page content -->
    <router-view></router-view>
  </div>
</template>

<style scoped>
#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.navigation-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #4f46e5;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: #4b5563;
  padding: 0.5rem 0;
  transition: color 0.3s ease, border-bottom 0.3s ease;
  border-bottom: 2px solid transparent;
}

.nav-link:hover {
  color: #4f46e5;
}

.nav-link.active {
  color: #4f46e5;
  font-weight: bold;
  border-bottom: 2px solid #4f46e5;
}

.logout-btn {
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #dc2626;
}
</style>