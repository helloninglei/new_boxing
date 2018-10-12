<template>
    <div id="version_detail">
        <TopBar v-if="isShowTop" firstTitle_name="版本管理" firstTitle_path="/versionlist" secondTitle_name="新增版本"></TopBar>
        <div class="container">
            <el-row> 
                <el-col :span="12" style='min-width:800px'>
                    <el-form :model="form" label-width="212px" :rules="rules" ref="ruleForm">
                        <el-form-item label="版本号" prop="version">
                            <el-input v-model="form.version" placeholder="请输入" type='' ></el-input>
                        </el-form-item>  
                        <el-form-item label="升级文案" prop="message">
                            <el-input type="textarea" v-model="form.message" :rows="8" :maxlength="1000"></el-input>
                        </el-form-item> 
                        <el-form-item label="是否强更" prop="force">
                            <el-radio-group v-model="form.force">
                                <el-radio :label="true"     name="force" >是</el-radio>
                                <el-radio :label="false"     name="force" >否</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="平台" prop="platform">
                            <el-radio-group v-model="form.platform">
                                <el-radio label="ios"     name="platform" >iOS</el-radio>
                                <el-radio label="android"     name="platform" >安卓</el-radio>
                            </el-radio-group>
                        </el-form-item> 
                        <el-form-item label="内部版本号" prop="inner_number" v-if='form.platform=="android"'>
                            <el-input v-model="form.inner_number" placeholder="请输入" type=''></el-input>
                        </el-form-item> 
                        <el-form-item label="安装包" prop="package" v-if='form.platform=="android"'>
                            <el-input  type='file' id='getImg' style='display: none' @change="upload"></el-input>
                            <el-button type="default" class='' @click="changeInput" style='width:107px;margin-left:20px' v-if="!form.package">上传</el-button>
                            <el-col :span="2" v-if='form.package'>
                                <img src="./img/anzhuo.png" alt="" @click="changeInput">
                            </el-col>
                            <el-col :span="22" v-if='form.package' class='fileDetail'>
                                <p>{{fileName}}</p>
                                <p>{{fileSize}}M 上传完成</p>
                            </el-col>
                            <el-col :span="22" v-show='uploadProgress>0&&uploadProgress<100'>
                            <!-- <el-col :span="22"> -->
                                <el-progress type="circle" :percentage="uploadProgress" :width='70' style='position:absolute;left:120px;top:-14px' ></el-progress>
                            </el-col>
                            
                        </el-form-item> 
                        <div style='text-align: left;margin-left:212px'>
                            <el-button class="myButton_40 myBtnHover_red" @click="cancelEv('ruleForm')" style='width:150px'>取消</el-button>
                            <el-button type="danger" class=' myColor_red' @click="submitForm('ruleForm')" style='width:150px;margin-left:58px'>确认</el-button>
                        </div>
                    </el-form>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<style lang="stylus">
    #version_detail .el-checkbox__label,#version_detail .el-radio__label,#version_detail .el-form-item__label{
        font-family: PingFangSC-Regular;
        font-size: 16px!important;
        color: #000;
    }
    #version_detail{
        .el-form-item{
            margin-bottom:50px
        }
        .fileDetail p{
            height:20px;line-height:20px;
            font-size:14px;color:#000;opacity:0.9;
            &:last-child{
                font-size:12px;color:#000;opacity:0.5;
            }
        }
    }
</style>
<script>
    import TopBar   from 'components/topBar';
    import config   from 'common/my_config'
    import Cropper from 'components/cropper';
    import $      from 'jquery' 
    export default {
        data() {
            return {
                isShowTop: true,
                showError: false,
                query:{},
                form: {
                    "version": "",
                    "platform": "android",
                    "message": "",
                    "inner_number": '',
                    "force": '',
                    "package": "",
                    status:'FUTURE'
                },
                rules:{
                    version: [{ required:true,message:'请输入版本号', trigger:'blur' }],
                    message : [{ required:true,message:'请输入升级文案', trigger:'blur' }],
                    force: [{ required:true,message:'请选择是否强更', trigger:'blur' }],
                    platform: [{ required:true,message:'请选择平台', trigger:'blur' }],
                },
                uploadProgress:0,
                fileSize:0,
                fileName:'',
            }
        },

        components: {
            TopBar,
            Cropper
        },

        created() {
            this.query = this.$route.query;
            if(this.query&&this.query.row){
                //编辑
                this.form = this.query.row
            }else{
                
            }
        },

        computed: {
           
        },

        watch:{
          
        },

        methods: {
            submitForm(formName) {
                if(this.form.platform=="android"){
                    this.rules.inner_number = [{ required:true,message:'请输入内部版本号', trigger:'blur' }]
                    this.rules.package = [{ required:true,message:'请添加安装包', trigger:'blur' }]
                }else{
                    delete this.rules['inner_number']
                    delete this.rules['package']
                }
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        if(this.form.platform!="android"){
                            delete this.form['inner_number']
                            delete this.form['package']
                        }
                        console.log(this.form)
                        let url = '';
                        let type=''
                        if(this.form.id){
                            //修改
                            url = '/app_versions/'+this.form.id
                            type = 'patch'
                        }else{
                            url = '/app_versions'
                            type='post'
                        }
                        this.ajax(url,type,this.form).then((res)=>{
                            this.cancelEv(formName)

                        },(err)=>{
                            if(err&&err.response){
                                let errors=err.response.data
                                for(var key in errors){
                                    console.log(errors[key][0])
                                    this.$message({
                                        message: errors[key][0],
                                        type: 'error'
                                    });
                                } 
                            } 
                        })
                        
                    }
                });
            },
            changeInput(){
                $('#getImg').click();
            },
            upload(e){
                var file=event.target.files[0];
                let formData = new FormData() 
                this.fileName = file.name
                this.fileSize = (file.size/1024/1024).toFixed(2)
                formData.append('file', file) 
                this.ajax('/upload','post',formData,{},{},(val)=>{
                    this.uploadProgress = parseFloat(val)
                }).then((res)=>{
                    if(res&&res.data){
                        console.log(res)
                        this.form.package = res.data.urls[0]
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
            },
            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            },
            cancelEv(formName) {
                this.$router.push({path: '/versionlist'});
                this.$refs[formName].resetFields();
            },

        }
    }
</script>