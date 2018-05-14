<template>
    <div class='login_bg'>
        <div class="login">
            <div class='title'><b>拳民出击</b>—后台管理系统</div>
            <el-form ref="form" :model="form" label-width="173px" class='form'>
                <el-form-item label="账号">
                    <el-input v-model="form.username" class='myInput' placeholder='请输入账号'></el-input>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input v-model="form.password" class='myInput' placeholder='请输入密码'></el-input>
                </el-form-item>
                <el-form-item label="验证码">
                    <el-input v-model="form.captcha" class='myInput width-234' placeholder='请输入图形验证码'></el-input>
                    <div class='yzPicture' id='yzPicture' @click='getCaptcha'>
                        <img :src="captcha" alt="" width='100%' height='100%'>
                    </div>
                </el-form-item>
                <div class='error'><span v-if='isShowErr'>错误提示:{{errText}}</span></div>
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
    .login{height:426px;width:620px;position:absolute;top:50%;left:50%;margin-left:-310px;margin-top:-213px;background: #32323C;}
    .myInput,.myButton{width:370px!important;height:60px}
    .width-234{width:234px!important;}
    .form{margin-top:51px;}
    .yzPicture{float:right;width:122px;height:49px;background: #fff;margin-right:77px;margin-top:5px;}
    .error{padding-left:173px;height:20px;margin-top:15px;margin-bottom:20px;color:#FF635A;font-size:14px;}
</style>
<style>
    /*login里面的style*/
    body{
        /*font-family: 'PingFang SC', 'Microsoft Yahei', 'WenQuanYi Micro Hei', Arial, Verdana, sans-serif;*/
        font-family: 'PingFangSC-Light;', 'Microsoft Yahei', 'WenQuanYi Micro Hei', Arial, Verdana, sans-serif;
    }
    .el-input__inner,.el-form-item__label{
        height:60px!important;
        line-height:60px!important;
        padding-left:30px;
        font-size:20px;
        font-family: 'PingFangSC-Light', 'Microsoft Yahei', 'WenQuanYi Micro Hei', Arial, Verdana, sans-serif;

    }
    .el-form-item__label{
        /*font-family: "PingFangSC-Regular";*/
        font-size: 20px;
        color: #FFFFFF;
        letter-spacing: 0;
        text-align: right;
        font-weight:lighter;
        padding-right:26px;
    }
    .el-button{
        height:60px!important;
        border-radius: 4px;
        font-size:20px;
    }
    .el-button.myColor_red{
        background: #F95862;
    }
    .el-form-item{
        margin-bottom:15px!important;
    }
</style>
<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                disabled: false,
                form: {
                   username: '',
                   password: '',
                   captcha:''
                },
                captcha:'',
                isShowErr:false,
                errText:'',
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
                    console.log(res.data)
                    console.log($this.captcha)
                    $this.captcha=$this.config.baseUrl+res.data.url;
                },function(err){
                    console.log(err)
                })
            },
            onSubmit() {
                console.log(this.config.baseUrl)
                var reg=/^[a-zA-Z0-9]{6,16}$/
                if(!this.form.username){
                    this.errText='请输入账号'
                    this.isShowErr=true;
                    return
                }else if(!this.form.password){
                    this.errText='请输入密码'
                    this.isShowErr=true;
                    return
                }else if(!reg.test(this.form.password)){
                    this.errText='密码格式不正确'
                    this.isShowErr=true;
                    return
                }else if(!this.form.captcha){
                    this.errText='请输入图形验证码'
                    this.isShowErr=true;
                    return
                }else{
                    this.isShowErr=false;
                    console.log('submit!');
                    console.log(this.form)
                    this.$router.push({path:'/index'});
                }
                
            }
        }
    }
</script>