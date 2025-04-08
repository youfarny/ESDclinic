<template>
    <div class="container mx-auto p-6">
      <h1 class="text-2xl font-bold mb-4">My Appointments</h1>
  
      <!-- New Appointment Form -->
      <div class="bg-white shadow p-4 rounded mb-8">
        <h2 class="text-lg font-semibold mb-2">Create New Appointment</h2>
        <div class="space-y-4">
          <input
            v-model="form.doctor_id"
            type="number"
            placeholder="Doctor ID"
            class="w-full p-2 border rounded"
          />
          <textarea
            v-model="form.symptoms"
            placeholder="Describe your symptoms"
            class="w-full p-2 border rounded"
          ></textarea>
          <button
            @click="createAppointment"
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Book Appointment
          </button>
        </div>
      </div>
  
      <!-- Appointments List -->
      <div>
        <h2 class="text-lg font-semibold mb-4">Your Appointment History</h2>
        <div v-if="loading" class="text-center text-gray-500">Loading...</div>
        <div v-else-if="error" class="text-red-500">{{ error }}</div>
        <div v-else-if="appointments.length === 0" class="text-gray-500">No appointments found.</div>
        <div v-else class="space-y-4">
          <div
            v-for="appt in appointments"
            :key="appt.appointment_id"
            class="border p-4 rounded bg-white shadow"
          >
            <p><strong>Appointment ID:</strong> {{ appt.appointment_id }}</p>
            <p><strong>Doctor ID:</strong> {{ appt.doctor_id }}</p>
            <p><strong>Symptoms:</strong> {{ appt.patient_symptoms?.description || 'N/A' }}</p>
            <p><strong>Start Time:</strong> {{ appt.start_time || 'Not started' }}</p>
            <p><strong>End Time:</strong> {{ appt.end_time || 'Not ended' }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "PatientAppointments",
    data() {
      return {
        patientId: 1, // TEMP: Replace with actual logged-in patient ID
        form: {
          doctor_id: "",
          symptoms: "",
        },
        appointments: [],
        loading: false,
        error: "",
      };
    },
    methods: {
      async fetchAppointments() {
        this.loading = true;
        try {
          const res = await axios.get(
            `http://116.15.73.191:5100/appointment/records/${this.patientId}`
          );
          this.appointments = res.data;
          this.error = "";
        } catch (err) {
          this.error = "Failed to load appointments.";
        } finally {
          this.loading = false;
        }
      },
      async createAppointment() {
        try {
          const res = await axios.post(
            "http://116.15.73.191:5100/appointment/new",
            {
              patient_id: this.patientId,
              doctor_id: Number(this.form.doctor_id),
              patient_symptoms: { description: this.form.symptoms },
            }
          );
          alert("Appointment created! ID: " + res.data.appointment_id);
          this.form = { doctor_id: "", symptoms: "" };
          this.fetchAppointments(); // Refresh list
        } catch (err) {
          alert("Failed to create appointment.");
          console.error(err);
        }
      },
    },
    mounted() {
      this.fetchAppointments();
    },
  };
  </script>
  
  <style scoped>
  textarea {
    resize: vertical;
  }
  </style>
  