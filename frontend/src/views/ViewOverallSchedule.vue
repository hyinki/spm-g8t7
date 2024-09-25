<template>
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
            <a class="nav-link active" aria-current="page" href="/homepage"
              >Home</a
            >
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/viewoverallschedule"
              >View Overall Schedule</a
            >
          </li>

          <li class="nav-item">
            <a class="nav-link" href="/viewteamschedule">View Team Schedule</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div>
    <h1>Welcome to the viewoverallschedule</h1>
  </div>
</template>

<script>
export default {
  name: "viewoverallschedule",
};
</script>
