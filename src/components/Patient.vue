<template>
  <div>
  <v-layout>
    <v-flex>
      <v-card class='elevation-1'>
        <v-card-title>
          <h4 class='mt-2 yellow--text text--darken-3'
            style='text-transform: uppercase'>
            {{patient.hid}}
          </h4>
          <v-spacer></v-spacer>

          <v-btn flat primary @click.native='downloadData' v-if="downloadStatus=='notReady'">
            <v-icon left>cloud_download</v-icon>
            Download
          </v-btn>

          <v-btn v-if="downloadStatus=='preparing'">
            <v-icon left>
              av_timer
             </v-icon>
             One Moment...
          </v-btn>
          
          <v-btn :href='fileUrl' v-if="downloadStatus=='ready'">
            <v-icon left>
                file_download
             </v-icon>
             Download
          </v-btn>

          <v-btn
            @click.native='deletePatient' error>
            <v-icon class='white--text'>
              delete_forever
            </v-icon>
          </v-btn>
          
          <v-btn 
            @click.native='updatePatient' primary>
            <v-icon left>
              update
            </v-icon>
            Update
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-layout>
            <v-flex xs4>
              <v-select
                v-bind:items='genders'
                v-model='patient.gender'
                item-value='value'
                label='Gender'>
              </v-select>
            </v-flex>
            <v-flex xs4 offset-xs1>
              <v-text-field label='Age' v-model='patient.age'>
              </v-text-field>
            </v-flex>
            <v-flex xs4 offset-xs1>
              <v-select
                v-bind:items='gcs'
                v-model='patient.gcs'
                label='GCS'></v-select>
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
      </v-card>
    </v-flex>
    </v-layout>

    <br/>

    <v-layout>
    <v-flex>
        <v-card>
          <v-card-title>
            <v-subheader>
              Patient Scans
            </v-subheader>
                <v-spacer>
                </v-spacer>
                <v-btn primary @click.native='createScan'>
                 <v-icon left>
                   add_circle
                 </v-icon>
                 Add Scan
                </v-btn>
          </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <v-data-table
                v-bind:pagination.sync="pagination"
                v-bind:headers="headers"
                :items="scans"
                no-data-text='No Scans Available'
                class="elevation-0">
                <template slot="items" scope="props">
                  <td>
                    <v-subheader class='upper'>
                      <router-link 
                        :to="{name:'Scan', params:{'id': props.item._id}}">
                       {{ props.item.createdAt }}
                      </router-link>
                    </v-subheader>
                  </td>
                </template>
              </v-data-table>
            </v-card-text>
        </v-card>
    </v-flex>

    <v-snackbar v-model='showMessage' :top=true primary>
      {{message}}
    </v-snackbar>

  </v-layout>
  </div>

</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: ['id'],

    data () {
      return {
        message: '',
        showMessage: false,
        gcs: [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        genders: [
          {text: 'Female', value: 'female'},
          {text: 'Male', value: 'male'}
        ],
        headers: [{
            text: 'Created At', 
            sortable: true, 
            align:'left', 
            value:'createdAt'
            }],
        pagination: {sortBy: 'createdAt'},
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
      },

      createScan () {
        this.$store.dispatch('createScan', this.id)
      },

      downloadData () {
        this.$store.dispatch('getDownload', this.patient._id)
      }

    },

    computed: {

      downloadStatus () {
          return this.$store.state.downloadStatus
      },

      fileUrl () {
        return this.$store.state.fileUrl
      },

      patient () {
        return this.$store.state.patient
      },

      scans () {
        this.pagination.descending = true
        return this.$store.state.scans
      }

    },

    mounted () {
      this.$store.dispatch('getPatient', this.id)
      this.$store.dispatch('getScans', this.id)
      this.$store.commit('setDownloadStatus', 'notReady')
    }
  }

</script>

<style>

</style>
