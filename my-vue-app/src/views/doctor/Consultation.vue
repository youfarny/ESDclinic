<!-- src/views/doctor/Consultation.vue -->
<template>
    <div class="consultation-container">
      <doctor-navigation />
      
      <div class="content">
        <h1>Doctor Consultation</h1>
        
        <div v-if="!isConsultationEnded">
          <div class="appointment-details">
            <div class="info-card">
              <h2>Appointment Details</h2>
              <div class="patient-info">
                <div class="patient-avatar"></div>
                <div class="patient-details">
                  <h3>{{ patientDetails.name }}</h3>
                  <p><strong>Age:</strong> {{ patientDetails.age }} years</p>
                  <p><strong>Medical ID:</strong> {{ patientDetails.medicalId }}</p>
                </div>
              </div>
              
              <div class="consultation-reason">
                <h3>Reason for Consultation</h3>
                <p>{{ patientDetails.consultationReason }}</p>
              </div>
              
              <div class="medical-history">
                <h3>Medical History</h3>
                <ul>
                  <li v-for="(item, index) in patientDetails.medicalHistory" :key="index">
                    {{ item }}
                  </li>
                </ul>
              </div>
            </div>
            
            <div class="video-card">
              <h2>Video Consultation</h2>
              <div class="video-container">
                <div class="video-placeholder">
                  <span>Video feed will appear here</span>
                </div>
                <div class="video-controls">
                  <button class="control-btn">
                    <i class="mic-icon"></i>
                  </button>
                  <button class="control-btn">
                    <i class="camera-icon"></i>
                  </button>
                  <button class="control-btn">
                    <i class="screen-icon"></i>
                  </button>
                  <button class="control-btn" @click="endConsultation">
                    <i class="end-call-icon"></i> End
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="recommendations-card" v-if="showRecommendations">
            <h2>Appointment Recommendations</h2>
            <div class="recommendations-content">
              <p><strong>Based on patient symptoms:</strong></p>
              <ul>
                <li v-for="(rec, index) in recommendations" :key="index">
                  {{ rec }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div v-else class="end-consultation-form">
          <h2>Complete Consultation</h2>
          <div class="form-card">
            <div class="form-group">
              <label for="diagnosis">Diagnosis</label>
              <textarea 
                id="diagnosis" 
                v-model="diagnosis" 
                rows="3" 
                placeholder="Enter your diagnosis..."
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="prescription">Prescription</label>
              <textarea 
                id="prescription" 
                v-model="prescription" 
                rows="5" 
                placeholder="Enter prescription details..."
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="followUp">Follow-up Recommendations</label>
              <textarea 
                id="followUp" 
                v-model="followUp" 
                rows="3" 
                placeholder="Enter follow-up instructions if needed..."
              ></textarea>
            </div>
            
            <div class="action-buttons">
              <button class="secondary-btn" @click="isConsultationEnded = false">
                Back to Consultation
              </button>
              <button class="primary-btn" @click="submitConsultation">
                Complete & Submit
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="isSubmitted" class="confirmation-message">
          <h3>Consultation Completed Successfully!</h3>
          <p>The patient has been notified and prescription details have been forwarded to the pharmacy.</p>
          <button class="primary-btn" @click="returnToDashboard">
            Return to Dashboard
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import DoctorNavigation from '../../components/doctor/NavigationBar.vue'
  
  export default {
    name: 'DoctorConsultation',
    components: {
      DoctorNavigation
    },
    data() {
      return {
        isConsultationEnded: false,
        isSubmitted: false,
        showRecommendations: false,
        patientDetails: {
          name: 'John Smith',
          age: 35,
          medicalId: 'P-23456',
          consultationReason: 'Persistent fever for 3 days with headache and fatigue.',
          medicalHistory: [
            'Hypertension (diagnosed 2020)',
            'Allergic to penicillin',
            'Previous appendectomy (2018)'
          ]
        },
        recommendations: [
          'Consider blood tests to rule out infection',
          'Check for signs of dehydration',
          'Potential diagnoses: viral infection, flu, early signs of COVID-19',
          'Recommended medication: acetaminophen for fever'
        ],
        diagnosis: '',
        prescription: '',
        followUp: ''
      }
    },
    mounted() {
      // Simulate API call to get recommendations
      setTimeout(() => {
        this.showRecommendations = true
      }, 2000)
    },
    methods: {
      endConsultation() {
        this.isConsultationEnded = true
      },
      submitConsultation() {
        // In a real app, you would submit this data to your API
        console.log('Diagnosis:', this.diagnosis)
        console.log('Prescription:', this.prescription)
        console.log('Follow-up:', this.followUp)
        
        // Show confirmation
        this.isSubmitted = true
      },
      returnToDashboard() {
        this.$router.push('/doctor')
      }
    }
  }
  </script>
  
  <style scoped>
  .consultation-container {
    min-height: 100vh;
    background-color: #d1eef3;
  }


  .content {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .appointment-details {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-top: 1.5rem;
  }
  
  @media (max-width: 768px) {
    .appointment-details {
      grid-template-columns: 1fr;
    }
  }
  
  .info-card, .video-card, .recommendations-card, .form-card {
    background-color: #536b7b;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    margin-bottom: 1.5rem;
  }
  
  .patient-info {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
  }
  
  .patient-avatar {
    width: 80px;
    height: 80px;
    background-color: #4c5566;
    border-radius: 50%;
    margin-right: 1rem;
  }
  
  .consultation-reason, .medical-history {
    margin-top: 1.5rem;
  }
  
  .medical-history ul {
    margin-left: 1.5rem;
  }
  
  .medical-history li {
    margin-bottom: 0.5rem;
  }
  
  .video-container {
    margin-top: 1rem;
  }
  
  .video-placeholder {
    height: 300px;
    background-color: #1f2937;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }
  
  .video-controls {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .control-btn {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #8b9ec5;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  
  .control-btn:last-child {
    background-color: #ef4444;
    color: white;
    width: auto;
    padding: 0 1.5rem;
    border-radius: 25px;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  
  textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    font-family: inherit;
    resize: vertical;
  }
  
  .action-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
  }
  
  .primary-btn, .secondary-btn {
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
  }
  
  .primary-btn {
    background-color: #4f46e5;
    color: white;
    border: none;
  }
  
  .secondary-btn {
    background-color: white;
    color: #111827;
    border: 1px solid #e5e7eb;
  }
  
  .confirmation-message {
    margin-top: 2rem;
    padding: 1.5rem;
    background-color: #ecfdf5;
    border: 1px solid #10b981;
    border-radius: 8px;
    text-align: center;
  }
  
  .confirmation-message h3 {
    color: #047857;
    margin-bottom: 0.5rem;
  }
  
  .confirmation-message button {
    margin-top: 1rem;
  }
  </style>