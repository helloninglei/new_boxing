<template>
    <div class="account_handle">
        <el-dropdown trigger="click"  @command="handleCommand">
            <span class="el-dropdown-link">{{identity}}<i class="el-icon-arrow-down el-icon--right"></i></span>
            <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="modify_password" :disabled="disabled"><i class="account_handle_icon modify_icon"></i>修改密码</el-dropdown-item>
                <el-dropdown-item command="logout"><i class="account_handle_icon logout_icon"></i>退出</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">

</style>

<script type="text/ecmascript-6">
    import axios from 'axios';
    export default {
        data() {
            return {
                identity: '',
                disabled: false
            }
        },
        created() {
            // this.getData();
        },
        methods: {
            getData() {
                let userInfo = window.PYDATA.user;
                let ifSetPassword = userInfo.has_changed_password;
                if (!ifSetPassword) {
                    this.disabled = true;
                }
                axios.get(`${site}/user/${userInfo.id}`)
                    .then((res) => {
                        this.identity = res.data.identity;
                    })
            },
            handleCommand(command) {
                if (command === 'modify_password') {
                    this.$router.push({path: 'checkProgress/modifyPassword'});
                }
                else {
                    window.location = '/logout';
                }
            }
        }
    }
</script>