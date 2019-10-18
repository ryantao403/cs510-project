<template>
    <div>
        <el-table
            :data="$store.state.documents"
            empty-text="No data"
            style="width: 100%">
            <el-table-column prop="id" label="No." width="180"></el-table-column>
            <el-table-column prop="title" label="Title" width="180"></el-table-column>
            <el-table-column prop="abstract" label="Abstract"></el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    
}
</script>