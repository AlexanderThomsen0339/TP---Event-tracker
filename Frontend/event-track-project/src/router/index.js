// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { reactive } from 'vue' // Importer reactive
import HomeView from '../views/HomeView.vue'
import UserLogin from '../components/UserLogin.vue'
import EventListTemplate from '../components/EventListTemplate.vue'

// Opret en reaktiv global state
export const globalAuthState = reactive({
  loggedIn: false
})

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin
  },
  {
    path: '/events',
    name: 'events',
    component: EventListTemplate
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  // Tillad adgang til login-siden uden at tjekke autentifikation
  if (to.name === 'UserLogin') {
    next()
    return
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/api/users/check', {
      method: 'GET',
      credentials: 'include'
    })

    // Håndter 401 UNAUTHORIZED
    if (response.status === 401) {
      globalAuthState.loggedIn = false // Opdater global state
      next({ name: 'UserLogin' }) // Omdiriger til login-siden
      return
    }

    // Hvis statuskoden er 200, fortsæt til den ønskede rute
    if (response.ok) {
      globalAuthState.loggedIn = true // Opdater global state
      next()
      return
    }

    // Håndter andre fejl
    console.error('Serveren returnerede en uventet status:', response.status)
    globalAuthState.loggedIn = false // Opdater global state
    next({ name: 'UserLogin' }) // Omdiriger til login-siden som en fallback
  } catch (error) {
    console.error('Fejl under autentifikation:', error)
    globalAuthState.loggedIn = false // Opdater global state
    next({ name: 'UserLogin' }) // Omdiriger til login-siden ved fejl
  }
})

export default router
