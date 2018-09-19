<template>
    <div id="boxer_detail">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/infolist" secondTitle_name="资讯"></TopBar>
        <div class="container">
            <el-row> 
                <el-col :span="12" style='min-width:800px'>
                    <el-form :model="form" label-width="90px" :rules="rules" ref="ruleForm">
                        <p class='content_title'>添加参赛拳手</p>
                        <p class='title'>拳手信息</p>
                        <el-row>
                            <el-col :span="11">
                                <el-form-item label="拳手姓名" prop="title">
                                    <el-input v-model="form.title" placeholder="请输入姓名" :maxlength="20"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="11" :offset="2">
                                <el-form-item label="拳手手机号" prop="title">
                                    <el-input v-model="form.title"  placeholder="请输入手机号" :maxlength="11"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>  
                        
                        <el-form-item label="拳手头像" prop="picture">
                            <el-input v-model="form.picture" type='hidden'></el-input>
                            <Cropper @getUrl='getUrl' :url_f='url_f' :changeUrl='changeUrl' :imgId='imgId' :width='100' :height='100'></Cropper>

                            <div class='show' @click="addImg('inputId2','img2')">  
                               <img :src="config.baseUrl+imgUrl" alt="" width='100%' id='img2' v-if='imgUrl'> 
                               <div>  
                                   <input type="file" id="inputId2" style='display:none' accept="image" @change="change">  
                                   <label for="inputId2"></label>  
                                </div> 
                            </div>
                            
                            <div style='width:100px;height:100px;border:1px solid #ccc' @click="addImg('inputId2','img2')">
                               
                            </div>
                            <div class="el-form-item__error" v-if="showError">
                                请上传资讯主题图
                            </div>
                        </el-form-item>
                        <p class='title'>能力雷达图 <el-button type="danger" class='myColor_red margin_rt25 border_raduis_100' style='width:60px;height:30px;line-height:30px;padding:0'>预览</el-button></p>
                        <el-row>
                            <el-col :span="11">
                                <el-form-item label="耐力" prop="title">
                                    <el-input v-model="form.title" placeholder="请输入" :maxlength="20"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="11" :offset="2">
                                <el-form-item label="技术" prop="title">
                                    <el-input v-model="form.title"  placeholder="请输入" :maxlength="11"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>  
                        <el-row>
                            <el-col :span="11">
                                <el-form-item label="进攻" prop="title">
                                    <el-input v-model="form.title" placeholder="请输入" :maxlength="20"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="11" :offset="2">
                                <el-form-item label="防守" prop="title">
                                    <el-input v-model="form.title"  placeholder="请输入" :maxlength="11"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>  
                        <el-row>
                            <el-col :span="11">
                                <el-form-item label="力量" prop="title">
                                    <el-input v-model="form.title" placeholder="请输入" :maxlength="20"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="11" :offset="2">
                                <el-form-item label="意志力" prop="title">
                                    <el-input v-model="form.title"  placeholder="请输入" :maxlength="11"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>  
                        <div style='text-align: center'>
                            <el-button class="myButton_40 myBtnHover_red btn_width_200" @click="cancelEv('ruleForm')">取消</el-button>
                            <el-button type="danger" class='btn_width_200 myColor_red' @click="submitForm('ruleForm')">{{confirmText}}</el-button>
                        </div>
                    </el-form>
                </el-col>
            </el-row>
        </div>
        <div class="dialog-modal indexNone"> <!-- 根元素，z-index 需要高于父容器其他元素 -->
            <div class="dialog-wrapper" @click="prevVisible = false" v-show="prevVisible"></div> <!-- 加载一个具有透明度的背景，使根元素透明，子元素会继承该透明度 -->
            <transition name="drop">
                <div class="dialog-container" v-show="prevVisible">  <!-- 模态框容器，z-index 需要高于背景 -->
                    <h2 style='font-size:24px;font-weight:bold'>预览</h2>
                    <div class='content'>
                        <h4 class="prev_title">{{form.title}}</h4>
                        <div id='priv_content'></div>
                    </div>
                    <div slot="footer" class="dialog-footer" style='text-align: center'>
                        <el-button @click="prevVisible = false">关闭</el-button>
                    </div>
                </div>
            </transition>
        </div>
    </div>
</template>

<style lang="stylus" scoped>

    .el-icon-circle-close {
        position absolute
        right  0
        top 0
        font-size 20px
    }
</style>
<style scope>
  
    .dialog-modal{
        position: absolute;
        z-index: 5;
        font-family: PingFangSC-light;
        font-size: 16px;
        color: #fff;
    }
    .dialog-modal.indexNone{
        z-index: -5;
    }
    .dialog-wrapper
    {
        position: fixed;
        height: 100%;
        width: 100%;
        z-index: 5;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background-color: #000;
        opacity: .5;
      
    }
    .dialog-container{
        position: fixed;
        z-index:80;
        width:400px;height:500px;top:50%;left:50%;margin-left:-200px;margin-top:-250px!important;border-radius:10px;
        background-color: #000;
        padding:20px;
        color:#fff;
        box-shadow: 0 5px 15px rgba(0,0,0,.5);
    }
    .content{
        height:calc(100% - 80px);
        overflow-y: auto;
        margin-bottom:10px;
        margin-top:10px;
    }
    .content_title{
        font-family: PingFangSC-Regular;
        font-size: 16px;
        color: #000000;
    }
    .title{
        font-family: PingFangSC-Regular;
        font-size: 14px;
        color: #000000;
    }
</style>
<style>
    #boxer_detail .el-checkbox__label,#boxer_detail .el-radio__label,#boxer_detail .el-form-item__label{
        font-family: PingFangSC-Regular;
        font-size: 14px!important;
        color: #606266;
    }
    #boxer_detail .show{
        width: 100px;  
        height: 100px;  
        overflow: hidden;  
        position: relative;  
        float:left;
        z-index:20;
        /*border: 1px solid #d5d5d5; */
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
                isShowTop: true,
                inputId:'',
                url_f:'',
                changeUrl:false,
                imgId :'',
                imgUrl:'',
                cropper_width:0,
                cropper_height:0,

                showPrev1:false,
                showPrev2:false,

                showError: false,
                confirmText:'发布',
                action: `${config.baseUrl}/upload`,
                checkType: 'voteId',
                dateArr: [],
                type:'',//1正文 2 外文
                prevVisible:true,//是否显示预览
                form: {
                    title: '',
                    sub_title: '',
                    initial_views_count: '',
                    picture: '',
                    stay_top: false,
                    push_news: false,
                    start_time: '',
                    end_time: '',
                    app_content: '',
                    share_content: '',
                },
                rules: {
                    title    : [{ message: '请输入主标题', trigger: 'blur' }],
                    sub_title: [{ message: '请输入副标题', trigger: 'blur' }],
                    picture: [
                        { validator: (rule, value, callback) => {
                            if (value==='') {
                                callback(new Error('请选择主题图片'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur',}
                    ],
                    stay_top: [{ message: '请选择是否置顶', trigger: 'blur' }],
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
                this.form=this.query;
            }else{
                
            }
        },

        computed: {
           
        },

        watch:{
            
        },

        methods: {
            getUrl(url,imgId){
                this.changeUrl=false
                this.imgUrl = url;
                this.form.picture = url;
                // console.log(url,imgId)

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
                // console.log(this.form)
                let $this = this;
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let reg = '/'+this.config.baseUrl+'/g'
                        this.form.app_content   = this.form.app_content?this.form.app_content.replace(new RegExp("(" + this.config.baseUrl + ")", "g"),''):'';
                        this.form.share_content = this.form.share_content?this.form.share_content.replace(new RegExp("(" + this.config.baseUrl + ")", "g"),''):'';
                        if(!this.form.push_news){
                           delete this.form['start_time']; 
                           delete this.form['end_time']; 
                        }
                        
                        if(this.form.id){
                            //修改
                            this.ajax('/game_news/'+this.form.id,'put',this.form).then(function(res){
                                if(res&&res.data){
                                    $this.cancelEv(formName)
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
                            this.ajax('/game_news','post',this.form).then(function(res){
                                if(res&&res.data){
                                    // console.log(res.data)
                                    $this.cancelEv(formName)
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
                        
                    }
                });
            },

            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            },

            cancelEv(formName) {
                this.$router.push({path: '/infolist'});
                this.$refs[formName].resetFields();
            },

        }
    }
</script>