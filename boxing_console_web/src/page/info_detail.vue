<template>
    <div id="info_detail">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/infolist" secondTitle_name="资讯"></TopBar>
        <div class="container">
            <el-row> 
                <el-col :span="12">
                    <el-form :model="form" label-width="110px" :rules="rules" ref="ruleForm">
                        <el-form-item label="主标题" prop="title">
                            <el-input v-model="form.title" placeholder="限制20字" :maxlength="20"></el-input>
                        </el-form-item>
                        <el-form-item label="副标题" prop="sub_title">
                            <el-input v-model="form.sub_title" placeholder="限制20字" :maxlength="20"></el-input>
                        </el-form-item>
                        <el-form-item label="初始阅读量" prop="initial_views_count" style='width:284px'>
                            <el-input v-model="form.initial_views_count" placeholder="请输入正整数"></el-input>
                        </el-form-item>
                        <el-form-item label="资讯主题图" prop="picture">
                            <el-input v-model="form.picture" type='hidden'></el-input>
                            <Cropper @getUrl='getUrl' :url_f='url_f' :changeUrl='changeUrl' :imgId='imgId' :width='244' :height='144'></Cropper>

                            <div class='show' @click="addImg('inputId2','img2')">  
                               <img :src="config.baseUrl+imgUrl" alt="" width='100%' id='img2' v-if='imgUrl'> 
                               <div>  
                                   <input type="file" id="inputId2" style='display:none' accept="image" @change="change">  
                                   <label for="inputId2"></label>  
                                </div> 
                            </div>
                            
                            <div style='width:244px;height:144px;border:1px solid #ccc' @click="addImg('inputId2','img2')">
                                <i class="el-icon-plus avatar-uploader-icon"></i>
                                <div class="upload_tip_text">尺寸大小：244*144</div>
                            </div>
                            <div class="el-form-item__error" v-if="showError">
                                请上传资讯主题图
                            </div>
                        </el-form-item>
                        <el-form-item label="是否置顶" prop="stay_top">
                            <el-radio-group v-model="form.stay_top">
                                <el-radio :label="true" >是</el-radio>
                                <el-radio :label="false">否</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-checkbox-group v-model="form.push_news" style='margin-bottom:22px'>
                          <el-checkbox label="创建推送" name="push_news"></el-checkbox>
                        </el-checkbox-group>
                        <el-form-item label="发送时间" style='margin-left:32px' id='addTime'>
                            <el-date-picker
                                    class="margin_rt25"
                                    v-model="dateArr"
                                    type="datetimerange"
                                    range-separator="至"
                                    start-placeholder="起始日期"
                                    end-placeholder="结束日期"
                                    @change="getDateTime"
                                    :default-value='new Date()'
                                    value-format="yyyy-MM-dd HH:mm:ss">
                            </el-date-picker>
                        </el-form-item>
                        <el-form-item style='margin-left:30px;margin-top:-30px'>
                            <el-form-item prop="end_time" >
                                <el-input v-model="form.end_time" style='display: none'></el-input>
                            </el-form-item>
                        </el-form-item>
                        
                        <p class='udeitor_title'>App内正文（<span style='color:#F95862'>必填</span>），如未填写App外分享正文，App内和App外都显示App内正文。</p>
                        <div class='udeitor_content' id='ueditor1'>
                            <Ueditor @changeEditor="onEditorChange" myQuillEditor='myQuillEditor' imgInput='imgInput1' :appContent='form.app_content'></Ueditor>
                            <div class='text_rt margin_tp10'>
                                <el-button class="myButton_40 myBtnHover_red btn_width_95" @click='preview(1)' v-if='showPrev1'>预览</el-button>
                                <el-button class="myButton_40 btn_width_95" disabled v-else>预览</el-button>
                            </div>
                        </div>
                        <p class='udeitor_title'>App外分享正文</p>
                        <div class='udeitor_content' id='ueditor2'>
                            <Ueditor @changeEditor="onEditorChangeSub" myQuillEditor='myQuillEditorSub' imgInput='imgInput2' :appContent='form.share_content'></Ueditor>
                            <div class='text_rt margin_tp10'>
                                <el-button class="myButton_40 myBtnHover_red btn_width_95" @click='preview(2)' v-if='showPrev2'>预览</el-button>
                                <el-button class="myButton_40 btn_width_95" disabled  v-else>预览</el-button>
                            </div>
                        </div>
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

<style lang="stylus" type="text/stylus" scoped>

    .el-icon-circle-close {
        position absolute
        right  0
        top 0
        font-size 20px
    }
    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        position:absolute;
        left:0;
        width: 244px;
        height: 144px;
        line-height: 144px;
        text-align: center;
        z-index:2;
    }
    .avatar {
        display: block;
        width: 244px;
        height 144px;
        z-index:2;
    }
    .handle_btn {
        margin-top 60px
        .cancel {
            margin-right 30px
        }
    }
    .upload_tip_text {
        width 244px
        text-align center
        position absolute
        bottom 0
        color #909399
    }
    .info{
        border-radius: 10px;
        line-height: 20px;
        padding: 10px;
        margin: 10px;
        background-color: #ffffff;
    }
    .udeitor_content,.udeitor_title{width:105%;margin-left:30px}
    .udeitor_title{
        margin-bottom:20px;
    }
    .udeitor_content{
        margin-bottom:60px
    }
    .prev_title{font-size:20px;margin-bottom:10px}
    .prev_time{font-size:14px}
</style>
<style scope>
    .drop-enter-active {
      transition: all .5s;
    }
    .drop-leave-active {
      transition: all .3s;
    }
    .drop-enter {
      transform: translateY(-500px);
    }
    .drop-leave-active {
      transform: translateY(-500px);
    }   
  
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
      
    }
    .dialog-wrapper{
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
    span.close-btn{
        padding: 0 5px;
        float: right;
        cursor: pointer;
        font-size: 18px;
        font-weight: bold;
    }
    .content{
        height:calc(100% - 80px);
        overflow-y: auto;
        margin-bottom:10px;
        margin-top:10px;
    }
</style>
<style>
    #info_detail .el-checkbox__label,#info_detail .el-radio__label,#info_detail .el-form-item__label,.udeitor_title{
        font-family: PingFangSC-Regular;
        font-size: 16px;
        color: #000000;
    }
    #info_detail .show{
        width: 244px;  
        height: 144px;  
        overflow: hidden;  
        position: relative;  
        float:left;
        z-index:20;
        border: 1px solid #d5d5d5; 
    }
    #priv_content{line-height:24px;}
    #priv_content img,#priv_content video{width:100%;}
    #prevShow{z-index:-1!important}
    .v-modal.addIndex{z-index:-1!important}
    .v-modal.addIndex.removeIndex{z-index:2001!important}
    #prevShow.addIndex{z-index:2002!important}
    .ql-video{width:100%;height:220px;}
    .ql-align-center{text-align: center}
    .ql-align-right{text-align: right}
    #priv_content iframe{width:100%;height:220px;}
</style>
<script>
    import TopBar   from 'components/topBar';
    import config   from 'common/my_config'
    import Ueditor  from 'components/ueditor'
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
                    title    : [{ required: true, message: '请输入主标题', trigger: 'blur' }],
                    sub_title: [{ required: true, message: '请输入副标题', trigger: 'blur' }],
                    picture: [
                        { validator: (rule, value, callback) => {
                            if (value==='') {
                                callback(new Error('请选择主题图片'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur', required: true}
                    ],
                    stay_top: [{ required: true, message: '请选择是否置顶', trigger: 'blur' }],
                    end_time: [
                        { validator: (rule, value, callback) => {
                            if(this.form.push_news=='false'||!this.form.push_news){
                                callback();
                            }else if(this.form.start_time===''){
                                callback(new Error('请选择发送的开始时间'));
                            }else if (value==='') {
                                callback(new Error('请选择发送的结束时间'));
                            }else if(new Date(this.form.start_time)-new Date()<0){
                                callback(new Error('开始发送时间不能小于当前时间'));
                            }else if(new Date(value)-new Date(this.form.start_time)<0){
                                callback(new Error('结束时间不能早于开始时间'));
                            }else if(new Date(value)-new Date(this.form.start_time)> 60*60*24*14*1000){
                                callback(new Error('推送有效时间不能超过14天'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur', }
                    ],
                    initial_views_count: [
                        { validator: (rule, value, callback) => {
                            if (value === '') callback(new Error('请输入初始阅读量'))
                            else {
                                if (value < 0 || !/^[0-9]*$/.test(value)) {
                                    callback(new Error('只能输入正整数'));
                                    return;
                                }
                                callback();
                            }
                        }, trigger: 'blur',required: true }
                    ],  
                },
            }
        },

        components: {
            TopBar,
            Ueditor,
            Cropper
        },

        created() {
            this.query = this.$route.query;
            if(this.query.id){
                //编辑
                this.form=this.query;
                if(this.form.app_content&&this.form.app_content.indexOf('http')==-1){
                   this.form.app_content   = this.form.app_content.replace(/src="/g,'src="'+this.config.baseUrl) 
                }
                if(this.form.share_content&&this.form.share_content.indexOf('http')==-1){
                   this.form.share_content   = this.form.share_content.replace(/src="/g,'src="'+this.config.baseUrl) 
                }
                this.form.push_news = this.query.push_news;
                // this.form.share_content = this.form.share_content.replace(/src="/g,'src="'+this.config.baseUrl)
                let startDate = new Date();
                let endDate   = new Date();
                startDate.setMinutes(startDate.getMinutes()+5);
                endDate.setDate(endDate.getDate()+1);
                this.dateArr=[this.query.start_time?this.query.start_time:startDate.Format("yyyy-MM-dd hh:mm:ss"),this.query.end_time?this.query.end_time:endDate.Format("yyyy-MM-dd hh:mm:ss")]
                this.imgUrl = this.form.picture ;
                this.confirmText = '修改'
            }else{
                // 2018-06-12 08:06:08
                let startDate = new Date();
                let endDate   = new Date();
                startDate.setMinutes(startDate.getMinutes()+5);
                endDate.setDate(endDate.getDate()+1);
                this.dateArr=[startDate.Format("yyyy-MM-dd hh:mm:ss"),endDate.Format("yyyy-MM-dd hh:mm:ss")]
            }
            if(this.form.push_news=='false'){
                this.form.push_news=false;
            }
            if(this.form.push_news=='true'){
                this.form.push_news=true;
            }
            this.isshowPrev();
            this.getDateTime();
        },

        computed: {
           
        },

        watch:{
            'form.title'(val){
                // console.log(val)
                this.isshowPrev();
            },
            'form.initial_views_count'(){
                this.isshowPrev();
            },
            'imgUrl'(){
                this.isshowPrev();
            },
            'form.app_content'(){
                this.isshowPrev();
            },
            'form.share_content'(){
                this.isshowPrev();
            },
            'form.push_news'(val){
                
                if(val=='false'||!val){
                    $('#addTime').removeClass('is-required')

                }else{
                    $('#addTime').addClass('is-required')
                }
            },
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
            isshowPrev(){
                if(!this.form.title||this.form.initial_views_count==""||this.form.initial_views_count<=0||(this.form.picture === '')||!this.form.app_content){
                    this.showPrev1 = false
                }else{
                    this.showPrev1 = true
                }
                if(!this.form.title||this.form.initial_views_count==''||this.form.initial_views_count<=0||(this.form.picture === '')||!this.form.share_content){
                    this.showPrev2 = false
                }else{
                    this.showPrev2 = true
                }
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

            getDateTime() {
                this.form.start_time = this.dateArr?this.dateArr[0]:'';
                this.form.end_time = this.dateArr?this.dateArr[1]:'';
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
            preview(type){
                // console.log(this.form)
                this.type = type
                // console.log(this.form.app_content)
                $('.dialog-modal').removeClass('indexNone')
                
                if(type==1){
                    $('#priv_content').html(this.form.app_content)
                }else{
                    $('#priv_content').html(this.form.share_content)
                }
                
                this.prevVisible = true
                
            },

            onEditorChange(value) {
                // console.log('editor change!', editor, html, text)
                 this.form.app_content = value ;
                 $('#priv_content').html(value)
            },
            onEditorChangeSub(value) {
                // console.log('editor change!', editor, html, text)
                 // console.log(value)
                 this.form.share_content = value ;
            }

        }
    }
</script>