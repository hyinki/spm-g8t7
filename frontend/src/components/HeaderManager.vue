<template>
   
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid m-5">
        <a class="navbar-brand" href="/homepage">
          <img :src="calendarIcon" alt="Calendar Icon" style="width: 20px; margin-right: 5px" />
          PlanPro</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="/homepage">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/viewownteamschedule">Own Team Schedule</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/viewteamschedule">Managed Team Schedule</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/arrangement">Approve/RejectArrangement</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/viewownschedule">Own Schedule</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/applyforarrangement">Apply For Arrangement</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/viewarrangement">View Arrangement</a>
            </li>
           
          </ul>
  
          <!-- Account Section -->
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <span class="nav-link">
                <img :src="accountIcon" alt="Account Icon" style="width: 20px; margin-right: 5px" />
                Hello, {{ userRole }}
              </span>
            </li>
            <li class="nav-item">
              <button class="btn btn-primary" @click="performLogout">Logout</button>
            </li>
          </ul>
        </div>
      </div>

    </nav>
    
  
    <!-- Optionally, you can show a message while logging out -->
    <div v-if="loggingOut">Logging out...</div>
  </template>
  
  <script>
  import { mapActions } from "vuex";
  import Cookies from "js-cookie";
  import accountIcon from "@/assets/account.png"; // Import the account icon
  import calendarIcon from "@/assets/calendar.png";

  
  export default {
    name: "HeaderManager",
  
    data() {
      return {
        loggingOut: false, // To show loading message when logging out
        accountIcon, // Set the imported icon to data
        calendarIcon
      };
    },
  
    methods: {
      ...mapActions(["logout"]), // Map the logout action from Vuex
  
      async performLogout() {
        this.loggingOut = true; // Set logging out state
        await this.logout(); // Call the Vuex logout action
        this.clearAllCookies(); // Clear all cookies
        this.$router.push("/"); // Redirect to the login page
      },
  
      clearAllCookies() {
        const allCookies = Cookies.get();
        for (const cookieName in allCookies) {
          Cookies.remove(cookieName);
        }
      },
    },
  
    computed: {
      userRole() {
        return Cookies.get("username") || "Guest"; // Display user role from cookies or default to "Guest"
      },
    },
  };
  </script>
  
  <style scoped>
  .navbar{
    height: 75px;
  }
  
  </style>
  