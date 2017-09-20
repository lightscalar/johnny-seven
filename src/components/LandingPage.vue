<template>

  <v-layout>
    <v-flex xs6 offset-xs3>
    <v-card>
      <v-card-title text-xs-center>
        <v-subheader>
          Patients
        </v-subheader>
        <v-spacer></v-spacer>
        <v-btn
          class='black white--text'
          @click.native='createPatient'>
          <v-icon left>
            person_add
          </v-icon>
          Add New Patient
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-data-table
          v-bind:pagination.sync="pagination"
          v-bind:headers="headers"
          :items="patients"
          no-data-text='No Patients Available'
          class="elevation-0">
          <template slot="items" scope="props">
            <td>{{ props.item.hid }}</td>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    </v-flex>
  </v-layout>

</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: [],

    data () {
      return {

        headers: [
          {text: 'Patient Code', value: 'hid', align: 'left'},
          {text: 'Created At', value: 'createdAt', sortable: true, align: 'left'}],

        pagination: {sortBy: 'createdAt'}


      }
    },

    methods: {

      getPatients () {
        this.$store.socket.emit('getPatients')
      },

      createPatient () {
        this.$store.dispatch('createPatient')
      },

    },

    computed: {

      patients () {
        return this.$store.state.patients
      }

    },

    mounted () {
      this.$store.dispatch('getPatients')
    }
  }

</script>

<style>

.logo {
    width:100px;
    height:100px;
}

</style>
