import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)


export default new Vuex.Store ({

  state: {
    socket: {connected: false},
    connected: false,
    patient: {},
    patients: [],
    scan: {},
    scans: []
  },

  mutations: {

    setSocket (state) {
      if (!state.connected) {
        state.socket = io.connect('http://localhost:5200')
      }
    },

    setPatient (state, patient) {
      state.patient = patient
    },

    setPatients (state, patients) {
      state.patients = patients
    },

    setScan (state, scan) {
      state.scan = scan
      console.log('SCAN RECVD!')
      console.log(scan)
      router.push({name: 'Scan', params: {id: scan._id}})
    },

    setScans (state, scans) {
      state.scans = scans
    }

  },

  actions: {

    establishSocketConnection (context) {

      // CALLBACK FUNCTIONS

      // PATIENTS
      function setPatient (patient) {
        context.commit('setPatient', patient)
        router.push({name: 'Patient', params: {id: patient._id}})
      }

      function setPatients (patients) {
        context.commit('setPatients', patients)
      }

      function patientCreated(patient) {
        setPatient(patient)
      }

      // SCANS
      function setScan (scan) {
        console.log('RECVD Scan Event')
        context.commit('setScan', scan)
      }

      function setScans (scans) {
        context.commit('setScans', scans)
      }

      function scanCreated(scan) {
        setScan(scan)
        router.push({name: 'Scan', params: {id: scan._id}})
      }

      function yell(scan) {
        console.log('YELLING')
      }

      // Set up the socket.
      context.commit('setSocket')
      context.state.socket.emit('request_status')

      // Register listeners for the app.
      context.state.socket.on('patientCreated', patientCreated)
      context.state.socket.on('patient', setPatient)
      context.state.socket.on('patients', setPatients)

      context.state.socket.on('scan', setScan)
      context.state.socket.on('scans', setScans)
      context.state.socket.on('scanComplete', yell)
    },

    getPatients (context, patient) {
      context.dispatch('establishSocketConnection')
      context.state.socket.emit('getPatients')
    },

    createPatient(context) {
      context.dispatch('establishSocketConnection')
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
    },

    createScan (context, patient_id) {
      context.dispatch('establishSocketConnection')
      context.state.socket.emit('createScan', patient_id)
    },

    getScans (context, patient_id) {
      context.dispatch('establishSocketConnection')
      context.state.socket.emit('getScans', patient_id)
    },

    getScan (context, scan_id) {
      context.dispatch('establishSocketConnection')
      context.state.socket.emit('getScan', scan_id)
    },

    deleteScan (context, scan_id) {
      context.dispatch('establishSocketConnection')
      context.state.socket.emit('deleteScan', scan_id)
      router.push({name: 'LandingPage'})
    },

    startScan (context, scan) {
      console.log('Starting Scan.')
      context.dispatch('establishSocketConnection')
      context.state.socket.emit('startScan', scan)
    }

 },

})


