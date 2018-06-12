<template>
  <div id="dialog_label">
    <el-dialog  :visible.sync="showDialog">
          <div class="dialog_title">{{content_title}}</div>
          <div class="dialog_content" style='margin-top:40px' v-if="type=='phone'">
            <el-form ref="form1" :model="form1" label-width="70px" :rules="rules1">
              <el-form-item label="手机号" prop="mobile">
                <el-input v-model="form1.mobile" placeholder="请输入注册手机号" ></el-input>
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
                },
                form2 :{
                  balance :'',
                },
                rules1:{
                  mobile: [
                    { validator: validatePhone, trigger: 'blur' }
                  ],
                },
                rules2:{
                  balance: [
                    { validator: validateBalace, trigger: 'blur' }
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
            default:1,
          }
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
              if(this.type=='phone'){
                this.$refs['form1'].resetFields();
              }else{
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