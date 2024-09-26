import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
    userId: localStorage.getItem('userId') || null,
    username: localStorage.getItem('username') || '',
    email: localStorage.getItem('email') || '',
    role: localStorage.getItem('role') || '',
    experience: localStorage.getItem('experience') || ''
  }),

  actions: {
    login(userId, username, email, role, experience) {
      this.isLoggedIn = true;
      this.userId = userId;
      this.username = username;
      this.email = email;
      this.role = role;
      this.experience = experience;

      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('userId', userId);
      localStorage.setItem('username', username);
      localStorage.setItem('email', email);
      localStorage.setItem('role', role);
      localStorage.setItem('experience', experience);
    },

    logout() {
      this.isLoggedIn = false;
      this.userId = null;
      this.username = '';
      this.email = '';
      this.role = '';
      this.experience = '';

      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('userId');
      localStorage.removeItem('username');
      localStorage.removeItem('email');
      localStorage.removeItem('role');
      localStorage.removeItem('experience');
    }
  }
});
