<script setup>
import HeaderStaff from '../components/HeaderStaff.vue';
</script>

<template>
  <HeaderStaff />
  <div class="container">

    <div>
      <h1 class="mt-3 mb-3">Welcome to apply for arrangement </h1>
    </div>



    <div class="container">
      <!-- Date and Timeslot Picker -->
      <div class="row mb-4">
        <div class="col">
        
          <h4>Start date</h4>
          <input type="date" id="datePickerStart" v-model="selectedDateStart" class="form-control" />
        </div>

        <div class="col">
          <h4>End date</h4>
          <input type="date" id="datePickerEnd" v-model="selectedDateEnd" class="form-control" />
        </div>


      </div>
      

      <!-- day selection -->
      <!-- <div class="row mb-4">
        <div class="col">
          <h4>Select Days:</h4>
          <div v-for="(day, index) in days" :key="index">
            <label>
              <input type="checkbox" v-model="selectedDays[day]" /> {{ day }}
            </label>
            <select v-if="selectedDays[day]" v-model="selectedTimeslot[day]">
              <option value="">Select Timeslot</option>
              <option value="AM">AM</option>
              <option value="PM">PM</option>
              <option value="Whole day">Full day</option>
            </select>
          </div>
        </div>
      </div> -->

      <div class="row mb-4">
        <div class="col">
          <h4>Select Days</h4>
          <div class="form-group">
            <div v-for="(day, index) in days" :key="index" class="mb-3">
              <!-- Checkbox for each day -->
              <div class="form-check">
                <input 
                  type="checkbox" 
                  class="form-check-input" 
                  :id="`day-${index}`" 
                  v-model="selectedDays[day]"
                />
                <label class="form-check-label" :for="`day-${index}`">{{ day }}</label>
              </div>

              <!-- Timeslot dropdown, shown if the day is selected -->
              <div v-if="selectedDays[day]" class="mt-2">
                <select 
                  v-model="selectedTimeslot[day]" 
                  class="form-select" 
                  :id="`timeslot-${index}`"
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
        
        
        <!-- <div class="col">
          <div class="upload-container">
            <h4>Upload Image as proof of reason</h4>
            <input type="file" @change="handleFileUpload" />
            <button @click="uploadImage">Upload</button>
            <p v-if="imageUrl">Image URL: {{ imageUrl }}</p>
          </div>

        </div> -->

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


    </div>
  </div>
</template>
  
<script>
import { mapState, mapGetters } from "vuex";
import axios from 'axios';
import Cookies from "js-cookie";
import Toastify from 'toastify-js'

import "toastify-js/src/toastify.css";  // Import Toastify CSS

export default {
  name: "ApplyForArrangement",
  data() {
    return {
      selectedDateStart: null,
      selectedEndDate: null,
      repeating: false,
      selectedTimeslot: {

      },
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
      days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], // Ensure this is included
      arrangements: [], // To store the arrangements
    };
  },
  created() {
    this.userID = Cookies.get('userid')
    this.dept = Cookies.get('dept')
    this.supervisor = Cookies.get('supervisor')
    console.log(this.userID)
  },
  computed: {

    ...mapState(['supervisor', "dept", 'userid']),
    ...mapGetters(['supervisor', "dept", 'userid']) // Access state variables // Access getters
  },

  methods: {

    // Method to select the timeslot
    // selectTimeslot(timeslot) {
    //   this.selectedTimeslot = timeslot;
    // },
    // Method to handle file upload to cloudinary
    updateRepeating() {
      // This method can be used if you want to perform any actions on checkbox change
      console.log(this.repeating)
    },

    handleFileUpload(event) {
      this.imageFile = event.target.files[0];
    },
    async uploadImageToCloudinary(file) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('upload_preset', 'upload_proof'); // Set your upload preset

      const response = await axios.post('https://api.cloudinary.com/v1_1/dofj7bkm3/image/upload', formData);
      console.log('Image uploaded successfully:', this.imageUrl);
      console.log("tickbox value " + this.repeating)
      return response.data.secure_url; // Return the URL of the uploaded image
    },


    // Method to submit the arrangement
    async submitArrangement() {
      if (this.selectedDateStart && Object.values(this.selectedDays).some(day => day)) {
        try {
          // Initialize imageUrl to an empty string or null
          let imageUrl = null;
          console.log(this.repeating);

          // If an image is uploaded, upload it to Cloudinary
          if (this.imageFile) {
            imageUrl = await this.uploadImageToCloudinary(this.imageFile);
            console.log(imageUrl);
          }

          console.log(this.repeating);
          console.log("userid is " + this.userID);
          console.log("Selected Timeslot:", this.selectedTimeslot);

          const newArrangement = {
            userId: this.userID,
            supervisor: this.supervisor,
            dept: this.dept,
            startDate: this.selectedDateStart,
            endDate: this.selectedDateEnd,
            repeating: this.repeating,

            selectedDays: this.days.map(day => ({
              day,
              timeslot: this.selectedDays[day] ? this.selectedTimeslot[day] : null // Return null if not selected
            })),
            approved: "pending",
            cloudinary_link: imageUrl // Use imageUrl which will be null if no image was uploaded
          };

          const response = await axios.post('http://localhost:5000/submit_wfh_request', newArrangement);
          Toastify({
            text: `Request submitted successfully!`,
            duration: 3000,  // Toast duration in milliseconds
            close: true,     // Show close button
            gravity: "top",  // Position of toast
            position: "center", // Center horizontally
            backgroundColor: "#4caf50",  // Green for success
          }).showToast();

          this.arrangements.push(newArrangement);

          this.resetForm();
        } catch (error) {
          console.error('Error submitting arrangement:', error);
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
      this.selectedDays = {
        Monday: false,
        Tuesday: false,
        Wednesday: false,
        Thursday: false,
        Friday: false,
        Saturday: false,
        Sunday: false,
      }

      this.imageFile = null; // Reset image file
    },
    formatDate(date) {
      const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(date).toLocaleDateString('en-US', options);
    },
  },//methods



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