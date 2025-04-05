<!-- src/views/Login.vue -->
<template>
    <div class="page-container">
      <div class="content-card login-card">
        <h1 class="text-center text-2xl mb-6">SMUDOC Online Consultation</h1>
          <div class="tabs">
          <button 
            :class="['tab', { 'active': activeTab === 'patient' }]" 
            @click="activeTab = 'patient'"
          >
            Patient
          </button>
          <button 
            :class="['tab', { 'active': activeTab === 'doctor' }]" 
            @click="activeTab = 'doctor'"
          >
            Doctor
        </button>
        </div>
        
        <form @submit.prevent="handleLogin" class="mt-6">
          <div class="form-group">
            <label for="username">Username/Email</label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              required 
              placeholder="Enter your username"
            />
          </div>
          
          <div class="form-group">
            <label for="password">Password</label>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              required 
              placeholder="Enter your password"
            />
          </div>
          
          <button type="submit" class="login-button">Login</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Login',
    data() {
      return {
        activeTab: 'patient',
        username: '',
        password: ''
      }
    },
    methods: {
      handleLogin() {
        // In a real app, you would validate credentials against your API
        localStorage.setItem('userRole', this.activeTab)
        localStorage.setItem('isAuthenticated', 'true')
        
        // Redirect based on user type
        this.$router.push(`/${this.activeTab}`)
      }
    }
  }
  </script>
  
  <style scoped>
  
  .login-card {
    width: 400px;
    padding: 2rem;
    background-color: #536b7b;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
 /* In your Login.vue component's scoped styles */
.tabs {
  display: flex;
  width: 100%;
  border-bottom: 1px solid #554e4e;
  margin-bottom: 1.5rem;
}

.tab {
  flex: 1;
  padding: 0.75rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #333333;
  color: white;
  border-radius: 4px 4px 0 0;
}

.tab.active {
  background-color: #4f46e5;
  color: white;
  font-weight: 600;
}

/* Form styling */
form {
  width: 100%;
}

.form-group {
  margin-bottom: 1.25rem;
  width: 100%;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: white;
  text-align: left;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  box-sizing: border-box; /* Important - ensures padding doesn't increase width */
  background-color: #333333;
  color: white;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #46455f;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 1rem;
}

.login-button:hover {
  background-color: #4338ca;
}

/* Add this to make title text centered and properly sized */
h1 {
  color: white;
  margin-bottom: 1.5rem;
  text-align: center;
  width: 100%;
}
  </style>



