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
  