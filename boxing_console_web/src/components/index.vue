<template>
    <div class="index">
        <el-row style="height: 100%;">
            <el-col :span="4"  style="height: 100%; background: #1D1D27;;overflow: hidden;width:216px;overflow: auto">
                <el-menu active-text-color="#fff" :default-active="defaultActive" router>
                    <el-menu-item index="/usermanage" :disabled="disabled">
                        <div class='menu-item-inner' >用户管理</div>
                    </el-menu-item>
                    <el-submenu index='1'>
                        <template slot="title"><div class='mySubMenu'>财务管理</div></template>
                        <el-menu-item index="/paymentlist" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>用户支付流水</div>
                        </el-menu-item>
                        <el-menu-item index="/precentlist" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>用户提现记录</div>
                        </el-menu-item>
                    </el-submenu>
                    <!-- <el-menu-item index="/boxBean" :disabled="disabled">
                        <div class='menu-item-inner'>公司拳豆记录</div>
                    </el-menu-item> -->
                    <el-menu-item index="/accound_record" :disabled="disabled">
                        <div class='menu-item-inner'>公司账户金额记录</div>
                    </el-menu-item>
                    <el-menu-item index="/hotvideo" :disabled="disabled">
                        <div class='menu-item-inner'>视频管理</div>
                    </el-menu-item>
                    <el-menu-item index="/album" :disabled="disabled">
                        <div class='menu-item-inner'>相册管理</div>
                    </el-menu-item>
                    <el-submenu index='2'>
                        <template slot="title" ><div class='mySubMenu'>约单管理</div></template>
                        <el-menu-item index="/classmanage" :disabled="disabled">
                            <div class='menu-item-inner'><div class='_hr'></div>课程管理</div>
                        </el-menu-item>
                        <el-menu-item index="/ordermanage" :disabled="disabled">
                            <div class='menu-item-inner'><div class='_hr'></div>订单管理</div>
                        </el-menu-item>
                        <el-menu-item index="/settlemanage" :disabled="disabled">
                            <div class='menu-item-inner'><div class='_hr'></div>结算管理</div>
                        </el-menu-item>
                    </el-submenu>
                    <el-menu-item index="/boxerindentify" :disabled="disabled">
                        <div class='menu-item-inner'>拳手认证审核管理</div>
                    </el-menu-item>
                    <el-menu-item index="/bannermanage" :disabled="disabled">
                        <div class='menu-item-inner'>Banner管理</div>
                    </el-menu-item>
                    <el-menu-item index="/boxinglist" :disabled="disabled">
                        <div class='menu-item-inner'>拳馆管理</div>
                    </el-menu-item>
                    <el-submenu index='4'>
                        <template slot="title" ><div class='mySubMenu'>赛事管理</div></template>
                        <el-menu-item index="/infoList" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>资讯</div>
                        </el-menu-item>
                        <el-menu-item index="/boxerlist" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>参赛选手管理</div>
                        </el-menu-item>
                        <el-menu-item index="/metchlist" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>赛程管理</div>
                        </el-menu-item>
                        <!-- <el-menu-item index="/" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>添加报名</div>
                        </el-menu-item> -->
                        <!-- <el-menu-item index="/" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>查看报名</div>
                        </el-menu-item> -->
                    </el-submenu>
                    <el-submenu index='5'>
                        <template slot="title" ><div class='mySubMenu'>动态管理</div></template>
                        <el-menu-item index="/dynamic" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>动态列表</div>
                        </el-menu-item>
                    </el-submenu>
                    <el-submenu index='6'>
                        <template slot="title" ><div class='mySubMenu'>反馈建议</div></template>
                        <el-menu-item index="/feedback" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>反馈建议</div>
                        </el-menu-item>
                        <el-menu-item index="/report" :disabled="disabled">
                            <div class="menu-item-inner" ><div class='_hr'></div>举报处理</div>
                        </el-menu-item>
                    </el-submenu>
                    <el-menu-item index="/admin" :disabled="disabled">
                        <div class='menu-item-inner'>管理员</div>
                    </el-menu-item>
                    <el-menu-item index="/sensitiveword" :disabled="disabled">
                        <div class='menu-item-inner'>拳城BB敏感词</div>
                    </el-menu-item>
                    <el-menu-item index="/versionlist" :disabled="disabled">
                        <div class='menu-item-inner'>版本管理</div>
                    </el-menu-item>
                    <!-- <el-menu-item index="/useDialog" :disabled="disabled">
                        <div class='menu-item-inner'>弹框管理</div>
                    </el-menu-item> -->
                </el-menu>
            </el-col>
            <el-col  style="height: 100%;overflow: auto;background: #fff;width:calc(100vw - 225px);float:left">
                <router-view></router-view>
            </el-col>
        </el-row>
    </div>
</template>

<style scoped >
    /*左侧边栏的样式*/
    .index{height:100%;}
    ._hr{height:40px;float:left;width:20px;}
    .el-menu{background:#1d1d27;font-size: 14px;color: #FBFBFB;height:100%;margin-top:100px;}
    .el-menu .el-menu-item, .el-menu .el-submenu .el-submenu__title{font-size: 14px;background-color: #1D1D27;padding-left:0!important;height:40px;line-height:40px;}
    .el-menu .el-menu-item .menu-item-inner, .el-menu .el-submenu__title .menu-item-inner{color: #FBFBFB;opacity: 0.3;}
    .el-menu .el-menu-item.is-active .menu-item-inner, .el-menu .el-submenu__title.is-active .menu-item-inner,.el-menu .el-menu-item:hover .menu-item-inner, .el-menu .el-submenu__title:hover .menu-item-inner{background: #32323C;opacity: 1}
    .index .menu-item-inner{width:200px;margin-left:8px;padding-left:42px;box-sizing: border-box;}
    
</style>
<style>
    /*.index .el-submenu .el-submenu__title:focus{}*/
    .index .el-submenu  .el-submenu__title{
        padding-left: 12px!important;
        height: 40px;
        line-height: 40px;
        width: 200px;
        margin-left: 8px;}
    .index .el-submenu  .el-submenu__title:hover {background: #32323C!important;opacity: 1;}
    .index .el-submenu .el-submenu__title .mySubMenu{opacity: 1;padding-left:30px;}
</style>
<script type="text/ecmascript-6">
    import TopBar from 'components/topBar';
    import router from '../router';
    export default {
        data() {
            return {
                disabled : false,
                user_name: 'admin',
                title1   : '用户管理',
                title2   : '',
                isShowTitle : false,
                isShowTop   : true
            }
        },
        components: {
            TopBar,
            router
        },
        computed: {
            defaultActive: function(){
                //监听路由变化
                let path = this.$route.path;
                 if (path == '/index' || path == '/userdetail' || path == '/walletlist') {
                    return '/usermanage'
                }
                return path;
                
            }
        },
        created() {
            
        },
        methods: {
        }
    }
</script>