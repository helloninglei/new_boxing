<template>
  <div id="dialog_label">
    <el-dialog  :visible.sync="showDialog">
          <div class="dialog_title">{{content_title}}</div>
          <div class="dialog_content" style='margin-top:40px' v-if="type=='phone'">
            <el-form ref="form" :model="form" label-width="70px">
              <el-form-item label="手机号" >
                <el-input v-model="form.mobile" placeholder="请输入注册手机号" ></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div class="dialog_content" style='margin-top:20px' v-else>
            <el-form ref="form" :model="form" label-width="70px">
              <el-input v-model="form.balance" placeholder="整数，不能为负"></el-input>
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
            return {
              showDialog:false,
                form :{
                  mobile:'',
                  balance :'',
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
              console.log(val)
              if(!val){
                this.$emit('cancel',val)
              }
            },
            'form.class_name'(val){
              console.log(val)
            }

        },
        components: {
        },
        created() {
        },
        methods: {
            confirm(){
              this.$emit('confirm')
            },
            close(){
              this.$emit('cancel',false)
            },
        },
    }
</script>