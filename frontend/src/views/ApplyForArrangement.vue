<script setup>
import HeaderStaff from '../components/HeaderStaff.vue';
</script>

<template>
   <HeaderStaff/>
   <div class="container">
  
    <div>
      <h1>Welcome to apply for arrangement {{ userid }}</h1>
    </div>

    

    <div class="container">
    <!-- Date and Timeslot Picker -->
    <div class="row mb-4">
      <div class="col">
        <label for="datePicker">Start date</label>
        <input type="date" id="datePickerStart" v-model="selectedDateStart" class="form-control" />
      </div>

      <div class="col">
        <label for="datePicker">End date</label>
        <input type="date" id="datePickerEnd" v-model="selectedDateEnd" class="form-control" />
      </div>


    </div>
    <div class="row mb-4">
      <div class="col">
      <label>
        <input type="checkbox" v-model="repeating" @change="updateRepeating" />
        For weekly applications, tick this
      </label>
    </div>
    <div class="col">
      <div class="upload-container">
    <h4>Upload Image as proof of reason</h4>
    <input type="file" @change="handleFileUpload" />
    <button @click="uploadImage">Upload</button>
    <p v-if="imageUrl">Image URL: {{ imageUrl }}</p>
    </div>

    </div>

    </div>

<!-- day selection -->
<div class="row mb-4">
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
</div>

    <!-- Timeslot Selection -->
    <!-- <div class="row mb-4">
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
    </div> -->

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
  </div>
  
   
  
  </template>
  
  <script>
  import { mapState,mapGetters } from "vuex";
  import axios from 'axios';
  import Cookies from "js-cookie";

  export default {
    name: "ApplyForArrangement",
    data() {
    return {
      selectedDateStart: null,
      selectedEndDate:null,
      repeating:false,
      selectedTimeslot: {

      },
      reason: null,
      selectedDays: {
      Monday: false,
      Tuesday: false,
      Wednesday:false,
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

    ...mapState(['supervisor',"dept",'userid']),
    ...mapGetters(['supervisor',"dept",'userid']) // Access state variables // Access getters
  },

  methods: {
    
    // Method to select the timeslot
    // selectTimeslot(timeslot) {
    //   this.selectedTimeslot = timeslot;
    // },
    // Method to handle file upload to cloudinary
    updateRepeating() {
      // This method can be used if you want to perform any actions on checkbox change
      console.log(this.repeating)},

    handleFileUpload(event) {
      this.imageFile = event.target.files[0];
    },
    async uploadImageToCloudinary(file) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('upload_preset', 'upload_proof'); // Set your upload preset

      const response = await axios.post('https://api.cloudinary.com/v1_1/dofj7bkm3/image/upload', formData);
      console.log('Image uploaded successfully:', this.imageUrl);
      console.log("tickbox value "+this.repeating)
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
            console.log('Arrangement submitted:', response.data);
           
            this.arrangements.push(newArrangement);
            alert('Arrangement submitted successfully!');
        
            this.resetForm();
        } catch (error) {
            console.error('Error submitting arrangement:', error);
            alert('Failed to submit arrangement. Please try again.');
        }
    }
},
    resetForm() {
      this.selectedDate = null;
      this.selectedTimeslot = {};
      this.selectedDays= {
      Monday: false,
      Tuesday: false,
      Wednesday:false,
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
  