<template>
  <div class="container">
    <h1 class="text-center mt-5">Login</h1>
    <form @submit.prevent="submitForm" class="mt-3">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input
          type="text"
          id="username"
          v-model="username"
          class="form-control"
          placeholder="Enter your username"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="form-control"
          placeholder="Enter your password"
          required
        />
        <a href="#" @click.prevent="forgotPassword">Forgot Password?</a>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script>
import Cookies from "js-cookie"; // Import js-cookie to manage cookies
import { mapActions } from "vuex";
import axios from "axios"; // Import Axios for HTTP requests
import Toastify from "toastify-js"; // Correct path for Toastify
import "toastify-js/src/toastify.css";  // Import Toastify CSS


export default {
  data() {
    return {
      username: "",
      password: "",
      error: null, // To store any error messages
    };
  },
  methods: {
    ...mapActions(["login"]),
    async submitForm() {
      try {
        // Make the login request to the Flask backend
        const response = await axios.post("https://spm-g8t7-flask.onrender.com/login", {
          username: this.username,
          password: this.password,
        });

        // Assuming the backend returns a role in the response
        // console.log(response.data);
        const fetchedRole = response.data.role;
        const name=response.data.user_name
        const supervisor=response.data.supervisor
        const dept=response.data.dept
        const email=response.data.email
        const position=response.data.position
        const userid=response.data.userid
        // console.log(response.data.userid)
        // Store the role in Vuex state
        this.login({ role: fetchedRole, username: name, userid: userid, dept: dept, email: email, supervisor: supervisor, position: position });

        // Set a cookie for the role, which expires in 7 days
        Cookies.set("userRole", fetchedRole, { expires: 7, secure: true});
        Cookies.set("username", name, { expires: 7, secure: true});
        Cookies.set("supervisor", supervisor, { expires: 7, secure: true});
        Cookies.set("dept", dept, { expires: 7, secure: true});
        Cookies.set("email", email, { expires: 7, secure: true});
        Cookies.set("position", position, { expires: 7, secure: true});
        Cookies.set("userid", userid, { expires: 7, secure: true});


        Toastify({
            text: `Login successful for ${this.username}`,
            duration: 3000,  // Toast duration in milliseconds
            close: true,     // Show close button
            gravity: "top",  // Position of toast
            position: "center", // Center horizontally
            backgroundColor: "#4caf50",  // Green for success
          }).showToast();

        this.$router.push("/homepage"); // Redirect after login
      } catch (error) {
        // this.error = error.response.data.msg || "Login failed."; // Capture error message
        // alert(this.error); // Display error message

        Toastify({
          text: `An error occurred: wrong username or password.`,
          duration: 3000,
          close: true,
          gravity: "top",
          position: "center",
          backgroundColor: "#f44336",  // Red for failure
        }).showToast();
      }
    },
    forgotPassword() {
      if (this.username) {
        alert(`Password reset link has been sent to ${this.username}`);
      } else {
        alert("Please enter your username to reset your password.");
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin-top: 50px;
}
</style>
