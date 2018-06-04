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
                            <el-input v-model="form.sub_title" placeholder="请输入"></el-input>
                        </el-form-item>
                        <el-form-item label="初始阅读量" prop="initial_views_count" style='width:284px'>
                            <el-input v-model="form.initial_views_count" placeholder="请输入"></el-input>
                        </el-form-item>
                        <el-form-item label="资讯主题图">
                            <!-- <el-upload
                                    class="avatar-uploader"
                                    :action=action
                                    :show-file-list="false"
                                    :on-success="handleAvatarSuccess"
                                    style="position: relative;width: 244px;border: 1px solid #d9d9d9;overflow: hidden;cursor: pointer;">
                                <template v-if="picture">
                                    <i class="el-icon-circle-close close_btn" @click.stop="removeImageEv"></i>
                                    <img  :src="picture" class="avatar">
                                </template>
                                <template v-else>
                                    
                                </template>
                            </el-upload> -->
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
                                <el-radio label="true">是</el-radio>
                                <el-radio label="false">否</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-checkbox-group v-model="form.push_news" style='margin-bottom:22px'>
                          <el-checkbox label="创建推送" name="push_news"></el-checkbox>
                        </el-checkbox-group>
                        <el-form-item label="发送时间" prop="stay_top">
                            <el-date-picker
                                    class="margin_rt25"
                                    v-model="dateArr"
                                    type="datetimerange"
                                    range-separator="至"
                                    start-placeholder="起始日期"
                                    end-placeholder="结束日期"
                                    @change="getDateTime"
                                    value-format="yyyy-MM-dd hh:mm:ss">
                            </el-date-picker>
                        </el-form-item>
                        <p class='udeitor_title'>App内正文（<span style='color:#F95862'>必填</span>），如未填写App外分享正文，App内和App外都显示App内正文。</p>
                        <div class='udeitor_content' id='ueditor1'>
                            <Ueditor @changeEditor="onEditorChange" myQuillEditor='myQuillEditor' imgInput='imgInput1' :appContent='form.app_content'></Ueditor>
                            <div class='text_rt margin_tp10'>
                                <el-button class="myButton_40 myBtnHover_red btn_width_95" @click='preview(1)' v-if='(form.title&&form.initial_views_count>0&&form.start_time&&form.end_time&&form.app_content)&&(form.picture||picture)'>预览</el-button>
                                <el-button class="myButton_40 btn_width_95" disabled v-else>预览</el-button>
                            </div>
                        </div>
                        <p class='udeitor_title'>App内正文（必填），如未填写App外分享正文，App内和App外都显示App内正文。</p>
                        <div class='udeitor_content' id='ueditor2'>
                            <Ueditor @changeEditor="onEditorChangeSub" myQuillEditor='myQuillEditorSub' imgInput='imgInput2' :appContent='form.share_content'></Ueditor>
                            <div class='text_rt margin_tp10'>
                                <el-button class="myButton_40 myBtnHover_red btn_width_95" @click='preview(2)' v-if='(form.title&&form.initial_views_count>0&&form.start_time&&form.end_time&&form.share_content)&&(form.picture||picture)'>预览</el-button>
                                <el-button class="myButton_40 btn_width_95" disabled v-else>预览</el-button>
                            </div>
                        </div>
                        <div style='text-align: center'>
                            <el-button class="myButton_40 myBtnHover_red btn_width_200" @click="cancelEv">取消</el-button>
                            <el-button type="danger" class='btn_width_200 myColor_red' @click="submitForm('ruleForm')">发布</el-button>
                        </div>
                    </el-form>
                </el-col>
            </el-row>
        </div>
        <el-dialog title="预览" :visible.sync="dialogVisible">
            <div>
                <h4 class="prev_title">{{form.title}}</h4>
                <p class="prev_time">{{form.start_time}}</p>
                <div id='priv_content'></div>
            </div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">关闭</el-button>
            </div>
        </el-dialog>
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
    .prev_title{font-size:20px}
    .prev_time{font-size:14px}
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
    #info_detail .el-dialog{
        width:400px;height:500px;top:50%;margin-top:-250px!important;border-radius:10px;
    }
    #info_detail .el-dialog__body{
        height:calc(100% - 140px);
        padding:20px;
        background:#000;
        color:#fff;
        border:1px solid #ccc;
    }
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

                showError: false,
                action: `${config.baseUrl}/upload`,
                checkType: 'voteId',
                dateArr: [],
                type:'',//1正文 2 外文
                dialogVisible:false,//是否显示预览
                form: {
                    title: '',
                    sub_title: ' ',
                    initial_views_count: 1,
                    picture: '',
                    picture_change: '',
                    stay_top: 'false',
                    push_news: '',
                    start_time: '',
                    end_time: '',
                    app_content: '',
                    share_content: '',
                },
                picture: '',
                rules: {
                    title    : [{ required: true, message: '请输入主标题', trigger: 'blur' }],
                    sub_title: [{ required: true, message: '请输入副标题', trigger: 'blur' }],
                    picture_change: [
                        { validator: (rule, value, callback) => {
                            if (this.picture === ''&&value==='') {
                                callback(new Error('请选择主题图片'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur', required: true}
                    ],
                    stay_top: [{ required: true, message: '请选择是否置顶', trigger: 'blur' }],
                    start_time: [{ required: true, message: '请输入发送时间', trigger: 'blur' }],
                    end_time: [{ required: true, message: '请输入发送时间', trigger: 'blur' }],
                    // app_content: [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    // share_content: [{ required: true, message: '请输入名称', trigger: 'blur' }],
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
                this.dateArr=[this.query.start_time,this.query.end_time]
                this.form.push_news = this.form.push_news== 'true'?true:false
                this.imgUrl = this.form.picture ;
                console.log(this.form)
            }
        },

        computed: {
           
        },

        methods: {
            getUrl(url,imgId){
                this.changeUrl=false
                this.imgUrl = url;
                console.log(url,imgId)

            },
            addImg(ele,imgId){
                // alert(1)
                this.imgId=imgId;
                console.log($("#inputId2"))
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
            // handleAvatarSuccess(res, file) {
            //     let picUrl = `${config.baseUrl}/${res.urls[res.urls.length-1]}`;
            //     let image = new Image();
            //     image.src = picUrl;
            //     image.onload = () => {
            //         this.picture = picUrl
            //         this.showError = false;
            //         // if (image.width !== 750 || image.height != 340) {
            //         //     this.showErrorTip('请上传符合尺寸的商品详情图');
            //         // }
            //         // else {
            //         //     this.picture = picUrl
            //         //     this.showError = false;
            //         // }
            //     };
            // },

            submitForm(formName) {
                console.log(this.form)
                console.log(this.imgUrl)
                this.$refs[formName].validate((valid) => {
                    if (!this.imgUrl) {
                        this.showError = true;
                        return false;
                    }
                    if (valid) {
                        
                    }
                });
            },

            getDateTime() {
                this.form.start_time = this.dateArr[0];
                this.form.end_time = this.dateArr[1];
            },

            removeImageEv() {
                this.picture = '';
            },

            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            },

            cancelEv() {
                this.$router.push({path: '/infolist'});
            },

            preview(type){
                console.log(this.form)
                this.type = type

                console.log(this.form.app_content)
                console.log(this.form.app_content+'')
                console.log($('#priv_content').html())
                $('#priv_content').html(""+this.form.app_content+"")
                console.log($('#priv_content').html())
                this.dialogVisible = true
                
            },

            onEditorChange(value) {
                // console.log('editor change!', editor, html, text)
                 // console.log(value)
                 this.form.app_content = value ;
            },
            onEditorChangeSub(value) {
                // console.log('editor change!', editor, html, text)
                 // console.log(value)
                 this.form.share_content = value ;
            }

        }
    }
</script>