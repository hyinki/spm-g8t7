<script setup>
import HeaderStaff from '../components/HeaderStaff.vue';
</script>

<template>
  <HeaderStaff/>
 
  <div>
    <h1>Welcome to the view own schedule</h1>
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
</template>

<script>
import axios from 'axios';

export default {
  name: "ViewOwnSchedule",
  data() {
    return {
      selectedMonth: new Date().getMonth() + 1,
      viewType: 'calendar',
      daysOfWeek: ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'],
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
  },
  computed: {
    filteredWFHDays() {
    return this.wfhRequests
      .filter(req => req.Request_Status === 'Approved') // Only approved requests
      .map(req => {
        const wfhDays = [];

        // Get WFH status for each day of the week
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'].forEach(day => {
          if (req[day] && req[day] !== 'NULL') {
            wfhDays.push({
              date: this.formatDate(new Date(req.start_date)), // Format the date
              event: `WFH (${req[day]})`
            });
          }
        });

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
      return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    },
    // Fetch the WFH requests from the backend
    fetchWFHRequests() {
      axios.get("https://spm-g8t7-flask.onrender.com/api/individual_view", { withCredentials: true })
        .then(response => {
          // console.log(response.data);
          this.wfhRequests = response.data.filter(req => req.Request_Status === 'Approved'); // Store only approved requests
          console.log(this.wfhRequests)
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
