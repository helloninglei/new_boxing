<template>
	<div id="dialog">
		<el-dialog  :visible.sync="showDialog">
          <div class="dialog_title">{{content_title}}</div>
          <div class="dialog_content" v-if="type==1">
          	<el-input type="textarea" v-model="form.textarea_val"></el-input>
          </div>
          <div class="dialog_content" v-if="type==2" style='margin-top:40px'>
          	<el-checkbox-group v-model="form.class_name">
			    <el-checkbox label="泰拳" name="class_name"></el-checkbox>
			    <el-checkbox label="拳击" name="class_name"></el-checkbox>
			    <el-checkbox label="MMA" name="class_name"></el-checkbox>
			</el-checkbox-group>
          </div>
          <div class="content_foot" v-if="type==1">{{content_foot}}</div>
          <div slot="footer" class="dialog-footer" style='text-align:center'>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="confirm()">确定</el-button>
            <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="close()">取消</el-button>
          </div>
        </el-dialog>
	</div>
</template>
<style>
  #dialog .el-dialog{width:385px; height:294px; margin-top:20vh;}
  .border_raduis_100{border-radius: 100px!important}
  #dialog .el-dialog__body{height:130px; font-family: "PingFang SC";padding:16px 30px 30px 30px;font-size: 16px;color: #000000;}
  #dialog .dialog_content{margin:20px 0;}
  #dialog .el-dialog__footer{padding-bottom:38px;}
  .content_foot{font-size:14px!important;color:#212121;}
  #dialog .el-checkbox,#dialog .el-checkbox__input.is-checked+.el-checkbox__label{font-family: PingFangSC-Regular;font-size: 16px;color: #000000;}
  .el-checkbox__input.is-checked .el-checkbox__inner, .el-checkbox__input.is-indeterminate .el-checkbox__inner{background: #F95862;border-color:#F95862;}
</style>
<script >
    export default {
        data() {
            return {
            	showDialog:false,
              	form :{
              		class_name:[],
              		textarea_val:'',
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
          	type : Number,
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
            	this.$emit('confirm',this.form)
            },
            close(){
              this.$emit('cancel',false)
            },
        },
    }
</script>