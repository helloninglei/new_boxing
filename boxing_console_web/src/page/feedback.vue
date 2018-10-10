<template>
    <div class="feedback" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="反馈建议" firstTitle_path="/dynamic" secondTitle_name="反馈建议"></TopBar>
        <div class="container">
            <header style='margin:20px 0 50px'>
                <el-input v-model="search"  class='myInput_40 margin_rt25' placeholder='输入用户昵称/用户手机号搜索' style='width:280px' @keyup.enter.native="searchEv"></el-input>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click.native="searchEv">查询</el-button>
            </header>
            <template>
                <el-table
                        :data="tableData"
                        :row-class-name="tableRowClassName"
                        style="width: 100%">
                    <el-table-column
                            prop="id"
                            label="id">
                    </el-table-column>
                    <el-table-column
                            prop="user_nick_name"
                            label="用户昵称">
                    </el-table-column>
                    <el-table-column
                            prop="user_mobile"
                            label="用户手机号">
                    </el-table-column>
                    <el-table-column
                            prop="created_time"
                            label="提交时间">
                    </el-table-column>
                    <el-table-column label="操作" width='200'>
                        <template slot-scope="scope">
                            <el-button
                                    size="mini"
                                    @click="toDetail(scope.$index, scope.row)">查看详情</el-button>
                            <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleEdit(scope.$index, scope.row)">{{scope.row.mark==true?"取消标记":"标记"}}</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </template>
            <footer v-if='total>10'>
                <Pagination :total="total" @changePage="changePage" :page="page"></Pagination>
            </footer>
        </div>
        <Confirm :isshow="confirmData.isshow" @confirm="confirm" @cancel="cancel()" :content="confirmData.content" :id='confirmData.id' :index='confirmData.index'></Confirm>
        <el-dialog  :visible.sync="showDetail" class='myDialog'>
            <div class="dialog_content" >
                <div class="dialog_title">用户信息</div>
                <p>用户昵称：{{detail.user_nick_name}}</p>
                <p>用户手机号：{{detail.user_mobile}}</p>
                <p>提交时间：{{detail.created_time}}</p>
                <div class="dialog_title">反馈建议</div>
                <p class='clearfix'><el-col :span="2">内容：</el-col><el-col :span='16'>{{detail.content}}</el-col></p>
                <p class='clearfix'>
                    <el-col :span="2">图片：</el-col>
                    <el-col :span='22'>
                        <div class='img_container' v-for='item in detail.images'>
                            <img :src="item" alt="" width='100%'>
                        </div>
                    </el-col>
                </p>
            </div>
            <div slot="footer" class="dialog-footer" style='text-align:left;margin-left:36px'>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="showDetail=false">关闭</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<style lang="stylus">
    .feedback .myDialog .el-dialog{
        width:620px;
        height:635px;
        margin-top:8vh!important;
        .el-dialog__body{
            padding:23px 53px 0;
            height:500px;
            overflow:auto;
            .dialog_title{
                font-family: PingFangSC-Regular;
                font-size: 14px;
                color: #000000;
                margin-bottom:24px;
            }
            .dialog_content>p{
                font-size: 14px;
                color: #606266;
                margin-bottom:18px;
                .img_container{
                    width:100px;
                    height:100px;
                    float:left;
                    margin:0 20px 20px 0;
                    overflow:hidden;
                }
            }
            .el-dialog__footer{margin-top:0!important}
            .el-checkbox:first-child{margin-left:0}
        }
    }
    .el-table .gray-row {
        background: #F2F2F2;
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
                showDetail:false,
                tableData: [
                    
                ],
                detail:{
                    
                },
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'确认删除该条资讯？'
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
        methods: {
            getData(ifBtn) {
                ifBtn && (this.page = 1);
                let param = {page: this.page, search: this.search};
                !this.hasSearch && (param = {page: this.page});
                this.ajax('/feedback','get',{},param).then((res) => {
                    if(res&&res.data){
                        console.log(res.data)
                        this.tableData = res.data.results;
                        this.total = res.data.count;
                        ifBtn && (this.hasSearch = true);
                    }
                })
            },
            handleEdit(index, row) {
                let $this = this;
                let ismark=row.mark==true?'unmark':'mark'
                this.ajax(`/feedback/${row.id}/${ismark}`,'post').then(function(res){
                    row.mark = !row.mark

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
            toDetail(index, row) {
                this.ajax(`/feedback/${row.id}`).then((res) => {
                    if(res&&res.data){
                        this.detail = res.data
                        this.showDetail = true;
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
            confirm(){},
            cancel(){},
            changePage(page) {
                this.page = page;
                this.getData();
            },
            tableRowClassName({row, rowIndex}) {
                if (row.mark==true) {
                  return 'gray-row';
                }
                return '';
            },
            searchEv() {
                this.hasSearch = true
                this.getData(true);
            },
            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            }
        }
    }
</script>
