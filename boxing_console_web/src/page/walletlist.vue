<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="用户管理" firstTitle_path="/usermanage" secondTitle_name="钱包余额记录"
                secondTitle_path="/walletlist"></TopBar>
        <div class="wallerlist">
            <header>
                <el-date-picker
                        v-model="sendData.start_time"
                        type="datetime"
                        value-format="yyyy-MM-dd HH:mm:ss"
                        :default-value="new Date()"
                        placeholder="开始时间" style='width:200px' class="margin_rt25">
                </el-date-picker>
                <el-date-picker
                        v-model="sendData.end_time"
                        type="datetime"
                        value-format="yyyy-MM-dd HH:mm:ss"
                        :default-value="(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                        placeholder="结束时间" style='width:200px' class="margin_rt25">
                </el-date-picker>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click='filter()'>查询
                </el-button>
            </header>
            <nav>
                <template>
                    <el-table
                            :data="tableData"
                            style="width: 100%"
                            :highlight-current-row="true">
                        <el-table-column
                                label="余额"
                        >
                            <template slot-scope="scope">
                                <span class=''>{{(scope.row.change_amount/100).toFixed(2)}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                                label="时间"
                                prop="created_time">
                        </el-table-column>
                        <el-table-column
                                label="备注">
                            <template slot-scope="scope">
                                <span class=''>{{scope.row.change_type}} ID: {{scope.row.remarks}}</span>
                            </template>
                        </el-table-column>
                    </el-table>
                </template>
            </nav>
            <footer v-show="total>10">
                <Pagination :total="total" @changePage="changePage" :page='page'></Pagination>
            </footer>
        </div>
    </div>
</template>
<style scoped>
    .wallerlist {
        padding: 25px 30px;
    }

    nav {
        margin-top: 30px;
    }
</style>
<script>
    import TopBar from 'components/topBar';
    import Pagination from 'components/pagination';

    export default {
        data() {
            return {
                isShowTop: true,
                issearch: false,
                page: 1,
                id: '',
                sendData: {
                    start_time: '',
                    end_time: '',
                },
                total: 100,
                tableData: [
                    {
                        change_type: "充值",
                        change_amount: '+1000',
                        created_time: "2017-11-03 16:35:17",
                        remarks: '充值ID:XXX'
                    },
                ]
            }
        },
        components: {
            TopBar,
            Pagination
        },
        created() {
            let query = this.$route.query;
            this.id = query.id;
            this.getDetailData();
        },
        methods: {
            getDetailData(page) {
                //获取data数据
                let $this = this;
                let sendData = {};
                if (this.issearch) {
                    sendData = this.sendData
                }
                if (page) {
                    sendData.page = page
                }
                this.ajax('/money_change_logs/' + this.id, 'get', {}, sendData).then(function (res) {
                    if (res && res.data) {
                        $this.tableData = res.data.results;//后台没数据先不用
                        $this.total = res.data.count;
                    }

                }, function (err) {
                    if (err && err.response) {
                        let errors = err.response.data;
                        for (var key in errors) {
                            console.log(errors[key])
                            // return
                        }
                    }
                })
            },
            changePage(val) {
                this.page = val;
                this.getDetailData(val)
            },
            filter() {
                this.issearch = true;
                //搜索是先看第一页
                this.page = 1;
                this.getDetailData(1)
            },
        },
    }
</script>