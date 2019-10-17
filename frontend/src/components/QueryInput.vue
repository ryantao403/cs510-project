<template>
    <div class="query-input">
        <el-input v-model="query" placeholder="Enter the query" size='medium'></el-input>
    </div>    
</template>

<script>
export default {
    name: 'QueryInput'
}
</script>

<style scoped>
.query-input {
    text-align: center;
    width: 20%;
}
</style>