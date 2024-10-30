<script setup>
import Cookies from 'js-cookie';
import HeaderStaff from '../components/HeaderStaff.vue';
</script>

<template>
  <HeaderStaff/>
 

  <div>
    <h1>Welcome {{ username }}</h1>
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
                <div v-if="day.dayNumber >= 1">AM: {{ day.AM }}</div>
                <div v-if="day.dayNumber >= 1">PM: {{ day.PM }}</div>
                <div v-if="day.dayNumber >= 1">Full Day: {{ day.wholeday }}</div>
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
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Date</th>
            <th>Timeblock</th>
            <th>Staff Name</th>
          </tr>
          <tr v-for="requests in ownteamschedule" :key="requests.request_ID">
            <td>{{requests.Date}}</td>
            <td>{{requests.Timeblock}}</td>
            <td>{{requests.staff_name}}</td>
          </tr>
        </thead>
      </table>
      <br><h4>In office list</h4>
      <div v-for="(dictionary, date_time) in ownteaminoffice">
      <h5>{{ date_time }}</h5>
      <table class="table table-striped">
      <tr>
      <th>Timeblock</th>
      <th>Staff Name</th>
      </tr>
      <!-- This dictionary here represents the AM:"Array names" -->
      <tbody>
      <tr v-for="(names, time_block) in dictionary" :key="time_block">
        <td>{{ time_block }}</td>
        <td>
          <span v-for="(name, index) in names" :key="index">{{ name }}<span v-if="index < names.length - 1">, </span></span>
        </td>
      </tr>
    </tbody>
      </table>
      </div>
    </div>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import axios from 'axios';

export default {
  name: "ViewOwnTeamSchedule",
  data() {
    return {
      username: "",
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
      dummyEvents: [
      
        // Add more events here
      ],
      ownteamschedule: [],
      own_team_calendar_data:[{1:{"AM": 4, "PM": 3, "wholeday": 5}}],
      ownteaminoffice: {"11/04/24":{"AM":["Michael", "Charles"], "PM":["Michael"], "Whole Day":["Michael", "Charles"]}, "12/04/24":{"AM":["Michael", "Charles"], "PM":["Michael", "Charles"], "Whole Day":["Michael", "Charles"]}},
    };
  },
  computed: {
    calendarWeeks() {
      const firstDayOfMonth = new Date(
        new Date().getFullYear(),
        this.selectedMonth - 1,
        1
      );
      const lastDayOfMonth = new Date(
        new Date().getFullYear(),
        this.selectedMonth,
        0
      );
      const startDate =
        firstDayOfMonth.getDay() === 0 ? -6 : 1 - firstDayOfMonth.getDay();
      const daysArray = [];
      let week = [];

      // Create a mapping from day numbers to AM/PM/full-day data
      const amPmData = {};
      this.own_team_calendar_data.forEach(item => {
        const dayKey = Object.keys(item)[0]; // Get the key (e.g., "1", "2")
        amPmData[dayKey] = item[dayKey]; // Map to the corresponding data
      });


      
      for (let i = startDate; i <= lastDayOfMonth.getDate(); i++) {
        const dayDate = new Date(
          new Date().getFullYear(),
          this.selectedMonth - 1,
          i
        );

      
        const dayKey = i.toString(); // Convert day number to string for key access

        const dayEvents = this.dummyEvents.filter(
          (event) => event.date === dayDate.toISOString().split("T")[0]
        );

        // Fetch AM/PM/full-day data
        // const amPmCounts = amPmData[dayKey] || { am: 0, pm: 0, fullday: 0 };

        // Only set AM/PM counts if the day number is valid (greater than 0)
        const amPmCounts = (i > 0 && i <= lastDayOfMonth.getDate())
        ? (amPmData[dayKey] || { AM: 0, PM: 0, wholeday: 0 })
        : { AM: 0, PM: 0, wholeday: 0 };


        week.push({
          date: dayDate,
          dayNumber: i > 0 ? i : "",
          events: dayEvents,

          //To handle Am Pm counts
          AM: amPmCounts.AM,
          PM: amPmCounts.PM,
          wholeday: amPmCounts.wholeday,


        });
        if (week.length === 7) {
          daysArray.push(week);
          week = [];
        }
      }
      if (week.length) daysArray.push(week);

      return daysArray.filter(week => week.some(day => day.dayNumber !== ""));
      // Original Code
      //return daysArray;
    },
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
    },

    fetchownteamschedule(){
      console.log('Selected month before fetching:', this.selectedMonth)
      var params = { month: this.selectedMonth }
      console.log(params)
      axios.get("https://spm-g8t7-flask.onrender.com/view_own_team_schedule", { headers: {'X-Month': this.selectedMonth,'X-supervisor':Cookies.get("supervisor")}},{withCredentials:true})
      .then(response => {
      this.ownteamschedule = response.data
      console.log(this.ownteamschedule)
      console.log(typeof ownteamschedule)
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    })
    },

    usernameassign(){
      this.username = Cookies.get('username')
    },

    fetchstaffteamdata(){
      var params = {month: this.selectedMonth}
      axios.get("https://spm-g8t7-flask.onrender.com/staff_team_view_calendar",{ headers: {'X-Month': this.selectedMonth,"X-supervisor":Cookies.get()} },{params:params, withCredentials:true})
      .then(response =>{
        // this.calendar_data = response.data
        this.own_team_calendar_data = Object.entries(response.data).map(([key, value]) => ({
        [key]: value
        }));
        console.log(this.own_team_calendar_data)
        console.log(typeof this.own_team_calendar_data)
      })
      .catch(error=>{
        console.error('Error fetching data:', error)
      })
    },

    fetchteaminofficelist(){
      var params = {month: this.selectedMonth}
      axios.get("https://spm-g8t7-flask.onrender.com/view_own_team_in_office_list", {params:params, withCredentials:true})
      .then(response =>{
        this.ownteaminoffice = response.data
        console.log(this.ownteaminoffice)
        console.log(typeof this.ownteaminoffice)
      })
      .catch(error=>{
        console.error('Error fetching data:', error)
      })
    }

  },

  created(){
    this.fetchownteamschedule();
    this.usernameassign();
    this.fetchstaffteamdata();
    this.fetchteaminofficelist();
  },

  watch:{
    selectedMonth(){
      this.fetchownteamschedule();
      this.fetchstaffteamdata();
      this.fetchteaminofficelist();
    }
  }

};

</script>
  