<template>
  <div class="main">

    <el-row :gutter="20">
      <el-col :span="16"><div class="grid-content bg-purple"></div></el-col>
      <el-col :span="4"></el-col>
    </el-row>
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
