<template>
    <div id="topBar" :class="disNone">
        <div class='index-top'>
            <el-button  class='myButton_40 btn_width_95 myBtnHover_red' @click='openConfirm()'>退出</el-button>
            <!-- <el-button type="danger" class='myColor_red myButton_40 btn_width_95'>退出</el-button> -->
            <div class='user_name'>{{user_name}}</div>
            <el-breadcrumb separator-class="el-icon-arrow-right">
              <el-breadcrumb-item :to="{ path: firstTitle_path }" ><div class="firstTitle">{{firstTitle_name}}</div></el-breadcrumb-item>
              <el-breadcrumb-item :to="{ path: secondTitle_path }"><div class="titles">{{secondTitle_name}}</div></el-breadcrumb-item>
              <el-breadcrumb-item :to="{ path: thirdTitle_path }" v-if="thirdTitle_name"><div class="titles">{{thirdTitle_name}}</div></el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <Confirm1 :isshow="confirmData.isshow" @confirm="close()" @cancel="cancel1()" :content="confirmData.content"></Confirm1>
    </div>
</template>

<style scoped>
    .index-top{height:88px;border-bottom:1px solid rgba(51,51,51,0.1);}
    .index-top .btn_width_95,.index-top .user_name{float:right;margin-top:31px;margin-right:68px;font-size:14px;font-family: 'PingFangSC-Light;'}
    .user_name{float:right;margin-right:14px!important;height:40px;line-height: 40px}
    .firstTitle{float:left;font-size: 32px;color: #000000;margin:36px 0 0 30px;font-family: 'PingFangSC'}
    .el-breadcrumb__separator,.titles{float:left;font-size: 14px;color: rgba(0,0,0,0.60);margin:49px 0 0 25px!important;}
    .titles{margin:49px 0 0 -3px!important;font-family: "PingFangSC"}
</style>
<style>
    #topBar .el-breadcrumb__separator.el-icon-arrow-right{margin-top:50px!important;margin-left:10px;font-size:8px;color:#333;}
    #topBar .el-breadcrumb__item:first-child .el-breadcrumb__separator.el-icon-arrow-right{margin-left:20px}
    #topBar.disNone .el-breadcrumb__separator.el-icon-arrow-right{display: none}
</style>
<script >
    import Confirm1 from "components/confirm"
    export default {
        data() {
            return {
                user_name: 'admin',
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'确认退出？'
                },
            }
        },
        components: {
            Confirm1
        },
        props: {
            firstTitle_name: {
                type: String,
                default: ''
            },
            firstTitle_path: {
                type: String,
                default: ''
            },
            secondTitle_name: {
                type: String,
                default: ''
            },
            thirdTitle_name: {
                type: String,
                default: ''
            },
            secondTitle_path: {
                type: String,
                default: ''
            },
            thirdTitle_path: {
                type: String,
                default: ''
            },
            disNone: {
                type: String,
                default: ''
            }
        },
        watch: {
        // 监测路由变化,只要变化了就调用获取路由参数方法将数据存储本组件即可
          '$route': 'getParams'
        },
        created() {
            
        },
        methods: {
            getParams(){
                this.getMsg = this.$route.params.dataobj;
            },
            openConfirm(){
                this.confirmData.isshow=true
            },
            cancel1(){
                this.confirmData.isshow=false
            },
            close(){
                let $this=this;
                this.ajax('/logout','delete',{},{}).then(function(res){
                    localStorage.token='';
                    $this.$router.push({path:'/login'});

                },function(err){
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            console.log(errors[key])
                            // return
                        } 
                    } 
                })
            }
        },
    }
</script>
