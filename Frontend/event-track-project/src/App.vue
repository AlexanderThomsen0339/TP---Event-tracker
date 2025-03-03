<template>
  <div id="app">
    <MainMenubar v-if="!loggedIn" />
    <LoggedInMenubar v-else />
    <router-view />
  </div>
</template>

<script>
import { ref, watchEffect } from 'vue'
import MainMenubar from './components/MainMenubar.vue'
import LoggedInMenubar from './components/LoggedInMenubar.vue'
import { globalAuthState } from './router/index' // Importer global state korrekt

export default {
  name: 'App',
  components: {
    MainMenubar,
    LoggedInMenubar
  },
  setup () {
    const loggedIn = ref(globalAuthState.loggedIn) // Brug global state

    // Opdater loggedIn når globalAuthState ændres
    watchEffect(() => {
      loggedIn.value = globalAuthState.loggedIn
    })

    // Tilføj latitude og longitude som reactive variabler
    const latitude = ref(null)
    const longitude = ref(null)

    // Metode til at hente brugerens geolokation
    const getLocation = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            latitude.value = position.coords.latitude
            longitude.value = position.coords.longitude
          },
          (error) => {
            console.error('Error getting location:', error)
          }
        )
      } else {
        console.error('Geolocation is not supported by this browser.')
      }
    }

    // Kald getLocation, når komponenten er oprettet
    getLocation()

    return {
      loggedIn,
      latitude,
      longitude
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
