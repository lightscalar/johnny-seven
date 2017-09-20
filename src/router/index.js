import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/components/LandingPage'
import Patient from '@/components/Patient'
import Scan from '@/components/Scan'

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
var scan = {
  path: '/scan/:id',
  name: 'Scan',
  component: Scan,
  props: true
}

export default new Router({
  routes: [
    landingPage, patient, scan
  ]
})
