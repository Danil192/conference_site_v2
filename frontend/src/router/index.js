import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import KonferentsiyaList from '../views/KonferentsiyaList.vue'
import KonferentsiyaDetail from '../views/KonferentsiyaDetail.vue'
import UchastnikList from '../views/UchastnikList.vue'
import SekciyaList from '../views/SekciyaList.vue'
import DokladList from '../views/DokladList.vue'
import ProzhivanieList from '../views/ProzhivanieList.vue'
import TransferList from '../views/TransferList.vue'
import ProgrammaList from '../views/ProgrammaList.vue'
import ProgramList from '../views/ProgramList.vue'
import OtkazList from '../views/OtkazList.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import SystemUsersList from '../views/SystemUsersList.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
    {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/konferentsiyas',
    name: 'KonferentsiyaList',
    component: KonferentsiyaList
  },
    {
    path: '/konferentsiyas/:id', 
    name: 'KonferentsiyaDetail',
    component: KonferentsiyaDetail
  },
  {
    path: '/uchastniks',
    name: 'UchastnikList',
    component: UchastnikList
  },
  {
    path: '/sekciyas',
    name: 'SekciyaList',
    component: SekciyaList
  },
  {
    path: '/doklads',
    name: 'DokladList',
    component: DokladList
  },
  {
    path: '/prozhivanies',
    name: 'ProzhivanieList',
    component: ProzhivanieList
  },
  {
    path: '/transfers',
    name: 'TransferList',
    component: TransferList
  },
  {
    path: '/programmas',
    name: 'ProgrammaList',
    component: ProgrammaList
  },
  {
    path: '/programs',
    name: 'ProgramList',
    component: ProgramList
  },
  {
    path: '/otkazs',
    name: 'OtkazList',
    component: OtkazList
  },
  {
    path: '/system-users',
    name: 'SystemUsersList',
    component: SystemUsersList,
    meta: { requiresAdmin: true } 
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    alert('У вас нет прав для просмотра этой страницы!')
    next('/')
  } else {
    next()
  }
})

export default router