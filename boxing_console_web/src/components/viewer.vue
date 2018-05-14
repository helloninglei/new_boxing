<template>
    <div class="fillcontain">
        <DropDown></DropDown>
        <el-row style="height: 100%;">
            <el-col :span="4"  style="min-height: 100%; background-color: #333;overflow: hidden">
                <el-menu active-text-color="#fff" :default-active="defaultActive" router>
                    <el-menu-item index="/viewer" :disabled="disabled">考核进度管理</el-menu-item>
                    <el-menu-item index="/checkRecordView" :disabled="disabled">考核记录</el-menu-item>
                    <el-menu-item index="/checkTaskView" :disabled="disabled">考核任务</el-menu-item>
                </el-menu>
            </el-col>
            <el-col :span="20" style="height: 100%;overflow: auto;">
                <router-view></router-view>
            </el-col>
        </el-row>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">

</style>

<script type="text/ecmascript-6">
    import axios from 'axios';
    import router from '../router';
    import DropDown from 'components/dropDown';
    export default {
        data() {
            return {
                disabled: false
            }
        },
        components: {
            DropDown
        },
        computed: {
            defaultActive: function(){
                let path = this.$route.path;
                if (path === '/checkDetailView' || path === '/viewer/modifyPassword' || path === '/roleDetailView') {
                    return '/viewer';
                }
                else if (path === '/checkRecordDetailView') {
                    return '/checkRecordView';
                }
                else if (path === '/checkDetailTaskView' || path === '/checkHandleTaskView') {
                    return '/checkTaskView';
                }
                return path;
            }
        },
        created() {
            let userInfo = window.PYDATA.user;
            let ifSetPassword = userInfo.has_changed_password;
            if (!ifSetPassword) {
                this.disabled = true;
            }
        },
        methods: {

        }
    }
</script>