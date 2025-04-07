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

const isActive = (path) => {
  return route.path === path || route.path.startsWith(`${path}/`);
};
</script>

<template>
  <div id="app" class="d-flex flex-column align-items-center bg-light min-vh-100">
    <div class="w-100" style="max-width: 430px;">
      <!-- Navigation -->
      <nav v-if="isLoggedIn" class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-3 py-2">
        <div class="container-fluid">
          <span class="navbar-brand text-primary fw-bold">SMUDOC</span>

          <div class="d-flex gap-3 align-items-center">
            <template v-if="userRole === 'patient'">
              <router-link to="/patient" class="nav-link" :class="{ active: isActive('/patient') && route.path === '/patient' }">
                Dashboard
              </router-link>
              <router-link to="/patient/book-appointment" class="nav-link" :class="{ active: isActive('/patient/book-appointment') }">
                Book
              </router-link>
              <router-link to="/patient/appointments" class="nav-link" :class="{ active: isActive('/patient/appointments') }">
                My Appt
              </router-link>
              <router-link to="/patient/medical-records" class="nav-link" :class="{ active: isActive('/patient/medical-records') }">
                Records
              </router-link>
              <router-link to="/patient/about" class="nav-link" :class="{ active: isActive('/patient/about') }">
                About
              </router-link>
            </template>

            <template v-else-if="userRole === 'doctor'">
              <router-link to="/doctor" class="nav-link" :class="{ active: isActive('/doctor') && route.path === '/doctor' }">
                Dashboard
              </router-link>
              <router-link to="/doctor/consultation" class="nav-link" :class="{ active: isActive('/doctor/consultation') }">
                Consultation
              </router-link>
            </template>

            <!-- Uncomment if needed
            <template v-else-if="userRole === 'pharmacist'">
              ...
            </template>
            -->

            <button class="btn btn-danger btn-sm ms-3" @click="logout">Logout</button>
          </div>
        </div>
      </nav>

      <!-- Page content -->
      <main class="p-3">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style scoped>
.nav-link {
  color: #6c757d;
  transition: all 0.3s ease;
}
.nav-link.active {
  font-weight: bold;
  color: #0d6efd !important;
  border-bottom: 2px solid #0d6efd;
}
</style>



<!-- <script setup>
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

    <nav v-if="isLoggedIn" class="navigation-bar">
      <div class="logo">SMUDOC</div>
      
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
      
      <div v-else-if="userRole === 'doctor'" class="nav-links">
        <router-link to="/doctor" class="nav-link" :class="{ active: isActive('/doctor') && route.path === '/doctor' }">
          Dashboard
        </router-link>
        <router-link to="/doctor/consultation" class="nav-link" :class="{ active: isActive('/doctor/consultation') }">
          Consultation
        </router-link>
      </div>
      
  
      
      <button @click="logout" class="logout-btn">Logout</button>
    </nav>

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
</style> -->