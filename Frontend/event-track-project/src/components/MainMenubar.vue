<!-- src/components/Menubar.vue -->
<template>
    <div class="menubar">
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/login">Login</router-link></li>
      </ul>
    </div>
  </template>

<script>
export default {
  name: 'MainMenubar'
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
