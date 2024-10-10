import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Homepage from '../views/Homepage.vue';
import ViewTeamSchedule from '../views/ViewTeamSchedule.vue';
import ViewOwnSchedule from '../views/ViewOwnSchedule.vue';
import ApplyForArrangement from '../views/ApplyForArrangement.vue';
import Arrangement from '../views/Arrangement.vue';
import ViewOverallSchedule from '../views/ViewOverallSchedule.vue';
import Logout from '../views/logout.vue';
import store from '../store/store.js';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/homepage', name: 'Homepage', component: Homepage, meta: { requiresAuth: true }},
  { path: '/viewteamschedule', name: 'ViewTeamSchedule', component: ViewTeamSchedule, meta: { requiresAuth: true }},
  { path: '/viewownschedule', name: 'ViewOwnSchedule', component: ViewOwnSchedule, meta: { requiresAuth: true }},
  { path: '/applyforarrangement', name: 'ApplyForArrangement', component: ApplyForArrangement },
  { path: '/Arrangement', name: 'Arrangement', component: Arrangement },
  { path: '/viewoverallschedule', name: 'ViewOverallSchedule', component: ViewOverallSchedule },
  { path: '/logout', name: 'Logout', component: Logout },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ path: '/login' });
  } else {
    next();
  }
});

export default router;
