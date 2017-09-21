<template>
  <v-layout>
    <v-flex xs6 v-if='!scan.complete'>
      <v-card>
        <v-card-title>
            <v-subheader>
              Eye Scan
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
    <v-flex v-else>
      <v-card>
        <v-card-title>
          <h5 class='mt-3'>
            Scan {{scan.updatedAt}}
          </h5>  
          <v-spacer></v-spacer>
          <v-btn icon error>
            <v-icon class='white--text'>
              delete
            </v-icon>
          </v-btn>
        </v-card-title>
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
      }
    },

    methods: {

      startScan () {
        this.$store.dispatch('startScan', this.scan)
      }

    },

    computed: {

      scan () {
        console.log(this.$store.state.scan)
        return this.$store.state.scan
      }

    },

    mounted () {
      this.$store.dispatch('getScan', this.id)
    }
  }

</script>

<style>

</style>
