<template>
    <div class="ordermanage">
        <TopBar v-if="isShowTop" firstTitle_name="约单管理" firstTitle_path="/classall" secondTitle_name="订单管理" secondTitle_path="/ordermanage"></TopBar>
        <div class='container'>
            <header>
                <el-form ref="form" :model="form" label-width="100px">
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="用户/拳手">
                                <el-input v-model="form.search" placeholder='姓名／手机号'></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="订单状态">
                               <el-select v-model="form.status" class="margin_rt25">
                                    <el-option value="" label="全部">全部</el-option>
                                    <el-option value="1" label="待付款">待付款</el-option>
                                    <el-option value="2" label="待使用">待使用</el-option>
                                    <el-option value="3" label="待评价">待评价</el-option>
                                    <el-option value="4" label="已完成">已完成</el-option>
                                    <el-option value="5" label="已过期">已过期</el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :xl="12" :md="24">
                            <el-form-item label="支付时间" label-width="100px" >
                               <el-date-picker
                                v-model="form.pay_time_start"
                                type="datetime"
                                :default-value= "new Date()"
                                value-format="yyyy-MM-dd hh:mm:ss"
                                placeholder="请选择">
                                </el-date-picker>
                                <span>-</span>
                                <el-date-picker
                                v-model="form.pay_time_end"
                                type="datetime"
                                value-format="yyyy-MM-dd hh:mm:ss"
                                :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                                placeholder="请选择"  class="margin_rt25">
                                </el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="购买课程">
                                <el-select v-model="form.course__course_name">
                                    <el-option value="" label="全部">全部</el-option>
                                    <el-option value="THAI_BOXING" label="泰拳">泰拳</el-option>
                                    <el-option value="BOXING" label="拳击">拳击</el-option>
                                    <el-option value="MMA" label="MMA">MMA</el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="支付方式">
                                <el-select v-model="form.payment_type" >
                                    <el-option value="" label="全部">全部</el-option>
                                    <el-option value="2" label="微信">微信</el-option>
                                    <el-option value="1" label="支付宝">支付宝</el-option>
                                    <el-option value="3" label="余额">余额</el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="6" style="margin-left:100px">
                               <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
                                <el-button  class='myButton_40 btn_width_95'  @click="reset()">重置</el-button>
                        </el-col>
                    </el-row>
                </el-form>
            </header>
            <nav>
               <Table :tableColumn="tableColumn" :tableData="tableData" @toDetail="toDetail"></Table> 
            </nav>
            <footer v-show='total>10'>
                <Pagination :total="total" @changePage="changePage" :page='page'></Pagination>
            </footer>
        </div>
    </div>
</template>
<style>
    .ordermanage .el-form-item__label{font-family: PingFangSC-Regular;font-size: 16px!important;color: #000000;text-align: right;height:40px!important;line-height:40px!important;padding-left: 0}
</style>
<style>
nav{min-height: 528px}
</style>
<script >
    import TopBar from 'components/topBar';
    import Table  from 'components/table';
    import Pagination  from 'components/pagination';
    export default {
        data() {
            return {
                isShowTop : true,
                page      :1,
                issearch  :false,
                form : {
                    search     : '',
                    payment_type    : '',
                    course__course_name : '',
                    pay_time_start : '',
                    pay_time_end   : '',
                    courseStatus : '',
                    status  : '',
                    is_accept_order : '',
                },
                total     : 20,
                tableData : [
                    
                ],
                tableColumn:[
                    {title:'order_time',  name :'下单时间',  width:'155'},
                    {title:'out_trade_no',  name :'订单号',    width:'120'},
                    {title:'user_nickname',  name :'用户昵称',   width:''},
                    {title:'user_mobile',name :'用户手机号', width:'95'},
                    {title:'course_name',name :'购买课程',   width:''},
                    {title:'boxer_name', name :'拳手姓名',   width:''},
                    {title:'boxer_mobile',     name :'拳手手机号', width:'100'},
                    {title:'amount',      name :'支付金额（元）',width:''},
                    {title:'payment_type_name',    name :'支付方式',   width:'50'},
                    {title:'pay_time',   name :'支付时间',   width:'155'},
                    {title:'status_name',   name :'订单状态',   width:'55'},
                ],
            }
        },
        components: {
            TopBar,
            Table ,
            Pagination
        },
        created() {
            this.getTableData();
        },
        methods: {
            getTableData(page) {
                //获取data数据
                let $this = this ;
                let sendData={} ;
                if(this.issearch){
                   sendData=this.form
                }
                if(page){
                    sendData.page=page
                }
                this.ajax('/course/orders','get',{},sendData).then(function(res){
                    if(res&&res.data){
                        // console.log(res.data)
                        for(var i=0;i<res.data.results.length;i++){
                            if(res.data.results[i].course_name=='BOXING'){
                                res.data.results[i].course_name='拳击'
                            }else if(res.data.results[i].course_name=='THAI_BOXING'){
                                res.data.results[i].course_name='泰拳'
                            }
                            if(res.data.results[i].payment_type==1){
                                res.data.results[i].payment_type_name='支付宝'
                            }else if(res.data.results[i].payment_type==2){
                                res.data.results[i].payment_type_name='微信'
                            }else{
                                res.data.results[i].payment_type_name='余额'
                            }
                            res.data.results[i].amount = (res.data.results[i].amount/100).toFixed(2)
                            switch (res.data.results[i].status){
                                case 1 :
                                res.data.results[i].status_name='待付款';
                                break;
                                case 2 :
                                res.data.results[i].status_name='待使用';
                                break;
                                case 3:
                                res.data.results[i].status_name='待评论';
                                break;
                                case 4 :
                                res.data.results[i].status_name='已完成';
                                break;
                                case 5 :
                                res.data.results[i].status_name='已过期';
                                break;
                            }
                        }

                        $this.tableData=res.data.results;
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
                this.page=val
                this.getTableData(val) ;
            },
            toDetail(row){
                // console.log(row)
                this.$router.push({path: '/orderdetail', query:{id:row.id}});

            },
            filter(){
                this.issearch=true;
                //搜索是先看第一页
                this.page=1
                this.getTableData(1);
            },
            reset(){
                this.form={};
                this.getTableData()
            }
        },
    }
</script>