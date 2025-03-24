<template>
    <div class="process-container">
      <h1 class="page-title">Process Prescription</h1>
      
      <div class="prescription-details" v-if="prescription">
        <div class="detail-card">
          <h2>Prescription Information</h2>
          <div class="detail-row">
            <span class="label">Prescription ID:</span>
            <span class="value">{{ prescription.id }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Date:</span>
            <span class="value">{{ prescription.date }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Time:</span>
            <span class="value">{{ prescription.time }}</span>
          </div>
        </div>
        
        <div class="detail-card">
          <h2>Patient Information</h2>
          <div class="detail-row">
            <span class="label">Name:</span>
            <span class="value">{{ prescription.patient.name }}</span>
          </div>
          <div class="detail-row">
            <span class="label">ID:</span>
            <span class="value">{{ prescription.patient.id }}</span>
          </div>
          <div class="detail-row">
            <span class="label">DOB:</span>
            <span class="value">{{ prescription.patient.dob }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Contact:</span>
            <span class="value">{{ prescription.patient.contact }}</span>
          </div>
        </div>
        
        <div class="detail-card">
          <h2>Doctor Information</h2>
          <div class="detail-row">
            <span class="label">Name:</span>
            <span class="value">{{ prescription.doctor.name }}</span>
          </div>
          <div class="detail-row">
            <span class="label">ID:</span>
            <span class="value">{{ prescription.doctor.id }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Department:</span>
            <span class="value">{{ prescription.doctor.department }}</span>
          </div>
        </div>
      </div>
      
      <div class="medications">
        <h2>Medications</h2>
        <table>
          <thead>
            <tr>
              <th>Medication</th>
              <th>Dosage</th>
              <th>Frequency</th>
              <th>Duration</th>
              <th>Stock Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(med, index) in prescription.medications" :key="index">
              <td>{{ med.name }}</td>
              <td>{{ med.dosage }}</td>
              <td>{{ med.frequency }}</td>
              <td>{{ med.duration }}</td>
              <td>
                <span :class="{ 'in-stock': med.inStock, 'out-of-stock': !med.inStock }">
                  {{ med.inStock ? 'In Stock' : 'Out of Stock' }}
                </span>
              </td>
              <td>
                <button 
                  :disabled="!med.inStock" 
                  @click="prepareItem(med)" 
                  class="action-btn"
                  :class="{ 'disabled': !med.inStock }"
                >
                  Prepare
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="action-buttons">
        <button @click="completeProcessing" class="complete-btn">Complete Processing</button>
        <button @click="cancelProcessing" class="cancel-btn">Cancel</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ProcessPrescription',
    data() {
      return {
        prescription: {
          id: 'RX123456',
          date: '2025-03-16',
          time: '9:45 AM',
          patient: {
            name: 'John Smith',
            id: 'P123456',
            dob: '1985-06-15',
            contact: '555-123-4567'
          },
          doctor: {
            name: 'Dr. Sarah Chen',
            id: 'D789012',
            department: 'Cardiology'
          },
          medications: [
            {
              name: 'Atorvastatin 20mg',
              dosage: '1 tablet',
              frequency: 'Once daily',
              duration: '30 days',
              inStock: true
            },
            {
              name: 'Metformin 500mg',
              dosage: '1 tablet',
              frequency: 'Twice daily',
              duration: '30 days',
              inStock: true
            },
            {
              name: 'Lisinopril 10mg',
              dosage: '1 tablet',
              frequency: 'Once daily',
              duration: '30 days',
              inStock: false
            }
          ]
        }
      }
    },
    methods: {
      prepareItem(medication) {
        // Logic to prepare medication
        alert(`Preparing ${medication.name}`);
      },
      completeProcessing() {
        // Logic to complete prescription processing
        alert('Prescription processing completed!');
        this.$router.push('/pharmacist/dashboard');
      },
      cancelProcessing() {
        // Logic to cancel prescription processing
        this.$router.push('/pharmacist/dashboard');
      }
    },
    mounted() {
      // Get prescription ID from route params and fetch real data
      const prescriptionId = this.$route.params.id;
      // In a real app, you would fetch the prescription data here
      console.log('Fetching prescription with ID:', prescriptionId);
    }
  }
  </script>
  
  <style scoped>
  .process-container {
    padding: 20px;
  }
  
  .page-title {
    margin-bottom: 20px;
  }
  
  .prescription-details {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
  }
  
  .detail-card {
    background-color: white;
    border-radius: 4px;
    padding: 15px;
    width: 30%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .detail-card h2 {
    color: #3366CC;
    border-bottom: 1px solid #2a1e1e;
    padding-bottom: 10px;
    margin-top: 0;
  }
  
  .detail-row {
  margin: 10px 0;
  display: flex;
  justify-content: space-between;
}

.label {
  font-weight: bold;
  color: #666;
}

.value {
  color: #333;
}

.medications {
  background-color: white;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.medications h2 {
  color: #3366CC;
  margin-top: 0;
  border-bottom: 1px solid #403636;
  padding-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

th {
  background-color: #3366CC;
  color: white;
  padding: 10px;
  text-align: left;
}

td {
  padding: 10px;
  border-bottom: 1px solid #432828;
}

.in-stock {
  color: #4CAF50;
  font-weight: bold;
}

.out-of-stock {
  color: #F44336;
  font-weight: bold;
}

.action-btn {
  background-color: #3366CC;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.action-btn:hover {
  background-color: #2650a5;
}

.action-btn.disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.complete-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.complete-btn:hover {
  background-color: #3e8e41;
}

.cancel-btn {
  background-color: #F44336;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.cancel-btn:hover {
  background-color: #d32f2f;
}
</style>