<template>
    <div class="query-div">
      <el-row :gutter="10">
        <el-col :span="14">
          <el-input v-model="query" placeholder="Enter the query" @keyup.enter.native="search">
          <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
        </el-input></el-col>
        <el-col :span="10"><Topics /></el-col>
      </el-row>     
    </div>
</template>

<script>
  import Topics from './Topics'
  export default {
    components : {
      Topics
    },
    data() {
      return {
        query: ''
      }
    },
    methods: {
      search() {
        this.$store.dispatch('search', this.query)
      }
    }
  }
</script>

<style>
.query-div {
  min-width: 1000px;
  display: inline-block;
  margin-bottom: 50px;
}
</style>