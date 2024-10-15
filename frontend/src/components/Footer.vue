<template>
    <footer class="footer bg-body-tertiary mt-5">
      <div class="containe mt-3">
        <p>&copy; 2024 PlanPro. All rights reserved.</p>
        
      </div>
    </footer>
  </template>
  
  <script>
  export default {
    name: "FooterComponent",
  };
  </script>
  
  <style scoped>
  .footer {
    color: black;
    padding: 20px 0;
    text-align: center;
  }
  
  .footer a {
    color: black;
    text-decoration: none;
  }
  
  .footer a:hover {
    text-decoration: underline;
  }
  
  .footer-links {
    list-style-type: none;
    padding: 0;
    margin: 10px 0 0 0;
    display: flex;
    justify-content: center;
    gap: 15px;
  }
  </style>
  