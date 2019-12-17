<template>
  <div class="page">
  	<h1>{{$store.state.doc.title}}</h1>
    <el-col :span="12"><div class="grid-content bg-purple-dark">{{$store.state.doc.abstract}}</div></el-col>
    <el-col :span="12">
        <div class="document-table">
            <el-table
                :data="$store.getters.recommendedDocs"
                style="width:80%"
                border
                empty-text="No Recommendation">
                <el-table-column type="index"></el-table-column>
                <el-table-column label="Title" width="200">
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
            </el-table>
        </div>
    </el-col>
    
  </div>
</template>

<script>

export default {
  name: 'Page',
  created() {
    this.fetchData()
  },
  methods: {
       fetchData(){
            let path = this.$route.params.id + ".tei.xml"
            this.$store.dispatch('getDocRecommendation', {path: path})
       },
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
    },
}


</script>
