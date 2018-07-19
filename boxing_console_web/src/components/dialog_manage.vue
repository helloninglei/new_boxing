<template>
  <div id="dialog_manage">
    <el-dialog  :visible.sync="showDialog">
          <div class="dialog_content" style='margin-top:10px'>
            <el-form ref="form3" :model="form3" label-width="97px" :rules="rules3">
              <el-form-item label="用户昵称" prop="forward_num">
                {{nick_name}}
              </el-form-item>
              <el-form-item label="增加余额" prop="change_amount">
                <el-input v-model="form3.change_amount" placeholder="请输入" type='number'></el-input>
              </el-form-item>
              <el-form-item label="用户类别" prop="user_type" v-if='row.user_type=="拳手"'>
                拳手
              </el-form-item>
              <el-form-item label="用户类别" prop="user_type" v-else>
                <el-radio-group v-model="form3.user_type">
                  <el-radio label="名人" name="user_type">名人</el-radio>
                  <el-radio label="自媒体" name="user_type">自媒体</el-radio>
                  <el-radio label="普通用户" name="user_type">普通用户</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="认证称号" prop="title" v-if='form3.user_type!=="普通用户"'>
                <el-input v-model="form3.title" placeholder="请输入" :maxlength="16"></el-input>
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
  #dialog_manage .el-dialog{width:385px; height:352px; margin-top:20vh;}
  #dialog_manage .el-dialog__header{padding:1px 20px 0px;}
  .border_raduis_100{border-radius: 100px!important}
  #dialog_manage .el-dialog__body{height:230px; font-family: "PingFang SC";padding:16px 30px 30px 15px;font-size: 16px;color: #000000;}
  #dialog_manage .dialog_content{margin:20px 0;}
  #dialog_manage .el-dialog__footer{padding-bottom:38px;}
  #dialog_manage .el-input__inner, .el-form-item__label{height: 40px!important;line-height: 40px!important;font-size:16px!important;padding-left:0px;color:#000;}
  #dialog_manage .el-input__inner{padding-left:10px}
  /*#dialog_manage .el-radio{margin-top:13px;}*/
  #dialog_manage .el-radio+.el-radio{margin-left:20px;}
  #dialog_manage .el-radio__label{color:#000!important;}
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
                form3:{
                  change_amount:0,
                  title:'',
                  user_type:'拳手',
                },
                rules3:{
                  change_amount: [
                    { validator: (rule, value, callback) => {
                        if(value===''){
                            callback(new Error('请输入钱包余额'));
                        }else if (value<0) {
                            callback(new Error('请输入正数'));
                        } else {
                            callback();
                        }
                      }, trigger: 'blur'}
                  ],
                  user_type: [
                    { validator: (rule, value, callback) => {
                        if(this.row.user_type=='拳手'){
                            callback();
                        }
                        else if(value==''){
                            callback(new Error('请选择身份'));
                        }else {
                        
                            callback();
                        }
                      }, trigger: 'blur'}
                  ],
                  title: [
                    { validator: (rule, value, callback) => {
                      if(this.row.user_type=='普通用户'){
                            callback();
                        }
                        else if(value==''){
                            callback(new Error('请输入认证称号'));
                        }else {
                        
                            callback();
                        }
                      }, trigger: 'blur'}
                  ],
                }
            }
        },
        props:{
          isshow :{
              type : Boolean,
              default:false,
            },
          nick_name:{
            type : String,
            default:"",
          },
          row:{
            type : Object,
            default:function(row){
              console.log(row)
              return row
            }
          },
          index:{
            type:[Number,String],
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
          row(row){
            if(row&&row.id){
              // this.form3.change_amount = row.money_balance
              this.form3.title = row.title
              this.form3.user_type = row.user_type
            }
          },
          "form3.user_type"(val){
            console.log(val)
          }

        },
        components: {
        },
        created() {
          
        },
        methods: {
            confirm(){
              let sendData={
                row:this.row,
                index:this.index,
              }
              let $this = this
              this.$refs['form3'].validate((valid) => {
                  if (valid) {
                    if(this.form3.user_type=='普通用户'){
                      delete this.form3.title
                    }
                      this.ajax('/edit_user/'+this.row.id,'put',this.form3).then(function(res){
                          if(res&&res.data){
                            console.log(res.data)
                              sendData.row.title = res.data.title
                              sendData.row.user_type = res.data.user_type
                              sendData.row.money_balance = res.data.money_balance
                              $this.$emit('confirm')
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
                    
                  } else {
                    console.log('error submit!!');
                    return false;
                  }
                });
              
            },
            resetForm(form) {
              this.$refs['form3'].resetFields();
            },
            close(){
              this.resetForm();
              this.$emit('cancel',false)
            },
        },
    }
</script>