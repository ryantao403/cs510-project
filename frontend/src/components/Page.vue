<template>
  <div class="page">
    <el-menu
      mode="horizontal"
      background-color="#212121"
      text-color="#FF5722"
      style="border:none;">
      <el-menu-item style="font-size:20px; font-weight: bold;">ACL Paper Search Engine</el-menu-item>
    </el-menu>

    <el-page-header @back="goBack" title="Back">
    </el-page-header>
    <el-row>
        <el-col :span="18" :offset="3">
            <el-container>
                <el-header>{{$store.state.doc.title}}</el-header>
                <el-main style="color:#606266; background-color:#fff3e0;">
                    <div style="">
                        <h4 style="color:#414345;">Abstract</h4>
                        <p style="padding-left:70px; padding-right:70px;">{{$store.state.doc.abstract}}</p>
                    </div>

                    <div>
                        <i class="el-icon-download"></i>
                        <a :href="getAclLink($store.state.doc)" target="_blank"> PDF </a>
                    </div>
                </el-main>
            </el-container>
            <p/>   
            <div>
                <h5 style="padding-left:20px; margin-top:5%; margin-bottom:3%;"><i class="el-icon-cherry"></i> Related papers</h5>
                <div>
                    <el-carousel :interval="50000" type="card" height="250px">
                        <el-carousel-item v-for="item in $store.getters.recommendedDocs" :key="item.path" style="border:none;">

                            <el-card class="box-card" shadow="hover" style="background-color: #FF5722; color: #FFFFFF; border:none;" body-style="background-color: #fbe9e7; color:#757575; border:none; ">
                                <div slot="header" style="border:none;" >
                                    <span>{{item.title}}</span>
                                </div>
                                <div class="text item" style="font-size:13px;border:none;">{{ getAbstract(item) }}</div>
                                <el-button type="text" size="small" round><a :href="getDocPage(item)"> More </a></el-button>
                                
                            </el-card>
                        </el-carousel-item>
                    </el-carousel>
                </div>
            <br/>  
            <br/>  
            <br/>  
            </div> 
        </el-col>
    </el-row>
    
  </div>
</template>

<style>
    .page {
        border: none;
        border-weight: 0px;
        margin:0px;
    }

  .el-header, .el-footer {
    background-color:#E64A19;
    color: #FFFFFF;
    text-align: center;
    line-height: 60px;
    font-weight: bold;
    font-size: 20px;
  }
  

  .el-main {
    text-align: center;
    line-height: 20px;
  }

</style>

<script>
import Header from './Header.vue'

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
        goBack() {
             this.$router.push('/');
        }
    },
}


</script>
