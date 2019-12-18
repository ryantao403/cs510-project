<template>
  <div id="app">
    <router-view :key="$route.path"/>
  </div>
</template>

<script>

export default {
  name: 'app',
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fff;
  margin: 0px;
  border: none;
  padding: 0;
  background-color: #26262A;
  
}

* {
  margin: 0;
}
</style>
