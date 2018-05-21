<template>
  <div id="weight_range">
    <el-dialog  :visible.sync="showDialog">
          <div class="dialog_title">{{content_title}}</div>
          <div class="dialog_content" style='margin-top:0px'>
            <el-form ref="form" :model="form" label-width="76px">
              <el-form-item label="最小体重" >
                <el-input v-model="form.min_weight" placeholder="请输入" ></el-input>
              </el-form-item>
              <el-form-item label="最大体重" >
                <el-input v-model="form.max_weight" placeholder="请输入" ></el-input>
              </el-form-item>
              <el-form-item label="性别" >
                <el-checkbox-group v-model="form.gender">
                    <el-checkbox label="男" name="gender" style='margin-left:0px'></el-checkbox>
                    <el-checkbox label="女" name="gender"></el-checkbox>
                </el-checkbox-group>
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
  #weight_range .el-dialog{width:385px; height:294px; margin-top:20vh;}
  .border_raduis_100{border-radius: 100px!important}
  #weight_range .el-dialog__body{height:147px; font-family: "PingFang SC";padding:0px 30px 30px 30px;font-size: 16px;color: #000000;}
  #weight_range .dialog_content{margin:20px 0;}
  #weight_range .el-dialog__footer{padding-bottom:38px;}
  #weight_range .el-input__inner, .el-form-item__label{height: 40px!important;line-height: 40px!important;font-size:16px!important;padding-left:0px}
  #weight_range .el-input__inner{padding-left:10px}
  .el-dialog__headerbtn{display: none}
</style>
<script >
    export default {
        data() {
            return {
              showDialog:false,
                form :{
                  min_weight:'',
                  max_weight:'',
                  gender :[],
                }
            }
        },
        props:{
          isshow :{
              type : Boolean,
              default:false,
            },
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