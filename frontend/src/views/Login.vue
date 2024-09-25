<template>
  <div class="container">
    <h1 class="text-center mt-5">Login</h1>
    <form @submit.prevent="submitForm" class="mt-3">
      <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input
          type="text"
          id="name"
          v-model="name"
          class="form-control"
          placeholder="Enter your name"
          required
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          class="form-control"
          placeholder="Enter your email"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      name: "",
      email: ""
    };
  },
  methods: {
    submitForm() {
      // Simple form submission logic (you can add your own)
      console.log("Name:", this.name);
      console.log("Email:", this.email);
      alert(`Login successful for ${this.name}`);
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin-top: 50px;
}
</style>
