<template>
<div v-if="isStaff">
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
    <h1>Welcome to the view team schedule (Staff)</h1>
  </div>

</div>

<div v-if="isManager">
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
              <a class="nav-link" href="/viewteamschedule">View Team Schedule</a>
            </li>
            
            <li class="nav-item">
              <a class="nav-link" href="/arrangement">Approve/RejectArrangement</a>
            </li>
            
          </ul>
        </div>
      </div>
    </nav>
    <div>
    <h1>Welcome to the view team schedule (Manager)</h1>
  </div>
</div>

<div v-if="isHR">
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
              <a class="nav-link" href="/viewoverallschedule">View Overall Schedule</a>
            </li>
            
            <li class="nav-item">
              <a class="nav-link" href="/viewteamschedule">View Team Schedule</a>
            </li>
            
          </ul>
        </div>
      </div>
    </nav>

    <div>
    <h1>Welcome to the view team schedule (HR)</h1>
  </div>
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
            <td v-for="day in week" :key="day.date">
              <div :class="['calendar-day', { 'today': isToday(day.date) }]">
                <span>{{ day.dayNumber }}</span>
                <div v-if="day.events.length" class="events">
                  <div v-for="event in day.events" :key="event.name" :class="['event', event.type === 'office' ? 'text-warning' : 'text-success']">
                    {{ event.name }} {{ event.type === 'office' ? 'in Office' : 'WFH' }}
                  </div>
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
            <th>Time</th>
            <th>Activity</th>
            <th>Office/WFH</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in dummyEvents" :key="event.name">
            <td>{{ formatDate(event.date) }}</td>
            <td>1pm - 2pm</td> <!-- You can customize the time format -->
            <td>Meeting</td>
            <td>
              <div v-if="event.type === 'office'">
                {{ event.name }} - Office
              </div>
              <div v-else>
                {{ event.name }} - WFH
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

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
      dummyEvents: [
        { name: 'Sarah Koh', date: '2024-09-10', type: 'office' },
        { name: 'Mary Tan', date: '2024-10-03', type: 'office' },
        { name: 'Sean Goh', date: '2024-10-03', type: 'office' },
        { name: 'Elliot Tay', date: '2024-10-03', type: 'wfh' },
        // Add more events here
      ],
    };
  },
  computed: {
    ...mapGetters(['userRole']), // Access the user's role from Vuex
    isStaff() {
      return this.userRole === 'Staff'; // Only true if the user's role is 'Staff'
    },
    isManager() {
      return this.userRole === 'Manager'; // Only true if the user's role is 'Manager'
    },
    isHR() {
      return this.userRole === 'HR'; // Only true if the user's role is 'Manager'
    },
    calendarWeeks() {
      const firstDayOfMonth = new Date(new Date().getFullYear(), this.selectedMonth - 1, 1);
      const lastDayOfMonth = new Date(new Date().getFullYear(), this.selectedMonth, 0);
      const startDate = firstDayOfMonth.getDay() === 0 ? -6 : 1 - firstDayOfMonth.getDay();
      const daysArray = [];
      let week = [];

      for (let i = startDate; i <= lastDayOfMonth.getDate(); i++) {
        const dayDate = new Date(new Date().getFullYear(), this.selectedMonth - 1, i);
        const dayEvents = this.dummyEvents.filter(event => event.date === dayDate.toISOString().split('T')[0]);
        week.push({ date: dayDate, dayNumber: i > 0 ? i : '', events: dayEvents });
        if (week.length === 7) {
          daysArray.push(week);
          week = [];
        }
      }
      if (week.length) daysArray.push(week);

      return daysArray;
    }
  },
  methods: {
    toggleView(view) {
      this.viewType = view;
    },
    isToday(date) {
      const today = new Date();
      return today.toDateString() === date.toDateString();
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    }
  }
};
</script>
  