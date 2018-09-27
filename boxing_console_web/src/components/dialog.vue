<template>
	<div id="dialog">
		<el-dialog  :visible.sync="showDialog">
          <div class="dialog_title">{{content_title}}</div>
          <div class="dialog_content" v-if="type==1">
          	<el-input type="textarea" v-model="form.textarea_val" :rows='5' :maxlength='100' placeholder="请输入（最多100个字符）"></el-input>
            <div class="el-form-item__error">{{errorTxt}}</div>
          </div>
          <div class="dialog_content" v-if="type==2" style='margin-top:40px'>
          	<el-checkbox-group v-model="form.class_name">
      			    <el-checkbox label="自由搏击" name="class_name">自由搏击</el-checkbox>
      			    <el-checkbox label="拳击" name="class_name">拳击</el-checkbox>
      			    <el-checkbox label="MMA" name="class_name">MMA</el-checkbox>
      			</el-checkbox-group>
            <el-form ref="form" :model="form" label-width="80px" v-if='showIndenTitle'>
              <el-form-item label="认证称号" class='mytitle'>
                <el-input v-model="form.title" placeholder="请输入" ></el-input>
              </el-form-item>
            </el-form>
            <div class="el-form-item__error">{{errorTxt}}</div>
          </div>
          <div slot="footer" class="dialog-footer" style='text-align:center'>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="confirm()">确定</el-button>
            <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="close()">取消</el-button>
          </div>
        </el-dialog>
	</div>
</template>
<style>
  #dialog .el-dialog{width:385px; height:294px; margin-top:20vh;}
  .border_raduis_100{border-radius: 140px!important}
  #dialog .el-dialog__body{height:145px; font-family: "PingFang SC";padding:16px 30px 30px 30px;font-size: 16px;color: #000000;}
  #dialog .dialog_content{margin:20px 0; position:relative;}
  #dialog .el-dialog__footer{padding-bottom:38px;}
  /*.content_foot{font-size:14px!important;color:#F95862;}*/
  #dialog .el-checkbox,#dialog .el-checkbox__input.is-checked+.el-checkbox__label{font-family: PingFangSC-Regular;font-size: 16px;color: #000000;}
  .el-checkbox__input.is-checked .el-checkbox__inner, .el-checkbox__input.is-indeterminate .el-checkbox__inner{background: #F95862;border-color:#F95862;}
  .mytitle{
    margin-top:20px;
  }
  .mytitle .el-form-item__label {
    font-family: "PingFang SC";
    color:#000;
  }
</style>
<script >
    export default {
        data() {
            return {
            	showDialog:false,
              	form :{
              		class_name:[],
              		textarea_val:'',
                  title:''
              	},
                errorTxt:'',
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
          	type : Number,
            default:1,
          },
          showIndenTitle:{
            type : Boolean,
            default:false,
          },
          title:{
            type : String,
            default:"",
          }
        },
        watch:{
        	isshow(newval,oldval){
        		this.showDialog=newval;
        	},
        	showDialog(val){
          	// console.log(val)
            if(!val){
              this.$emit('cancel',val)
              this.form.textarea_val = '';
            }
        	},
        	'showIndenTitle'(val){
        		// console.log(val)
        	},
          title(val){
            this.form.title = val
          }

        },
        components: {
        },
        created() {
        },
        methods: {
            confirm(){
              if(this.type==1){
                if(!this.form.textarea_val){
                  this.errorTxt = '请输入驳回原因'
                  return;
                }else{
                  this.errorTxt = '';
                }
              }else{
                if(this.form.class_name.length==0){
                  this.errorTxt = '请至少选择一个课程'
                  return;
                }else if(this.showIndenTitle&&this.form.title==''){
                  this.errorTxt = '请填写认证称号';
                  return;
                }else{
                  this.errorTxt = '';
                }
              }
            	this.$emit('confirm',this.form)
            },
            close(){
              this.form ={
                  class_name:[],
                  textarea_val:'',
                  title:''
                }
              this.$emit('cancel',false)
            },
        },
    }
</script>