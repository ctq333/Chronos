import { createRouter,createWebHistory } from 'vue-router';

import HomeView from '@/views/HomeView.vue'
import Admin from '@/views/Admin.vue';
import About from '@/views/About.vue';
import Login from '@/views/Login.vue';
import Signup from '@/views/Signup.vue';
import ScheduleView from '@/views/ScheduleView.vue';
import Tasks from '@/views/TaskView.vue';
import WeeklyReportView from '@/views/WeeklyReportView.vue';
import MonthlyReportView from '@/views/MonthlyReportView.vue';
import IncomingEventManagementView from '@/views/IncomingEventManagementView.vue';

const routes = [
  { path: '/', component: HomeView, name: 'home'},
  { path: '/admin', component: Admin, name: 'admin'},
  { path: '/about', component: About, name: 'about'},
  { path: '/login', component: Login, name: 'login'},
  { path: '/signup', component: Signup, name: 'signup'},
  { path: '/schedule', component: ScheduleView, name: 'schedule'},
  { path: '/tasks', component: Tasks, name: 'tasks'},
  { path: '/weekreport', component: WeeklyReportView, name: 'weekreport'},
  { path: '/monthreport', component: MonthlyReportView, name: 'monthreport'},
  { path: '/incomingevent', component: IncomingEventManagementView, name: 'incomingevent'},

  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})                     

export default router;