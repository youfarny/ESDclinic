<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to your account
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <!-- Role Selection -->
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Login As</label>
            <div class="flex space-x-4">
              <button
                @click="selectedRole = 'doctor'"
                :class="[
                  'flex-1 py-2 px-4 rounded',
                  selectedRole === 'doctor'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-700'
                ]"
              >
                Doctor
              </button>
              <button
                @click="selectedRole = 'patient'"
                :class="[
                  'flex-1 py-2 px-4 rounded',
                  selectedRole === 'patient'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-700'
                ]"
              >
                Patient
              </button>
            </div>
          </div>

          <!-- ID Input -->
          <div>
            <label for="id" class="sr-only">ID</label>
            <input
              id="id"
              v-model="id"
              name="id"
              type="text"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              :placeholder="selectedRole === 'doctor' ? 'Doctor ID' : 'Patient ID'"
            />
          </div>

          <!-- Password Input -->
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Password"
            />
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="text-red-500 text-sm text-center">
          {{ error }}
        </div>

        <!-- Submit Button -->
        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ isLoading ? 'Signing in...' : 'Sign in' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const selectedRole = ref('doctor')
const id = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')

const handleLogin = async () => {
  try {
    isLoading.value = true
    error.value = ''

    // Here you would typically make an API call to your authentication service
    // For now, we'll simulate a successful login
    const response = {
      token: 'sample-token',
      user: {
        id: id.value,
        role: selectedRole.value
      }
    }

    // Store authentication data
    localStorage.setItem('token', response.token)
    localStorage.setItem('userRole', response.user.role)
    localStorage.setItem(`${response.user.role}Id`, response.user.id)

    // Redirect based on role
    router.push(`/${response.user.role}`)
  } catch (err) {
    error.value = err.message || 'Failed to login. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script> 