<template>
    <div class="fillcontain">
        <div class="account_handle">
            <el-dropdown trigger="click"  @command="handleCommand">
                  <span class="el-dropdown-link">
                    1234455666<i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item command="modify_password"><i class="account_handle_icon modify_icon"></i>修改密码</el-dropdown-item>
                    <el-dropdown-item command="logout"><i class="account_handle_icon logout_icon"></i>退出</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>

        <el-row style="height: 100%;">
            <el-col :span="4"  style="min-height: 100%; background-color: #333;overflow: hidden">
                <el-menu active-text-color="#fff" default-active="checkRecord" router>
                    <el-menu-item index="checkRecord">考核记录</el-menu-item>
                </el-menu>
            </el-col>
            <el-col :span="20" style="height: 100%;overflow: auto;">
                <keep-alive>
                    <router-view></router-view>
                </keep-alive>
            </el-col>
        </el-row>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">

</style>

<script type="text/ecmascript-6">
    import axios from 'axios';
    export default {
        data() {
            return {

            }
        },
        computed: {
            defaultActive: function(){
                return this.$route.path.replace('/', '');
            }
        },
        created() {
//            axios.post(`${site}/a`).then((res) => {
//
//            })
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