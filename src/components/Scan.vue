<template>
  <v-layout>
    <v-flex xs12 v-if='!scan.isComplete && !isScanning'>
      <v-card>
        <v-card-title>
            <v-subheader>
              Pupillary Light Reflex Scan
            </v-subheader>
            <v-spacer></v-spacer>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <p>
          Get ready to start the scan. Instruct the patient to look at the
          flash lamp on top of the eye tracker. The scan will take
          approximately 16 seconds. Ensure the patient does not look away from
          the eye tracker after the flash.
          </p>
          <v-layout>
            <v-flex xs6>
              <v-text-field
                v-model='scan.notes'
                label='Notes'>
              </v-text-field>
            </v-flex>
            <v-flex xs4 offset-xs1>
              <v-select
                v-bind:items='gcs'
                v-model='scan.gcs'
                label='GCS'></v-select>
            </v-flex>
          </v-layout>

        </v-card-text>
        <v-card-actions>
          <v-btn large primary @click.native='startScan'>
            <v-icon left>
              play_arrow
            </v-icon>
            Start Scan
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>

    <v-flex v-if='isScanning' xs12>

    <v-card>
      <v-card-text>
        <v-layout>
          <v-flex lg6 md6>
            <v-progress-circular
              indeterminate
              v-bind:size="70"
              v-bind:width="7"
              class="blue--text text--darken-3">
            </v-progress-circular>
          </v-flex>
          <v-flex lg6 md6 v-if='processing'>
            <h5 class='mt-4'>Scan Complete. Processing data...</h5>
          </v-flex>
          <v-flex lg6 md6 v-else>
            <h5 class='mt-4'>Hold Steady. Scan is underway!</h5>
          </v-flex>
        </v-layout>
      </v-card-text>
    </v-card>
    </v-flex>

    <v-flex v-if='scan.isComplete'>
      <v-card>
        <v-card-title>
          <h6 class='mt-3'>
            <span class=''>Patient</span>
            <router-link :to="{name: 'Patient', params: {id: patient._id}}">
            <span class='' style='text-transform: uppercase'>
              {{patient.hid}}
            </span>
            </router-link>
            @ {{scan.updatedAt}}
          </h6>
          <v-spacer></v-spacer>
          <v-btn icon error @click.native='deleteScan'>
            <v-icon class='white--text'>
              delete_forever
            </v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-layout>
            <v-flex xs4 lg2>
              <v-text-field  v-model='scan.notes' label='Notes' disabled>
              </v-text-field>
            </v-flex>
            <v-flex xs4 lg2 offset-xs1>
              <v-text-field v-model='scan.gcs' label='GCS' disabled>
              </v-text-field>
            </v-flex>
            <v-flex xs4 lg2 offset-xs1>
              <v-chip v-if='scan.isSuccess' class='green white--text'>
                Scan Successful
              </v-chip>
              <v-chip v-else class='red darken-3 white--text'>
                Scan Failed
              </v-chip>
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-text>
          <v-data-table
              v-bind:headers="headers"
              :items="results"
              hide-actions
              no-data-text='No Scans Available'
              class="elevation-0">
            <template slot="items" scope="props">
              <td>
                {{props.item.description}}
              </td>
              <td>
                {{props.item.left | formatNumber('%0.2f')}}
              </td>
              <td>
                {{props.item.right | formatNumber('%0.2f')}}
              </td>
              <td>
                {{props.item.units}}
              </td>
            </template>
          </v-data-table>
        </v-card-text>
        </v-card>
        </br>
        <v-card>
            <v-card-title>
            <v-subheader>
                Left Eye Scan
            </v-subheader>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <img class='scan-plot' v-bind:src='scanPlotUrl("LEFT")'/>
            </v-card-text>
        </v-card>
        <br/>
        <v-card>
            <v-card-title>
            <v-subheader>
                Right Eye Scan
            </v-subheader>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <img class='scan-plot' v-bind:src='scanPlotUrl("RIGHT")'/>
            </v-card-text>
        </v-card>
    </v-flex>
  </v-layout>

</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: ['id'],

    data () {
      return {
        gcs: [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        headers: [
          {text: 'Description', value: 'description', sortable: false, align: 'left'},
          {text: 'Left', value: 'left', sortable: false, align: 'left'},
          {text: 'Right', value: 'right', sortable: false, align: 'left'},
          {text: 'Units', value: 'units', sortable: false, align: 'left'},
        ],
        processing: false
      }
    },

    methods: {

      startScan () {
        var self = this  
        this.$store.dispatch('startScan', this.scan)
        setTimeout(function(){self.processing=true}, 16000)
      },

      deleteScan () {
        this.$store.dispatch('deleteScan', this.scan._id)
      },

      scanPlotUrl(whichEye) {
        return 'static/plots/' + this.scan._id + '_' + whichEye + '.png'
      },

    },

    computed: {

      scan () {
        return this.$store.state.scan
      },


      patient () {
        return this.$store.state.patient
      },

      isScanning () {
        return this.$store.state.isScanning
      },

      results () {

        var res = []

        res.push({
            description: 'Starting Diameter',
            left: this.scan.left.starting_diameter,
            right: this.scan.right.starting_diameter,
            units: 'mm'
        })
        res.push({
            description: 'Minimum Diameter',
            left: this.scan.left.minimum_diameter,
            right: this.scan.right.minimum_diameter,
            units: 'mm'
        })
        res.push({
            description: 'Absolute Diameter Change',
            left: this.scan.left.absolute_diameter_change,
            right: this.scan.right.absolute_diameter_change,
            units: 'mm'
        })
        res.push({
            description: 'Relative Diameter Change',
            left: this.scan.left.relative_diameter_change,
            right: this.scan.right.relative_diameter_change,
            units: '%'
        })
        res.push({
            description: 'Latency',
            left: this.scan.left.latency * 1000,
            right: this.scan.right.latency * 1000,
            units: 'ms'
        })
        res.push({
            description: 'Average Constriction Speed',
            left: this.scan.left.average_speed,
            right: this.scan.right.average_speed,
            units: 'mm/s'
        })
        res.push({
            description: '75% Recovery Time',
            left: this.scan.left.recovery_time * 1000,
            right: this.scan.right.recovery_time * 1000,
            units: 'ms'
        })

        return res

      }

    },

    mounted () {
      this.$store.dispatch('getScan', this.id)
    }
  }

</script>

<style>
.scan-plot {
    width: 100%
}
</style>
