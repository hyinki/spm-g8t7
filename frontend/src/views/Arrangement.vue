<script setup>

import HeaderManager from '../components/HeaderManager.vue';
</script>
<template>
  <!-- Navbar -->
  <HeaderManager/>

  <!-- Title -->
  <div>
    <h1>Pending Work Arrangements</h1>
  </div>

  <!-- Table of Pending Requests -->
  <div class="container mt-4">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Name</th>
          <th>Start date</th>
          <th>End date</th>
          <th>Monday</th>
          <th>Tuesday</th>
          <th>Wednesday</th>
          <th>Thursday</th>
          <th>Friday</th>
          <th>Saturday</th>
          <th>Sunday</th>
          <th>Proof</th>
          <th>Approve/Reject</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in teamRequests" :key="request.id">
          <td>{{ request.staff_name}}</td>
          <td>{{ formatDate(request.start_date) }}</td>
          <td>{{ formatDate(request.end_date) }}</td>
          <td>{{request.Monday }}</td>
          <td>{{request.Tuesday }}</td>
          <td>{{request.Wednesday}}</td>
          <td>{{request.Thursday}}</td>
          <td>{{request.Friday}}</td>
          <td>{{request.Saturday}}</td>
          <td>{{request.Sunday}}</td>
          <td>       <a v-if="request.cloudinary_link" :href="request.cloudinary_link" target="_blank" rel="noopener noreferrer">
        View Proof
      </a>
      <span v-else>No proof uploaded</span> <!-- Placeholder when there's no link -->
    </td>
          <td>
            <button class="btn btn-success" @click="approveRequest(request.request_ID)">Approve</button>
            <button class="btn btn-danger" @click="rejectRequest(request.request_ID)">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios, { HttpStatusCode } from 'axios';
import Toastify from "toastify-js";

export default {
  name: "Arrangement",
  data() {
    return {
      // Simulate static data (pending requests)
      pendingRequests: [
        { id: 1, name: 'James Teo', date: '2024-03-02' },
        { id: 2, name: 'Mary Tan', date: '2024-04-05' },
        { id: 3, name: 'Sean Goh', date: '2024-11-15' }
      ],
      teamRequests: [],
    };
  },computed(){
    selectedRequestId:0
  },
  methods: {

    fetchRequests(){
      
      axios.get("http://localhost:5000/manager_to_approve", {withCredentials:true}).then(response => {
        this.teamRequests = response.data
        console.log(response.data)
      
      
    })
    },

    // Approve request action (to be integrated with backend later)
    approveRequest(request) {
      var params = {request: request}
      console.log(params)
      // Placeholder for future API call
      axios.get('http://localhost:5000/approve_request', {params:params, withCredentials:true}).then(response => {

        Toastify({
          text: response.data.message,
          duration: 3000, // Duration in milliseconds
          gravity: "top", // `top` or `bottom`
          position: 'center', // `left`, `center` or `right`
          backgroundColor: "#4caf50", // Customize color
          className: "info",
          stopOnFocus: true, // Prevents dismissing of toast on hover
        }).showToast();
        console.log(response.data.message)

        setTimeout(() => {
          location.reload();
        }, 1000);
      });
    },
    // Reject request action (to be integrated with backend later)
    rejectRequest(request) {
      var params = {request: request}
      console.log(params)
      // Placeholder for future API call
      axios.get('http://localhost:5000/reject_request', {params:params, withCredentials:true}).then(response => {
        Toastify({
          text: response.data.message,
          duration: 3000, // Duration in milliseconds
          gravity: "top", // `top` or `bottom`
          position: 'center', // `left`, `center` or `right`
          backgroundColor: "#4caf50", // Customize color
          className: "info",
          stopOnFocus: true, // Prevents dismissing of toast on hover
        }).showToast();
        console.log(response.data.message)

        setTimeout(() => {
        location.reload();
      }, 1000);
      });
    },
    // Format date to a readable format
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    }
  },
  created(){
    this.fetchRequests();

  },
};
</script>

<style scoped>
.table {
  margin-top: 20px;
}
.btn-success {
  margin-right: 10px;
}
</style>
