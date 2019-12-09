<template>
  <div class="main">
    <QueryInput />
    <DocumentTable />
  </div>
</template>

<script>
import QueryInput from './QueryInput.vue'
import DocumentTable from './DocumentTable'
import Topics from './Topics'

export default {
  name: 'Main',
  components: {
    QueryInput,
    DocumentTable,
    Topics
  },
}
</script>
