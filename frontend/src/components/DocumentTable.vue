<template>
    <div class="document-table">
        <el-table
            :data="$store.getters.filteredDocuments"
            style="width:80%"
            border
            empty-text="No data">
            <el-table-column type="index"></el-table-column>
            <el-table-column label="Title" width="180">
                <template slot-scope="scope">
                    <div><a :href="getAclLink(scope.row)" target="_blank">{{ scope.row.title }}</a></div>
                </template>
            </el-table-column>
            <el-table-column prop="abstract" label="Abstract"></el-table-column>
            <el-table-column
                fixed="right"
                label="Relevant?"
                width="150">
                <template slot-scope="scope">
                    <el-button @click="yesClicked(scope.row)" type="success" icon="el-icon-check" circle size="mini"></el-button>
                    <el-button @click="noClicked(scope.row)" type="danger" icon="el-icon-close" circle size="mini"></el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    methods: {
        getAclLink(row) {            
            if(!row || !row.path) {
                return ''
            }
            // sample: P01-1020.tei.xml, where P-01-1020 is the ACL ID
            let dot = row.path.indexOf('.')
            if(dot >= 0) {
                return "https://www.aclweb.org/anthology/" + row.path.substring(0, dot) + ".pdf"
            }
            return ""
        },
        yesClicked(row) {
            console.log('relevant' + row.title)
            this.$store.dispatch('markRelevance', {
                title: row.title,
                path: row.path,
                relevant: true
             })            
        },
        noClicked(row) {
            console.log('not relevant' + row.title)
            this.$store.dispatch('markRelevance', {
                title: row.title,
                path: row.path,
                relevant: false
            })            
        }
    }
}
</script>

<style>
.el-table {
    margin: 0 auto;
}
</style>