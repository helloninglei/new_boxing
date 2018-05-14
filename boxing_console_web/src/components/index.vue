<template>
    <div class="index">
        <el-row style="height: 100%;">
            <el-col :span="4"  style="min-height: 100%; background: #1D1D27;;overflow: hidden;width:216px">
                <el-menu active-text-color="#fff" :default-active="defaultActive" router>
                    <el-menu-item index="/usermanage" :disabled="disabled">
                        <div class='menu-item-inner' @click="changeTitle('用户管理','')">用户管理</div>
                    </el-menu-item>
                    <el-menu-item index="/boxingmanage" :disabled="disabled">
                        <div class='menu-item-inner' @click="changeTitle('拳馆管理','')">拳馆管理</div>
                    </el-menu-item>
                    <el-menu-item index="/boxinglist" :disabled="disabled">
                        <div class="menu-item-inner" @click="changeTitle('拳馆管理','拳馆列表')"><div class='_hr'></div>拳馆列表</div>
                    </el-menu-item>
                    <el-menu-item index="/addBoxing" :disabled="disabled">
                        <div class="menu-item-inner" @click="changeTitle('拳馆管理','添加拳馆')"><div class='_hr'></div>添加拳馆</div>
                    </el-menu-item>
                </el-menu>
            </el-col>
            <el-col  style="height: 100%;overflow: auto;background: #fff;width:calc(100vw - 216px);float:left">
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
    .firstTitle{float:left;font-size: 32px;color: #000000;margin:36px 0 0 30px;font-family: 'PingFangSC'}
    .firstTitle+p{float:left;font-size: 14px;color: rgba(0,0,0,0.60);margin:49px 0 0 25px;}
</style>

<script type="text/ecmascript-6">
    import axios from 'axios';
    import router from '../router';
    export default {
        data() {
            return {
                disabled : false,
                user_name: 'admin',
                title1   : '用户管理',
                title2   : '',
                isShowTitle : false,
            }
        },
        components: {

        },
        computed: {
            defaultActive: function(){
                
            }
        },
        created() {
            
        },
        methods: {
            changeTitle(title1,title2){
                this.title1 = title1
                this.title2 = title2
                this.isShowTitle = title2 ? true : false ;
            }
        }
    }
</script>