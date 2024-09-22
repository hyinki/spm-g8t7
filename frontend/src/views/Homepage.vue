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
            <a class="nav-link active" aria-current="page" href="/homepage">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/viewteamschedule">Team Schedule</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">placeholder2</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div>
    <h1>Welcome to the HomePage</h1>
  </div>

  <div>
    <router-link to="/viewteamschedule">
  <button type="button" class="btn btn-primary btn-lg m-5">
    View Team Schedule
  </button>
</router-link>
  </div>
  <div>
    <button type="button" class="btn btn-primary btn-lg m-5">
      View Own Schedule
    </button>
  </div>
  <div>
    <button type="button" class="btn btn-primary btn-lg m-5">
      Apply for arangement
    </button>
  </div>

</template>

<script>
export default {
  name: "Homepage",
};
</script>
