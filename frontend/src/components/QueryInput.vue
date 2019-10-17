<template>
    <div class="query-input">
        <el-input v-model="query" placeholder="Enter the query" size='medium'></el-input>
        <el-button type="primary" @click="search">Search</el-button>
    </div>    
</template>

<script>
export default {
    name: 'QueryInput',
    data() {
        return {
            query: ''
        }        
    },
    methods: {
        search() {
            alert(this.query)
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