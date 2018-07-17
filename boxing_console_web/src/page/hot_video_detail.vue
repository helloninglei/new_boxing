<template>
    <div id="addHotvideo">
        <TopBar v-if="isShowTop" firstTitle_name="视频管理" firstTitle_path="/hotvideo" :secondTitle_name="secondTitle_name" ></TopBar>
        <div class='container'>
            <el-row> 
                <el-col :span="12">
                    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
                        <el-form-item label="视频名称" prop="name">
                            <el-input v-model="ruleForm.name"  :maxlength="40" placeholder='限制40字数'></el-input>
                        </el-form-item>
                        <el-form-item label="视频介绍" prop="description">
                            <el-input type="textarea" v-model="ruleForm.description" :rows="6" placeholder='限制140字数'></el-input>
                        </el-form-item>
                        <el-form-item label="付费金额" prop="price_int">
                            <el-input v-model="ruleForm.price_int" :span="5" placeholder="付费金额为自然数" type='number'></el-input>
                        </el-form-item>
                        <el-form-item label="完整视频" prop="tsurl">
                            <el-button class='myButton_40 btn_width_95 myBtnHover_red'  @click="addFullVideo()" v-if="!(tsurl)">添加视频</el-button>
                            <p v-if="(tsurl)">
                                <span class='video_name'>{{tsurl}} </span>
                                <span ><i class="el-icon-error" style='cursor:pointer' @click='deleteUrl(1)'></i></span>
                            </p>
                            <el-progress type="circle" :percentage="tsurlProgress" :width='70' style='position:absolute;right:-69px;top:-14px' v-show='tsurlProgress>0&&tsurlProgress<100'></el-progress>
                            <el-input v-model="ruleForm.tsurl" type='file' id='full_video' @change='getFullVideo' style='display: none'></el-input>
                        </el-form-item>
                        <el-form-item label="不完整视频" prop="try_ts_url">
                            <el-button class='myButton_40 btn_width_95 myBtnHover_red' @click="addLittleVideo()" v-if="!(try_ts_url)">添加视频</el-button>
                            <p v-if="(try_ts_url)">
                                <span class='video_name'>{{try_ts_url}}</span> 
                                <span ><i class="el-icon-error" style='cursor:pointer' @click='deleteUrl(2)'></i></span>
                            </p>
                            <el-progress type="circle" :percentage="tryTsurlProgress" :width='70' style='position:absolute;right:-69px;top:-14px' v-show='tryTsurlProgress>0&&tryTsurlProgress<100'></el-progress>
                            <el-input v-model="ruleForm.try_ts_url" type='file' id='little_video' @change='getLittleVideo' style='display: none'></el-input>
                        </el-form-item>
                        <el-form-item label="视频封面" prop="avatar">
                            <el-row>
                                <Cropper @getUrl='getUrl' :url_f='url_f' :changeUrl='changeUrl' :imgId='imgId' :width='750' :height='400'></Cropper>
                                <div>  
                                      <div class='showImg' @click="addImg('inputId3','src_avatar')">  
                                      <img :src="src_avatar" alt="" width='100%' id='src_avatar'> 
                                      <div class='noImg' v-if="!src_avatar"> 
                                          <p>添加视频封面</p>
                                          <p>750*400</p>
                                      </div>
                                    </div>
                                    <div style="margin-top:63px;float:left;margin-left:20px">  
                                      <input type="file" id="inputId3" style='display:none' accept="image" @change="change">  
                                      <label for="inputId1"></label>  
                                    </div>  

                                </div> 
                            </el-row>
                            <el-input v-model="ruleForm.avatar" type='hidden'></el-input>
                        </el-form-item>
                        <el-form-item label="关联用户">
                            <ul>
                                <li class='lf'>
                                    <p style='border-radius: 50%;width:50px;height:50px;overflow: hidden;margin-left:15px;cursor: pointer' @click='showChangeUser=true'>
                                        <img :src="'./static/img/edit_user_img.png'" alt="" width="100%">
                                    </p>
                                    <p style='text-align: center'>编辑关联用户</p>
                                </li>
                                <li class='lf' v-for="item in userImgIds" style='width:80px'>
                                    <p style='border-radius: 50%;overflow: hidden;width:50px;height:50px;margin-left:15px'>
                                        <img :src="config.baseUrl+item.avatar" alt="" width="100%">
                                        <!-- <img src="/static/img/edit_user_img.png" alt="" width="100%"> -->
                                    </p>
                                    <p style='text-align: center'>{{item.nick_name}}</p>
                                </li>
                            </ul>
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
        <el-dialog  :visible.sync="showChangeUser" class='myDialog' title="编辑关联用户">
          <!-- <div class="dialog_title">编辑关联用户</div> -->
          <div class="dialog_content myUser" >
            <template>
              <el-transfer 
                filterable
                :filter-method="filterMethod"
                filter-placeholder="请输入用户名称"
                :titles="['待选择', '已选择']"
                :props="{
                  key: 'id',
                  label: 'nick_name',

                }"
                v-model="ruleForm.users" 
                :data="userIds"></el-transfer>
            </template>
          </div>
          <div slot="footer" class="dialog-footer" style='text-align:center'>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="confirm()">确定</el-button>
            <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="close()">取消</el-button>
          </div>
        </el-dialog>

    </div>
</template>

<style>
    #addHotvideo .el-form-item__label{
        font-family: "PingFangSC-Regular";
        font-size: 16px;
        color: #000000;
    }
    #addHotvideo .el-form-item{margin-bottom:30px;}
    #addHotvideo .button{height:37px;width:45px;border:none;border-right:1px solid #ccc;margin-top:2px;margin-left:2px!important;font-size:20px;padding-top:8px;padding-left:12px;}
    #addHotvideo .myAddress input{padding-left:50px;}
    .el-checkbox__inner:hover,.el-checkbox__input.is-focus .el-checkbox__inner,.el-input__inner:focus{
        border-color:#F95862!important;
    }
    .el-checkbox__input.is-checked+.el-checkbox__label{
        color:#F95862!important;
    }
    .el-transfer-panel__item.el-checkbox {
        color: #606266;
    }
</style>
<style scope>
    .myDialog .el-dialog{position:fixed;left:50%;margin-left:-302px;width:604px;}
    .myUser .el-checkbox:first-child{margin-left:0px!important;}
    .myDialog .el-dialog__body{padding-top:10px;}
    .image{height:140px;width:140px;border:1px solid #ccc;vertical-align: middle}
    .image img{height:100%;}
    .myUser .el-button--primary{
        background:#F95862!important;
        border-color:#F95862!important;
    }
    .video_name{
        width:90%;
        display: inline-block;
        vertical-align: middle;
        margin-right:20px;
        white-space:nowrap;
        overflow:auto;
        /*text-overflow:ellipse;*/
    }
    .showImg{
        width:188px;
        height:100px;
        overflow: hidden;
        position: relative;
        float: left;
        /* border-radius: 50%; */
        border: 1px solid #d5d5d5;
    }
    .noImg{
        text-align: center;
        font-size: 14px;
        line-height: 25px;
        margin:-17px auto;
    }
</style>
<script>
    import TopBar from 'components/topBar';
    import $      from 'jquery' 
    import Cropper from 'components/cropper';
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
                userIds     : [],
                userHash    : [],
                userImgIds  : [
                    
                ],
                tryTsurlProgress:0,
                tsurlProgress:0,
                showChangeUser:false,
                ruleForm: {
                    users   : [],
                    name    : '',
                    description: '',
                    price_int  : '',
                    price   : '',
                    tsurl   :'',
                    try_ts_url: '',
                },
                rules:{
                    users:[
                        { required:true,message:'请选择用户id', trigger:'blur' }
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
                },
                inputId:'',
                url_f:'',
                changeUrl:false,
                imgId :'',
                src_avatar:'',
            }
        },
        components: {
            TopBar,
            Cropper
        },
        created() {
            let query     = this.$route.query
            this.id = query.id
            if(this.id){
                this.secondTitle_name = '修改视频'
                this.btn_name = '修改'
                this.getData(this.id)
                let tsurl = query.url
                this.tsurl=query.url
                let try_ts_url = query.try_url
                this.try_ts_url= query.try_url
                $('#full_video').val(tsurl) 
                $('#little_video').val(try_ts_url) 
            }
            
            this.getUserIds();
            
        },
        methods: {
            getFullVideo(){
                var _this=this
                var file=event.target.files;
                var $this=this
                this.upload(file[0],function(url){
                    $this.tsurl = url
                },2);
            },
            getUserIds(){
                let $this = this;
                this.ajax('/hot_videos/users','get').then(function(res){
                    if(res&&res.data){
                        res.data.forEach((val, index) => {
                          $this.userHash[val.id]=val
                        });
                        $this.userIds = res.data
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
            getData(id){
                let $this = this;
                this.ajax('/hot_videos/'+id,'get').then(function(res){
                    if(res&&res.data){
                        $this.ruleForm.name    = res.data.name;
                        $this.ruleForm.price_int   = parseInt(res.data.price);
                        $this.ruleForm.description = res.data.description;
                        $this.ruleForm.cover = res.data.cover;
                        $this.userImgIds = res.data.user_list;
                        for(var i=0;i<$this.userImgIds.length;i++){
                            $this.ruleForm.users.push($this.userImgIds[i].id)
                        }
                        $this.src_avatar = $this.config.baseUrl + res.data.cover;
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
            filterMethod(query, item){
                return item.nick_name.indexOf(query) > -1;

            },
            getLittleVideo(){
                var _this=this
                var file=event.target.files;
                var $this=this
                this.upload(file[0],function(url){
                    $this.try_ts_url = url
                },1);
            },
            upload(file,fun,type){
                // console.log(file)
                let formData = new FormData() 
                let $this = this;
                formData.append('file', file) 
                this.ajax('/upload','post',formData,{},{},function(val){
                    if(type==1){
                        $this.tryTsurlProgress = parseFloat(val)
                    }
                    if(type==2){
                        $this.tsurlProgress = parseFloat(val)
                    }
                    
                }).then(function(res){
                    if(res&&res.data){
                        fun(res.data.urls[res.data.urls.length-1])
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
            close(){
                this.showChangeUser = false;
            },
            confirm(){
                this.showChangeUser = false;
                // console.log(this.ruleForm.users)
                let userImgIds = []
                for(var i=0;i<this.ruleForm.users.length;i++){
                    userImgIds.push(this.userHash[this.ruleForm.users[i]])
                }
                this.userImgIds = userImgIds
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
            //宣传图
            getUrl(url,imgId){
                this.changeUrl=false
                // this.src_avatar = this.config.baseUrl+url
                this.ruleForm.cover = url
            },
            addImg(ele,imgId){
                this.imgId=imgId;
                $("#"+ele).click();
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
        },
    }
</script>
