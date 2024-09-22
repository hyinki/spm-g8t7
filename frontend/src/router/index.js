import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';  // Import from views
import Login from '../views/Login.vue';
import Homepage from '../views/Homepage.vue';
import ViewTeamSchedule from '../views/ViewTeamSchedule.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/homepage',
    name: 'Homepage',
    component: Homepage
  },
  {
    path: '/viewteamschedule',
    name: 'ViewTeamSchedule',
    component: ViewTeamSchedule
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
