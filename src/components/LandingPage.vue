<template>

  <v-layout>
    <v-flex xs8 offset-xs2>
    <v-card>
      <v-card-title text-xs-center>
        <v-subheader>
          Patients
        </v-subheader>
        <v-spacer></v-spacer>
        <v-btn
          primary
          @click.native='createPatient'>
          <v-icon left>
            person_add
          </v-icon>
          Add New Patient
        </v-btn>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-data-table
          v-bind:pagination.sync="pagination"
          v-bind:headers="headers"
          :items="patients"
          no-data-text='No Patients Available'
          class="elevation-0">
          <template slot="items" scope="props">
            <td>
              <v-subheader class='upper'>
              <router-link :to="{name:'Patient', params:{'id': props.item._id}}">
                {{ props.item.hid }}
              </router-link>
              </v-subheader>
            </td>
            <td>{{ props.item.createdAt }}</td>
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
        this.pagination.descending = true
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
.upper {
  text-transform: uppercase;
}
</style>
