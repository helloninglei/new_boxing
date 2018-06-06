<template>
	<div id="report_content">
		<el-dialog  :visible.sync="showDialog">
        <h3 style='color:#909399'>用户昵称：{{getData.nick_name}}</h3>
        <p class="detail_title text_lf">发布时间：{{getData.created_time}}</p>
        <p style='font-size:14px'>{{getData.content}}</p>
        <div class='imgs' v-if='getData.pictures'>
          <img :src="value" alt="" v-for='value in getData.pictures' width='100%'>
        </div>
        <div class='imgs' v-if='getData.video'>
          <video :src="config.baseUrl+getData.video" controls="controls" width='100%'>
                您的浏览器不支持 video 标签。
          </video>
          <!-- <img :src="value" alt="" v-for='value in getData.pictures' width='100%'> -->
        </div>
      <div slot="footer" class="dialog-footer" style='text-align:center'>
        <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="close()">关闭</el-button>
      </div>
    </el-dialog>
	</div>
</template>
<style scope>
  h3,p{margin-bottom:5px;}
  .imgs{width:100%;}
</style>
<style>
  #report_content .el-dialog{width:385px; height:274px; margin-top:20vh;}
  #report_content .el-dialog__header{padding-top:20px;}
  .border_raduis_100{border-radius: 100px!important}
  #report_content .el-dialog__body{height:156px; font-family: "PingFang SC";padding:0px 30px 30px 30px;font-size: 16px;color: #000000;overflow: auto}
  #report_content .dialog_content{margin:20px 0;}
  #report_content .el-dialog__footer{padding-bottom:38px;}
  .content_foot{font-size:14px!important;color:#212121;}
  #report_content .el-checkbox,#report_content .el-checkbox__input.is-checked+.el-checkbox__label{font-family: PingFangSC-Regular;font-size: 16px;color: #000000;}
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
          getData:{
            type:Object,
          },
        },
        watch:{
        	isshow(newval,oldval){
        		this.showDialog=newval;
        	},
        	showDialog(val){
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
          console.log(this.getData)
        },
        methods: {
            close(){
              this.$emit('cancel',false)
            },
        },
    }
</script>