<template>
    <div class="ordermanage">
        <TopBar v-if="isShowTop" firstTitle_name="约单管理" firstTitle_path="/classall" secondTitle_name="订单管理" secondTitle_path="/ordermanage"></TopBar>
        <div class='container'>
            <header>
                <el-form ref="form" :model="form" label-width="100px">
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="用户/拳手">
                                <el-input v-model="form.search" placeholder='姓名／昵称／手机号'></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="订单状态">
                               <el-select v-model="form.status" class="margin_rt25">
                                    <el-option value="0" label="全部">全部</el-option>
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
                                placeholder="请选择">
                                </el-date-picker>
                                <span>-</span>
                                <el-date-picker
                                v-model="form.pay_time_end"
                                type="datetime"
                                :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                                placeholder="请选择"  class="margin_rt25">
                                </el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="购买课程">
                                <el-select v-model="form.course_name">
                                    <el-option value="0" label="全部">全部</el-option>
                                    <el-option value="拳馆" label="拳馆">拳馆</el-option>
                                    <el-option value="泰拳" label="泰拳">泰拳</el-option>
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
                                <el-button  class='myButton_40 btn_width_95'>重置</el-button>
                        </el-col>
                    </el-row>
                </el-form>
            </header>
            <nav>
               <Table :tableColumn="tableColumn" :tableData="tableData" @toDetail="toDetail"></Table> 
            </nav>
            <footer>
                <Pagination :total="total" @changePage="changePage"></Pagination>
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
                form : {
                    search     : '',
                    payment_type    : '',
                    course_name : '',
                    pay_time_start : '',
                    pay_time_end   : '',
                    courseStatus : '',
                    status  : '',
                    is_accept_order : '',
                },
                total     : 1000,
                tableData : [
                    {
                        "id": 1,
                        "out_trade_no":"2018020300001",
                        "order_time":"2018-02-03 12:32:23",
                        "boxer_name": "王五", //拳手姓名
                        "boxer_mobile": "111111111", //拳手手机号
                        "user_nickname":"用户一",
                        "user_mobile":"13900000000",
                        "is_professional_boxer": true, //是否是职业选手
                        "is_accept_order": true,  //是否可以接单
                        "course_name": "THAI_BOXING", //课程名称
                        "amount": 120, //价格
                        "payment_type":1,
                        "pay_time":"2018-02-03 14:32:23",
                        "duration": 120, //时长
                        "status": "待使用" //有效期
                    },
                    {
                        "id": 2,
                        "out_trade_no":"2018020300001",
                        "order_time":"2018-02-03 12:32:23",
                        "boxer_name": "王五", //拳手姓名
                        "boxer_mobile": "111111111", //拳手手机号
                        "user_nickname":"用户一",
                        "user_mobile":"13900000000",
                        "is_professional_boxer": true, //是否是职业选手
                        "is_accept_order": true,  //是否可以接单
                        "course_name": "THAI_BOXING", //课程名称
                        "amount": 120, //价格
                        "payment_type":2,
                        "pay_time":"2018-02-03 14:32:23",
                        "duration": 120, //时长
                        "status": "待使用" //有效期
                    },
                ],
                tableColumn:[
                    {title:'order_time',  name :'下单时间',  width:'195'},
                    {title:'out_trade_no',  name :'订单号',    width:'145'},
                    {title:'user_nickname',  name :'用户昵称',   width:''},
                    {title:'user_mobile',name :'用户手机号', width:'130'},
                    {title:'course_name',name :'购买课程',   width:''},
                    {title:'boxer_name', name :'拳手姓名',   width:''},
                    {title:'boxer_mobile',     name :'拳手手机号', width:''},
                    {title:'amount',      name :'支付金额（元）',width:''},
                    {title:'payment_type_name',    name :'支付方式',   width:''},
                    {title:'pay_time',   name :'支付时间',   width:'195'},
                    {title:'status_name',   name :'订单状态',   width:''},
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
            getTableData(data,page) {
                //获取data数据
                let $this = this
                let url   = '/course/orders';
                if(page&&page>1){
                    data.page=page
                }
                this.ajax(url,'get',{},data).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        for(var i=0;i<res.data.results.length;i++){
                            if(res.data.results[i].payment_type==1){
                                res.data.results[i].payment_type_name='支付宝'
                            }else if(res.data.results[i].payment_type==2){
                                res.data.results[i].payment_type_name='微信'
                            }else{
                                res.data.results[i].payment_type_name='余额'
                            }
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
                // console.log(val)
                this.getTableData(this.sendData,val);
            },
            toDetail(row){
                // console.log(row)
                this.$router.push({path: '/orderdetail', query:{id:row.id}});

            },
            filter(){
                // var phoneReg = /^((13[0-9])|(15[^4,\\D])|(18[0,0-9]))\\d{8}$/;
                // if(this.form.search){
                //     console.log(/^\d$/.test(this.form.search))
                //     console.log(!/^\d$/.test(this.form.search))
                //     if(/^\d$/.test(this.form.search)&&phoneReg.test(this.form.search)){
                //         alert('用户名 、手机号输入不合法')
                //         return;
                //     }
                // }
                console.log(this.form)
                this.getTableData(this.sendData);
            },
        },
    }
</script>