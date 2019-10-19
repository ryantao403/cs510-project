<template>
    <div class="query-div">
      <el-input v-model="query" placeholder="Enter the query" @keyup.enter.native="search">
        <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
      </el-input>
    </div>
</template>

<script>
  export default {
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
  min-width: 500px;
  display: inline-block;
  margin-bottom: 50px;
}
</style>