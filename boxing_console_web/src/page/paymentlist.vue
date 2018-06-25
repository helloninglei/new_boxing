<template>
    <div class="usermanage">
        <TopBar v-if="isShowTop" firstTitle_name="财务管理" firstTitle_path="/boxingmanage" secondTitle_name="用户支付流水" secondTitle_path="/addBoxing"></TopBar>
        <div class='container'>
            <header>
                 <el-row>
                    <el-col :span="7" style='width:364px;margin-bottom:30px'>
                        <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='用户ID/手机号/昵称/订单号' style='width:334px'></el-input>
                    </el-col> 
                    <el-col :span="7" style='width:480px'>
                        <el-date-picker
                        v-model="sendData.start_time"
                        type="datetime"
                        value-format="yyyy-MM-dd HH:mm:ss"
                        :default-value= "new Date()"
                        placeholder="交易开始时间" style='width:200px'>
                        </el-date-picker>
                        <span>-</span>
                        <el-date-picker
                        v-model="sendData.end_time"
                        type="datetime"
                        value-format="yyyy-MM-dd HH:mm:ss"

                        :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                        placeholder="交易结束时间" style='width:200px' class="margin_rt25">
                        </el-date-picker>
                    </el-col> 
                </el-row>  
                <el-row>
                    <el-col :span="5" style='margin-bottom:30px'>
                        <el-select v-model="sendData.device" class="margin_rt25">
                            <el-option value="" label="交易终端"></el-option>
                            <el-option value="1" label="ios">ios</el-option>
                            <el-option value="2" label="android">android</el-option>
                        </el-select>
                    </el-col> 
                    <el-col :span="5" >
                        <el-select v-model="sendData.payment_type" class="margin_rt25">
                            <el-option value="" label="交易渠道">全部</el-option>
                            <el-option value="1" label="支付宝">支付宝</el-option>
                            <el-option value="2" label="微信">微信</el-option>
                            <el-option value="3" label="余额">余额</el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="5" >
                        <el-select v-model="sendData.status" class="margin_rt25">
                            <el-option value="" label="交易状态">全部</el-option>
                            <el-option value="1" label="支付未完成">支付未完成</el-option>
                            <el-option value="2" label="支付成功">支付成功</el-option>
                            <el-option value="3" label="支付失败">支付失败</el-option>
                        </el-select>
                    </el-col>  
                </el-row>     
                <el-row>     
                    <el-col :span='6'>
                        <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
                        <el-button  class='myButton_40 btn_width_95 myBtnHover_red' @click="reset()">重置</el-button>
                    </el-col>   
                </el-row>
            </header>
            <nav class='myTable'>
                <template>
                    <el-table
                      :data="tableData"
                      style="width: 100%"
                      :highlight-current-row="true">
                        <el-table-column
                        :prop="value.title"
                        :label="value.name"
                        :width="value.width"
                        v-for="value in tableColumn">
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
                issearch  :false,
                page      :1,
                sendData  : {
                    start_time : '',
                    end_time   : '',
                    search     : '',
                    device     :'',
                    payment_type :'',
                    status     :'',
                },
                userTotal : 1000000,//付费人数
                moneyTotal : 1000000,//付费金额
                total     : 1000,//数据的总条数
                tableData : [
                    
                ],
                tableColumn:[
                    // {title:'id',    name :'ID',   width: ''},
                    {title:'out_trade_no',  name :'流水号',width: '100'},
                    {title:'amount',name :'金额（元）' ,width: '120'},
                    {title:'user',name :'用户ID',width: ''},
                    {title:'user_nickname', name :'用户昵称'   ,width: ''},
                    {title:'user_mobile',name :'用户手机号',width: '120'},
                    {title:'device',name :'交易终端' ,width: ''},
                    {title:'payment_type',name :'交易渠道' ,width: ''},
                    {title:'status',name :'交易状态' ,width: ''},
                    {title:'order_time',name :'交易时间' ,width: '200'},
                    {title:'remarks',name :'备注' ,width: '120'},
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
                let $this   = this
                let sendData={}
                if(this.issearch){
                   sendData=this.sendData
                }
                if(page){
                    sendData.page=page
                }
                this.ajax('/pay_orders','get',{},sendData).then(function(res){
                    if(res&&res.data){
                        
                        $this.tableData=res.data.results;
                        for (var i=0;i<$this.tableData.length;i++){
                            $this.tableData[i].amount = ($this.tableData[i].amount /100).toFixed(2);
                        }
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
                console.log(val)
            },
            filter(){
                this.issearch=true;
                //搜索是先看第一页
                this.page=1
                this.getTableData(1) 
            },
            reset(){
                this.sendData={};
                this.getTableData();
            },
        },
    }
</script>