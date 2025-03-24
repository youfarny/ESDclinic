<template>
    <div class="about-container">
      <h1 class="page-title">About SMUDOC Pharmacy System</h1>
      
      <div class="about-content">
        <Card title="About the System">
          <p>SMUDOC Pharmacy Management System is designed to streamline pharmacy operations, manage prescriptions, track inventory, and improve patient care.</p>
          <p>This system helps pharmacists efficiently process prescriptions, monitor medication inventory, and provide better service to patients.</p>
        </Card>
        
        <Card title="Features">
          <ul class="feature-list">
            <li>
              <div class="feature-icon">
                <i class="fas fa-prescription"></i>
              </div>
              <div class="feature-info">
                <h4>Prescription Management</h4>
                <p>Process and track patient prescriptions efficiently.</p>
              </div>
            </li>
            <li>
              <div class="feature-icon">
                <i class="fas fa-pills"></i>
              </div>
              <div class="feature-info">
                <h4>Inventory Control</h4>
                <p>Monitor medication stock levels and receive alerts for low inventory.</p>
              </div>
            </li>
            <li>
              <div class="feature-icon">
                <i class="fas fa-user-md"></i>
              </div>
              <div class="feature-info">
                <h4>Doctor Communication</h4>
                <p>Easily communicate with prescribing doctors regarding patient medications.</p>
              </div>
            </li>
            <li>
              <div class="feature-icon">
                <i class="fas fa-chart-bar"></i>
              </div>
              <div class="feature-info">
                <h4>Reporting</h4>
                <p>Generate reports on dispensed medications, inventory, and more.</p>
              </div>
            </li>
          </ul>
        </Card>
        
        <Card title="System Requirements">
          <div class="requirements">
            <div class="req-item">
              <h4>Browser</h4>
              <p>Chrome, Firefox, Safari, Edge (latest versions)</p>
            </div>
            <div class="req-item">
              <h4>Internet Connection</h4>
              <p>Minimum 2 Mbps broadband connection</p>
            </div>
            <div class="req-item">
              <h4>Screen Resolution</h4>
              <p>Minimum 1280x720 pixels</p>
            </div>
          </div>
        </Card>
        
        <Card title="Contact Support">
          <div class="support-info">
            <p>For technical assistance, please contact:</p>
            <p><strong>Email:</strong> support@smudoc.com</p>
            <p><strong>Phone:</strong> (555) 123-4567</p>
            <p><strong>Hours:</strong> Monday - Friday, 8:00 AM - 6:00 PM</p>
          </div>
        </Card>
      </div>
    </div>
  </template>
  
  <script>
  import Card from '../../components/Card.vue';
  
  export default {
    name: 'About',
    components: {
      Card
    }
  }
  </script>
  
  <style scoped>
  .about-container {
    padding: 20px;
  }
  
  .page-title {
    margin-bottom: 20px;
  }
  
  .about-content {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .feature-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .feature-list li {
    display: flex;
    margin-bottom: 20px;
    align-items: flex-start;
  }
  
  .feature-icon {
    font-size: 2rem;
    color: #3366CC;
    margin-right: 15px;
    min-width: 40px;
    text-align: center;
  }
  
  .feature-info h4 {
    margin-top: 0;
    margin-bottom: 5px;
    color: #2c3e50;
  }
  
  .feature-info p {
    margin: 0;
    color: #666;
  }
  
  .requirements {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .req-item {
    flex: 1;
    min-width: 200px;
  }
  
  .req-item h4 {
    margin-top: 0;
    color: #2c3e50;
    border-bottom: 2px solid #3366CC;
    padding-bottom: 5px;
  }
  
  .support-info p {
    margin: 10px 0;
  }
  </style>