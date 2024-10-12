<script setup>
import HeaderStaff from '../components/HeaderStaff.vue';

</script>

<template>
  <HeaderStaff />
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
              <th>Action</th> <!-- New column for the Cancel button -->
            </tr>
          </thead>
          <tbody>
            <tr v-for="(arrangement, index) in arrangements" :key="index">
              
              <td>{{ arrangement.Requester_ID }}</td>
              <td>{{ arrangement.start_date }}</td>
              <td>{{ arrangement.end_date }}</td>
              <td>{{ arrangement.Requester_Supervisor }}</td>
              <td>{{ arrangement.Request_Status }}</td>
              <td>{{ arrangement.Monday }}</td>
              <td>{{ arrangement.Tuesday }}</td>
              <td>{{ arrangement.Wednesday }}</td>
              <td>{{ arrangement.Thursday }}</td>
              <td>{{ arrangement.Friday }}</td>
              <td>{{ arrangement.Saturday }}</td>
              <td>{{ arrangement.Sunday }}</td>
              <td>
                <button class="btn btn-danger btn-sm" @click="cancelRequest(arrangement.request_ID, index)">
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

export default {
  name: "ViewArrangement",
  data() {
    return {
      arrangements: [],
    };
  },
  computed: {
    ...mapGetters(["userRole"]),
  },
  methods: {
    // Fetch the user's requests
    async fetchArrangements() {
      try {
        const response = await axios.get("http://localhost:5000/viewownrequests", {
          withCredentials: true, // Include cookies in the request
        });
        console.log(response.data);
        this.arrangements = response.data;
      } catch (error) {
        console.error("Error fetching arrangements:", error);
      }
    },

    // Method to cancel/delete a request
    async cancelRequest(requestId, index) {
      try {
        const response = await axios.delete(`http://localhost:5000/deleterequest/${requestId}`, {
          withCredentials: true, // Include cookies in the request
        });

        if (response.data.status === "success") {
          // Remove the deleted request from the table
          this.arrangements.splice(index, 1);
          console.log("Request deleted successfully!");
          Toastify({
            text: `Cancel arrangement successful`,
            duration: 3000,  // Toast duration in milliseconds
            close: true,     // Show close button
            gravity: "top",  // Position of toast
            position: "center", // Center horizontally
            backgroundColor: "#4caf50",  // Green for success
          }).showToast();

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
    },
  },
  mounted() {
    this.fetchArrangements(); // Fetch data when the component is mounted
  },
};
</script>

<style scoped>
/* Add your styles here if needed */
</style>
