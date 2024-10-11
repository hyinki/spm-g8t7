<template>
  <!-- Staff Section -->
  <div v-if="isStaff">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">PlanPro</a>
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
              <a class="nav-link active" aria-current="page" href="/homepage"
                >Home</a
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/viewteamschedule">Team Schedule</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/viewownschedule">Own Schedule</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/applyforarrangement"
                >Apply For Arrangement</a
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div>
    <h1> Welcome to the HomePage, {{username}}, {{paper}} ,{{dept}} (Staff) </h1>
    </div>

    <div>
      <router-link to="/viewteamschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Team Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/viewownschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Own Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/applyforarrangement">
        <button type="button" class="btn btn-primary btn-lg m-5">
          Apply For Arrangement
        </button>
      </router-link>
    </div>
  </div>

  <!-- Manager Section -->
  <div v-if="isManager">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">PlanPro</a>
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
              <a class="nav-link active" aria-current="page" href="/homepage"
                >Home</a
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/viewteamschedule"
                >View Team Schedule</a
              >
            </li>

            <li class="nav-item">
              <a class="nav-link" href="/arrangement"
                >Approve/RejectArrangement</a
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div>
      <h1>Welcome to the HomePage, {{username}} (Manager)</h1>
    </div>

    <div>
      <router-link to="/viewteamschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Team Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/arrangement">
        <button type="button" class="btn btn-primary btn-lg m-5">
          Approve/Reject Arrangement
        </button>
      </router-link>
    </div>
  </div>

  <!-- HR Section -->
  <div v-if="isHR">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">PlanPro</a>
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
              <a class="nav-link active" aria-current="page" href="/homepage"
                >Home</a
              >
            </li>

            <li class="nav-item">
              <a class="nav-link" href="/viewoverallschedule"
                >View Overall Schedule</a
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/viewteamschedule"
                >View Team Schedule</a
              >
            </li>

           
          </ul>
        </div>
      </div>
    </nav>


    <div>
      <h1 >Welcome to the HomePage, {{ username }} (HR)</h1>
    
    </div>

    <div>
      
      <router-link to="/viewteamschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Team Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/viewoverallschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Overall Schedule
        </button>
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Cookies from "js-cookie"; // Import js-cookie to manage cookies



export default {
  name: "Homepage",
  created() {
    // Get the cookie value when the component is created
    this.userID = Cookies.get('userid') || 'Cookie not found';
  },
  computed: {
    ...mapGetters(["userRole","username","userid","dept"]), // Access the user's role, username from Vuex
    
    isStaff() {
    
      return this.userRole === "Staff"; // Only true if the user's role is 'Staff'
      
    },
    isManager() {
      return this.userRole === "Manager"; // Only true if the user's role is 'Manager'
    },
    isHR() {
      return this.userRole === "HR"; // Only true if the user's role is 'HR'
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin-top: 50px;
}
</style>
