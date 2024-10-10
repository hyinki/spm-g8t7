<template>
  <div>Logging out...</div>
</template>

<script>
import { mapActions } from 'vuex';
import Cookies from 'js-cookie';

export default {
  name: 'Logout',
  created() {
    this.performLogout();
  },
  methods: {
    ...mapActions(['logout']), // Map the logout action from Vuex
    async performLogout() {
      await this.logout(); // Call the Vuex logout action
      this.clearAllCookies(); // Clear all cookies
      this.$router.push('/login'); // Redirect to login page
    },
    clearAllCookies() {
      const allCookies = Cookies.get();
      for (const cookieName in allCookies) {
        Cookies.remove(cookieName);
      }
    },
  },
};
</script>