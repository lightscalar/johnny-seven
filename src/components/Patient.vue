<template>
  <v-layout>
    <v-flex xs6>
      <v-card class='elevation-1'>
        <v-card-title>
          <h4 class='mt-2 yellow--text text--darken-3'>
            {{patient.hid}}
          </h4>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-layout>
            <v-flex xs4>
              <v-select
                v-bind:items='genders'
                v-model='patient.gender'
                item-value='value'
                label='Gender'></v-select>
            </v-flex>
            <v-flex xs4 offset-xs1>
              <v-text-field label='Age' v-model='patient.age'>
              </v-text-field>
            </v-flex>
            <v-flex xs4 offset-xs1>
              <v-select
                v-bind:items='gcs'
                v-model='patient.gcs'
                label='Glasgow Coma Scale'></v-select>
            </v-flex>
          </v-layout>
          <v-layout>
            <v-flex xs12>
              <v-text-field
                v-model='patient.notes'
                label='Notes'>
              </v-text-field>
            </v-flex>
          </v-layout>
        </v-card-text>
        <v-card-actions>
          <v-btn error icon>
            <v-icon class='white--text'>
              delete_forever
            </v-icon>
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn @click.native='updatePatient' class='black white--text'>
            Update
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
    <v-flex xs6 class='ml-3'>
        <v-card>
          Hi
        </v-card>
    </v-flex>

    <v-snackbar v-model='showMessage' :top=true primary>
      {{message}}
    </v-snackbar>

  </v-layout>

</template>

<script>
  // import Component from "../component_location"
  import Messenger from "./Messenger.vue"

  export default {

    components: {Messenger},

    props: ['id'],

    data () {
      return {

        message: '',
        showMessage: false,
        gcs: [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        genders: [
          {text: 'Female', value: 'female'},
          {text: 'Male', value: 'male'}
        ]

      }
    },

    methods: {

      updatePatient () {
        this.$store.dispatch('updatePatient', this.patient)
        this.message = 'Updated Patient Information'
        this.showMessage = true
      },

      deletePatient () {
        this.$store.dispatch('deletePatient', this.id)
      }

    },

    computed: {

      patient () {
        return this.$store.state.patient
      }

    },

    mounted () {
      this.$store.dispatch('getPatient', this.id)

    }
  }

</script>

<style>

</style>
