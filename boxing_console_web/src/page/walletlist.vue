<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="用户管理" firstTitle_path="/usermanage" secondTitle_name="钱包余额记录" secondTitle_path="/walletlist"></TopBar>
        <div class="wallerlist">
            <header>
                <el-date-picker
                v-model="sendData.startTime"
                type="datetime"
                :default-value= "new Date()"
                placeholder="开始时间" style='width:200px' class="margin_rt25">
                </el-date-picker>
                <el-date-picker
                v-model="sendData.endTime"
                type="datetime"
                :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                placeholder="结束时间" style='width:200px' class="margin_rt25">
                </el-date-picker>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25'>查询</el-button>
            </header>
            <nav>
                <template>
                    <el-table
                      :data="tableData"
                      style="width: 100%"
                      :highlight-current-row="true">
                        <el-table-column
                        label="余额">
                            <template slot-scope="scope">
                                <span class='' >{{scope.row.derection=="add"?'+':'-'}}{{scope.row.balance}}</span>
                            </template>
                        </el-table-column>
                         <el-table-column
                        label="时间"
                        prop="time">
                        </el-table-column>
                         <el-table-column
                        label="备注"
                        prop="content">
                        </el-table-column>
                    </el-table>
                </template>
            </nav>
            <footer>
                <Pagination :total="total" @changePage="changePage"></Pagination>
            </footer>
        </div>
    </div>
</template>
<style scoped>
    .wallerlist{padding:25px 30px;}
    nav{margin-top:30px;}
</style>
<script type="text/ecmascript-6">
    import TopBar from 'components/topBar';
    import Pagination  from 'components/pagination';
    export default {
        data() {
            return {
                isShowTop : true,
                sendData  :{
                    startTime : '',
                    endTime   : '',
                },
                total     : 100,
                tableData :[
                    {
                        derection:"add",
                        balance : 1000,
                        time    : "2017-11-03 16:35:17",
                        content : '充值ID:XXX'
                    },
                    {
                        derection:"",
                        balance : 1000,
                        time    : "2017-11-03 16:35:17",
                        content : '约单(支出)ID:xxxx'
                    },
                    {
                        derection:"",
                        balance : 1000,
                        time    : "2017-11-03 16:35:17",
                        content : '付费视频ID:xxxx'
                    },
                    {
                        derection:"add",
                        balance : 1000,
                        time    : "2017-11-03 16:35:17",
                        content : '约单(收入)ID:XXX'
                    },
                    {
                        derection:"add",
                        balance : 1000,
                        time    : "2017-11-03 16:35:17",
                        content : '提现(拒绝打款)ID:xxxx'
                    }
                ]
            }
        },
        components: {
            TopBar,
            Pagination
        },
        created() {
            let query = this.$route.query
            this.getDetailData(query.id);
        },
        methods: {
            getDetailData(id) {
                //获取data数据
                let $this   = this
                // this.ajax('/','get',{},{id:id}).then(function(res){
                //     if(res&&res.data){
                //         console.log(res.data)
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
            changePage(val){
                console.log(val)
            }
        },
    }
</script>