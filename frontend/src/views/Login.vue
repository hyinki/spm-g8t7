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

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    ...mapActions(["login"]),
    submitForm() {
      // Simulate a role fetched from the backend after login
      const fetchedRole = "HR"; // This would come from your backend API in a real scenario

      // Store the role in Vuex state
      this.login({ role: fetchedRole });

      // Set a cookie for the role, which expires in 7 days
      Cookies.set("userRole", fetchedRole, { expires: 7 });

      alert(`Login successful for ${this.username}`);
      this.$router.push("/homepage"); // Redirect after login
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
