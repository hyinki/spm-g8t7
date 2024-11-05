<script setup>
import HeaderStaff from '../components/HeaderStaff.vue'; // Import the Staff header component
import HeaderHR from '../components/HeaderHR.vue'; // Import the HR header component
import HeaderManager from '../components/HeaderManager.vue'; // Import the Manager header component
</script>

<template>
  <!-- Staff Section -->
  <div v-if="isStaff">
    <HeaderStaff/>
  
    <div>
    <h1 class="mb-3 mt-2 mx-5"> Welcome to the HomePage, {{username}}, {{dept}} (Staff) </h1>
    </div>

    
    <div>
      <router-link to="/viewownteamschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Own Team Schedule
        </button>
      </router-link>
    </div>
  

    <div>
      <router-link to="/viewownschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Own Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/applyforarrangement">
        <button type="button" class="btn btn-primary btn-lg m-5">
          Apply For Arrangement
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/viewarrangement">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Arrangement
        </button>
      </router-link>
    </div>

    
  </div>


  

  <!-- Manager Section -->
  <div v-if="isManager">
    <HeaderManager/>

    <div>
      <h1 class="mb-3 mt-2 mx-5">Welcome to the HomePage, {{username}} (Manager)</h1>
    </div>

    <div>
      <router-link to="/viewownteamschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Own Team Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/viewteamschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Your Managed Team's Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/arrangement">
        <button type="button" class="btn btn-primary btn-lg m-5">
          Approve/Reject Arrangement
        </button>
      </router-link>
    </div>
    <div>
      <router-link to="/viewownschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Own Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/applyforarrangement">
        <button type="button" class="btn btn-primary btn-lg m-5">
          Apply For Arrangement
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/viewarrangement">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Arrangement
        </button>
      </router-link>
    </div>
   

  </div>

  <!-- HR Section -->
  <div v-if="isHR">
    <HeaderHR/>


    <div>
      <h1 class="mb-3 mt-2 mx-5" >Welcome to the HomePage, {{ username }} ( {{dept}} )</h1>
    
    </div>

    <div>
      <div v-if="dept == 'MD' || dept == 'CEO'||dept=='Director'">
    <router-link to="/viewownteamschedule">
      <button type="button" class="btn btn-primary btn-lg m-5">
        View Own Team Schedule
      </button>
    </router-link>
  </div>

      <div>
      <router-link to="/viewoverallschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Overall Schedule
        </button>
      </router-link>
    </div>
      
      <router-link to="/viewteamschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Team Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/viewownschedule">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Own Schedule
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/applyforarrangement">
        <button type="button" class="btn btn-primary btn-lg m-5">
          Apply For Arrangement
        </button>
      </router-link>
    </div>

    <div>
      <router-link to="/viewarrangement">
        <button type="button" class="btn btn-primary btn-lg m-5">
          View Arrangement
        </button>
      </router-link>
    </div>
    
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import Cookies from "js-cookie"; // Import js-cookie to manage cookies




export default {
 
  created() {
    // Get the cookie value when the component is created
    this.userID = Cookies.get('userid') || 'Cookie not found';
  },
  computed: {
    ...mapGetters(["userRole","username","id","dept","email","supervisor"]), // Access the user's role, username from Vuex
   

    isStaff() {
    
      return this.userRole === "Staff"; // Only true if the user's role is 'Staff'
      
    },
    isManager() {
      return this.userRole === "Manager"; // Only true if the user's role is 'Manager'
    },
    isHR() {
      return this.userRole === "HR"; // Only true if the user's role is 'HR'
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 400px; /* Set maximum width for any container elements if needed */
  margin-top: 50px;  /* Add margin to top for spacing */
}
</style>
