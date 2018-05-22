<template>
    <div class="settlemanage">
        <TopBar v-if="isShowTop" firstTitle_name="约单管理" firstTitle_path="/classall" secondTitle_name="结算管理" secondTitle_path="/settlemanage"></TopBar>
        <div class='container'>
            <header style='margin-bottom:17px'>
                <el-form ref="form" :model="form" label-width="100px">
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="买家姓名">
                                <el-input v-model="form.name" placeholder='请输入'></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="拳手">
                               <el-input v-model="form.name"  class='myInput_40 margin_rt25' placeholder='姓名/手机号'></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :xl="12" :md="24">
                            <el-form-item label="实际结算时间" label-width="122px" class='width_change'>
                               <el-date-picker
                                v-model="form.startTime"
                                type="datetime"
                                :default-value= "new Date()"
                                placeholder="请选择">
                                </el-date-picker>
                                <span>-</span>
                                <el-date-picker
                                v-model="form.endTime"
                                type="datetime"
                                :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                                placeholder="请选择" class="margin_rt25">
                                </el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="6">
                            <el-form-item label="课程">
                               <el-select v-model="form.courseStatus" class="margin_rt25">
                                    <el-option value="0" label="全部">全部</el-option>
                                    <el-option value="已通过" label="已通过">已通过</el-option>
                                    <el-option value="已驳回" label="已驳回">已驳回</el-option>
                                    <el-option value="待审核" label="待审核">待审核</el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <el-form-item label="结算状态">
                               <el-select v-model="form.settleStatus" class="margin_rt25">
                                    <el-option value="0" label="全部">全部</el-option>
                                    <el-option value="待结算" label="待结算">待结算</el-option>
                                    <el-option value="已结算" label="已结算">已结算</el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="8">
                            <el-form-item label="">
                               <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
                                <el-button  class='myButton_40 btn_width_95'>重置</el-button>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
            </header>
            <nav>
               <Table :tableColumn="tableColumn" :tableData="tableData" @toDetail="toDetail" operaname='订单详情'></Table> 
            </nav>
            <footer>
                <Pagination :total="total" @changePage="changePage"></Pagination>
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
                    startTime  : '',
                    name       : '',
                    endTime    : '',
                    search     : '',
                    courseStatus : '',
                    settleStatus : '',
                    is_accept_order : '',
                },
                total     : 1000,
                tableData : [
                    {
                        "id": 1,
                        "order_num":"2018020300001",
                        "boxer_name": "张三", //拳手姓名
                        "mobile": "111111111", //拳手手机号
                        "is_professional_boxer": true, //是否是职业选手
                        "is_accept_order": true,  //是否可以接单
                        "course_name": "THAI_BOXING", //课程名称
                        "price": 120, //价格
                        "duration": 120, //时长
                        "validity": "2018-08-25" //有效期
                    },
                    {
                        "id": 2,
                        "order_num":"2018020300001",
                        "boxer_name": "张三", //拳手姓名
                        "mobile": "111111111", //拳手手机号
                        "is_professional_boxer": true, //是否是职业选手
                        "is_accept_order": true,  //是否可以接单
                        "course_name": "THAI_BOXING", //课程名称
                        "price": 120, //价格
                        "duration": 120, //时长
                        "validity": "2018-08-25" //有效期
                    },
                    {
                        "id": 3,
                        "order_num":"2018020300001",
                        "boxer_name": "李四", //拳手姓名
                        "mobile": "111111111", //拳手手机号
                        "is_professional_boxer": true, //是否是职业选手
                        "is_accept_order": true,  //是否可以接单
                        "course_name": "THAI_BOXING", //课程名称
                        "price": 120, //价格
                        "duration": 120, //时长
                        "validity": "2018-08-25" //有效期
                    },
                ],
                tableColumn:[
                    {title:'order_num',      name :'订单号',    width:'145'},
                    {title:'course_name',      name :'课程',      width:''},
                    {title:'boxer_name',       name :'拳手姓名',   width:''},
                    {title:'mobile',           name :'拳手手机号', width:''},
                    {title:'professional_boxer', name :'选手类型', width:''},
                    {title:'price',            name :'课程金额', width:''},
                    {title:'boxer_name',       name :'买家姓名',   width:''},
                    {title:'duration',         name :'预计结算日期',width:''},
                    {title:'is_accept_order',  name :'结算状态',   width:''},
                    {title:'duration',         name :'实际结算日期',width:''},
                    {title:'duration',         name :'结算金额（元）',width:''},
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
            getTableData() {
                //获取data数据
                let $this   = this
                for(var i=0;i<this.tableData.length;i++){
                    this.tableData[i].professional_boxer=this.tableData[i].is_professional_boxer? "职业":"非职业"
                    this.tableData[i].is_accept_order=this.tableData[i].is_accept_order? "是":"否"
                }
                // this.ajax('/','get',{},{}).then(function(res){
                //     if(res&&res.data){
                //         console.log(res.data)
                //         for(var i=0;i<res.data.results.length;i++){
                //             res.data.results[i].professional_boxer=res.data.results[i].is_professional_boxer? "职业":"非职业"
                //             res.data.results[i].is_accept_order=res.data.results[i].is_accept_order? "是":"否"
                //         }
                //         $this.tableData=res.data.results;
                //         $this.total = res.data.count;
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
                // 要看第几页
                console.log(val)
            },
            toDetail(row){
                // console.log(row)
                this.$router.push({path: '/orderdetail', query:{id:row.id}});

            },
            filter(){
                console.log(this.form)
            }
        },
    }
</script>