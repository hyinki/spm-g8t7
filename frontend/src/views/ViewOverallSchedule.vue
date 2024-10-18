<script setup>
import HeaderHR from '../components/HeaderHR.vue';
</script>
<template>
  <HeaderHR/>
  <div>
    <h1>Welcome to the viewoverallschedule</h1>
  </div>

  <div class="d-flex justify-content-between mb-3">
      <div>
        <label for="monthSelect">Month</label>
        <select id="monthSelect" class="form-select" v-model="selectedMonth">
          <option v-for="month in months" :key="month.value" :value="month.value">{{ month.name }}</option>
        </select>
      </div>
      <div>
        <label for="deptSelect">Department</label>
        <select id="deptSelect" class="form-select" v-model="selectedDept">
          <option v-for="dept in depts" :value="dept">{{ dept }}</option>
        </select>
      </div>
      <div>
        <button class="btn" @click="toggleView('list')">List View</button>
        <button class="btn btn-outline-primary" @click="toggleView('calendar')">Calendar View</button>
      </div>
    </div>
    <br><h4>WFH list</h4>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Date</th>
            <th>Timeblock</th>
            <th>Staff Name</th>
          </tr>
          <tr v-for="requests in wfh" :key="requests.request_ID">
            <td>{{corrected_date(requests.Date)}}</td>
            <td>{{requests.Timeblock}}</td>
            <td>{{requests.staff_name}}</td>
          </tr>
        </thead>
      </table>
    
      <br><h4>In office list</h4>
      <div v-for="(dictionary, date_time) in inoffice">
      <h5>{{ date_time }}</h5>
      <table class="table table-striped">

      <!-- This dictionary here represents the AM:"Array names" -->
      <tbody>
        <tr>
      <th>Timeblock</th>
      <th>Staff Name</th>
      </tr>
      <tr v-for="(names, time_block) in dictionary" :key="time_block">
        <td>{{ time_block }}</td>
        <td>
          <span v-for="(name, index) in names" :key="index">{{ name }}<span v-if="index < names.length - 1">, </span></span>
        </td>
      </tr>
    </tbody>
      </table>
      </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from 'axios';

export default {
  name: "viewoverallschedule",
  data() {
    return {
      selectedMonth: new Date().getMonth() + 1,
      selectedDept:"HR",
      viewType: "calendar",
      daysOfWeek: ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
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
      depts: [
        "CEO",
        "Sales",
        "Solutioning",
        "Engineering",
        "HR",
        "Finance",
        "Consultancy",
        "IT"
      
      ],
      wfh:{},
      allschedule: [],
      calendar_data:[{1:{"AM": 4, "PM": 3, "wholeday": 5}}],
      inoffice: {"11/04/24":{"AM":["Michael", "Charles"], "PM":["Michael"], "Whole Day":["Michael", "Charles"]}, "12/04/24":{"AM":["Michael", "Charles"], "PM":["Michael", "Charles"], "Whole Day":["Michael", "Charles"]}},
    };
  },

  computed: {
    ...mapGetters(["userRole"]), // Access the user's role from Vuex
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

      return daysArray;
    },
  },


  methods: {
    corrected_date(dateString) {
      
      return dateString.split(" 00:00:00")[0];
        // Returns something like 'Mon Oct 21 2024'
    },


    fetchwfhschedule(){
      console.log('Selected month before fetching:', this.selectedMonth)
      var params = { month: this.selectedMonth, dept: this.selectedDept }
      console.log(params)
      axios.get("http://localhost:5000/api/hr_view", { params:params, withCredentials:true})
      .then(response => {
      this.wfh= response.data
      console.log("wfh is this ",this.wfh)
    
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    })
    },



    fetchallschedule(){
      console.log('Selected month before fetching:', this.selectedMonth)
      var params = { month: this.selectedMonth, dept: this.selectedDept }
      console.log("these are the " , params)
      axios.get("http://localhost:5000/api/view_all_team_in_office_list", { params:params, withCredentials:true})
      .then(response => {
      this.inoffice = response.data
      // this.allschedule = response.data
      // console.log("this is the schedule",this.allschedule)
    })
    .catch(error => {
      console.error('Error fetching data:', error);
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
    this.fetchallschedule();
    this.fetchwfhschedule();

  },

  watch:{
    selectedDept(){
      this.fetchallschedule();
      this.fetchwfhschedule();
    },
    selectedMonth(){
      this.fetchallschedule();
      this.fetchwfhschedule();

    }
  }
};




</script>
