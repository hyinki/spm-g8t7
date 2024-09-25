<template>
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
            <a class="nav-link active" aria-current="page" href="/homepage">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/viewteamschedule">Team Schedule</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/viewownschedule">Own Schedule</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/applyforarrangement">Apply For Arrangement</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  
    <div>
      <h1>Welcome to apply for arrangement</h1>
    </div>

    

    <div class="container">
    <!-- Date and Timeslot Picker -->
    <div class="row mb-4">
      <div class="col">
        <label for="datePicker">Which day are you applying for arrangement?</label>
        <input type="date" id="datePicker" v-model="selectedDate" class="form-control" />
      </div>
    </div>

    <!-- Timeslot Selection -->
    <div class="row mb-4">
      <div class="col">
        <label for="timeslotSelect">Timeslot</label>
        <div class="btn-group d-block" role="group">
          <button
            type="button"
            class="btn"
            :class="selectedTimeslot === 'AM' ? 'btn-primary' : 'btn-outline-primary'"
            @click="selectTimeslot('AM')"
          >
            AM (9AM - 1PM)
          </button>
          <button
            type="button"
            class="btn"
            :class="selectedTimeslot === 'PM' ? 'btn-primary' : 'btn-outline-primary'"
            @click="selectTimeslot('PM')"
          >
            PM (2PM - 6PM)
          </button>
          <button
            type="button"
            class="btn"
            :class="selectedTimeslot === 'Full day' ? 'btn-primary' : 'btn-outline-primary'"
            @click="selectTimeslot('Full day')"
          >
            Full day (9AM - 6PM)
          </button>
        </div>
      </div>
    </div>

    <!-- Submit Button -->
    <div class="row mb-4">
      <div class="col">
        <button class="btn btn-primary" @click="submitArrangement">Submit</button>
      </div>
    </div>

    <!-- Arrangements Table -->
    <div class="row">
      <div class="col">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Date</th>
              <th>Timeslot</th>
              <th>Approved</th>
              <th>Cancel</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(arrangement, index) in arrangements" :key="index">
              <td>{{ formatDate(arrangement.date) }}</td>
              <td>{{ arrangement.timeslot }}</td>
              <td>{{ arrangement.approved ? 'Yes' : 'No' }}</td>
              <td>
                <button class="btn btn-danger" @click="cancelArrangement(index)">Cancel</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  
   
  
  </template>
  
  <script>
  
  export default {
    name: "ApplyForArrangement",
    data() {
    return {
      selectedDate: null, // To hold the selected date
      selectedTimeslot: '', // To hold the selected timeslot
      arrangements: [], // To store the arrangements
    };
  },
  methods: {
    // Method to select the timeslot
    selectTimeslot(timeslot) {
      this.selectedTimeslot = timeslot;
    },
    
    // Method to submit the arrangement
    submitArrangement() {
      if (this.selectedDate && this.selectedTimeslot) {
        this.arrangements.push({
          date: this.selectedDate,
          timeslot: this.selectedTimeslot,
          approved: Math.random() > 0.5, // Randomly approve or deny for demo purposes
        });
        this.resetForm();
      } else {
        alert('Please select a date and timeslot');
      }
    },

    // Method to cancel an arrangement
    cancelArrangement(index) {
      this.arrangements.splice(index, 1);
    },

    // Reset form inputs after submission
    resetForm() {
      this.selectedDate = null;
      this.selectedTimeslot = '';
    },

    // Format date for display
    formatDate(date) {
      const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(date).toLocaleDateString('en-US', options);
    },
  },
};

  </script>
  