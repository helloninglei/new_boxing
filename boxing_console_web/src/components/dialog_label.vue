<template>
  <div id="dialog_label">
    <el-dialog  :visible.sync="showDialog">
          <div class="dialog_title">{{content_title}}</div>
          <div class="dialog_content" style='margin-top:40px' v-if="type=='phone'||type=='sensitive'">
            <el-form ref="form1" :model="form1" label-width="70px" :rules="rules1">
              <el-form-item label="手机号" prop="mobile" v-if="type=='phone'">
                <el-input v-model="form1.mobile" placeholder="请输入注册手机号" ></el-input>
              </el-form-item>
              <el-form-item label="敏感词" prop="sensitive" v-if="type=='sensitive'">
                <el-input v-model="form1.sensitive" placeholder="请输入敏感词" ></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div class="dialog_content" style='margin-top:20px' v-else-if="type=='forward'">
            <el-form ref="form3" :model="form3" label-width="105px" :rules="rules3">
              <el-form-item label="初始转发量" prop="forward_num">
                <el-input v-model="form3.forward_num" placeholder="请输入" ></el-input>
              </el-form-item>
              <el-form-item label="初始点赞数" prop="thumbs_up_num">
                <el-input v-model="form3.thumbs_up_num" placeholder="请输入" ></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div class="dialog_content" style='margin-top:20px' v-else>
            <el-form ref="form2" :model="form2" label-width="70px" :rules="rules2">
              <el-form-item  prop="balance" label-width="0px">
                <el-input v-model="form2.balance" placeholder="整数，不能为负"></el-input>
              </el-form-item>
              
            </el-form>
          </div>
          <div slot="footer" class="dialog-footer" style='text-align:center'>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="confirm()">确定</el-button>
            <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="close()">取消</el-button>
          </div>
        </el-dialog>
  </div>
</template>
<style>
  #dialog_label .el-dialog{width:385px; height:294px; margin-top:20vh;}
  .border_raduis_100{border-radius: 100px!important}
  #dialog_label .el-dialog__body{height:130px; font-family: "PingFang SC";padding:16px 30px 30px 30px;font-size: 16px;color: #000000;}
  #dialog_label .dialog_content{margin:20px 0;}
  #dialog_label .el-dialog__footer{padding-bottom:38px;}
  #dialog_label .el-input__inner, .el-form-item__label{height: 40px!important;line-height: 40px!important;font-size:16px!important;padding-left:0px}
  #dialog_label .el-input__inner{padding-left:10px}
</style>
<script >
    export default {
        data() {
            var validatePhone = (rule, value, callback) => {
              if(this.type=='sensitive'){
                callback();
              }else
              if (value === '') {
                callback(new Error('请输入手机号'));
              } else {
                var reg=this.phoneReg;
                if (!reg.test(value) ){
                  callback(new Error('请输入合法的手机号'));
                }
                callback();
              }
            };
            var validateSensitive = (rule, value, callback) => {
              if(this.type=='phone'){
                callback();
              }else
              if (value === '') {
                callback(new Error('请输入敏感词'));
              } else {
                callback();
              }
            };
            var validateBalace = (rule, value, callback) => {
              if (value === '') {
                callback(new Error('请输入数字'));
              } else {
                var reg=/^[0-9]*$/;
                if (!reg.test(value) ){
                  callback(new Error('请输入数字'));
                }
                callback();
              }
            };
            return {
              showDialog:false,
                form1 :{
                  mobile:'',
                  sensitive:''
                },
                form2 :{
                  balance :'',
                },
                form3:{
                  forward_num:'',
                  thumbs_up_num:'',
                },
                rules1:{
                  mobile: [
                    { validator: validatePhone, trigger: 'blur' }
                  ],
                  sensitive: [
                    { validator: validateSensitive, trigger: 'blur' }
                  ],
                },
                rules2:{
                  balance: [
                    { validator: validateBalace, trigger: 'blur' }
                  ],
                },
                rules3:{
                  forward_num: [
                    { validator: (rule, value, callback) => {
                        var reg=/^[0-9]*$/;
                        if(value==''){
                            callback(new Error('请输入初始阅读量'));
                        }else if (!reg.test(value)) {
                            callback(new Error('请输入数字'));
                        } else {
                        
                            callback();
                        }
                      }, trigger: 'blur' ,required:true}
                  ],
                  thumbs_up_num: [
                    { validator: (rule, value, callback) => {
                        var reg=/^[0-9]*$/;
                        if(value==''){
                            callback(new Error('请输入初始点赞数'));
                        }else if (!reg.test(value)) {
                            callback(new Error('请输入数字'));
                        } else {
                        
                            callback();
                        }
                      }, trigger: 'blur' ,required:true}
                  ],
                }
            }
        },
        props:{
          isshow :{
              type : Boolean,
              default:false,
            },
          content_title:{
            type : String,
            default:"",
          },
          content_foot:{
            type : String,
            default:"",
          },
          type:{
            type : String,
            default:'',
          },
          sensitive_name:{
            type : String,
            default:"",
          },
        },
        watch:{
          isshow(newval,oldval){
            this.showDialog=newval;
          },
          showDialog(val){
            if(!val){
              this.$emit('cancel',val)
              this.resetForm();
            }
          },
          'form.class_name'(val){
            // console.log(val)
          },
          sensitive_name(val){
            this.form1.sensitive = val
          }

        },
        components: {
        },
        created() {
        },
        methods: {
            confirm(){
              if(this.type=='phone'){
                //手机号
                this.$refs['form1'].validate((valid) => {
                  if (valid) {
                    // console.log(this.form1.mobile)
                    this.$emit('confirm',this.form1.mobile)
                  } else {
                    // console.log('error submit!!');
                    return false;
                  }
                });
              }else if(this.type=='sensitive'){
                this.$refs['form1'].validate((valid) => {
                  if (valid) {
                    this.$emit('confirm',this.form1.sensitive)
                  } else {
                    console.log('error submit!!');
                    return false;
                  }
                });
              }else if(this.type=='forward'){
                this.$refs['form3'].validate((valid) => {
                  if (valid) {
                    this.$emit('confirm',this.form3)
                  } else {
                    console.log('error submit!!');
                    return false;
                  }
                });
              }else{
                this.$refs['form2'].validate((valid) => {
                  if (valid) {
                    this.$emit('confirm',this.form2.balance)
                  } else {
                    console.log('error submit!!');
                    return false;
                  }
                });
              }
              
            },
            resetForm(form) {
              if(this.type=='phone'||this.type=='sensitive'){
                this.$refs['form1'].resetFields();
              }else if(this.type=='forward'){
                this.$refs['form3'].resetFields();
              } else{
                this.$refs['form2'].resetFields();
              } 
            },
            close(){
              this.resetForm();
              this.$emit('cancel',false)
            },
        },
    }
</script>