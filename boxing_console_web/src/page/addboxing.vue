<template>
    <div id="addBoxing">
        <TopBar v-if="isShowTop" firstTitle_name="拳馆管理" firstTitle_path="/boxinglist" :secondTitle_name="secondTitle_name"></TopBar>
        <div class='container'>
            <el-row> 
                <el-col :span="9">
                    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                        <el-form-item label="拳馆名称" prop="name">
                            <el-input v-model="ruleForm.name"></el-input>
                        </el-form-item>
                        <el-form-item label="宣传图" prop="avatar">
                            <el-row>
                                <Cropper @getUrl='getUrl' :url_f='url_f' :changeUrl='changeUrl' :imgId='imgId' :width='160' :height='90'></Cropper>
                                <div>  
                                    <div class='show' >  
                                      <img :src="src_avatar" alt="" width='100%' id='img1'> 
                                    </div>
                                    <div style="margin-top:63px;float:left;margin-left:20px">  
                                      <el-button type="danger" class='myColor_red myButton_40 btn_width_95' @click="addImg('inputId1','img1',144,144)">上传</el-button>
                                      <input type="file" id="inputId1" style='display:none' accept="image" @change="change">  
                                      <label for="inputId1"></label>  
                                    </div>  

                                </div> 
                            </el-row>
                            <el-input v-model="ruleForm.avatar" type='hidden'></el-input>
                        </el-form-item>
                        <el-form-item label="地址" prop="address">
                            <span style='position:absolute;z-index:1;'><el-button class="button" icon="el-icon-location" circle @click='openMap'></el-button></span>
                            <el-input  v-model="ruleForm.address" class="myAddress"></el-input>
                        </el-form-item>
                        <el-form-item label="电话" prop="phone">
                            <el-input v-model="ruleForm.phone"></el-input>
                        </el-form-item>
                        <el-form-item label="营业时间" prop="startTime">
                            <el-col :span="11">
                                <el-form-item prop="startTime">
                                    <el-time-select
                                    placeholder="营业开始时间"
                                    v-model="ruleForm.startTime"
                                    :picker-options="{
                                      step: '00:15',
                                    }">
                                    </el-time-select>
                                </el-form-item>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                            <el-col :span="11">
                                <el-form-item prop="endTime">
                                    <el-time-select
                                    placeholder="营业结束时间"
                                    v-model="ruleForm.endTime"
                                    :picker-options="{
                                      step: '00:15',
                                      minTime: ruleForm.startTime
                                    }">
                                    </el-time-select>
                                </el-form-item>
                            </el-col>
                            <!-- <el-input v-model="ruleForm.opening_hours"></el-input>
                            <template>
                                  <el-time-select
                                    placeholder="营业开始时间"
                                    v-model="ruleForm.startTime"
                                    :picker-options="{
                                      step: '00:15',
                                    }">
                                  </el-time-select>
                                  <el-time-select
                                    placeholder="营业结束时间"
                                    v-model="ruleForm.endTime"
                                    :picker-options="{
                                      step: '00:15',
                                      minTime: ruleForm.startTime
                                    }">
                                  </el-time-select>
                            </template> -->
                        </el-form-item>
                        <el-form-item label="拳馆简介" prop="introduction">
                            <el-input type="textarea" v-model="ruleForm.introduction" :rows="6" :maxlength='120' placeholder='限制120字'></el-input>
                        </el-form-item>
                        <el-form-item label="展示图" prop="images">
                            <div style='width:200%'>
                                <el-row>
                                    <el-col :span="6">
                                       <div class='show1' @click="addImg('inputId2','img2')">  
                                          <img :src="images['img2']" alt="" width='100%' id='img2' > 
                                        </div>
                                        <div>  
                                          <input type="file" id="inputId2" style='display:none' accept="image" @change="change">  
                                          <label for="inputId2"></label>  
                                        </div> 
                                    </el-col>
                                    <el-col :span="6">
                                        <div class='show1' @click="addImg('inputId3','img3')">  
                                          <img :src="images['img3']" alt="" width='100%' id='img3' > 
                                        </div>
                                        <div>  
                                          <input type="file" id="inputId3" style='display:none' accept="image" @change="change">  
                                          <label for="inputId3"></label>  
                                        </div> 
                                    </el-col>
                                    <el-col :span="6">
                                        <div class='show1' @click="addImg('inputId4','img4')">  
                                          <img :src="images['img4']" alt="" width='100%' id='img4' > 
                                        </div>
                                        <div>  
                                          <input type="file" id="inputId4" style='display:none' accept="image" @change="change">  
                                          <label for="inputId4"></label>  
                                        </div> 
                                    </el-col>
                                    <el-col :span="6">
                                        <div class='show1' @click="addImg('inputId5','img5')">  
                                          <img :src="images['img5']" alt="" width='100%' id='img5' > 
                                        </div>
                                        <div>  
                                          <input type="file" id="inputId5" style='display:none' accept="image" @change="change">  
                                          <label for="inputId5"></label>  
                                        </div> 
                                    </el-col>
                                </el-row>
                                <div class='el-form-item__error'>{{sendErr}}</div>
                            </div>
                        </el-form-item>
                        <el-form-item>
                            <!-- <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button> -->
                             <el-button type="danger" class='myColor_red myButton_40 btn_width_95' @click="submitForm('ruleForm')">提交</el-button>
                             <el-button class='myButton_40 btn_width_95 myBtnHover_red' @click="resetForm('ruleForm')">重置</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>
        </div>
        <el-dialog title="选择地点" :visible.sync="map.isshow">
            <Map @address='getPause' @address_str='getAddressStr'></Map>
            <input type="hidden" id='myAddress_lon'>
            <input type="hidden" id='myAddress_lat'>
            <input type="hidden" id='myAddress'>
            <div slot="footer" class="dialog-footer" style='text-align: center'>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95' @click="getAddress">确定</el-button>
                <el-button class='myButton_40 btn_width_95 myBtnHover_red'  @click="map.isshow = false">取消</el-button>
            </div>
        </el-dialog>
        
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
    #addBoxing .el-dialog__body{padding-top:0px;}
    #addBoxing .el-dialog__header{font-family:"PingFangSC-Regular";
        font-size: 16px;
        color:#000;}
    .image{height:140px;width:140px;border:1px solid #ccc;vertical-align: middle}
    .image img{height:100%;}
    #addBoxing .show {  
      width: 100px;  
      height: 100px;  
      overflow: hidden;  
      position: relative;  
      float:left;
      /*border-radius: 50%;  */
      border: 1px solid #d5d5d5;  
    } 
    #addBoxing .show1 {  
      width: 160px;  
      height: 90px;  
      overflow: hidden;  
      position: relative;  
      /*border-radius: 50%;  */
      border: 1px solid #d5d5d5;
      cursor:pointer;  
    } 
    #addBoxing .el-date-editor.el-input,#addBoxing  .el-date-editor.el-input__inner{
        width:136px;
    }
</style>
<script>
    import TopBar  from 'components/topBar';
    import Cropper from 'components/cropper';
    import Map     from 'components/map';
    export default {
        data() {
            return {
                inputId:'',
                url_f:'',
                changeUrl:false,
                imgId :'',
                cropper_width:0,
                cropper_height:0,
                secondTitle_name:'',
                sendErr:'',//图片的错误提示
                sendErr1:'',//图片的错误提示
                src_avatar:'',//显示的宣传图的半个url
                images:[],
                isadd:true,//是否是添加
                map:{
                    isshow:false
                },
                isShowTop : true,
                ruleForm: {
                    name: '',
                    address: '',
                    phone: '',
                    startTime:'',
                    endTime:'',
                    opening_hours: '',
                    introduction: '',
                    avatar:'',//宣传图url
                    images:[],
                },
                rules:{
                    name:[
                        { required:true, message:'请输入拳馆', trigger:'change' }
                    ],
                    address:[
                        { required:true, message:'请输入拳馆地址', trigger:'blur' },
                    ],
                    phone:[
                        { validator: (rule, value, callback) => {
                            if(!this.phoneReg.test(value)){
                                callback(new Error('请输入合法的手机号'));
                            }else {
                                callback();
                            }
                        }, trigger: 'blur' ,required:true}
                    ],
                    startTime:[
                        { required:true, message:'请选择营业开始时间', trigger:'change' }
                    ],
                    endTime:[
                        { required:true, message:'请选择营业结束时间', trigger:'change' }
                    ],
                    avatar:[
                        { required:true, message:'请选择宣传图', trigger:'change' }
                    ],
                    introduction:[
                        { required:true, message:'请输入拳馆简介', trigger:'blur' }
                    ],
                    images:[
                        { validator: (rule, value, callback) => {
                            if(!($('#img2').attr('src')&&$('#img3').attr('src')&&$('#img4').attr('src')&&$('#img5').attr('src'))){
                                this.sendErr='请选择4张展示图'
                            }else{
                                callback();
                            }
                        }, trigger: 'blur' ,required:true}
                    ],
                }
                
            }
        },
        components: {
            TopBar,
            Cropper,
            Map
        },
        created() {
            let query = this.$route.query
            if(query.id){
                //编辑
                this.isadd=false;
                this.clubId=query.id;
                this.secondTitle_name = '修改拳馆'
                this.ruleForm.address = query.address;
                this.ruleForm.longitude = query.longitude;
                this.ruleForm.latitude = query.latitude;
                this.ruleForm.avatar = query.avatar;
                this.ruleForm.name = query.name;
                this.ruleForm.phone = query.phone
                this.ruleForm.startTime = query.opening_hours.split(/[-]+/)[0]
                this.ruleForm.endTime = query.opening_hours.split(/[-]+/)[1]
                this.ruleForm.introduction = query.introduction;
                this.src_avatar = this.config.baseUrl+query.avatar
                this.images['img2'] = this.config.baseUrl+query.images[0]
                this.images['img3'] = this.config.baseUrl+query.images[1]
                this.images['img4'] = this.config.baseUrl+query.images[2]
                this.images['img5'] = this.config.baseUrl+query.images[3]
                // console.log(this.config.baseUrl)
                // console.log(query.avatar)
                // console.log(this.config.baseUrl+query.avatar)

            }else{
                this.isadd=true
                this.secondTitle_name = '添加拳馆'
            }
        },
        methods: {
            getUrl(url,imgId){
                this.changeUrl=false
                
                if(imgId=='img1'){
                    this.src_avatar = this.config.baseUrl+url
                    this.ruleForm.avatar = url
                }else{
                    this.images[imgId]=this.config.baseUrl+url
                }

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
            getAddress(){
                // console.log($('#myAddress').val())
                this.ruleForm.address=$('#myAddress').val();
                this.ruleForm.longitude = $('#myAddress_lon').val();
                this.ruleForm.latitude = $('#myAddress_lat').val();
                if(!$('#myAddress').val()){
                   
                   this.$message({
                        message: '请输入具体地址',
                        type: 'error'
                    }); 
                }else if(!$('#myAddress_lat').val()){
                   this.$message({
                        message: '请点击地图地点获取经纬度',
                        type: 'error'
                    }); 
                }else{
                    this.map.isshow = false
                }
            },
            getPause(lng, lat,address){
                // console.log(lng, lat)
                $('#myAddress_lon').val(lng);
                $('#myAddress_lat').val(lat);
            },
            getAddressStr(address){
                // console.log(address)
                $('#myAddress').val(address)
            },
            openMap(){
                this.map.isshow=true;
            },
            submitForm(formName) {
                let $this = this
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        this.ruleForm.opening_hours = this.ruleForm.startTime + '--' + this.ruleForm.endTime
                        // console.log(this.ruleForm)
                        if(!($('#img2').attr('src')&&$('#img3').attr('src')&&$('#img4').attr('src')&&$('#img5').attr('src'))){
                            this.sendErr='请选择4张展示图'
                            return;
                        }else{
                            this.sendErr='';
                            this.ruleForm.images[0] = $('#img2').attr('src').split(this.config.baseUrl)[1];
                            this.ruleForm.images[1] = $('#img3').attr('src').split(this.config.baseUrl)[1];
                            this.ruleForm.images[2] = $('#img4').attr('src').split(this.config.baseUrl)[1];
                            this.ruleForm.images[3] = $('#img5').attr('src').split(this.config.baseUrl)[1];
                        }
                        if(this.isadd){
                            this.ajax('/club','post',this.ruleForm).then(function(res){
                            if(res&&res.data){
                                
                                console.log(res.data)
                                $this.$router.push({path: '/boxinglist'});
                                $this.$refs[formName].resetFields();
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
                        }else{
                            this.ajax('/club/'+this.clubId,'put',this.ruleForm).then(function(res){
                                if(res&&res.data){
                                    console.log(res.data)
                                    $this.$router.push({path: '/boxinglist'});
                                    $this.$refs[formName].resetFields();
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
                        }
                        
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            }
        },
    }
</script>