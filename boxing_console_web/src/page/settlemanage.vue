<template>
    <div class="settlemanage">
        <TopBar v-if="isShowTop" firstTitle_name="约单管理" firstTitle_path="/classall" secondTitle_name="结算管理" secondTitle_path="/settlemanage"></TopBar>
        <div class='container'>
            <header style='margin-bottom:17px'>
                <el-form ref="form" :model="form" label-width="100px">
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="买家">
                                <el-input v-model="form.buyer" placeholder='请输入手机号'></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="拳手">
                               <el-input v-model="form.boxer"  class='myInput_40 margin_rt25' placeholder='姓名/手机号'></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :xl="12" :md="24">
                            <el-form-item label="实际结算时间" label-width="122px" class='width_change'>
                               <el-date-picker
                                v-model="form.start_date"
                                type="datetime"
                                :default-value= "new Date()"
                                value-format="yyyy-MM-dd hh:mm:ss"
                                placeholder="请选择">
                                </el-date-picker>
                                <span>-</span>
                                <el-date-picker
                                v-model="form.end_date"
                                type="datetime"
                                value-format="yyyy-MM-dd hh:mm:ss"
                                :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                                placeholder="请选择" class="margin_rt25">
                                </el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="课程">
                               <el-select v-model="form.course" class="margin_rt25">
                                    <el-option value="" label="全部">全部</el-option>
                                    <el-option value="泰拳" label="泰拳">泰拳</el-option>
                                    <el-option value="MMA" label="MMA">MMA</el-option>
                                    <el-option value="拳击" label="拳击">拳击</el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="结算状态">
                               <el-select v-model="form.status" class="margin_rt25">
                                    <el-option value="" label="全部">全部</el-option>
                                    <el-option value="unsettled" label="待结算">待结算</el-option>
                                    <el-option value="settled" label="已结算">已结算</el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="8">
                            <el-form-item label="">
                               <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
                                <el-button  class='myButton_40 btn_width_95' @click='reset()'>重置</el-button>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
            </header>
            <nav>
               <Table :tableColumn="tableColumn" :tableData="tableData" @toDetail="toDetail" operaname='订单详情'></Table> 
            </nav>
            <footer v-show='total>10'>
                <Pagination :total="total" @changePage="changePage" :page='page'></Pagination>
            </footer>
        </div>
    </div>
</template>
<style scoped>
</style>
<style>
    .settlemanage .el-form-item__label{font-family: PingFangSC-Regular;font-size: 16px!important;color: #000000;text-align: right;height:40px!important;line-height:40px!important;padding-left: 0}
    @media screen and (min-width:1920px){
        .width_change{margin-left:22px;}
    }
    @media screen and (max-width:1919px){
       .width_change{margin-left:-22px;} 
    }
    
</style>
<script>
    import TopBar from 'components/topBar';
    import Table  from 'components/table';
    import Pagination  from 'components/pagination';
    export default {
        data() {
            return {
                isShowTop : true,
                form : {
                    start_date  : '',
                    buyer       : '',
                    end_date    : '',
                    boxer       : '',
                    course      : '',
                    status      : ''
                },
                total     : 1000,
                issearch  : false,
                page      : 1,
                tableData : [
                    
                ],
                tableColumn:[
                    {title:'order_id',      name :'订单号',    width:'145'},
                    {title:'course_name',      name :'课程',      width:''},
                    {title:'boxer_name',       name :'拳手姓名',   width:''},
                    {title:'boxer_mobile',           name :'拳手手机号', width:''},
                    {title:'course_amount',            name :'课程金额', width:''},
                    {title:'buyer_mobile',       name :'买家',   width:''},
                    {title:'predicted_settle_date',         name :'预计结算日期',width:''},
                    {title:'settled',  name :'结算状态',   width:''},
                    {title:'actual_settle_date',         name :'实际结算日期',width:''},
                    {title:'settled_amount',         name :'结算金额（元）',width:''},
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
                let $this   = this
                let sendData={}
                if(this.issearch){
                   sendData=this.form
                }
                if(page){
                    sendData.page=page
                }
                this.ajax('/course/settle_orders','get',{},sendData).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        for(var i=0;i<res.data.results.length;i++){
                            res.data.results[i].settled=res.data.results[i].settled? "已结算":"待结算"
                            res.data.results[i].course_amount=(res.data.results[i].course_amount/100).toFixed(2)
                            res.data.results[i].settled_amount=(res.data.results[i].settled_amount/100).toFixed(2)
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
                console.log(val)
            },
            toDetail(row){
                // console.log(row)
                this.$router.push({path: '/orderdetail', query:{id:row.id}});

            },
            filter(){
                this.issearch= true;
                this.page    = 1;
                this.getTableData(1)
            },
            reset(){
                this.form={};
                this.getTableData()
            }
        },
    }
</script>