<template>
    <el-form :inline="true" :model="form">
        <el-form-item>
            <el-input v-model="form.query" placeholder="Enter the query"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="search">Search</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
  export default {
    data() {
      return {
        form: {
          query: ''
        }
      }
    },
    methods: {
      search() {
        //alert('Search ' + this.form.query)
        this.$store.commit('setDummyDocuments')
      }
    }
  }
</script>

<style scoped>
.query-input {
    text-align: center;
    width: 20%;
}
</style>