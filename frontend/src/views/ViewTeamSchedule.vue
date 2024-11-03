<script setup>
import HeaderStaff from '../components/HeaderStaff.vue';
import HeaderHR from '../components/HeaderHR.vue';
import HeaderManager from '../components/HeaderManager.vue';

</script>

<template>
  <!-- Staff Section -->
  <div v-if="isStaff"> 
    <HeaderStaff/>
    
    <div>
      <h1 >Welcome to the view team schedule (Staff)</h1>
    </div>
  </div>
  
  <!-- Manager Section -->
  <div v-if="isManager">
    <HeaderManager/>
    <div class="container">
      <h1 class="mb-3 mt-2">View Team Schedule (Manager)</h1>
    </div>
  </div>

  <!-- HR Section -->
  <div v-if="isHR">
    <HeaderHR/>

    <div class="container">
      <h1 class="mb-3 mt-2">View Team Schedule (HR)</h1>
    </div>
  </div>

  <div class="container">
    <div class="d-flex justify-content-between mb-3">
      <div>
        <label for="monthSelect">Month</label>
        <select id="monthSelect" class="form-select" v-model="selectedMonth">
          <option
            v-for="month in months"
            :key="month.value"
            :value="month.value"
          >
            {{ month.name }}
          </option>
        </select>
      </div>
      <div>
        <button class="btn" @click="toggleView('list')">List View</button>
        <button class="btn btn-outline-primary" @click="toggleView('calendar')">
          Calendar View
        </button>
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
              <div :class="['calendar-day', { today: isToday(day.date) }]">
                <span>{{ day.dayNumber }}</span>
                <div v-if="day.dayNumber >= 1">AM: {{ day.AM }}</div>
                <div v-if="day.dayNumber >= 1">PM: {{ day.PM }}</div>
                <div v-if="day.dayNumber >= 1">Full Day: {{ day.wholeday }}</div>
                <div v-if="day.events.length" class="events">
                  <div
                    v-for="event in day.events"
                    :key="event.name"
                    :class="[
                      'event',
                      event.type === 'office' ? 'text-warning' : 'text-success',
                    ]"
                  >
                    {{ event.name }}
                    {{ event.type === "office" ? "in Office" : "WFH" }}
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
            <td>1pm - 2pm</td>
            <!-- You can customize the time format to match what is needed-->
            <td>Meeting</td>
            <td>
              <div v-if="event.type === 'office'">
                {{ event.name }} - Office
              </div>
              <div v-else>{{ event.name }} - WFH</div>
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
          <tr v-for="requests in teamschedule" :key="requests.request_ID">
            <td>{{requests.Date}}</td>
            <td>{{requests.Timeblock}}</td>
            <td>{{requests.staff_name}}</td>
          </tr>
        </thead>
      </table>
      <br><h4>In office list</h4>
      <div v-for="(dictionary, date_time) in inoffice">
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
import { mapGetters } from "vuex";
import axios, { HttpStatusCode } from 'axios';
import Cookies from 'js-cookie'

export default {
  name: "ViewOwnSchedule",
  data() {
    return {
      selectedMonth: new Date().getMonth() + 1,
      viewType: "calendar",
      daysOfWeek: ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"],
      months: [
        { name: "Jan", value: 1 },
        { name: "Feb", value: 2 },
        { name: "Mar", value: 3 },
        { name: "Apr", value: 4 },
        { name: "May", value: 5 },
        { name: "Jun", value: 6 },
        { name: "Jul", value: 7 },
        { name: "Aug", value: 8 },
        { name: "Sep", value: 9 },
        { name: "Oct", value: 10 },
        { name: "Nov", value: 11 },
        { name: "Dec", value: 12 },
      ],
      dummyEvents: [

        // Add more events here
      ],
      teamschedule: [],
calendar_data: [
    {
        1: {
            "AM": 999,
            "PM": 999,
            "wholeday": 999
        }
    }
],
inoffice: {
    "11/04/24": {
        "AM": ["Michael", "Charles"],
        "PM": ["Michael"],
        "Whole Day": ["Michael", "Charles"]
    },
    "12/04/24": {
        "AM": ["Michael", "Charles"],
        "PM": ["Michael", "Charles"],
        "Whole Day": ["Michael", "Charles"]
    }
},
    };
  },


  computed: {
    ...mapGetters(["userRole"]), // Access the user's role from Vuex
    isStaff() {
      return this.userRole === "Staff"; // Only true if the user's role is 'Staff'
    },
    isManager() {
      return this.userRole === "Manager"; // Only true if the user's role is 'Manager'
    },
    isHR() {
      return this.userRole === "HR"; // Only true if the user's role is 'Manager'
    },
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
      this.calendar_data.forEach(item => {
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
    fetchteamschedule(){
      console.log('Selected month before fetching:', this.selectedMonth)
      var params = { month: this.selectedMonth }
      console.log(params)
      console.log("User id is ",Cookies.get("userid"))
      
      axios.get("https://spm-g8t7-flask.onrender.com/api/manager_view", 
      { headers: {'X-Month': this.selectedMonth, "X-userid": Cookies.get("userid")}}
      // {params:params, withCredentials:true}
    )
      .then(response => {
      this.teamschedule = response.data
      console.log(this.teamschedule)
      console.log(typeof teamschedule)
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    })
    },

    fetch_calendar_data(){
      var params = {month: this.selectedMonth}
      axios.get("https://spm-g8t7-flask.onrender.com/manager_view_calendar",
      { headers: {'X-Month': this.selectedMonth, "X-userid": Cookies.get("userid")}}
      //{ headers: {month: this.selectedMonth,}}
   
  )
      
      .then(response =>{
        // this.calendar_data = response.data
        this.calendar_data = Object.entries(response.data).map(([key, value]) => ({
        [key]: value
      
        }));
        console.log(this.calendar_data)
        console.log(typeof this.calendar_data)
      })
      .catch(error=>{
        console.error('Error fetching data:', error)
      })
    },

    fetch_team_schedule_list(){
      var params = {month: this.selectedMonth}
      axios.get("https://spm-g8t7-flask.onrender.com/manager_list_in_office",
      { headers: {'X-Month': this.selectedMonth, "X-userid": Cookies.get("userid")}}
      
      // {params:params, withCredentials:true}
    )
      .then(response =>{
        this.inoffice = response.data
        console.log(this.inoffice)
        console.log(typeof this.inoffice)
      })
      .catch(error=>{
        console.error('Error fetching data:', error)
      })
    },

    toggleView(view) {
      this.viewType = view;
    },
    isToday(date) {
      const today = new Date();
      return today.toDateString() === date.toDateString();
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
      });
    },
  },

  created(){
    this.fetchteamschedule();
    this.fetch_calendar_data();
    this.fetch_team_schedule_list();
  },

  watch:{
    selectedMonth(){
      this.fetchteamschedule();
      this.fetch_calendar_data();
      this.fetch_team_schedule_list();
    }
  }
};


</script>
