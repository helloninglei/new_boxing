<template>
	<div id="confirm">
		<el-dialog  :visible.sync="showDialog">
          <div class="confirm_content">{{content}}</div>
          <div slot="footer" class="dialog-footer" style='text-align:center'>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="confirm()">确定</el-button>
            <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="close()">取消</el-button>
          </div>
        </el-dialog>
	</div>
</template>
<style>
  #confirm .el-dialog{width:385px; height:251px; margin-top:20vh;}
  #confirm .border_raduis_100{border-radius: 100px!important}
  #confirm .el-dialog__body{height:67px; font-family: "PingFang SC"}
  #confirm .confirm_content{font-size: 16px;color: #000000;text-align:center;margin:20px 25px 25px 25px;}
</style>
<script >
    export default {
        data() {
            return {
            	showDialog:false,
              formLabelWidth: '120px' 
            }
        },
        props:{
        	isshow :{
              type : Boolean,
              default:false,
            },
          content:{
            type : String,
            default:"",
          },
          id:{
            type : [String,Number],
            default:"",
          },
          index:{
            type : [String,Number],
            default:"",
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
        },
        components: {
        },
        created() {
        },
        methods: {
            confirm(){
            	this.$emit('confirm',this.id,this.index)
            },
            close(){
              this.$emit('cancel',false)
            },
        },
    }
</script>