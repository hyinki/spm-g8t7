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
    <h1 class="mb-3 mt-2">Own schedule</h1>
  </div>

  <div class="container">
    <div class="d-flex justify-content-between mb-3">
      <div>
        <label for="monthSelect">Month</label>
        <select id="monthSelect" class="form-select" v-model="selectedMonth">
          <option v-for="month in months" :key="month.value" :value="month.value">{{ month.name }}</option>
        </select>
      </div>
      <div>
        <button class="btn" @click="toggleView('list')">List View</button>
        <button class="btn btn-outline-primary" @click="toggleView('calendar')">Calendar View</button>
      </div>
    </div>

    <!-- Calendar View -->
    <div v-if="viewType === 'calendar'" class="calendar">
      <table class="table table-bordered">
        <thead>
          <tr>
            <th v-for="day in daysOfWeek" :key="day">{{ day }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="week in calendarWeeks" :key="week">
            <td v-for="day in week" :key="day.dayNumber">
              <div :class="['calendar-day', { 'today': isToday(day.date) }]">
                <span>{{ day.dayNumber }}</span>
                <div v-if="day.event">
                  <span :class="day.event.includes('WFH') ? 'text-success' : 'text-warning'">
                    {{ day.event }}
                  </span>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- List View -->
    <div v-else>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="wfhDay in filteredWFHDays" :key="wfhDay.date">
            <td>{{ formatDate(wfhDay.date) }}</td>
            <td :class="wfhDay.event.includes('WFH') ? 'text-success' : 'text-warning'">
              {{ wfhDay.event }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
<br><br><br>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';
export default {
  name: "ViewOwnSchedule",
  data() {
    return {
      selectedMonth: new Date().getMonth() + 1,
      viewType: 'calendar',
      daysOfWeek: ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'],
      months: [
        { name: 'Jan', value: 1 },
        { name: 'Feb', value: 2 },
        { name: 'Mar', value: 3 },
        { name: 'Apr', value: 4 },
        { name: 'May', value: 5 },
        { name: 'Jun', value: 6 },
        { name: 'Jul', value: 7 },
        { name: 'Aug', value: 8 },
        { name: 'Sep', value: 9 },
        { name: 'Oct', value: 10 },
        { name: 'Nov', value: 11 },
        { name: 'Dec', value: 12 },
      ],
      wfhRequests: [], // Store WFH requests fetched from API
    };
  },
  created() {
    this.fetchWFHRequests(); // Fetch WFH requests when the component is created
    this.userRole = Cookies.get('userRole'); // Assuming role is stored in cookies
    console.log('User role:', this.userRole);
  },
  computed: {
    isStaff() {
    
    return this.userRole === "Staff"; // Only true if the user's role is 'Staff'
    
  },
  isManager() {
    return this.userRole === "Manager"; // Only true if the user's role is 'Manager'
  },
  isHR() {
    return this.userRole === "HR"; // Only true if the user's role is 'HR'
  },
    filteredWFHDays() {
  return this.wfhRequests
    .filter(req => req.Request_Status === 'Approved') // Only approved requests
    .map(req => {
      const wfhDays = [];

      // Convert start and end dates into JavaScript Date objects
      const startDate = new Date(req.start_date);
      const endDate = new Date(req.end_date);

      // Iterate from startDate to endDate, checking each day
      for (let day = startDate; day <= endDate; day.setDate(day.getDate() + 1)) {
        const dayOfWeek = day.toLocaleDateString('en-US', { weekday: 'long' });
        if (req[dayOfWeek] && req[dayOfWeek] !== 'NULL') {
          wfhDays.push({
            date: new Date(day), // Store the actual date object here
            event: `WFH (${req[dayOfWeek]})`
          });
        }
      }

      return wfhDays;
      })
      .flat(); // Flatten the array to avoid nested arrays
  },
    calendarWeeks() {
  const year = new Date().getFullYear();
  const firstDayOfMonth = new Date(year, this.selectedMonth - 1, 1);
  const lastDayOfMonth = new Date(year, this.selectedMonth, 0);
  const daysInMonth = lastDayOfMonth.getDate();

  // Adjust for Monday being the first day of the week
  const startDay = (firstDayOfMonth.getDay() + 6) % 7;

  let daysArray = [];
  let week = [];

  // Fill empty cells at the start of the first week
  for (let i = 0; i < startDay; i++) {
    week.push({ dayNumber: '', event: null });
  }

  // Loop over all days of the month
  for (let day = 1; day <= daysInMonth; day++) {
    const currentDate = new Date(year, this.selectedMonth - 1, day);
    const formattedDate = currentDate.toISOString().split('T')[0];

    // Check if the current day has an approved WFH request
    const request = this.wfhRequests.find(req => {
      const startDate = new Date(Date.UTC(
        new Date(req.start_date).getFullYear(),
        new Date(req.start_date).getMonth(),
        new Date(req.start_date).getDate()
      ));

      const endDate = new Date(Date.UTC(
        new Date(req.end_date).getFullYear(),
        new Date(req.end_date).getMonth(),
        new Date(req.end_date).getDate()
      ));

      const currentDateUTC = new Date(Date.UTC(
        currentDate.getFullYear(),
        currentDate.getMonth(),
        currentDate.getDate()
      ));

      return currentDateUTC >= startDate && currentDateUTC <= endDate;
    });

    // Determine the event label based on the request
    let event = 'Work from Office'; // Default event
    if (request) {
      const dayOfWeek = currentDate.toLocaleDateString('en-US', { weekday: 'long' });
      const wfhStatus = request[dayOfWeek]; // Get the WFH status for this day of the week

      if (wfhStatus === 'Whole Day') {
        event = 'WFH (Whole Day)';
      } else if (wfhStatus === 'AM') {
        event = 'WFH (AM)';
      } else if (wfhStatus === 'PM') {
        event = 'WFH (PM)';
      }
    }

    week.push({ date: currentDate, dayNumber: day, event });
    if (week.length === 7) {
      daysArray.push(week);
      week = [];
    }
  }

  // Fill the remaining days of the week after the last day of the month
  if (week.length > 0) {
    while (week.length < 7) {
      week.push({ dayNumber: '', event: null });
    }
    daysArray.push(week);
  }

  return daysArray;
}
},
  methods: {
    toggleView(view) {
      this.viewType = view;
    },
    isToday(date) {
  if (!date) return false; // Check if the date is valid before proceeding
  const today = new Date();
  return today.toDateString() === date.toDateString();
},
    formatDate(dateStr) {
      const date = new Date(dateStr);
      // console.log("this is date: ",date)
      return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    },
    // Fetch the WFH requests from the backend
    fetchWFHRequests() {

      axios.get("https://spm-g8t7-flask.onrender.com/api/individual_view",{ headers: { "X-userid": Cookies.get("userid")}}, { withCredentials: true })
        .then(response => {
          // console.log(response.data);
          this.wfhRequests = response.data.filter(req => req.Request_Status === 'Approved'); // Store only approved requests
          // console.log(this.wfhRequests)
        })
        .catch(error => {
          console.error('Error fetching WFH requests:', error);
        });
    }
  }
};
</script>

<style scoped>
  .form-check-input {
    margin-right: 10px;
  }
  .form-select {
    max-width: 200px;
  }
  .calendar-day {
    padding: 10px;
  }
  .text-success {
    color: green;
  }
  .text-warning {
    color: orange;
  }
</style>
