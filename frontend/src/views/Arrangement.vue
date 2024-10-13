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
          <th>Date of Arrangement</th>
          <th>Approve/Reject</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in pendingRequests" :key="request.id">
          <td>{{ request.name }}</td>
          <td>{{ formatDate(request.date) }}</td>
          <td>
            <button class="btn btn-success" @click="approveRequest(request)">Approve</button>
            <button class="btn btn-danger" @click="rejectRequest(request)">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "Arrangement",
  data() {
    return {
      // Simulate static data (pending requests)
      pendingRequests: [
        { id: 1, name: 'James Teo', date: '2024-03-02' },
        { id: 2, name: 'Mary Tan', date: '2024-04-05' },
        { id: 3, name: 'Sean Goh', date: '2024-11-15' }
      ]
    };
  },
  methods: {
    // Approve request action (to be integrated with backend later)
    approveRequest(request) {
      console.log(`Approved request from ${request.name}`);
      // Placeholder for future API call
      // axios.post('/api/approve', { id: request.id }).then(...)
    },
    // Reject request action (to be integrated with backend later)
    rejectRequest(request) {
      console.log(`Rejected request from ${request.name}`);
      // Placeholder for future API call
      // axios.post('/api/reject', { id: request.id }).then(...)
    },
    // Format date to a readable format
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    }
  }
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
