<!-- src/components/UserLogin.vue -->
<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="username" type="text" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
      <button type="button" @click="handleCreateUser">Opret bruger</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UserLogin',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async handleLogin () {
      try {
        const response = await axios.post(
          'http://127.0.0.1:5000/api/users/user_login',
          {
            username: this.username,
            password: this.password
          },
          { withCredentials: true } // Sørger for at cookies sendes med
        )

        console.log('Login successful:', response.data)
        console.log(response)
      } catch (error) {
        console.error('Fejl ved login:', error)
      }
    },
    handleCreateUser () {
      axios.post('http://127.0.0.1:5000/api/users/user_create', {
        username: this.username,
        password: this.password
      })
        .then(response => {
          console.log('Bruger oprettet:', response.data)
        })
        .catch(error => {
          console.error('Fejl ved oprettelse af bruger', error)
        })
    }
  }
}
</script>

  <style scoped>
  form {
    display: flex;
    flex-direction: column;
    width: 200px;
    margin: 0 auto;
  }
  input {
    margin: 10px 0;
  }
  </style>
