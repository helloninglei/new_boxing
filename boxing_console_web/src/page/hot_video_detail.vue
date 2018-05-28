<template>
    <div id="addBoxing">
        <TopBar v-if="isShowTop" firstTitle_name="热门视频" firstTitle_path="/hotvideo" :secondTitle_name="secondTitle_name" ></TopBar>
        <div class='container'>
            <el-row> 
                <el-col :span="12">
                    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
                        <el-form-item label="用户ID" prop="user_id">
                            <el-input v-model="ruleForm.user_id"></el-input>
                        </el-form-item>
                        <el-form-item label="视频名称" prop="name">
                            <el-input v-model="ruleForm.name" :rows="6"></el-input>
                        </el-form-item>
                        <el-form-item label="视频介绍" prop="description">
                            <el-input type="textarea" v-model="ruleForm.description"></el-input>
                        </el-form-item>
                        <el-form-item label="付费金额" prop="price">
                            <el-input v-model="ruleForm.price" :span="5"></el-input>
                        </el-form-item>
                        <el-form-item label="完整视频" prop="tsurl" style='display: none'>
                            <el-input v-model="ruleForm.tsurl" type='file' id='full_video'></el-input>
                        </el-form-item>
                        <el-form-item label="完整视频" prop="try_ts_url" style='display: none'>
                            <el-input v-model="ruleForm.try_ts_url" type='file' id='little_video'></el-input>
                        </el-form-item>
                        <el-form-item label="完整视频">
                            <el-button class='myButton_40 btn_width_95 myBtnHover_red' @click="addFullVideo()" v-if="!(tsurl)">添加视频</el-button>
                            <p v-if="(tsurl)">
                                <span class='video_name'>{{tsurl}} </span>
                                <span ><i class="el-icon-error" style='cursor:pointer' @click='deleteUrl(1)'></i></span>
                            </p>
                        </el-form-item>
                        <el-form-item label="不完整视频" prop="try_ts_url">
                            <el-button class='myButton_40 btn_width_95 myBtnHover_red' @click="addLittleVideo()" v-if="!(try_ts_url)">添加视频</el-button>
                            <p v-if="(try_ts_url)">
                                <span class='video_name'>{{try_ts_url}}</span> 
                                <span ><i class="el-icon-error" style='cursor:pointer' @click='deleteUrl(2)'></i></span>
                            </p>
                        </el-form-item>
                        <el-form-item>
                            <!-- <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button> -->
                             <el-button type="danger" class='myColor_red myButton_40 btn_width_95' @click="submitForm('ruleForm')">发布</el-button>
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
              if (this.tsurl === ''&&value==='') {
                callback(new Error('选择完整视频'));
              } else {
                
                callback();
              }
            };
            var validateTryUrl = (rule, value, callback) => {
              if (this.try_ts_url === ''&&value==='') {
                callback(new Error('选择不完整视频'));
              } else {
                
                callback();
              }
            };
            return {
                isShowTop : true,
                tsurl       : '',
                try_ts_url   : '',
                secondTitle_name:'添加视频',
                ruleForm: {
                    user_id: '',
                    name: '',
                    description: '',
                    price: '',
                    tsurl:'',
                    try_ts_url: '',
                },
                rules:{
                    user_id:[
                        { required:false,message:'请输入用户id', trigger:'change' }
                    ],
                    name:[
                        { validator: (rule, value, callback) => {
                            let reg = /^[1-9]\d{1,}$/
                                if(value===''){
                                    callback(new Error('请输入视频名称'));
                                }else if (value.length>40) {
                                    callback(new Error('限制40字数'));
                                } else {
                                
                                    callback();
                                }
                        }, trigger: 'blur' },
                    ],
                    description:[
                        { validator: (rule, value, callback) => {
                            let reg = /^[1-9]\d{1,}$/
                                if(value===''){
                                    callback(new Error('请输入视频介绍'));
                                }else if (value.length>140) {
                                    callback(new Error('限制140字数'));
                                } else {
                                
                                    callback();
                                }
                        }, trigger: 'blur' }
                    ],
                    price:[
                        { validator: (rule, value, callback) => {
                            let reg = /^[1-9]\d{1,}$/
                              if (!reg.test(value)) {
                                callback(new Error('付费金额为自然整数'));
                              } else {
                                
                                callback();
                              }
                        }, trigger: 'blur' }
                    ],
                    tsurl:[
                        { validator: validateUrl, trigger: 'blur' }
                    ],
                    try_ts_url:[
                        { validator: validateTryUrl, trigger: 'blur' }
                    ]
                }
                
            }
        },
        watch:{
            'ruleForm.tsurl'(val){
                this.tsurl = val
            },
            'ruleForm.try_ts_url'(val){
                // console.log(val)
                this.try_ts_url = val
            },
        },
        components: {
            TopBar,
        },
        created() {
            let query     = this.$route.query
            this.ruleForm.user_id = query.user_id;
            this.ruleForm.name    = query.name;
            this.ruleForm.price   = query.price;
            this.ruleForm.description = query.description;
            let tsurl = query.url
            this.tsurl=query.url
            let try_ts_url = query.try_url
            this.try_ts_url= query.try_url
            $('#full_video').val(tsurl) 
            $('#little_video').val(try_ts_url) 
            if(query.user_id){
                this.secondTitle_name = '修改视频'
            }
            // this.ruleForm.try_ts_url = 'this.config.baseUrl+try_ts_url'
            console.log(query)
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let sendData = this.ruleForm;
                        sendData.try_url = this.try_ts_url;
                        sendData.url = this.tsurl;
                        console.log(this.ruleForm)
                        alert('submit!');
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
                console.log(111)
                this.try_ts_url=''
                this.ruleForm.try_ts_url=''
                console.log(this.try_ts_url)
            },
        },
    }
</script>