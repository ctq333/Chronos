import { createRouter,createWebHistory } from 'vue-router';
import store from '@/store'

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
  { path: '/', component: HomeView, name: 'home',meta:{requiresAuth: true,hideNavBar: false}},
  { path: '/admin', component: Admin, name: 'admin',meta:{requiresAuth: true,requiresAdmin: true,hideNavBar: false}},
  { path: '/about', component: About, name: 'about',meta:{requiresAuth: true,hideNavBar: false}},
  { path: '/login', component: Login, name: 'login',meta:{hideNavBar: true}},
  { path: '/signup', component: Signup, name: 'signup',meta:{hideNavBar: true}},
  { path: '/schedule', component: ScheduleView, name: 'schedule',meta:{requiresAuth: true,hideNavBar: false}},
  { path: '/tasks', component: Tasks, name: 'tasks',meta:{requiresAuth: true,hideNavBar: false}},
  { path: '/weekreport', component: WeeklyReportView, name: 'weekreport',meta:{requiresAuth: true,hideNavBar: false}},
  { path: '/monthreport', component: MonthlyReportView, name: 'monthreport',meta:{requiresAuth: true,hideNavBar: false}},
  { path: '/incomingevent', component: IncomingEventManagementView, name: 'incomingevent',meta:{requiresAuth: true,hideNavBar: false}},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
}) 

router.beforeEach((to,from,next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.meta.requiresAdmin
  const isLogin = store.getters.isLogin
  const isAdmin = store.getters.isAdmin

  if (requiresAuth && !isLogin) {
    next('/login')
  } else if (requiresAdmin && !isAdmin) {
    next('/')
  } else {
    next()
  }
})

export default router;