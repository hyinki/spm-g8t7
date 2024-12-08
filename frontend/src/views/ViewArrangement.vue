<script setup>
import HeaderStaff from '../components/HeaderStaff.vue';
import HeaderManager from '../components/HeaderManager.vue';
import HeaderHR from '../components/HeaderHR.vue'; // Import the HR header component
</script>

<template>
   <div v-if="isManager">
    <HeaderManager/>
  
  </div>

  <div v-if="isStaff">
    <HeaderStaff/>
  
  </div>

  <div v-if="isHR">
    <HeaderHR/>
  
  </div>
  <div class="container">
    <div>
      <h1 class="mb-3 mt-2">View Arrangement</h1> <!-- Main heading for the View Arrangement page -->
    </div>

    <!-- Arrangements Table -->
    <div class="row">
      <div class="col">
        <table class="table table-bordered">
          <thead>
            <tr>
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
              <th>Action</th> <!-- New column for the Cancel button -->
            </tr>
          </thead>
          <tbody>
            <tr v-for="(arrangement, index) in arrangements" :key="index">
              <td>{{ formatDate(arrangement.start_date) }}</td>
              <td>{{ formatDate(arrangement.end_date) }}</td>
              <td>{{ arrangement.Requester_Supervisor }}</td>
              <td>{{ arrangement.Request_Status }}</td>
              <td>{{ displayValue(arrangement.Monday) }}</td>
              <td>{{ displayValue(arrangement.Tuesday) }}</td>
              <td>{{ displayValue(arrangement.Wednesday) }}</td>
              <td>{{ displayValue(arrangement.Thursday) }}</td>
              <td>{{ displayValue(arrangement.Friday) }}</td>
              <td>{{ displayValue(arrangement.Saturday) }}</td>
              <td>{{ displayValue(arrangement.Sunday) }}</td>
              <td>
                <button 
                  class="btn btn-danger btn-sm" 

                  @click="confirmCancel(arrangement.request_ID)" 
                  :disabled="arrangement.Request_Status === 'Withdrawn'"
                >
                  Cancel
                </button>
              </td> <!-- Add a cancel button for each row -->
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios"; // Import axios for API requests
import Toastify from 'toastify-js';  // Import Toastify for notifications
import "toastify-js/src/toastify.css";  // Import Toastify CSS
import Cookies from 'js-cookie';

export default {
  name: "ViewArrangement", // Component name
  data() {
    return {
      arrangements: [], // Array to hold the arrangements
      id: Cookies.get('userid'), // Get the user ID from cookies
    };
  },
  created(){
    this.userRole = Cookies.get('userRole'); // Assuming role is stored in cookies
    console.log('User role:', this.userRole);
  },
  computed: {
    ...mapGetters(["userRole"]), // Access user role from Vuex
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
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString(); // Formats the date to 'MM/DD/YYYY' or as per the locale
    },

    displayValue(value) {
      return value === "NULL" || value === '' ? '-' : value; // Replace null or empty string with '-'
    },

    async fetchArrangements() {
      try {
        const response = await axios.get("https://spm-g8t7-flask.onrender.com/viewownrequests",{ headers: { "X-userid": Cookies.get("userid")}}, {
          withCredentials: true, // Include cookies in the request
        });
        // console.log(response.data);
        this.arrangements = response.data; // Set the arrangements data
      } catch (error) {
        console.error("Error fetching arrangements:", error);
        
        Toastify({
        text: "Error fetching arrangements. Please try again later.",
        duration: -1,      // Keeps the toast displayed until closed manually
        close: true,       // Shows close button
        gravity: "top",    // Positions the toast at the top
        position: "right", // Aligns the toast to the top right
        backgroundColor: "#ff0000",  // Optional: red color for error indication
      }).showToast();
        // Log any fetch errors
      }
    },

    // Confirm cancellation of an arrangement
    confirmCancel(requestId) {
      if (confirm("Are you sure you want to cancel this arrangement?")) {
        this.cancelRequest(requestId);
      }
    },

    // Cancel an arrangement request
    async cancelRequest(requestId) {
    try {
      const response = await axios.patch(`https://spm-g8t7-flask.onrender.com/withdrawrequest/${requestId}/${this.id}`, {
        withCredentials: true, // Include cookies in the request
      });

      if (response.data.status === "success") {
        Toastify({
          text: `Cancel arrangement successful`,
          duration: 3000,  // Toast duration in milliseconds
          close: true,
          gravity: "top",
          position: "center",
          backgroundColor: "#4caf50", // Green for success
        }).showToast();

        setTimeout(() => {
          window.location.reload();
        }, 1000); // 1 second delay

      } else {
        console.error("Error deleting request:", response.data.message);
        Toastify({
          text: `An error occurred.`,
          duration: 3000,
          close: true,
          gravity: "top",
          position: "center",
          backgroundColor: "#f44336",  // Red for failure
        }).showToast();
      }
    } catch (error) {
      console.error("Error canceling request:", error);
      Toastify({
        text: `An error occurred.`,
        duration: 3000,
        close: true,
        gravity: "top",
        position: "center",
        backgroundColor: "#f44336",  // Red for failure
      }).showToast();
    }
  } 
},
  mounted() {
    this.fetchArrangements(); // Fetch data when the component is mounted
  },
};
</script>

<style scoped>
/* Add your styles here if needed */
</style>