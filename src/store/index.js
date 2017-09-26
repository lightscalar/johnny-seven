import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/index'
Vue.use(Vuex)


export default new Vuex.Store ({

  state: {
    socket: {connected: false},
    connected: false,
    patient: {},
    patients: [],
    scan: {},
    scans: [],
    isScanning: false,
    downloadStatus: 'notReady',
    fileUrl: ''
  },

  mutations: {

    setPatient (state, patient) {
      state.patient = patient
    },

    setPatients (state, patients) {
      state.patients = patients
    },

    setScan (state, scan) {
      state.scan = scan
    },

    setScans (state, scans) {
      state.scans = scans
    },

    setScanning (state, isScanning) {
      state.isScanning = isScanning
    },

    setDownloadStatus (state, downloadStatus) {
       state.downloadStatus = downloadStatus
    },

    setFileUrl (state, fileUrl) {
       state.fileUrl = fileUrl
    }

  },

  actions: {

    createPatient(context) {
      api.postResource('patients').then( function(resp) {
        context.commit('setPatient', resp.data)
        router.push({name:'Patient', params:{id: resp.data._id}})
      })
    },

    deletePatient(context, patient_id) {
      api.deleteResource('patient', patient_id).then(function () {
        router.push({name: 'LandingPage'})
      })
    },

    getPatient (context, patient_id) {
      api.getResource('patient', patient_id).then( function (resp) {
        context.commit('setPatient', resp.data)
      })
    },

    getPatients (context) {
      api.listResource('patients').then( function (resp) {
        context.commit('setPatients', resp.data)
      })
    },


    getScans (context, patient_id) {
      api.listNestedResource('patient', patient_id, 'scans')
        .then( function (resp) {
        context.commit('setScans', resp.data)
      })
    },

    updatePatient(context, patient) {
      api.putResource('patient', patient).then(function (resp) {
        context.commit('setPatient', resp.data)
      })
    },

    createScan(context, patient_id) {
      api.postNestedResource('patient', patient_id, 'scans').then(function (resp) {
        context.commit('setScan', resp.data)
        router.push({name:'Scan', params: {id: resp.data._id}})
      })
    },

    getScan(context, scan_id) {
      api.getResource('scan', scan_id).then( function (resp) {
        context.commit('setScan', resp.data)
        context.dispatch('getPatient', resp.data.patient_id)
      })
    },

    startScan(context, scan) {
      context.commit('setScanning', true)
      api.postResource('commands', scan).then(function (resp) {
        console.log(resp.data)
        context.commit('setScan', resp.data)
        context.commit('setScanning', false)
      })
    },

    deleteScan(context, scan_id) {
      api.deleteResource('scan', scan_id).then(function (resp) {
        router.push({name:'Patient', params:{id:resp.data._id}})
      })
    },

    getDownload(context, patient_id) {
        context.commit('setDownloadStatus', 'preparing')
        api.getResource('download', patient_id).then( function (resp) {
            context.commit('setFileUrl', resp.data)
            context.commit('setDownloadStatus', 'ready')
        })
    }

 },

})


