import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import KonferentsiyaList from '../views/KonferentsiyaList.vue'
import UchastnikList from '../views/UchastnikList.vue'
import SekciyaList from '../views/SekciyaList.vue'

const routes = [
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
    path: '/uchastniks',
    name: 'UchastnikList',
    component: UchastnikList
  },
  {
    path: '/sekciyas',
    name: 'SekciyaList',
    component: SekciyaList
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router