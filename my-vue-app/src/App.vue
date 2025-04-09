<template>
  <div id="app">
    <!-- Navigation Bar -->
    <nav v-if="isLoggedIn" class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <router-link to="/doctor" class="navbar-brand">ESD Clinic</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link to="/doctor" class="nav-link" :class="{ active: $route.path === '/doctor' }">
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/doctor/appointments" class="nav-link" :class="{ active: $route.path === '/doctor/appointments' }">
                Appointments
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/doctor/records" class="nav-link" :class="{ active: $route.path === '/doctor/records' }">
                Records
              </router-link>
            </li>
          </ul>
          <div class="d-flex">
            <span class="navbar-text me-3">
              Welcome, Dr. {{ user?.name }}
            </span>
            <button @click="logout" class="btn btn-outline-danger">Logout</button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Loading Spinner -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Error Toast -->
    <div v-if="error" class="toast-container position-fixed top-0 end-0 p-3">
      <div class="toast show" role="alert">
        <div class="toast-header">
          <strong class="me-auto">Error</strong>
          <button type="button" class="btn-close" @click="clearError"></button>
        </div>
        <div class="toast-body">
          {{ error }}
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="container mt-4">
      <transition name="fade" mode="out-in">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </transition>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const user = computed(() => store.getters.getUser)
const isLoggedIn = computed(() => !!user.value)
const isLoading = computed(() => store.getters.isLoading)
const error = computed(() => store.getters.getError)

function logout() {
  store.dispatch('logout')
  router.push('/')
}

function clearError() {
  store.commit('SET_ERROR', null)
}
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: bold;
  color: #0d6efd;
}

.nav-link {
  font-weight: 500;
}

.nav-link.active {
  color: #0d6efd !important;
}

main {
  flex: 1;
}
</style> 