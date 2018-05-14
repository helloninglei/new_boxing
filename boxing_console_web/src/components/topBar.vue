<template>
    <div class="">
        <div class='index-top'>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95'>退出</el-button>
            <div class='user_name'>{{user_name}}</div>
            <el-breadcrumb separator-class="el-icon-arrow-right">
              <el-breadcrumb-item :to="{ path: '/boxingmanage' }" ><div class="firstTitle">拳馆管理</div></el-breadcrumb-item>
              <el-breadcrumb-item><div class="titles">拳馆列表</div></el-breadcrumb-item>
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
    .titles{margin:49px 0 0 6px!important;}
</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                user_name: 'admin',
                title1   : '用户管理',
                title2   : '',
                isShowTitle : false,
                
            }
        },
        components: {
        },
        created() {
            
        },
        methods: {
            
        },
    }
</script>