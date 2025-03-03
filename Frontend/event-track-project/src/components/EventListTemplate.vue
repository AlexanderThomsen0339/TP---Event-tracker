<!-- src/components/EventListTemplate.vue -->
<template>
  <div class="ListEvents">
    <div>
      <label for="radius">Radius (in kilometers):</label>
      <input type="number" id="radius" v-model="radius" placeholder="Enter radius" />
    </div>
    <button @click="fetchData">Hent events</button>
    <div v-if="data" class="event-list">
      <div v-for="event in data.events" :key="event.event_id" class="event-card">
        <h3>{{ event.event_name }}</h3>
        <p><strong>Start Time:</strong> {{ formatDate(event.event_start_time) }}</p>
        <p><strong>Location:</strong> {{ event.location_name }}</p>
      </div>
    </div>
    <div v-if="error">
      <p style="color: red;">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ListEvents',
  data () {
    return {
      radius: null, // User-defined radius
      latitude: null, // Device latitude
      longitude: null, // Device longitude
      data: null, // API response data
      error: null // Error message
    }
  },
  created () {
    this.fetchData()
  },
  methods: {
    async fetchData () {
      this.error = null // Nulstil fejlmeddelelse
      this.data = null // Nulstil data

      // Valider radius-input
      if (!this.radius || this.radius <= 0) {
        this.error = 'Indtast venligst en gyldig radius.'
        return
      }

      // Hent enhedens lokation
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            this.latitude = position.coords.latitude
            this.longitude = position.coords.longitude

            // Tjek om der er internetforbindelse
            if (navigator.onLine) {
              try {
                // Forsøg at hente data fra API'et
                const response = await axios.post('http://127.0.0.1:5000/api/events/get_users_within_radius', {
                  radius: this.radius,
                  latitude: this.latitude,
                  longitude: this.longitude
                })
                this.data = response.data // Gem API-svaret

                // Cache API-svaret for fremtidig brug
                if (navigator.serviceWorker) {
                  const cache = await caches.open('events-api-cache')
                  cache.put('http://127.0.0.1:5000/api/events/get_users_within_radius', new Response(JSON.stringify(this.data)))
                }
              } catch (error) {
                console.error('Fejl ved hentning af data:', error)

                // Hvis API-kaldet fejler, forsøg at hente cachelagrede data
                const cache = await caches.open('events-api-cache')
                const cachedResponse = await cache.match('http://127.0.0.1:5000/api/events/get_users_within_radius')

                if (cachedResponse) {
                  const cachedData = await cachedResponse.json()
                  this.data = cachedData // Vis cachelagrede data
                  this.error = 'API-et er ikke tilgængeligt. Viser cachelagrede data.'
                } else {
                  this.error = 'API-et er ikke tilgængeligt, og der er ingen cachelagrede data.'
                }
              }
            } else {
              // Hvis der ikke er internetforbindelse, forsøg at hente cachelagrede data
              const cache = await caches.open('events-api-cache')
              const cachedResponse = await cache.match('http://127.0.0.1:5000/api/events/get_users_within_radius')

              if (cachedResponse) {
                const cachedData = await cachedResponse.json()
                this.data = cachedData // Vis cachelagrede data
                this.error = 'Ingen internetforbindelse. Viser cachelagrede data.'
              } else {
                this.error = 'Ingen internetforbindelse, og der er ingen cachelagrede data.'
              }
            }
          },
          (error) => {
            console.error('Geolokationsfejl:', error)
            this.error = 'Kunne ikke hente din lokation.'
          }
        )
      } else {
        console.error('Geolokation understøttes ikke af denne browser.')
        this.error = 'Geolokation understøttes ikke af din browser.'
      }
    },
    formatDate (dateString) {
      const date = new Date(dateString)
      return date.toLocaleString() // Formatér datoen på en brugervenlig måde
    }
  }
}
</script>

<style scoped>
.ListEvents {
  margin: 20px;
}

label {
  margin-right: 10px;
}

input {
  padding: 5px;
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #369f6e;
}

.event-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.event-card {
  background-color: #f4f4f4;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.event-card h3 {
  margin: 0 0 10px;
  font-size: 1.2em;
}

.event-card p {
  margin: 5px 0;
  font-size: 0.9em;
  color: #555;
}
</style>
