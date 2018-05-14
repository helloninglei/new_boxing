<template>
    <div id="topBar" :class="disNone">
        <div class='index-top'>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95'>退出</el-button>
            <div class='user_name'>{{user_name}}</div>
            <el-breadcrumb separator-class="el-icon-arrow-right">
              <el-breadcrumb-item :to="{ path: firstTitle_path }" ><div class="firstTitle">{{firstTitle_name}}</div></el-breadcrumb-item>
              <el-breadcrumb-item :to="{ path: secondTitle_path }"><div class="titles">{{secondTitle_name}}</div></el-breadcrumb-item>
            </el-breadcrumb>
        </div>
    </div>
</template>

<style scoped>
    .index-top{height:88px;border-bottom:1px solid rgba(51,51,51,0.1);}
    .index-top .btn_width_95,.index-top .user_name{float:right;margin-top:31px;margin-right:68px;font-size:14px;font-family: 'PingFangSC-Light;'}
    .btn_width_95{width:95px;}
    .user_name{float:right;margin-right:14px!important;height:40px;line-height: 40px}
    .firstTitle{float:left;font-size: 32px;color: #000000;margin:36px 0 0 30px;font-family: 'PingFangSC'}
    .el-breadcrumb__separator,.titles{float:left;font-size: 14px;color: rgba(0,0,0,0.60);margin:49px 0 0 25px!important;}
    .titles{margin:49px 0 0 -3px!important;font-family: "PingFangSC"}
</style>
<style>
    #topBar .el-breadcrumb__separator.el-icon-arrow-right{margin-top:50px!important;margin-left:20px;font-size:8px;}
    #topBar.disNone .el-breadcrumb__separator.el-icon-arrow-right{display: none}
</style>
<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                user_name: 'admin',
                
            }
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
            secondTitle_path: {
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
        components: {
        },
        created() {
            
        },
        methods: {
            getParams(){
                let routerParams = this.$route.params.dataobj
                this.getMsg      = routerParams
            },
        },
    }
</script>