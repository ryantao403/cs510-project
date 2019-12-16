<template>
    <div class="document-table">
        <el-table
            :data="tableData"
            style="width:80%"
            border
            empty-text="No data">
            <el-table-column type="index"></el-table-column>
            <el-table-column label="Title" width="300">
                <template slot-scope="scope">
                    <div><a :href="getAclLink(scope.row)" target="_blank">{{ scope.row.title }}</a></div>
                </template>
            </el-table-column>
            <el-table-column prop="abstract" label="Abstract">
                <template slot-scope="scope">
                    <div>{{ getAbstract(scope.row) }}</div>
                    <div><a :href="getDocPage(scope.row)"> More </a></div>
                </template>
            </el-table-column>
            <el-table-column prop="area" label="Area" width="200">
                <template slot-scope="scope">
                    <el-tag v-if="scope.row.area">{{scope.row.area}}</el-tag>
                    <div v-else></div>
                </template>
            </el-table-column>
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
        <el-pagination
            @current-change="handleCurrentChange"
            background
            layout="->, prev, pager, next"
            :total="totalPage">
        </el-pagination>
    </div>
</template>

<script>
export default {
    data() {
        return {
          tableData: this.$store.getters.filteredDocuments,
          pageNum: 1,
          totalPage: Math.ceil(this.$store.getters.filteredDocuments.length/10) * 10
        };
    },
    /*computed: {  

        displayData() {
            console.log(this.pageNum, this.totalPage)
            console.log(this.tableData.length, this.tableData)
            if (!this.tableData || this.tableData.length === 0) return [];

            return this.tableData.slice((this.pageNum-1)*10, this.pageNum*10)

          },

    },*/
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
        getAbstract(row) {
            let abstract = row.abstract;
            if (abstract.length > 200){
                abstract = abstract.substring(0, 200) + "..."
            }
            return abstract
        },
        getDocPage(row){
            let link = "doc/";
            let dot = row.path.indexOf('.')
            if(dot >= 0) {
                link = link + row.path.substring(0, dot)
            }
            return link
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
            // Remove irrelevant items from store
            var index = this.$store.state.documents.map(e => e.title).indexOf(row.title)
            this.$delete(this.$store.state.documents,index)
            this.$store.dispatch('markRelevance', {
                title: row.title,
                path: row.path,
                relevant: false
            })            
        },

        handleCurrentChange(val) {
            console.log(`current page: ${val}`);
            this.pageNum=val;
        }
    }
}
</script>

<style>
.el-table {
    margin: 0 auto;
}
</style>