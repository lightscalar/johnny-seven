<template>

<v-app id="example-1" toolbar footer>
    <!-- <v-navigation-drawer -->
    <!--   persistent -->
    <!--   v-model="drawer" -->
    <!--   light -->
    <!--   enable-resize-watcher -->
    <!--   absolute> -->
    <!--   <v-list dense> -->
    <!--     <v-list-tile @click="" :to='{name: "LandingPage"}'> -->
    <!--       <v-list-tile-action> -->
    <!--         <v-icon>home</v-icon> -->
    <!--       </v-list-tile-action> -->
    <!--       <v-list-tile-content> -->
    <!--         <v-list-tile-title>Home</v-list-tile-title> -->
    <!--       </v-list-tile-content> -->
    <!--     </v-list-tile> -->
    <!--     <v-list-tile @click="" :to='{name: "Patients"}'> -->
    <!--       <v-list-tile-action> -->
    <!--         <v-icon>people</v-icon> -->
    <!--       </v-list-tile-action> -->
    <!--       <v-list-tile-content> -->
    <!--         <v-list-tile-title>Patient Archive</v-list-tile-title> -->
    <!--       </v-list-tile-content> -->
    <!--     </v-list-tile> -->
    <!--   </v-list> -->
    <!-- </v-navigation-drawer> -->
    <v-toolbar class="yellow darken-2 elevation-0" light fixed>
      <!-- <v-toolbar-side-icon @click.stop="drawer = !drawer"> -->
      <!-- </v-toolbar-side-icon> -->
      <a href='/#' class='navy'>
        <img src='/static/img/j7-logo@2x.png' width='50px'/>
      </a>
      <v-toolbar-title class='logo-text'>johnny seven</v-toolbar-title>
    </v-toolbar>
    <main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </main>
  </v-app>


</template>

<script>
export default {

  name: 'app',

  data () {
    return {
      drawer: false
    }
  },

  mounted () {
  }




}
</script>

<style>
.logo-text {
  letter-spacing: 20px !important;
  margin-top: -5px;
}
</style>
