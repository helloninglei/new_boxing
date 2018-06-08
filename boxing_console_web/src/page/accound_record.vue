<template>
    <div class="usermanage">
        <TopBar v-if="isShowTop" firstTitle_name="公司账户金额记录"  disNone="disNone"></TopBar>
        <div class='container'>
            <p class="showTotal">公司账户金额汇总:{{total_count}}</p>
            <nav class='myTable'>
                <template>
                    <el-table
                      :data="tableData"
                      style="width: 100%"
                      :highlight-current-row="true">
                        <el-table-column
                        prop="id"
                        label="ID"
                        >
                        </el-table-column>
                        <el-table-column
                        label="收入/支出"
                        >
                            <template slot-scope="scope">
                                <span>{{scope.row.change_amount>0?'+':''}} {{(scope.row.change_amount/100).toFixed(2)}}</span>                 
                            </template>
                        </el-table-column>
                        <el-table-column
                        prop="created_time"
                        label="时间"
                        >
                        </el-table-column>
                        <el-table-column
                        label="备注"
                        >
                            <template slot-scope="scope">
                                <span>[{{scope.row.change_type}}] 订单号：{{scope.row.remarks}}</span>                 
                            </template>
                        </el-table-column>
                    </el-table>
                </template>
            </nav>
            <footer v-show="total>10">
                <Pagination :total="total" @changePage="changePage"></Pagination>
            </footer>
        </div>
    </div>
</template>
<style scoped>
    .myTable{font-size:14px!important;}
    @media screen and (max-width:1919px){
       .margin_top_30{margin-top:30px;margin-left:0!important;} 
    } 
</style>
<style>
</style>
<script>
    import TopBar from 'components/topBar';
    import Table  from 'components/table';
    import Pagination  from 'components/pagination';
    export default {
        data() {
            return {
                isShowTop : true,
                total_count : 1000000,//付费金额
                total     : 1000,//数据的总条数
                tableData : [
                    {
                        "id": 1,   // id
                        "change_amount": -10000,   // 收入，支出
                        "created_time": "2018-02-23 18:00:00",  // 时间
                        "remarks": "23232323232",  // 订单号
                        "change_type": "提现"
                    },
                    {
                        "id": 2,   // id
                        "change_amount": 10000,   // 收入，支出
                        "created_time": "2018-02-23 18:00:00",  // 时间
                        "remarks": "23232323232",  // 订单号
                        "change_type": "提现"
                    },
                    {
                        "id": 3,   // id
                        "change_amount": -10000,   // 收入，支出
                        "created_time": "2018-02-23 18:00:00",  // 时间
                        "remarks": "23232323232",  // 订单号
                        "change_type": "提现"
                    },
                ],
            }
        },
        components: {
            TopBar,
            Table,
            Pagination,
        },
        created() {
            this.getTableData();
        },
        methods: {
            getTableData(page) {
                //获取data数据
                let $this    = this
                let sendData = {};
                if(page){
                    sendData.page = page;
                }
                this.ajax('/official_account_change_logs','get',{},sendData).then(function(res){
                    if(res&&res.data){
                        // console.log(res.data)
                        $this.tableData=res.data.results;
                        $this.total_count = res.data.total_count ? (res.data.total_count/100).toFixed(2) : 0;
                        $this.total = res.data.count;
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
            changePage(val){
                // 要看第几页
                this.getTableData(val)
            },
        },
    }
</script>