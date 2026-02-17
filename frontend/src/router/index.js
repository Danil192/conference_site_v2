import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import KonferentsiyaList from '../views/KonferentsiyaList.vue'
import UchastnikList from '../views/UchastnikList.vue'
import ProzhivanieList from '../views/ProzhivanieList.vue'
import TransferList from '../views/TransferList.vue'
import DokladList from '../views/DokladList.vue'
import OtkazList from '../views/OtkazList.vue'
import ProgrammaList from '../views/ProgrammaList.vue'
import ProgramList from '../views/ProgramList.vue'
import SekciyaList from '../views/SekciyaList.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
  },
  {
    path: '/konferentsiyas',
    name: 'KonferentsiyaList',
    component: KonferentsiyaList,
  },
  {
    path: '/uchastniks',
    name: 'UchastnikList',
    component: UchastnikList,
  },
  {
    path: '/prozhivanies',
    name: 'ProzhivanieList',
    component: ProzhivanieList,
  },
  {
    path: '/transfers',
    name: 'TransferList',
    component: TransferList,
  },
  {
    path: '/doklads',
    name: 'DokladList',
    component: DokladList,
  },
  {
    path: '/otkazs',
    name: 'OtkazList',
    component: OtkazList,
  },
  {
    path: '/programmas',
    name: 'ProgrammaList',
    component: ProgrammaList,
  },
  {
    path: '/programs',
    name: 'ProgramList',
    component: ProgramList,
  },
  {
    path: '/sekciyas',
    name: 'SekciyaList',
    component: SekciyaList,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router