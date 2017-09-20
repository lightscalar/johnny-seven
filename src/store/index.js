import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)


export default new Vuex.Store ({

  state: {
    socket: {connected: false},
    connected: false,
    patient: {}
  },

  mutations: {

    setSocket (state) {
      if (!state.connected) {
        state.socket = io.connect('http://localhost:5200')
      }
    },

    setPatient (state, patient) {
      state.patient = patient
    }

  },

  actions: {

    establishSocketConnection (context) {

      // CALLBACK FUNCTIONS
      function setPatient (patient) {
        context.commit('setPatient', patient)
        router.push({name: 'Patient', params: {id: patient._id}})
      }

      function patientCreated(patient) {
        setPatient(patient)
        console.log('Patient Created!')
      }

      // Set up the socket.
      context.commit('setSocket')
      context.state.socket.emit('request_status')

      // Register listeners for the app.
      context.state.socket.on('patient', setPatient)
      context.state.socket.on('patientCreated', patientCreated)

    },

    getPatients (context, patient) {
      context.dispatch('establishSocketConnection')
    },

    createPatient(context) {
      context.state.socket.emit('createPatient')
    },

    getPatient (context, patient_id) {
      context.dispatch('establishSocketConnection')
      context.state.socket.emit('getPatient', patient_id)
    },

    updatePatient (context, patient) {
      context.dispatch('establishSocketConnection')
      context.state.socket.emit('updatePatient', patient)
    },

    deletePatient (context, patient_id) {
      context.dispatch('establishSocketConnection')
      context.state.socket.emit('deletePatient', patient_id)
      router.push({name: 'LandingPage'})
    }

  },

})


