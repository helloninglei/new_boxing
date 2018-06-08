<template>
    <div id="addBoxing">
        <TopBar v-if="isShowTop" firstTitle_name="热门视频" firstTitle_path="/hotvideo" :secondTitle_name="secondTitle_name" ></TopBar>
        <div class='container'>
            <el-row> 
                <el-col :span="12">
                    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
                        <el-form-item label="用户ID" prop="user_id">
                            <el-input v-model="ruleForm.user_id" placeholder='必须为有效的用户ID'></el-input>
                        </el-form-item>
                        <el-form-item label="视频名称" prop="name">
                            <el-input v-model="ruleForm.name"  :maxlength="40" placeholder='限制40字数'></el-input>
                        </el-form-item>
                        <el-form-item label="视频介绍" prop="description">
                            <el-input type="textarea" v-model="ruleForm.description" :rows="6" placeholder='限制140字数'></el-input>
                        </el-form-item>
                        <el-form-item label="付费金额" prop="price_int">
                            <el-input v-model="ruleForm.price_int" :span="5" placeholder="付费金额为自然数" type='number'></el-input>
                        </el-form-item>
                        <!-- <el-form-item label="完整视频" prop="tsurl" style='display: none'>
                            
                        </el-form-item> -->
                        <!-- <el-form-item label="不完整视频" prop="try_ts_url" style='display: none'>
                            
                        </el-form-item> -->
                        <el-form-item label="完整视频" prop="tsurl">
                            <el-button class='myButton_40 btn_width_95 myBtnHover_red' @click="addFullVideo()" v-if="!(tsurl)">添加视频</el-button>
                            <p v-if="(tsurl)">
                                <span class='video_name'>{{tsurl}} </span>
                                <span ><i class="el-icon-error" style='cursor:pointer' @click='deleteUrl(1)'></i></span>
                            </p>
                            <el-input v-model="ruleForm.tsurl" type='file' id='full_video' @change='getFullVideo' style='display: none'></el-input>
                        </el-form-item>
                        <el-form-item label="不完整视频" prop="try_ts_url">
                            <el-button class='myButton_40 btn_width_95 myBtnHover_red' @click="addLittleVideo()" v-if="!(try_ts_url)">添加视频</el-button>
                            <p v-if="(try_ts_url)">
                                <span class='video_name'>{{try_ts_url}}</span> 
                                <span ><i class="el-icon-error" style='cursor:pointer' @click='deleteUrl(2)'></i></span>
                            </p>
                            <el-input v-model="ruleForm.try_ts_url" type='file' id='little_video' @change='getLittleVideo' style='display: none'></el-input>
                        </el-form-item>
                        <el-form-item>
                            <!-- <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button> -->
                             <el-button type="danger" class='myColor_red myButton_40 btn_width_95' @click="submitForm('ruleForm')">{{btn_name}}</el-button>
                             <el-button class='myButton_40 btn_width_95 myBtnHover_red' @click="resetForm('ruleForm')">取消</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<style>
#addBoxing .el-form-item__label{
    font-family: "PingFangSC-Regular";
    font-size: 16px;
    color: #000000;
}
#addBoxing .el-form-item{margin-bottom:30px;}
#addBoxing .button{height:37px;width:45px;border:none;border-right:1px solid #ccc;margin-top:2px;margin-left:2px!important;font-size:20px;padding-top:8px;padding-left:12px;}
#addBoxing .myAddress input{padding-left:50px;}
</style>
<style scope>
    .image{height:140px;width:140px;border:1px solid #ccc;vertical-align: middle}
    .image img{height:100%;}
    .video_name{
        width:90%;
        display: inline-block;
        vertical-align: middle;
        margin-right:20px;
        white-space:nowrap;
        overflow:auto;
        /*text-overflow:ellipse;*/
    }
</style>
<script>
    import TopBar from 'components/topBar';
    import $      from 'jquery' 
    export default {
        data() {
            var validateUrl = (rule, value, callback) => {
                // console.log(this.tsurl,value)
              if ((!this.tsurl )&&(!value)) {
                callback(new Error('选择完整视频'));
              } else {
                
                callback();
              }
            };
            var validateTryUrl = (rule, value, callback) => {
              if ((!this.try_ts_url) &&(!value)) {
                callback(new Error('选择不完整视频'));
              } else {
                
                callback();
              }
            };
            return {
                isShowTop   : true,
                tsurl       : '',
                try_ts_url  : '',
                secondTitle_name:'添加视频',
                id          :'',
                btn_name    : '发布',
                ruleForm: {
                    user_id : '',
                    name    : '',
                    description: '',
                    price_int  : '',
                    price   : '',
                    tsurl   :'',
                    try_ts_url: '',
                },
                rules:{
                    user_id:[
                        { required:true,message:'请输入用户id', trigger:'blur' }
                    ],
                    name:[
                        { required:true,message:'请输入视频名称', trigger:'blur' }
                    ],
                    description:[
                        { validator: (rule, value, callback) => {
                                if(!value){
                                    callback(new Error('请输入视频介绍'));
                                }else if (value&&value.length>140) {
                                    callback(new Error('限制140字数'));
                                } else {
                                
                                    callback();
                                }
                        }, trigger: 'blur' ,required:true}
                    ],
                    price_int:[
                        { validator: (rule, value, callback) => {
                              if (!/^[0-9]*$/.test(value)) {
                                callback(new Error('付费金额为自然整数'));
                              } else {
                                
                                callback();
                              }
                        }, trigger: 'blur',required:true }
                    ],
                    tsurl:[
                        { validator: validateUrl, trigger: 'blur',required:true }
                    ],
                    try_ts_url:[
                        { validator: validateTryUrl, trigger: 'blur',required:true }
                    ]
                }
                
            }
        },
        components: {
            TopBar,
        },
        created() {
            let query     = this.$route.query
            this.id = query.id
            this.ruleForm.user_id = query.user_id;
            this.ruleForm.name    = query.name;
            this.ruleForm.price_int   = parseInt(query.price_amount);
            this.ruleForm.description = query.description;
            let tsurl = query.url
            this.tsurl=query.url
            let try_ts_url = query.try_url
            this.try_ts_url= query.try_url
            $('#full_video').val(tsurl) 
            $('#little_video').val(try_ts_url) 
            if(this.id){
                this.secondTitle_name = '修改视频'
                this.btn_name = '修改'
            }
            // this.ruleForm.try_ts_url = 'this.config.baseUrl+try_ts_url'
            // console.log(query)
        },
        methods: {
            getData(){

            },
            getFullVideo(){
                var _this=this
                var file=event.target.files;
                var $this=this
                this.upload(file[0],function(url){
                    console.log(url)
                    $this.tsurl = url
                });
            },
            getLittleVideo(){
                var _this=this
                var file=event.target.files;
                var $this=this
                this.upload(file[0],function(url){
                    $this.try_ts_url = url
                });
            },
            upload(file,fun){
                // console.log(file)
                let formData = new FormData() 
                formData.append('file', file) 
                this.ajax('/upload','post',formData).then(function(res){
                    if(res&&res.data){
                        fun(res.data.urls[res.data.urls.length-1])
                    }

                },function(err){
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            console.log(errors[key])
                            // return
                        } 
                    } 
                })
            },
            submitForm(formName) {
                let $this = this
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let sendData = this.ruleForm;
                        sendData.try_url = this.try_ts_url;
                        sendData.url = this.tsurl;
                        sendData.price = parseInt(sendData.price_int)*100
                        let $this = this
                        if(this.id){
                            //编辑
                            this.ajax('/hot_videos/'+this.id,'put',sendData).then(function(res){
                                if(res&&res.data){
                                    $this.resetForm(formName)
                                }

                            },function(err){
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
                            //新建
                            this.ajax('/hot_videos','post',sendData).then(function(res){
                                if(res&&res.data){
                                    $this.resetForm(formName)
                                }

                            },function(err){
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
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$router.push({path: '/hotvideo'});
                this.$refs[formName].resetFields();
            },
            addFullVideo(){
                $('#full_video').click();
            },
            addLittleVideo(){
                $('#little_video').click();
            },
            deleteUrl(type){
                if(type==1){
                    this.tsurl=''
                    this.ruleForm.tsurl=''
                }else{
                    this.try_ts_url=''
                    this.ruleForm.try_ts_url=''
                }
                
            },
            deleteTryUrl(){
                this.try_ts_url=''
                this.ruleForm.try_ts_url=''
            },
        },
    }
</script>