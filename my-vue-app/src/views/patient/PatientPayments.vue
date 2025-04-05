<template>
    <div>
      <h1>Appointments</h1>
      <ul>
        <li v-for="appointment in appointments" :key="appointment.id">
          {{ appointment.name }} - {{ appointment.date }}
          <button @click="proceedToPay(appointment)">Proceed to Pay</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        appointments: [
          { id: 1, name: 'Appointment 1', date: '2023-04-01' },
          { id: 2, name: 'Appointment 2', date: '2023-04-15' },
          // Add more appointments here or fetch from backend
        ]
      }
    },
    methods: {
      proceedToPay(appointment) {
        // Send request to Flask backend to create a checkout session
        axios.post('http://localhost:5200/create-checkout-session', {
          appointment_id: appointment.id,
          amount: 5000 // Example amount
        })
        .then(response => {
          // Handle redirect to Stripe checkout
          window.open(response.data.url, '_blank');
        })
        .catch(error => console.error('Error:', error));
      }
    }
  }
  </script>
  