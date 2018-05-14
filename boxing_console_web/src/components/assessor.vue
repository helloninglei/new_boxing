<template>
    <div class="fillcontain">
        <DropDown></DropDown>
        <el-row style="height: 100%;">
            <el-col :span="4"  style="min-height: 100%; background-color: #333;overflow: hidden">
                <el-menu active-text-color="#fff" :default-active="defaultActive" router>
                    <el-menu-item index="/checkTask" :disabled="disabled">考核任务</el-menu-item>
                    <el-menu-item index="/checkRecord" :disabled="disabled">考核记录</el-menu-item>
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
            defaultActive: function() {
                let path = this.$route.path;
                if (path == '/checkRecordDetail' || path == '/checkRecord/modifyPassword') {
                    return '/checkRecord'
                }
                else if (path == '/checkDetailTask' || path === '/checkHandleTask') {
                    return '/checkTask'
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
            handleCommand(command) {
                if (command === 'modify_password') {
                    alert(1)
                }
                else {
                    alert(2)
                }
            }
        }
    }
</script>