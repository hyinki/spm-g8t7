<script setup>


import Footer from './components/Footer.vue';
</script>


<template>
  <header>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/homepage">Homepage</router-link> |
      <router-link to="/viewteamschedule">viewteamschedule </router-link> | 
      <router-link to="/logout">log Out</router-link> 
    </nav>
  </header>

  <main>
    <!-- Display the current page here -->
    <router-view />
  </main>
  <Footer></Footer>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
