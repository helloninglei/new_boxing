<template>
    <div id="boxer_detail">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/infolist" secondTitle_path="/boxerlist" secondTitle_name="参赛选手管理" :thirdTitle_name="content_title"></TopBar>
        <div class="container">
            <el-row> 
                <el-col :span="12" style='min-width:800px'>
                    <el-form :model="form" label-width="82px" :rules="rules" ref="ruleForm">
                        <p class='content_title'>{{content_title}}</p>
                        <p class='title' style='padding-left:15px'>拳手信息</p>
                        <el-row>
                            <el-col :span="11">
                                <el-form-item label="拳手姓名" prop="name">
                                    <el-input v-model="form.name" placeholder="请输入姓名" :maxlength="6"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="11" :offset="2">
                                <el-form-item label="拳手手机号" prop="mobile">
                                    <el-input v-model="form.mobile"  placeholder="请输入手机号" :maxlength="11" :disabled='form.id?true:false'></el-input>
                                    <div class="el-form-item__error" v-if="phoneError">
                                        {{phone_error_con}}
                                    </div>
                                </el-form-item>
                            </el-col>
                        </el-row>  
                        
                        <el-form-item label="拳手头像" prop="avatar">
                            <el-input v-model="form.avatar" type='hidden'></el-input>
                            <Cropper @getUrl='getUrl' :url_f='url_f' :changeUrl='changeUrl' :imgId='imgId' :width='100' :height='100'></Cropper>

                            <div class='show' @click="addImg('inputId2','img2')" style='width:100px;height:100px;border:1px solid #ccc;margin-top:-40px;cursor: pointer'>  
                               <img :src="form.avatar" alt="" width='100%' id='img2' v-if='form.avatar'> 
                               <div class='imgModel'>{{form.avatar?'更换头像':'添加头像'}}</div>
                               <div style='display:none'>  
                                   <input type="file" id="inputId2"  accept="image" @change="change">  
                                   <label for="inputId2"></label>  
                                </div> 
                            </div>
                            <div class="el-form-item__error" v-if="showError">
                                请上传拳手头像
                            </div>
                        </el-form-item>
                        <p class='title'>能力雷达图 <el-button type="danger" class='myColor_red margin_rt25 border_raduis_100' style='width:60px;height:30px;line-height:30px;padding:0;margin-left:8px' @click="prevImg('ruleForm')">预览</el-button></p>
                        <el-row>
                            <el-col :span="11">
                                <el-form-item label="耐力" prop="stamina">
                                    <el-input v-model="form.stamina" placeholder="请输入" type='number' :min="0" :max="101"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="11" :offset="2">
                                <el-form-item label="技术" prop="skill">
                                    <el-input v-model="form.skill"  placeholder="请输入" type='number' :min="0" :max="101"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>  
                        <el-row>
                            <el-col :span="11">
                                <el-form-item label="进攻" prop="attack">
                                    <el-input v-model="form.attack" placeholder="请输入" type='number' :min="0" :max="101"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="11" :offset="2">
                                <el-form-item label="防守" prop="defence">
                                    <el-input v-model="form.defence"  placeholder="请输入" type='number' :min="0" :max="101"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>  
                        <el-row>
                            <el-col :span="11">
                                <el-form-item label="力量" prop="strength">
                                    <el-input v-model="form.strength" placeholder="请输入" type='number' :min="0" :max="101"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="11" :offset="2">
                                <el-form-item label="意志力" prop="willpower">
                                    <el-input v-model="form.willpower"   placeholder="请输入" type='number' :min="0" :max="101"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>  
                        <div style='text-align: left;margin-left:40px'>
                            <el-button class="myButton_40 myBtnHover_red" @click="cancelEv('ruleForm')" style='width:100px'>取消</el-button>
                            <el-button type="danger" class=' myColor_red' @click="submitForm('ruleForm')" style='width:100px'>确定</el-button>
                        </div>
                    </el-form>
                </el-col>
            </el-row>
        </div>
        <el-dialog  :visible.sync="prevVisible">
            <div class="dialog_title">{{content_title}}</div>
            <div class='dialog_content'>
                <img :src="src" alt="" width="300">
            </div>
            <div slot="footer" class="dialog-footer" style='text-align:center'>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 border_raduis_100' @click="prevVisible = false">关闭</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<style lang="stylus" scoped>
    .el-icon-circle-close {
        position absolute
        right  0
        top 0
        font-size 20px
    }
    #boxer_detail {
        .margin_top25{
            margin:0;
            margin-top:25px;
        }
        .content{
            height:calc(100% - 80px);
            overflow-y: auto;
            margin-bottom:10px;
            margin-top:10px;
        }
        .dialog_title,.content_title{
            font-family: PingFangSC-Regular;
            font-size: 16px;
            color: #000000;
        }
        .content_title{
            margin:30px 0 27px;
        }
        .dialog_title{text-align:center}
        .dialog_content img{margin:25px 30px;}
        .title{
            font-family: PingFangSC-Regular;
            font-size: 14px;
            color: #000000;
            margin-bottom:22px;
        }
        .imgModel{
            position:absolute;
            width:80px;
            height:30px;
            line-height:30px;
            background:rgba(0,0,0,0.5);
            left:10px;
            bottom:10px;
            text-align:center;
            color:#fff;
        } 
    }
    
</style>
<style lang="stylus">
    #boxer_detail .el-checkbox__label,#boxer_detail .el-radio__label,#boxer_detail .el-form-item__label{
        font-family: PingFangSC-Regular;
        font-size: 14px!important;
        color: #606266;
    }
    #boxer_detail{
        .show{
            width: 100px;  
            height: 100px;  
            overflow: hidden;  
            position: relative;  
            float:left;
            z-index:20;
            // background:url('./img/person_img.png') no-repeat center center;
        }
        .el-form-item{
            margin-bottom:30px
        }
        .el-dialog{
            width:400px!important;
            height:473px!important;
        }
        .el-dialog__header{padding:0}
        .el-dialog__body{padding-top:25px;padding-bottom:0}
        .el-dialog__footer{padding-top:0}
    }
</style>
<script>
    import TopBar   from 'components/topBar';
    import config   from 'common/my_config'
    import Cropper from 'components/cropper';
    export default {
        data() {
            return {
                id: '',
                src:'',
                isShowTop: true,
                inputId:'',
                url_f:'',
                changeUrl:false,
                imgId :'',
                showError: false,
                phoneError:false,
                prevVisible:false,//是否显示预览
                content_title:'添加参赛拳手',
                phone_error_con:'',//拳手手机号错误信息
                isValidate:false,//是否验证姓名等字段
                form: {
                    "stamina": '',
                    "skill": '',
                    "attack": '',
                    "defence": '',
                    "strength": '',
                    "willpower": '',
                    "name": "",
                    "mobile": "",
                    "avatar": ""
                },
                rules: {
                    
                    skill: [
                        { validator: (rule, value, callback) => {
                            if (value==='') {
                                callback(new Error('请输入技术值'));
                            }else if(!/^[0-9]*$/.test(value)||value>100||value==0){
                                callback(new Error('请输入1-100的整数'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur',}
                    ],
                    stamina: [
                        { validator: (rule, value, callback) => {
                           if (value==='') {
                                callback(new Error('请输入耐力值'));
                            }else if(!/^[0-9]*$/.test(value)||value>100||value==0){
                                callback(new Error('请输入1-100的整数'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur',}
                    ],
                    attack: [
                        { validator: (rule, value, callback) => {
                            if (value==='') {
                                callback(new Error('请输入攻击值'));
                            }else if(!/^[0-9]*$/.test(value)||value>100||value==0){
                                callback(new Error('请输入1-100的整数'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur',}
                    ],
                    willpower: [
                        { validator: (rule, value, callback) => {
                            if (value==='') {
                                callback(new Error('请输入意志力值'));
                            }else if(!/^[0-9]*$/.test(value)||value>100||value==0){
                                callback(new Error('请输入1-100的整数'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur',}
                    ],
                    strength: [
                        { validator: (rule, value, callback) => {
                            if (value==='') {
                                callback(new Error('请输入力量值'));
                            }else if(!/^[0-9]*$/.test(value)||value>100||value==0){
                                callback(new Error('请输入1-100的整数'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur',}
                    ],
                    defence: [
                        { validator: (rule, value, callback) => {
                            if (value==='') {
                                callback(new Error('请输入防守值'));
                            }else if(!/^[0-9]*$/.test(value)||value>100||value==0){
                                callback(new Error('请输入1-100的整数'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur',}
                    ],
                },
            }
        },

        components: {
            TopBar,
            Cropper
        },

        created() {
            this.query = this.$route.query;
            if(this.query.id){
                //编辑
                this.getData(this.query.id)
                this.content_title = '编辑参赛拳手'
            }else{
                
            }
        },

        computed: {
           
        },

        watch:{
           'form.mobile':function(newValue){
            
                if(!this.form.id&&newValue&&newValue.length==11){
                    if(this.phoneReg.test(newValue)){
                        this.phoneError = false
                        this.ajax('/check_player_mobile?mobile='+newValue).then((res)=>{
                            if(res&&res.data){
                                if(!res.data.is_user){
                                    this.phone_error_con='该拳手不存在'
                                    this.phoneError = true
                                    return;
                                }
                                if(res.data.is_player){
                                    this.phone_error_con='该拳手已存在'
                                    this.phoneError = true
                                    return;
                                }
                                this.form.avatar = res.data.avatar?res.data.avatar:this.form.avatar;


                            }
                        },function(err){
                            console.log(err.response.status)
                            if(err&&err.response){
                                let errors=err.response.data
                                for(var key in errors){
                                    $this.$message({
                                        message: errors[key][0],
                                        type: 'error'
                                    });
                                } 
                            } 
                        })
                    }else{
                        this.phone_error_con='请输入正确的手机号'
                        this.phoneError = true
                    }
                }
           } 
        },

        methods: {
            getUrl(url,imgId){
                this.changeUrl=false
                this.form.avatar = url;
                this.form.picture = url;
            },
            addImg(ele,imgId){
                // alert(1)
                this.imgId=imgId;
                $("#inputId2").click();
            },
            change(e){
                let files = e.target.files || e.dataTransfer.files;  
                if (!files.length) return;  
                let picValue = files[0];  
                this.url_f = this.getObjectURL(picValue); 
                this.changeUrl=true
                console.log(this.url_f)
            },
            getObjectURL (file) {  
                var url = null ;   
                if (window.createObjectURL!=undefined) { // basic  
                  url = window.createObjectURL(file) ;  
                } else if (window.URL!=undefined) { // mozilla(firefox)  
                  url = window.URL.createObjectURL(file) ;  
                } else if (window.webkitURL!=undefined) { // webkit or chrome  
                  url = window.webkitURL.createObjectURL(file) ;  
                }  
                return url ;  
            }, 
            submitForm(formName) {
                let $this = this;
                this.rules.name=[
                            { validator: (rule, value, callback) => {
                                if(value===''){
                                    callback(new Error('请输入姓名'));
                                }else {
                                    callback();
                                } 
                                
                            }, trigger: 'blur'}
                        ]
                this.rules.mobile= [
                            { validator: (rule, value, callback) => {
                                if(value===''){
                                    callback(new Error('请输入手机号'));
                                }else {
                                    callback();
                                } 
                            }, trigger: 'blur'}
                        ] 
                this.rules.avatar= [
                            { required:true,message:'请添加拳手头像', trigger:'blur' }
                        ] 
                this.$refs[formName].validate((valid) => {
                    if (valid&&!this.phoneError) {
                        let url = '';
                        if(this.form.id){
                            //修改
                            url = '/player/'+this.form.id
                        }else{
                            url = '/player'
                        }
                        this.ajax(url,'post',this.form).then((res)=>{
                            if(res&&res.data){
                                console.log(res.data)
                                this.cancelEv(formName)
                            }

                        },function(err){
                            console.log(err.response.status)
                            if(err&&err.response){
                                let errors=err.response.data
                                for(var key in errors){
                                    $this.$message({
                                        message: errors[key][0],
                                        type: 'error'
                                    });
                                } 
                            } 
                        })
                        
                    }
                });
            },
            getData(id){
                this.ajax('/player/'+id).then((res)=>{
                    if(res&&res.data){
                        console.log(res.data.stamina)
                        this.form={
                            id:id,
                            "stamina":res.data.stamina,
                            "skill": res.data.skill,
                            "attack": res.data.attack,
                            "defence": res.data.defence,
                            "strength": res.data.strength,
                            "willpower": res.data.willpower,
                            "name": res.data.name,
                            "mobile": res.data.mobile,
                            "avatar": res.data.avatar
                        }
                    }
                },function(err){
                    console.log(err.response.status)
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            $this.$message({
                                message: errors[key][0],
                                type: 'error'
                            });
                        } 
                    } 
                })
            },
            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            },
            prevImg(formName){
                delete this.rules['name']
                delete this.rules['mobile']
                delete this.rules['avatar']
                this.$refs[formName].validate((valid) => {
                    console.log(valid)
                    if(valid){
                        this.src = this.config.baseUrl+`/ability?skill=${this.form.skill}&strength=${this.form.strength}&defence=${this.form.defence}&willpower=${this.form.willpower}&attack=${this.form.attack}&stamina=${this.form.stamina}`

                        this.prevVisible = true;
                    }
                })
            },
            cancelEv(formName) {
                this.$router.push({path: '/boxerlist'});
                this.$refs[formName].resetFields();
            },

        }
    }
</script>