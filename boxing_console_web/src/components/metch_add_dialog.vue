<template>
  <div id="dialog_label">
    <el-dialog  :visible.sync="showDialog" :title='content_title' class='metchAddDialog clearfix'>
      <div class="dialog_content" style='margin-top:20px'>
        <el-form ref="form" :model="form" label-width="90px" :rules="rules" id='form'>
            <el-form-item label="日期" prop="race_date">
                <el-date-picker
                    v-model="form.race_date"
                    type="date"
                    value-format="yyyy-MM-dd"
                    :default-value= "new Date()"
                    placeholder="请输入日期"
                    style="width: 100%;"
                    >
                    </el-date-picker>
            </el-form-item>
            <el-form-item label="赛事名称" prop="name">
                <el-input v-model="form.name" placeholder="请输入赛事名称" ></el-input>
            </el-form-item>
        </el-form>
      </div>
      <div slot="footer" class="dialog-footer" style='text-align:center'>
        <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="close">取消</el-button>
        <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="addmetch()">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<style lang="stylus" >
  .metchAddDialog .el-dialog{
        width:385px!important;
        height:274px!important;
        font-size:14px;
        color:#606266;
        text-align: center;
        .el-dialog__header{
            .el-dialog__title{
                font-size: 16px!important;
                color: #000;
            }
            padding-bottom: 6px;
            padding-top:22px;
        }
        .el-dialog__body{
          height:124px!important;
          padding:0 20px 4px!important;
        }
    }
</style>
<script >
    export default {
        data() {
          return {
            showDialog:false,
            form :{
              race_date:'',
              name:''
            },
            rules:{
              race_date: [
                { validator: (rule, value, callback) => {
                    var reg=/^[0-9]*$/;
                    if(value==''){
                        callback(new Error('请输入日期'));
                    }else {
                    
                        callback();
                    }
                  }, trigger: 'blur'}
              ],
              name: [
                { validator: (rule, value, callback) => {
                    if(value==''){
                        callback(new Error('请输入赛事名称'));
                    }else{
                    
                        callback();
                    }
                  }, trigger: 'blur'}
              ],
            },
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
          race_date:{
            type : String,
            default:'',
          },
          name:{
            type : String,
            default:"",
          },
          id:{
            default:"",
          },
        },
        watch:{
          isshow(newval,oldval){
            this.showDialog=newval;
            this.form.name = this.name
            this.form.race_date = this.race_date
          },
          showDialog(val){
            if(!val){
              this.$emit('cancel',val)
              this.resetForm();
            }
          },
        },
        components: {
        },
        created() {
          
        },
        methods: {
            addmetch(){
              this.$refs['form'].validate((valid) => {
                  if (valid) {
                    this.confirm1(this.form)
                  } else {
                    console.log('error submit!!');
                    return false;
                  }
                });
            },
            confirm1(data){
                let $this=this;
                // console.log(this.id)
                let url = this.id?'/schedules/'+this.id:'/schedules'
                let type = this.id?'PUT':'POST'
                this.ajax(url,type,data).then((res) => {
                    if(res&&res.data){
                      $this.$emit('confirm',{name:res.data.name,race_date:res.data.race_date}) 
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            this.showErrorTip(errors[key][0])
                        }
                    }
                })
            },
            close(){
              this.resetForm();
              this.$emit('cancel',false)
            },
            resetForm() {
              this.$refs['form'].resetFields();
            },
        },
    }
</script>