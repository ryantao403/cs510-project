<template>
  <div class="page">
    <el-col :span="18" :offset="3">
        <el-container>
            <el-header>{{$store.state.doc.title}}</el-header>
            <el-main>
                <div>
                    <h3>Abstract</h3>
                    <p>{{$store.state.doc.abstract}}</p>
                </div>

                <div>
                    <i class="el-icon-download"></i>
                    <a :href="getAclLink($store.state.doc)" target="_blank"> PDF </a>
                </div>
            </el-main>
            
            <el-container style="">
                <div><h3>Recommendations</h3></div>
                <div>
                    <el-carousel :interval="50000" type="card" height="250px">
                        <el-carousel-item v-for="item in $store.getters.recommendedDocs" :key="item.path">
                            <el-card class="box-card" shadow="hover" style="background-color: #409EFF; color: #F2F6FC">
                                <div slot="header" >
                                    <span>{{item.title}}</span>
                                </div>
                                <div class="text item">{{ getAbstract(item) }}</div>
                                <el-button type="text" size="small" round><a :href="getDocPage(item)"> More </a></el-button>
                                <div></div>
                                
                            </el-card>
                        </el-carousel-item>
                    </el-carousel>
                </div>
            </el-container>
        </el-container>        
    </el-col>
    
  </div>
</template>

<style>
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
    font-weight: bold;
  }
  

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 20px;
  }

</style>

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
            if (abstract.length > 150){
                abstract = abstract.substring(0, 150) + "..."
            }
            return abstract
        },
        getDocPage(row){
            let link = "/doc/";
            let dot = row.path.indexOf('.')
            if(dot >= 0) {
                link = link + row.path.substring(0, dot)
            }
            return link
        },
    },
}


</script>
