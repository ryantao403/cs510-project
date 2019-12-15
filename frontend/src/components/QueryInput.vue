<template>
    <div class="query-div">
      <el-row :gutter="20">
        <el-col :span="15">
          <el-autocomplete class="inline-input" v-model="query" placeholder="Enter the query" @keyup.enter.native="search" :fetch-suggestions="suggests" :trigger-on-focus="false" @select="change">
          <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
        </el-autocomplete></el-col>
        <el-col :span="9"><Topics /></el-col>
      </el-row>     
    </div>
</template>

<script>
  import Topics from './Topics'
  import $ from 'jquery'
  export default {
    components : {
      Topics
    },
    data() {
      return {
	  query: '',
	  timeout: null
      }
    },
    methods: {
    	search() {
	    this.$store.dispatch('search', this.query)
	},

	suggests(query, cb) {
	    this.$store.dispatch('getSuggests', {
		query: query,
		callback: cb,
	    })
	},

	change(item) {
	    console.log(item)
	    this.$store.dispatch('search', item.value)
	},

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
