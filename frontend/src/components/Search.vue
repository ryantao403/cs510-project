<template>
  <div id="search">
    <Header />
    <Main />
  </div>
</template>

<script>
import Header from './Header.vue'
import Main from './Main.vue'

export default {
  name: 'Search',
  components: {
    Header,
    Main,
  }
}
</script>

<style>
#search {
  min-height: 600px;
  margin:0px;
  
}
</style>
