import { createRouter, createWebHistory } from 'vue-router'
import StressForm from '../components/StressForm.vue'
import StressResults from '../components/StressResults.vue'

const routes = [
  {
    path: '/',
    name: 'Form',
    component: StressForm
  },
  {
    path: '/results',
    name: 'Results',
    component: StressResults
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
