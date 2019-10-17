<template>
  <div class="main">
    <QueryInput />
    <DocumentTable />
  </div>
</template>

<script>
import QueryInput from './QueryInput.vue'
import DocumentTable from './DocumentTable.vue'
export default {
  name: 'Main',
  components: {
    QueryInput, 
    DocumentTable
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
