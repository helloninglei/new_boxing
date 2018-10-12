<template>
    <div class='login_bg'>
        <div class="login">
            <div class='title'><b>拳城出击</b>—后台管理系统</div>
            <el-form ref="form" :model="form" label-width="173px" class='form' id='login'>
                <el-form-item label="账号">
                    <el-input v-model="form.username" class='myInput' placeholder='请输入账号' :maxlength="11"></el-input>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input v-model="form.password" type="password" class='myInput' placeholder='请输入密码'></el-input>
                </el-form-item>
                <el-form-item label="验证码">
                    <el-input v-model="form.captcha.captcha_code" class='myInput width-234' placeholder='请输入图形验证码'></el-input>
                    <div class='yzPicture' id='yzPicture' @click='getCaptcha'>
                        <img :src="captcha" alt="" width='100%' height='100%'>
                    </div>
                </el-form-item>
                <el-form-item>
                    <el-checkbox label="记住密码" name="isremember" v-model="isremember"></el-checkbox>
                </el-form-item>
                <div class='error' v-if='isShowErr'><span >{{errText}}</span></div>
                
                </el-form-item>
                <el-form-item label="">
                    <el-button type="danger" class='myColor_red myButton' @click="onSubmit">立即登录</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<style scoped>
    /*login里面的样式*/
    .title{position:absolute;top:-62px;font-size: 40px;color: #FFFFFF;letter-spacing: -0.29px;}
    .title b{font-family: 'pngFang SC'}
    .login_bg{background: #1D1D27;box-shadow: inset 0 1px 3px 0 rgba(0,0,0,0.50);height:100%;width:100%}
    .login{height:476px;width:620px;position:absolute;top:50%;left:50%;margin-left:-310px;margin-top:-213px;background: #32323C;}
    .myInput,.myButton{width:370px!important;height:60px}
    .width-234{width:234px!important;}
    .form{margin-top:51px;}
    .yzPicture{float:right;width:122px;height:49px;background: #fff;margin-right:77px;margin-top:5px;}
    .error{padding-left:173px;height:20px;margin-top:15px;margin-bottom:20px;color:#FF635A;font-size:14px;}
    .login_bg .el-checkbox{margin-left:0;}
</style>
<style>
    /*login里面的style*/
    body{
        /*font-family: 'PingFang SC', 'Microsoft Yahei', 'WenQuanYi Micro Hei', Arial, Verdana, sans-serif;*/
        font-family: 'PingFangSC-Light', 'Microsoft Yahei', 'WenQuanYi Micro Hei', Arial, Verdana, sans-serif;
    }
    .login_bg .el-input__inner,.el-form-item__label{
        height:60px!important;
        line-height:60px!important;
        padding-left:30px;
        font-size:20px!important;
        font-family: 'PingFangSC-Light', 'Microsoft Yahei', 'WenQuanYi Micro Hei', Arial, Verdana, sans-serif;

    }
    .login_bg .el-form-item__label{
        /*font-family: "PingFangSC-Regular";*/
        font-size: 20px;
        color: #FFFFFF;
        letter-spacing: 0;
        text-align: right;
        font-weight:lighter;
        padding-right:26px;
    }
    .login_bg .el-button{
        height:60px!important;
        border-radius: 4px;
        font-size:20px;
    }
    .login_bg .el-button.myColor_red{
        background: #F95862;
    }
    .login_bg .el-form-item{
        margin-bottom:15px!important;
    }
</style>
<script>
    export default {
        data() {
            return {
                disabled: false,
                form: {
                    username: '',
                    password: '',
                    captcha:{
                        captcha_hash: "",
                        captcha_code: ''
                    },
                },
                captcha:'',
                isShowErr:false,
                errText:'',
                isremember:false,
            }
        },
        components: {

        },
        computed: {
            defaultActive: function() {
                let path = this.$route.path;
                if (path == '' || path == '/login') {
                    return '/login'
                }
                return path;
            }
        },
        created() {
            this.getCaptcha();
        },
        methods: {
            getCaptcha() {
                let $this=this;
                this.ajax('/captcha-image').then(function(res){
                    $this.captcha         =$this.config.baseUrl+res.data.url;
                    $this.form.captcha.captcha_hash=res.data.captcha_hash;
                },function(err){
                    console.log(err)
                })
            },
            onSubmit() {
                var reg=/^[a-zA-Z0-9]{6,16}$/
                if(!this.form.username){
                    this.errText='请输入账号'
                    this.isShowErr=true;
                    this.getCaptcha();
                    return
                }else if(!this.form.password){
                    this.errText='请输入密码'
                    this.isShowErr=true;
                    this.getCaptcha();
                    return
                }else if(!reg.test(this.form.password)){
                    this.errText='密码格式不正确'
                    this.isShowErr=true;
                    this.getCaptcha();
                    return
                }else if(!this.form.captcha.captcha_code){
                    this.errText='请输入图形验证码'
                    this.isShowErr=true;
                    this.getCaptcha();
                    return
                }else{
                    this.isShowErr=false;
                    let $this=this;
                    this.ajax('/login','post',this.form).then(function(res){
                        if(res&&res.data){
                            localStorage.token=res.data.token;
                            $this.$router.push({path:'/index'});
                        }

                    },function(err){
                        let errors=err.response.data
                        for(var key in errors){
                            $this.errText=errors[key][0]
                            $this.isShowErr=true;
                            $this.getCaptcha();
                            return
                        }
                    })
                }
                
            }
        }
    }
</script>