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
        <Confirm :isshow="confirmData.isshow" @confirm="conform1" @cancel="cancel1" :content="confirmData.content" :id='confirmData.id' :index='confirmData.index'></Confirm>
        <Metchdialog :isshow="addDialog.isshow" @confirm="addmetch" @cancel="cancle2" content_title="添加赛程"></Metchdialog>
    </div>
</template>

<style lang="stylus">
    
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
                    content:'删除后连同赛程内的对战表一同删除，且不可恢复，是否确认删除？'
                },
                addDialog:{
                    isshow:false
                },
                
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
                this.ajax('/schedules','get',{},{page:this.page}).then((res) => {
                    if(res&&res.data){
                        this.tableData = res.data.results;
                        this.total = res.data.count;
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
            deleteData() {
                let $this = this;
                this.ajax(`/schedules/${this.confirmData.id}`,'delete').then((res) => {
                    $this.confirmData.isshow=false;
                    $this.tableData.splice(this.confirmData.index,1)
                    $this.confirmData.isshow=false;
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            this.showErrorTip(errors[key][0])
                        }
                    }
                })
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
            cancle2(val){
                this.addDialog.isshow = val;
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
            addmetch(data){
                this.getData();
                this.addDialog.isshow = false;
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
