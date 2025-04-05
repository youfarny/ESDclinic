import './assets/global.css';

import { createApp } from 'vue';  
import './style.css';
import App from './App.vue';
import router from './router';  
import store from './store'


createApp(App)
  .use(router)  
  .use(store)
  .mount('#app');  


  // src/main.js
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
