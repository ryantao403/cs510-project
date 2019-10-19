<template>
  <div class="main">
    <QueryInput />
    <DocumentTable />
  </div>
</template>

<script>
import QueryInput from './QueryInput.vue'
import DocumentTable from './DocumentTable'

export default {
  name: 'Main',
  components: {
    QueryInput,
    DocumentTable
  },
}
</script>
