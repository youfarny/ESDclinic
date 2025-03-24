<!-- src/components/pharmacist/NavigationBar.vue -->
<template>
    <nav class="navbar">
      <div class="logo">
        <router-link to="/pharmacist">SMUDOC</router-link>
      </div>
      
      <div class="nav-links">
        <router-link to="/pharmacist" class="nav-link">Dashboard</router-link>
        <router-link to="/pharmacist/process" class="nav-link">Process Prescription</router-link>
        <router-link to="/pharmacist/inventory" class="nav-link">Inventory</router-link>
      </div>
      
      <div class="user-menu">
        <div class="user-info" @click="toggleDropdown">
          <img :src="userAvatar" alt="User Avatar" class="avatar" />
          <span class="username">{{ username }}</span>
          <i class="dropdown-icon"></i>
        </div>
        
        <div class="dropdown-menu" v-if="showDropdown">
          <router-link to="/pharmacist/profile" class="dropdown-item">Profile</router-link>
          <router-link to="/pharmacist/settings" class="dropdown-item">Settings</router-link>
          <div class="dropdown-divider"></div>
          <a href="#" @click.prevent="logout" class="dropdown-item">Logout</a>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'PharmacistNavigationBar',
    props: {
      username: {
        type: String,
        default: 'Pharmacist'
      },
      userAvatar: {
        type: String,
        default: '/assets/img/default-avatar.png'
      }
    },
    data() {
      return {
        showDropdown: false
      }
    },
    methods: {
      toggleDropdown() {
        this.showDropdown = !this.showDropdown;
      },
      logout() {
        this.$emit('logout');
      }
    },
    created() {
      // Close dropdown when clicking outside
      document.addEventListener('click', this.closeDropdown);
    },
    beforeUnmount() {
      document.removeEventListener('click', this.closeDropdown);
    },
    methods: {
      toggleDropdown() {
        this.showDropdown = !this.showDropdown;
      },
      logout() {
        this.$emit('logout');
      },
      closeDropdown(e) {
        const userMenu = this.$el.querySelector('.user-menu');
        if (userMenu && !userMenu.contains(e.target)) {
          this.showDropdown = false;
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
    height: 60px;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .logo a {
    font-size: 1.5rem;
    font-weight: bold;
    color: #2c3e50;
    text-decoration: none;
  }
  
  .nav-links {
    display: flex;
    gap: 1.5rem;
  }
  
  .nav-link {
    color: #666;
    text-decoration: none;
    padding: 0.5rem 0;
    position: relative;
    transition: color 0.3s;
  }
  
  .nav-link:hover {
    color: #42b983;
  }
  
  .nav-link.router-link-exact-active {
    color: #42b983;
    font-weight: 500;
  }
  
  .nav-link.router-link-exact-active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: #42b983;
  }
  
  .user-menu {
    position: relative;
  }
  
  .user-info {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 4px;
  }
  
  .user-info:hover {
    background-color: #f5f5f5;
  }
  
  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 0.5rem;
  }
  
  .username {
    margin-right: 0.5rem;
    font-weight: 500;
  }
  
  .dropdown-icon::after {
    content: '▼';
    font-size: 0.7rem;
    color: #666;
  }
  
  .dropdown-menu {
    position: absolute;
    right: 0;
    top: 100%;
    width: 200px;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 10;
    margin-top: 0.5rem;
  }
  
  .dropdown-item {
    display: block;
    padding: 0.75rem 1rem;
    color: #333;
    text-decoration: none;
    transition: background-color 0.2s;
  }
  
  .dropdown-item:hover {
    background-color: #f5f5f5;
  }
  
  .dropdown-divider {
    height: 1px;
    background-color: #eee;
    margin: 0.5rem 0;
  }
  </style>