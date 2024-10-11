<template>
   <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="/homepage">PlanPro</a>
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
            <li class="nav-item">
              <a class="nav-link" href="/viewarrangement">View Arrangement</a>
            </li>
          </ul>
          <!-- Account Section -->
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <span class="nav-link">
                <img
                  :src="accountIcon"
                  alt="Account"
                  style="width: 20px; margin-right: 5px"
                />
                Hello, {{ userRole }}
              </span>
            </li>
            <li class="nav-item">
              <button class="btn btn-primary" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
    <div>
      <h1>View Arrangement</h1>
    </div>
  
    <!-- Arrangements Table -->
   
    <div class="row">
      <div class="col">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Requester_ID</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Requestor Supervisor</th>
              <th>Request Status</th>
              <th>Monday</th>
              <th>Tuesday</th>
              <th>Wednesday</th>
              <th>Thursday</th>
              <th>Friday</th>
              <th>Saturday</th>
              <th>Sunday</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(arrangement, index) in arrangements" :key="index">
              <td>{{ arrangement.Requester_ID }}</td>
              <td>{{ arrangement.start_date }}</td>
              <td>{{ arrangement.end_date }}</td>
              <td>{{ arrangement.Requester_Supervisor}}</td>
              <td>{{ arrangement.Request_Status }}</td>
              <td>{{ arrangement.Monday }}</td>
              <td>{{ arrangement.Tuesday }}</td>
              <td>{{ arrangement.Wednesday }}</td>
              <td>{{ arrangement.Thursday }}</td>
              <td>{{ arrangement.Friday }}</td>
              <td>{{ arrangement.Saturday }}</td>
              <td>{{ arrangement.Sunday }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  </template>
  
  <script>
import { mapGetters } from "vuex";
import accountIcon from "@/assets/account.png"; // Import the account icon
import Cookies from "js-cookie"; // Import js-cookie to manage cookies
import axios from "axios"; // Import axios for API requests

  
  export default {
    name: "ViewArrangement",
    data() {
      return {
        arrangements: [],
        accountIcon: accountIcon
      };
    },
    computed:{
      ...mapGetters(["userRole"]), 
    },
    methods: {
      async logout() {
      try {
        await axios.post(
          "http://localhost:5000/logout",
          {},
          { withCredentials: true }
        ); // Make POST request to logout
        Cookies.remove("Staff_ID");
        Cookies.remove("userRole");
        this.$router.push("/login"); // Redirect to the login page after logout
      } catch (error) {
        console.error("Logout failed:", error); // Handle any errors that occur during logout
      }
    },
      // Fetch the own requests
      async fetchArrangements() {
  try {
    const response = await axios.get('http://localhost:5000/viewownrequests', {
      withCredentials: true  // Include cookies in the request
    });
    console.log(response.data);
    this.arrangements = response.data;
  } catch (error) {
    console.error("Error fetching arrangements:", error);
  }

}
    },
    mounted() {
      this.fetchArrangements();  // Fetch data when the component is mounted
    }
  };
  </script>
  