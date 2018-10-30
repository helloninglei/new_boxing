<template>
    <div class="version_manage" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="版本管理" firstTitle_path="/versionlist" disNone="disNone"></TopBar>
        <div class="container">
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_bt20' @click.native="addVersion" v-if='hasShow'>新增版本</el-button>
            <template>
                <el-table
                        :data="tableData"
                        :row-class-name="tableRowClassName"
                        style="width: 100%">
                    <el-table-column
                            prop="version"
                            label="版本号">
                    </el-table-column>
                    <el-table-column
                            prop="inner_number"
                            label="内部版本号">
                    </el-table-column>
                    <el-table-column
                            prop="platform"
                            label="平台">
                        <template slot-scope="scope">
                            <span>{{scope.row.platform=='android'?'安卓':scope.row.platform=='ios'?'IOS':''}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column
                            label="状态">
                        <template slot-scope="scope">
                            <span>{{scope.row.status=='FUTURE'?'未上线':scope.row.status=='NOW'?'当前版本':scope.row.status=='PAST'?'历史版本':''}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column
                            prop="created_time"
                            label="创建时间">
                    </el-table-column>
                    <el-table-column label="操作" width='220'>
                        <template slot-scope="scope">
                            <el-button
                                    size="mini"
                                    @click="handleEdit(scope.row)" v-if="scope.row.status=='FUTURE'">编辑</el-button>
                            <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleUp(scope.row,scope.$index)" v-if="scope.row.status=='FUTURE'">上线</el-button>
                            <el-button
                                    size="mini"
                                    type="danger"
                                    @click="changeShow(scope.row,scope.$index)" v-if="scope.row.status!='FUTURE'">查看升级文案</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </template>
            <footer v-if='total>10'>
                <Pagination :total="total" @changePage="changePage" :page="page"></Pagination>
            </footer>
        </div>
        <Confirm :isshow="confirmData.isshow" @confirm="UpApk" @cancel="cancel1" :content="confirmData.content" :id='confirmData.id' :index='confirmData.index' buttonName='确认上线'></Confirm>
        <el-dialog  :visible.sync="updateMsg.isshow" class='my_dialog'>
            <div class='dialog_content'>
                {{updateMsg.content}}
            </div>
            <div slot="footer" class="dialog-footer" style='text-align:center'>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 border_raduis_100' @click="updateMsg.isshow = false">关闭</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<style lang="stylus">
    .version_manage{
       .my_dialog  .el-dialog{
            width:385px;height:277px;
            .el-dialog__body{
                padding:8px 60px 0 60px;
                height:160px;
                overflow:auto;
            }
        } 
    }
    .el-table .success-row {
        background: #F2F2F2;
      }
    
</style>

<script >
    import TopBar from 'components/topBar';
    import Pagination  from 'components/pagination';
    import Confirm from "components/confirm";
    import Metchdialog from "components/metch_add_dialog"
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
                    
                ],
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:''
                },
                updateMsg:{
                    isshow:false,
                    content:''
                },
                hasShow:false,
                
            }
        },
        components: {
            TopBar,
            Pagination,
            Confirm,
            Metchdialog
        },
        created() {
            this.getData();
        },
        methods: {
            getData() {
                this.ajax('/app_versions','get',{},{page:this.page}).then((res) => {
                    this.hasShow = true
                    if(res&&res.data){
                        this.tableData = res.data.results;
                        this.total = res.data.count;
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            console.log(errors[key])
                            this.showErrorTip(errors[key])
                        }
                    }
                })
            },
            addVersion() {
                this.$router.push({path: '/versiondetail'});
            },
            handleEdit(row) {
                this.$router.push({path: '/versiondetail', query:{row:row}});
            },
            handleUp(row,index) {
                if(row.platform!='ios'){
                    this.confirmData.content='请确认是否上线'+row.platform+row.version+'版本？'
                }else{
                    this.confirmData.content='请确认是否上线'+row.platform+row.version+'版本？上线前请确认苹果应用市场已审核通过'
                }
                
                this.confirmData.id = row.id
                this.confirmData.index = index
                this.confirmData.isshow=true;
                this.confirmData.row = row
            },
            UpApk(){
                //调上线的接口
                this.ajax('/app_release/'+this.confirmData.row.id,'post').then((res)=>{
                    this.confirmData.isshow=false;
                    this.getData();
                    if(res&&res.data){
                        console.log(111)
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
            },
            cancel1(val){
                this.confirmData.isshow=val;
            },
            changePage(page) {
                this.page = page;
                this.getData();
            },
            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            },
            tableRowClassName({row, rowIndex}) {
                if (row.status=='NOW') {
                  return 'success-row';
                }
                return '';
            },
            changeShow(row,index){
                // 状态改变
                let $this = this;
                console.log(row,index)
                this.updateMsg.content = row.message
                this.updateMsg.isshow = true
                
            },
        }
    }
</script>
