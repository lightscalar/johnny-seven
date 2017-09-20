import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/components/LandingPage'
import Patient from '@/components/Patient'

Vue.use(Router)
var landingPage = {
  path: '/',
  name: 'LandingPage',
  component: LandingPage
}
var patient = {
  path: '/patient/:id',
  name: 'Patient',
  component: Patient,
  props: true
}

export default new Router({
  routes: [
    landingPage, patient
  ]
})
