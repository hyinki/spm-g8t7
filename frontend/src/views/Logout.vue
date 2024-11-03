<template>
  <div>Logging out...</div> <!-- Simple message displayed during logout process -->
</template>

<script>
import { mapActions } from 'vuex';
import Cookies from 'js-cookie'; // Import js-cookie to manage cookies

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
      const allCookies = Cookies.get(); // Retrieve all cookies
      for (const cookieName in allCookies) {
        Cookies.remove(cookieName); // Remove the cookie by name
      }
    },
  },
};
</script>