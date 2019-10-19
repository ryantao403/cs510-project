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
        this.$store.dispatch('search', this.form.query)
      }
    }
  }
</script>