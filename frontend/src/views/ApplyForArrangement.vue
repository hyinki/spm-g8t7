<script setup>
import HeaderStaff from '../components/HeaderStaff.vue';
</script>

<template>
  <HeaderStaff />
  <div class="container">
    <div>
      <h1 class="mt-3 mb-3">Apply for arrangement</h1>
    </div>

    <div class="container">
      <!-- Date and Timeslot Picker -->
      <div class="row mb-4">
        <div class="col">
          <h4>Start date</h4>
          <input type="date" id="datePickerStart" v-model="selectedDateStart" class="form-control" :min="currentDate"/>
        </div>

        
        <div class="col">
          <h4>End date</h4>
          <input type="date" id="datePickerEnd" v-model="selectedDateEnd" class="form-control" :min="selectedDateStart || currentDate" />
        </div>
      </div>

      <!-- Timeslot Selection for Each Day -->
      <div class="row mb-4">
        <div class="col">
          <h4>Select Timeslots</h4>
          <div class="form-group">
            <div v-for="(day, index) in days" :key="index" class="mb-3">
              <div class="form-check">
                <!-- Timeslot dropdown, enabled only if the day is within the date range -->
                <label class="form-check-label">{{ day }}</label>
                <select 
                  v-model="selectedTimeslot[day]" 
                  class="form-select" 
                  :id="`timeslot-${index}`"
                  :disabled="!isDayInRange(day)"
                >
                  <option value="">Select Timeslot</option>
                  <option value="AM">AM</option>
                  <option value="PM">PM</option>
                  <option value="Whole day">Full day</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div class="col">
          <label>
            <input type="checkbox" v-model="repeating" @change="updateRepeating" />
            For weekly applications, tick this
          </label>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col">
          <div class="card p-3">
            <h5 class="card-title">Upload Proof</h5>
            <p class="card-text">Please upload an image as proof of your reason.</p>
            <div class="mb-3">
              <input type="file" class="form-control" id="uploadInput" @change="handleFileUpload" />
            </div>
            <button class="btn btn-primary" @click="uploadImage">Upload</button>
          </div>
        </div>
        <div class="col"></div>
      </div>

      <!-- Submit Button -->
      <div class="row mb-4">
        <div class="col">
          <button class="btn btn-primary" @click="submitArrangement">Submit</button>
        </div>
      </div>

      <div>
        
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";
import axios from 'axios';
import Cookies from "js-cookie";
import Toastify from 'toastify-js';

import "toastify-js/src/toastify.css";  // Import Toastify CSS

export default {
  name: "ApplyForArrangement",
  data() {
    return {
      selectedDateStart: null,
      selectedDateEnd: null,
      currentDate: new Date().toISOString().split('T')[0], // Get today's date in YYYY-MM-DD format
      repeating: false,
      selectedTimeslot: {},
      reason: null,
      selectedDays: {
        Monday: false,
        Tuesday: false,
        Wednesday: false,
        Thursday: false,
        Friday: false,
        Saturday: false,
        Sunday: false,
      },
      days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      arrangements: [], // To store the arrangements
    };
  },
  created() {
    this.userID = Cookies.get('userid');
    this.dept = Cookies.get('dept');
    this.supervisor = Cookies.get('supervisor');
    console.log(this.userID);
  },
  computed: {
    ...mapState(['supervisor', "dept", 'userid']),
    ...mapGetters(['supervisor', "dept", 'userid']) // Access state variables // Access getters
  },
  methods: {
    getDayIndex(day) {
      const dayIndices = {
        Monday: 1,
        Tuesday: 2,
        Wednesday: 3,
        Thursday: 4,
        Friday: 5,
        Saturday: 6,
        Sunday: 7,
      };
      return dayIndices[day];
    },

    // Check if the given day is within the selected date range
    isDayInRange(day) {
      if (!this.selectedDateStart || !this.selectedDateEnd) {
        return false;
      }

      const startDate = new Date(this.selectedDateStart);
      const endDate = new Date(this.selectedDateEnd);

      const startDayIndex = startDate.getDay(); // 0 = Sunday, 1 = Monday, ...
      const endDayIndex = endDate.getDay();

      const dayIndex = this.getDayIndex(day);

      return (
        (startDayIndex <= dayIndex && dayIndex <= endDayIndex) ||
        (startDayIndex > endDayIndex && (dayIndex >= startDayIndex || dayIndex <= endDayIndex))
      );
    },

    handleFileUpload(event) {
      this.imageFile = event.target.files[0];
    },

    async uploadImageToCloudinary(file) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('upload_preset', 'upload_proof'); // Set your upload preset

      const response = await axios.post('https://api.cloudinary.com/v1_1/dofj7bkm3/image/upload', formData);
      return response.data.secure_url; // Return the URL of the uploaded image
    },

    // Validate form to ensure timeslots are selected for each enabled day
    validateTimeslots() {
      for (const day of this.days) {
        if (this.isDayInRange(day) && (!this.selectedTimeslot[day] || this.selectedTimeslot[day] === "")) {
          Toastify({
            text: `Please select a timeslot for ${day}.`,
            duration: 3000,
            close: true,
            gravity: "top",
            position: "center",
            backgroundColor: "#ff9800",  // Orange for warning
          }).showToast();
          return false;
        }
      }
      return true;
    },

    // Method to submit the arrangement
    async submitArrangement() {
      // Validate that timeslots are selected for all enabled days
      if (!this.validateTimeslots()) {
        return; // Stop if validation fails
      }

      if (this.selectedDateStart && Object.values(this.selectedTimeslot).some(slot => slot)) {
        try {
          let imageUrl = null;

          if (this.imageFile) {
            imageUrl = await this.uploadImageToCloudinary(this.imageFile);
          }

          const newArrangement = {
            userId: this.userID,
            supervisor: this.supervisor,
            dept: this.dept,
            startDate: this.selectedDateStart,
            endDate: this.selectedDateEnd,
            repeating: this.repeating,
            selectedDays: this.days.map(day => ({
              day,
              timeslot: this.selectedTimeslot[day] ? this.selectedTimeslot[day] : null // Return null if not selected
            })),
            approved: "pending",
            cloudinary_link: imageUrl // Use imageUrl which will be null if no image was uploaded
          };
          
          await axios.post('https://spm-g8t7-flask.onrender.com/submit_wfh_request', newArrangement);
          Toastify({
            text: `Request submitted successfully!`,
            duration: 3000,  // Toast duration in milliseconds
            close: true,
            gravity: "top",
            position: "center",
            backgroundColor: "#4caf50",  // Green for success
          }).showToast();

          this.arrangements.push(newArrangement);
          this.resetForm();
        } catch (error) {
          Toastify({
            text: "Request submission failed.",
            duration: 3000,
            close: true,
            gravity: "top",
            position: "center",
            backgroundColor: "#ff9800",  // Orange for warning
          }).showToast();
        }
      }
    },

    resetForm() {
      this.selectedDateStart = null;
      this.selectedDateEnd = null;
      this.selectedTimeslot = {};
      this.imageFile = null; // Reset image file
    },
  },
};
</script>

<style scoped>
  .form-check-input {
    margin-right: 10px;
  }
  .form-select {
    max-width: 200px;
  }
</style>
