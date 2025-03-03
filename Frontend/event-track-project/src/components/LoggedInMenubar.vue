<!-- src/components/LoggedInMenubar.vue -->
<template>
    <div class="menubar">
      <ul>
        <li><router-link to="/events">Events</router-link></li>
        <li><router-link to="/logout">Logout</router-link></li>
      </ul>
    </div>
  </template>

<script>
export default {
  name: 'LoggedInMenubar'
}
</script>

  <style scoped>
  .menubar {
    background-color: #333;
    padding: 10px;
  }

  .menubar ul {
    list-style-type: none;
  }

  .menubar li {
    display: inline;
    margin-right: 20px;
  }

  .menubar a {
    color: white;
    text-decoration: none;
  }
  </style>
