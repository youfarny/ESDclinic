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
                type="button"
                @click="selectedRole = 'doctor'"
                :class="[ 
                  'flex-1 py-2 px-4 rounded', 
                  selectedRole === 'doctor' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
                ]"
              >
                Doctor
              </button>
              <button
                type="button"
                @click="selectedRole = 'patient'"
                :class="[ 
                  'flex-1 py-2 px-4 rounded', 
                  selectedRole === 'patient' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
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
            :disabled="isLoading || !id || !password"
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
import { useRouter } from 'vue-router'

const router = useRouter()

const selectedRole = ref('doctor')
const id = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')
const handleLogin = async () => {
  try {
    isLoading.value = true;
    error.value = '';

    console.log("Selected Role:", selectedRole.value);

    if (selectedRole.value === 'doctor') {
      // Doctor Authentication logic (existing)
      const response = {
        token: 'sample-doctor-token',
        user: {
          id: id.value,
          role: selectedRole.value
        }
      };

      localStorage.setItem('token', response.token);
      localStorage.setItem('userRole', response.user.role);
      localStorage.setItem(`${response.user.role}Id`, response.user.id);

      router.push(`/doctor/dashboard`);
    } else if (selectedRole.value === 'patient') {
      // Patient Authentication logic
      const patientAuthSuccess = await authenticatePatient(id.value, password.value);
      if (!patientAuthSuccess) {
        error.value = 'Failed to authenticate as patient';
        return;
      }

      // Only store patient data if authentication is successful
      const response = {
        token: 'sample-patient-token',
        user: {
          id: id.value,
          role: selectedRole.value
        }
      };

      localStorage.setItem('token', response.token);
      localStorage.setItem('userRole', response.user.role);
      localStorage.setItem(`${response.user.role}Id`, response.user.id);

      // Store patient data once
      localStorage.setItem('patientData', JSON.stringify(response.user));

      router.push(`/patient/dashboard`);
    } else {
      error.value = 'Invalid role selected';
    }
  } catch (err) {
    error.value = err.message || 'Failed to login. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

const authenticatePatient = async (patient_id, patient_password) => {
  try {
    const res = await fetch(`http://localhost:8000/patient/authenticate/${patient_id}&${patient_password}`, {
      method: 'GET',  // Use 'GET' for sending query parameters
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await res.json();

    if (res.ok) {
      // Store patient details in local storage
      localStorage.setItem('patient', JSON.stringify(data.patient));
      return true;
    } else {
      throw new Error('Authentication failed');
    }
  } catch (err) {
    console.error('Patient login failed:', err);
    return false;
  }
};

</script>
