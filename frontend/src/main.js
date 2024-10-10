// import './assets/main.css'

// import { createApp } from 'vue'
// import App from './App.vue'

// createApp(App).mount('#app')


// import 'bootstrap/dist/css/bootstrap.min.css';
// import { createApp } from 'vue';
// import App from './App.vue';
// import router from './router';


// createApp(App).use(router).mount('#app');


// Importing necessary libraries and styles
// import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CSS
// import { createApp } from 'vue'; // Vue 3 createApp function
// import App from './App.vue'; // Main App component
// import router from './router'; // Vue Router
// import store from './store/store.js';


// // Create the Vue application and register the router and Vuex store
// createApp(App)
//   .use(router) // Use Vue Router for navigation
//   .use(store)  // Use Vuex for state management
//   .mount('#app'); // Mount the app on the DOM element with id 'app'

import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CSS
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store/store';  // Vuex store
import Cookies from 'js-cookie'; // Import js-cookie to access cookies

const app = createApp(App);

// Check if a user role is stored in cookies and initialize it in Vuex
// Check for cookies and initialize Vuex state
const roleFromCookie = Cookies.get('userRole');
const nameFromCookie = Cookies.get('username');
const supervisorFromCookie = Cookies.get('supervisor');
const deptFromCookie = Cookies.get('dept');
const emailFromCookie = Cookies.get('email');
const positionFromCookie = Cookies.get('position');

if (roleFromCookie) {
  store.dispatch('login', {
    role: roleFromCookie,
    username: nameFromCookie,
    supervisor: supervisorFromCookie,
    dept: deptFromCookie,
    email: emailFromCookie,
    position: positionFromCookie,
  });  // Initialize Vuex state with data from cookies
}


app.use(router);
app.use(store);
app.mount('#app');
