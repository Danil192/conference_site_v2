import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin', 
  },
  
  actions: {
    async login(username, password) {
      const role = username.toLowerCase() === 'admin' ? 'admin' : 'organizer'
      
      const userData = { username: username, role: role }
      const fakeToken = 'fake-jwt-token-123'

      this.user = userData
      this.token = fakeToken
      
      localStorage.setItem('token', fakeToken)
      localStorage.setItem('user', JSON.stringify(userData))
    },
    
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})