<template>
    <div class="banner_manage" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/infolist" secondTitle_name="赛程管理"></TopBar>
        <div class="container">
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_bt20' @click.native="addMatchEv">添加赛程</el-button>
            <template>
                <el-table
                        :data="tableData"
                        style="width: 100%">
                    <el-table-column
                            prop="race_date"
                            label="比赛日期">
                    </el-table-column>
                    <el-table-column
                            prop="name"
                            label="名称">
                    </el-table-column>
                    <el-table-column
                            prop="status"
                            label="状态">
                    </el-table-column>
                    <el-table-column label="操作" width='220'>
                        <template slot-scope="scope">
                            <el-button
                                    size="mini"
                                    @click="handleEdit(scope.$index, scope.row)">详情</el-button>
                            <el-button
                                    size="mini"
                                    @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                            <el-button
                                    size="mini"
                                    type="danger"
                                    @click="changeShow(scope.row,scope.$index)">{{scope.row.status=="已发布"?"隐藏":"发布"}}</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </template>
            <footer>
                <Pagination :total="total" @changePage="changePage" :page="page"></Pagination>
            </footer>
        </div>
        <Confirm :isshow="confirmData.isshow" @confirm="conform1" @cancel="cancel1()" :content="confirmData.content" :id='confirmData.id' :index='confirmData.index'></Confirm>
        <el-dialog  :visible.sync="addDialog.isshow" title='添加赛程' class='metchAddDialog clearfix'>
          <div class="dialog_content" style='margin-top:20px'>
            <el-form ref="form" :model="form" label-width="90px" :rules="rules" id='form'>
                <el-form-item label="日期" prop="race_date">
                    <!-- <el-input v-model="form.race_date" placeholder="请输入日期" ></el-input> -->
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
            <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="addDialog.isshow = false">取消</el-button>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="addmetch()">保存</el-button>
          </div>
        </el-dialog>
    </div>
</template>

<style lang="stylus">
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
            padding:0 20px 4px;
        }
    }
    
</style>

<script >
    import TopBar from 'components/topBar';
    import Pagination  from 'components/pagination';
    import Confirm from "components/confirm"
    export default {
        data() {
            return {
                isShowTop: true,
                search: '',
                total: 1,
                page: 1,
                dateArr: [],
                start_date: '',
                end_date: '',
                stay_top: '',
                hasSearch: false,
                tableData: [
                    {
                        "name": "世界职业拳击比赛",
                        "race_date": "2018-10-21",
                        "id": 2,
                        "status": "已发布"
                    },
                    {
                        "name": "终极格斗冠军赛",
                        "race_date": "2018-09-21",
                        "id": 1,
                        "status": "未发布"
                    }
                ],
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'删除后不可恢复，是否确认删除？'
                },
                addDialog:{
                    isshow:false
                },
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
        components: {
            TopBar,
            Pagination,
            Confirm
        },
        created() {
            this.getData();
        },
        watch:{
            "addDialog.isshow":function(isshow){
                if(!isshow){
                    this.cancle();
                }
            }
        },
        methods: {
            getData(ifBtn) {
                // this.ajax('/schedules','get',{},{page:this.page}).then((res) => {
                //     if(res&&res.data){
                //         this.tableData = res.data.results;
                //         this.total = res.data.count;
                //     }
                // })
            },
            deleteData() {
                let $this = this;
                console.log(this.confirmData.id,this.confirmData.index)
                $this.tableData.splice(this.confirmData.index,1)
                $this.confirmData.isshow=false;
                // this.ajax(``,'delete').then((res) => {
                //     $this.confirmData.isshow=false;
                //     $this.tableData.splice(index,1)
                //     $this.confirmData.isshow=false;
                // },(err) => {
                //     if(err&&err.response){
                //         let errors=err.response.data
                //         for(var key in errors){
                //             this.showErrorTip(errors[key][0])
                //         }
                //     }
                // })
            },
            
            handleEdit(index, row) {
                this.$router.push({path: '/battlelist', query:row});
            },
            handleDelete(index, row) {
                console.log(index,row)
                this.confirmData.id = row.id
                this.confirmData.index = index
                this.confirmData.isshow=true;
            },
            cancel1(val){
                this.confirmData.isshow=val;
            },
            conform1(){
                this.deleteData();
            },
            changePage(page) {
                this.page = page;
                this.getData();
            },
            searchEv() {
                this.hasSearch = true
                this.getData(true);
            },
            getDateTime() {
                console.log(this.dateArr)
                if (this.dateArr) {
                    this.start_date = this.dateArr[0];
                    this.end_date = this.dateArr[1];
                }
                else {
                    this.start_date = '';
                    this.end_date = '';
                }
            },
            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            },
            addMatchEv() {
                this.addDialog.isshow = true
            },
            addmetch(){
                
                this.$refs['form'].validate((valid) => {
                  if (valid) {
                    this.addDialog.isshow= false
                    this.cancle();
                  } else {
                    console.log('error submit!!');
                    return false;
                  }
                });
                
            },
            cancle(){
                this.$refs['form'].resetFields();
                this.form = {
                    race_date:'',
                    name:''
                }
            },
            changeShow(row,index){
                // 状态改变
                let $this = this;
                console.log(row,index)
                row.status= row.status
                // this.ajax(''+row.id,'patch',{}).then(function(res){
                //     if(res&&res.data){
                //         row.status= res.data.status
                //     }

                // },function(err){
                //     if(err&&err.response){
                //         let errors=err.response.data
                //         for(var key in errors){
                //             console.log(errors[key])
                //             // return
                //         } 
                //     } 
                // })
            },
        }
    }
</script>
