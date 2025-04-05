<template>
  <div class="consultation-records-container">
    <doctor-navigation />
    
    <div class="content">
      <h1>Completed Consultation Records</h1>
      
      <div class="filter-bar">
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search by patient name or ID..." />
          <button class="search-btn" @click="searchRecords">Search</button>
        </div>
        <div class="date-filter">
          <label>Date Range:</label>
          <input type="date" v-model="startDate" />
          <span>to</span>
          <input type="date" v-model="endDate" />
          <button class="filter-btn" @click="filterByDate">Apply Filter</button>
        </div>
      </div>
      
      <div class="consultations-list">
        <table class="consultation-table">
          <thead>
            <tr>
              <th>Appt. ID</th>
              <th>Date</th>
              <th>Time</th>
              <th>Patient ID</th>
              <th>Patient Name</th>
              <th>Age/Gender</th>
              <th>Diagnosis</th>
              <th>Prescription</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in completedConsultations" :key="record.id">
              <td>{{ record.appointment_id }}</td>
              <td>{{ record.date }}</td>
              <td>{{ record.start_time }} - {{ record.end_time }}</td>
              <td>{{ record.patient_id }}</td>
              <td>{{ record.patient_name }}</td>
              <td>{{ record.patient_age }}y/{{ record.patient_gender }}</td>
              <td class="diagnosis-cell">{{ record.diagnosis }}</td>
              <td class="prescription-cell">
                <span class="prescription-id">ID: {{ record.prescription_id }}</span>
                <span class="prescription-details">{{ record.prescription_details }}</span>
              </td>
              <td>
                <button class="view-btn" @click="viewConsultation(record.appointment_id)">View Details</button>
                <button class="print-btn" @click="printRecord(record.appointment_id)">Print</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="currentPage--">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="currentPage++">Next</button>
      </div>
    </div>
    
    <!-- Detailed View Modal -->
    <div v-if="showDetailModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Consultation Details</h2>
          <button class="close-btn" @click="showDetailModal = false">&times;</button>
        </div>
        <div class="modal-body" v-if="selectedConsultation">
          <div class="detail-section">
            <h3>Appointment Information</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="label">Appointment ID:</span>
                <span class="value">{{ selectedConsultation.appointment_id }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Date:</span>
                <span class="value">{{ selectedConsultation.date }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Start Time:</span>
                <span class="value">{{ selectedConsultation.start_time }}</span>
              </div>
              <div class="detail-item">
                <span class="label">End Time:</span>
                <span class="value">{{ selectedConsultation.end_time }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Duration:</span>
                <span class="value">{{ selectedConsultation.duration }} minutes</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h3>Patient Information</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="label">Patient ID:</span>
                <span class="value">{{ selectedConsultation.patient_id }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Name:</span>
                <span class="value">{{ selectedConsultation.patient_name }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Age:</span>
                <span class="value">{{ selectedConsultation.patient_age }} years</span>
              </div>
              <div class="detail-item">
                <span class="label">Gender:</span>
                <span class="value">{{ selectedConsultation.patient_gender }}</span>
              </div>
              <div class="detail-item">
                <span class="label">Contact:</span>
                <span class="value">{{ selectedConsultation.patient_contact }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h3>Medical Details</h3>
            <div class="detail-item full-width">
              <span class="label">Chief Complaint:</span>
              <span class="value">{{ selectedConsultation.chief_complaint }}</span>
            </div>
            <div class="detail-item full-width">
              <span class="label">Symptoms:</span>
              <span class="value">{{ selectedConsultation.symptoms }}</span>
            </div>
            <div class="detail-item full-width">
              <span class="label">Diagnosis:</span>
              <span class="value">{{ selectedConsultation.diagnosis }}</span>
            </div>
            <div class="detail-item full-width">
              <span class="label">Treatment Plan:</span>
              <span class="value">{{ selectedConsultation.treatment_plan }}</span>
            </div>
          </div>
          
          <div class="detail-section">
            <h3>Prescription</h3>
            <div class="detail-item">
              <span class="label">Prescription ID:</span>
              <span class="value">{{ selectedConsultation.prescription_id }}</span>
            </div>
            <div class="detail-item full-width">
              <span class="label">Medications:</span>
              <div class="medication-list">
                <div v-for="med in selectedConsultation.medications" :key="med.id" class="medication-item">
                  <strong>{{ med.name }}</strong> - {{ med.dosage }}, {{ med.frequency }}
                  <div class="med-instructions">{{ med.instructions }}</div>
                </div>
              </div>
            </div>
            <div class="detail-item full-width">
              <span class="label">Special Instructions:</span>
              <span class="value">{{ selectedConsultation.prescription_notes }}</span>
            </div>
          </div>
          
          <div class="modal-footer">
            <button class="action-btn print" @click="printRecord(selectedConsultation.appointment_id)">Print Record</button>
            <button class="action-btn close" @click="showDetailModal = false">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DoctorNavigation from '../../components/doctor/DocNavigationBar.vue'

export default {
  name: 'CompletedConsultations',
  components: {
    DoctorNavigation
  },
  data() {
    return {
      searchQuery: '',
      startDate: '',
      endDate: '',
      currentPage: 1,
      totalPages: 5,
      showDetailModal: false,
      selectedConsultation: null,
      completedConsultations: [
        {
          appointment_id: 'APT-2025-0401',
          date: '2025-04-01',
          start_time: '09:00',
          end_time: '09:25',
          duration: 25,
          patient_id: 'PT-10045',
          patient_name: 'Emily Johnson',
          patient_age: 34,
          patient_gender: 'F',
          patient_contact: '555-123-4567',
          chief_complaint: 'Annual checkup',
          symptoms: 'None reported',
          diagnosis: 'Healthy, no concerns',
          treatment_plan: 'Continue regular health maintenance',
          prescription_id: 'RX-5692',
          prescription_details: 'Multivitamin (daily)',
          prescription_notes: 'Take with food',
          medications: [
            { id: 1, name: 'Multivitamin', dosage: '1 tablet', frequency: 'Once daily', instructions: 'Take with breakfast' }
          ]
        },
        {
          appointment_id: 'APT-2025-0401-2',
          date: '2025-04-01',
          start_time: '10:30',
          end_time: '11:00',
          duration: 30,
          patient_id: 'PT-10089',
          patient_name: 'Michael Wong',
          patient_age: 45,
          patient_gender: 'M',
          patient_contact: '555-789-0123',
          chief_complaint: 'Persistent cough',
          symptoms: 'Dry cough for 2 weeks, mild fatigue',
          diagnosis: 'Acute bronchitis',
          treatment_plan: 'Rest, hydration, medication for symptom relief',
          prescription_id: 'RX-5693',
          prescription_details: 'Dextromethorphan, Amoxicillin',
          prescription_notes: 'Complete full course of antibiotics',
          medications: [
            { id: 1, name: 'Dextromethorphan', dosage: '10mg', frequency: 'Every 4-6 hours as needed', instructions: 'For cough relief' },
            { id: 2, name: 'Amoxicillin', dosage: '500mg', frequency: 'Three times daily', instructions: 'Take for 7 days without missing any doses' }
          ]
        },
        {
          appointment_id: 'APT-2025-0402',
          date: '2025-04-02',
          start_time: '14:15',
          end_time: '14:40',
          duration: 25,
          patient_id: 'PT-10124',
          patient_name: 'Sarah Williams',
          patient_age: 28,
          patient_gender: 'F',
          patient_contact: '555-456-7890',
          chief_complaint: 'Allergy consultation',
          symptoms: 'Seasonal sneezing, itchy eyes, runny nose',
          diagnosis: 'Seasonal allergic rhinitis',
          treatment_plan: 'Allergen avoidance, medication for symptom control',
          prescription_id: 'RX-5701',
          prescription_details: 'Cetirizine, Fluticasone nasal spray',
          prescription_notes: 'Use as needed during high pollen seasons',
          medications: [
            { id: 1, name: 'Cetirizine', dosage: '10mg', frequency: 'Once daily', instructions: 'Take in the morning' },
            { id: 2, name: 'Fluticasone nasal spray', dosage: '1 spray per nostril', frequency: 'Twice daily', instructions: 'Use regularly for best results' }
          ]
        },
        {
          appointment_id: 'APT-2025-0403',
          date: '2025-04-03',
          start_time: '11:30',
          end_time: '12:00',
          duration: 30,
          patient_id: 'PT-10256',
          patient_name: 'Robert Garcia',
          patient_age: 62,
          patient_gender: 'M',
          patient_contact: '555-234-5678',
          chief_complaint: 'Blood pressure check',
          symptoms: 'Occasional dizziness, headaches',
          diagnosis: 'Hypertension - moderate, controlled',
          treatment_plan: 'Continue medication, lifestyle modifications, follow-up in 3 months',
          prescription_id: 'RX-5710',
          prescription_details: 'Lisinopril, Hydrochlorothiazide',
          prescription_notes: 'Continue taking as prescribed',
          medications: [
            { id: 1, name: 'Lisinopril', dosage: '10mg', frequency: 'Once daily', instructions: 'Take in the morning' },
            { id: 2, name: 'Hydrochlorothiazide', dosage: '12.5mg', frequency: 'Once daily', instructions: 'Take with lisinopril' }
          ]
        }
      ]
    }
  },
  methods: {
    searchRecords() {
      // Logic to filter records based on search query
      alert(`Searching for: ${this.searchQuery}`)
      // In a real app, you would filter the records or make an API call
    },
    filterByDate() {
      // Logic to filter records by date range
      alert(`Filtering from ${this.startDate} to ${this.endDate}`)
      // In a real app, you would filter the records or make an API call
    },
    viewConsultation(id) {
      // Find the consultation record and show details
      this.selectedConsultation = this.completedConsultations.find(
        consultation => consultation.appointment_id === id
      )
      this.showDetailModal = true
    },
    printRecord(id) {
      // Logic to print the record
      alert(`Printing record for appointment ${id}`)
      // In a real app, you would generate a PDF or use window.print()
    }
  }
}
</script>

<style scoped>
.consultation-records-container {
  min-height: 100vh;
  background-color: #d1eef3;
}

.content {
  padding: 2rem;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
}

.search-box input {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  width: 300px;
}

.date-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-filter input {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
}

.search-btn, .filter-btn {
  padding: 0.5rem 1rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.consultations-list {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.consultation-table {
  width: 100%;
  border-collapse: collapse;
}

.consultation-table th, 
.consultation-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.consultation-table th {
  background-color: #f9fafb;
  font-weight: 600;
}

.diagnosis-cell, .prescription-cell {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.prescription-cell {
  display: flex;
  flex-direction: column;
}

.prescription-id {
  font-size: 0.8rem;
  color: #6b7280;
}

.view-btn, .print-btn {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
  font-size: 0.85rem;
}

.view-btn {
  background-color: #4f46e5;
  color: white;
}

.print-btn {
  background-color: #10b981;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
  gap: 1rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.detail-section {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 1.5rem;
}

.detail-section h3 {
  margin-bottom: 1rem;
  color: #4f46e5;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.label {
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.medication-list {
  margin-top: 0.5rem;
}

.medication-item {
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  background-color: #f9fafb;
  border-radius: 4px;
}

.med-instructions {
  margin-top: 0.5rem;
  font-style: italic;
  color: #6b7280;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.action-btn.print {
  background-color: #10b981;
  color: white;
}

.action-btn.close {
  background-color: #6b7280;
  color: white;
}
</style>