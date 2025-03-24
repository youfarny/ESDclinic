<!-- src/views/pharmacist/NavigationBar.vue -->
<template>
    <div class="navigation-view">
      <pharmacist-navigation-bar 
        :username="currentUser.name"
        :userAvatar="currentUser.avatar"
        @logout="handleLogout"
      />
      
      <div class="content-wrapper">
        <div class="page-header">
          <h1>{{ pageTitle }}</h1>
          <p class="breadcrumb">Pharmacist / {{ currentRoute }}</p>
        </div>
        
        <div class="quick-actions">
          <button class="action-btn" @click="openNewPrescription">
            <i class="icon-prescription"></i> New Prescription
          </button>
          <button class="action-btn" @click="openInventoryCheck">
            <i class="icon-inventory"></i> Inventory Check
          </button>
          <button class="action-btn" @click="openReports">
            <i class="icon-reports"></i> Reports
          </button>
        </div>
        
        <div class="notifications">
          <div v-if="notifications.length > 0" class="notification-list">
            <div v-for="notification in notifications" :key="notification.id" class="notification-item">
              <div class="notification-icon" :class="notification.type"></div>
              <div class="notification-content">
                <p class="notification-text">{{ notification.message }}</p>
                <span class="notification-time">{{ notification.time }}</span>
              </div>
              <button class="close-btn" @click="dismissNotification(notification.id)">×</button>
            </div>
          </div>
          <div v-else class="no-notifications">
            No new notifications
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import PharmacistNavigationBar from '@/components/pharmacist/NavigationBar.vue';
  
  export default {
    name: 'NavigationBarView',
    components: {
      PharmacistNavigationBar
    },
    data() {
      return {
        currentUser: {
          name: 'Jane Doe',
          avatar: '/assets/img/pharmacist-avatar.png'
        },
        pageTitle: 'Pharmacist Dashboard',
        notifications: [
          {
            id: 1,
            type: 'warning',
            message: 'Low stock alert: Amoxicillin 500mg',
            time: '2 hours ago'
          },
          {
            id: 2,
            type: 'info',
            message: 'New prescription request from Dr. Smith',
            time: '3 hours ago'
          }
        ]
      }
    },
    computed: {
      currentRoute() {
        // Get the current route name for breadcrumb
        const path = this.$route.path;
        const pathSegments = path.split('/');
        return pathSegments[pathSegments.length - 1].charAt(0).toUpperCase() + 
               pathSegments[pathSegments.length - 1].slice(1);
      }
    },
    methods: {
      handleLogout() {
        // Handle logout logic
        this.$store.dispatch('auth/logout');
        this.$router.push('/login');
      },
      openNewPrescription() {
        this.$router.push('/pharmacist/process/new');
      },
      openInventoryCheck() {
        this.$router.push('/pharmacist/inventory/check');
      },
      openReports() {
        this.$router.push('/pharmacist/reports');
      },
      dismissNotification(id) {
        this.notifications = this.notifications.filter(notification => notification.id !== id);
      }
    },
    watch: {
      // Update page title when route changes
      '$route'(to) {
        const path = to.path;
        if (path.includes('process')) {
          this.pageTitle = 'Process Prescription';
        } else if (path.includes('inventory')) {
          this.pageTitle = 'Inventory Management';
        } else {
          this.pageTitle = 'Pharmacist Dashboard';
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .navigation-view {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  
  .content-wrapper {
    padding: 1.5rem 2rem;
    background-color: #f5f7fa;
    flex: 1;
  }
  
  .page-header {
    margin-bottom: 1.5rem;
  }
  
  .page-header h1 {
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #2c3e50;
  }
  
  .breadcrumb {
    font-size: 0.9rem;
    color: #666;
  }
  
  .quick-actions {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .action-btn {
    display: flex;
    align-items: center;
    padding: 0.75rem 1.25rem;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .action-btn:hover {
    background-color: #f9f9f9;
    border-color: #42b983;
    color: #42b983;
  }
  
  .action-btn i {
    margin-right: 0.5rem;
    font-size: 1.1rem;
  }
  
  .notifications {
    background-color: #fff;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    padding: 1rem;
  }
  
  .notification-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .notification-item {
    display: flex;
    align-items: center;
    padding: 0.75rem;
    border-radius: 4px;
    background-color: #f9f9f9;
    position: relative;
  }
  
  .notification-icon {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 1rem;
  }
  
  .notification-icon.warning {
    background-color: #f39c12;
  }
  
  .notification-icon.info {
    background-color: #3498db;
  }
  
  .notification-content {
    flex: 1;
  }
  
  .notification-text {
    margin: 0;
    font-size: 0.95rem;
  }
  
  .notification-time {
    font-size: 0.8rem;
    color: #777;
  }
  
  .close-btn {
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    color: #999;
    padding: 0.25rem;
  }
  
  .close-btn:hover {
    color: #333;
  }
  
  .no-notifications {
    text-align: center;
    padding: 2rem;
    color: #999;
  }
  </style>