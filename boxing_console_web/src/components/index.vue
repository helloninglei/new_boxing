<template>
    <div class="index">
        <el-row style="height: 100%;">
            <el-col :span="4"  style="min-height: 100%; background: #1D1D27;;overflow: hidden;width:216px">
                <el-menu active-text-color="#fff" :default-active="defaultActive" router>
                    <el-menu-item index="/usermanage" :disabled="disabled">
                        <div class='menu-item-inner'>用户管理</div>
                    </el-menu-item>
                    <el-menu-item index="/boxingmanage" :disabled="disabled">
                        <div class='menu-item-inner'>拳馆管理</div>
                    </el-menu-item>
                    <el-menu-item index="/boxinglist" :disabled="disabled">
                        <div class="menu-item-inner"><div class='_hr'></div>拳馆列表</div>
                    </el-menu-item>
                    <el-menu-item index="/addBoxing" :disabled="disabled">
                        <div class="menu-item-inner"><div class='_hr'></div>添加拳馆</div>
                    </el-menu-item>
                </el-menu>
            </el-col>
            <el-col  style="height: 100%;overflow: auto;background: #fff;width:calc(100vw - 216px);float:left">
                <div class='index-top'>
                    <el-button type="danger" class='myColor_red myButton_40 btn_width_95'>退出</el-button>
                    <div class='user_name'>{{user_name}}</div>
                </div>
                <router-view></router-view>
            </el-col>
        </el-row>
    </div>
</template>

<style scoped >
    .index{height:100%;}
    ._hr{height:40px;float:left;width:20px;}
    .el-menu{background:#1d1d27;font-size: 14px;color: #FBFBFB;height:100%;margin-top:100px;}
    .el-menu .el-menu-item, .el-menu .el-submenu__title{font-size: 14px;background-color: #1D1D27;padding-left:0!important;height:40px;line-height:40px;}
    .el-menu .el-menu-item .menu-item-inner, .el-menu .el-submenu__title .menu-item-inner{color: #FBFBFB;opacity: 0.3;}
    .el-menu .el-menu-item.is-active .menu-item-inner, .el-menu .el-submenu__title.is-active .menu-item-inner,.el-menu .el-menu-item:hover .menu-item-inner, .el-menu .el-submenu__title:hover .menu-item-inner{background: #32323C;opacity: 1}
    .menu-item-inner{width:200px;margin-left:8px;padding-left:42px;box-sizing: border-box;}
    .index-top{height:88px;border-bottom:1px solid rgba(51,51,51,0.1);}
    .index-top .btn_width_95,.index-top .user_name{float:right;margin-top:31px;margin-right:68px;font-size:14px;font-family: 'PingFangSC-Light;'}
    .btn_width_95{width:95px;}
    .user_name{float:right;margin-right:14px!important;height:40px;line-height: 40px}
</style>

<script type="text/ecmascript-6">
    import axios from 'axios';
    import router from '../router';
    export default {
        data() {
            return {
                disabled: false,
                user_name:'admin'
            }
        },
        components: {

        },
        computed: {
            defaultActive: function(){
                let path = this.$route.path;
                 if (path == '/checkDetail' || path == '/roleDetail' || path == '/checkProgress/modifyPassword') {
                    return '/checkProgress'
                }
                else if (path == '/addUser' || path == '/editUser' || path == '/modifyPassword') {
                    return '/userManage'
                }
                else if (path == '/addCheckSet' || path == '/editCheckSet' || path === '/seeCheckSetDetail' || path == '/modifyPassword')  {
                    return '/checkSet'
                }
                return path;
            }
        },
        created() {
            // let userInfo = window.PYDATA.user;
            // let ifSetPassword = userInfo.has_changed_password;
            // if (!ifSetPassword) {
            //     this.disabled = true;
            // }
        },
        methods: {

        }
    }
</script>