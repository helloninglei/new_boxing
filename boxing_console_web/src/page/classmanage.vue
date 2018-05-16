<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="约单管理" firstTitle_path="/" secondTitle_name="课程管理" secondTitle_path="/classmanage"></TopBar>
        <div class='container'>
            <header>
                <div style='display: inline-block;padding-bottom:30px'>
                    <span class="inlimeLabel">拳手</span>
                    <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='姓名/手机号/身份证号' style='width:18rem'></el-input>
                </div>
                <div style='display: inline-block;padding-bottom:30px'>
                    <span class="inlimeLabel">价格区间</span>
                    <el-input v-model="sendData.price_min"  class='myInput_40' style='width:9rem' placeholder='请输入'></el-input>
                    <span>-</span>
                    <el-input v-model="sendData.price_max"  class='myInput_40 margin_rt25' style='width:9rem' placeholder='请输入'></el-input>
                </div>
                <div style='display: inline-block;padding-bottom:30px'>
                    <span class="inlimeLabel">已开课程</span>
                    <el-select v-model="sendData.courseName" class="margin_rt25" style='width:11rem'>
                        <el-option value="0" label="全部">全部</el-option>
                        <el-option value="拳馆" label="拳馆">拳馆</el-option>
                        <el-option value="泰拳" label="泰拳">泰拳</el-option>
                        <el-option value="MMA" label="MMA">MMA</el-option>
                    </el-select>
                </div>
                <div style='display: inline-block;padding-bottom:30px'>
                    <span class="inlimeLabel">接单状态</span>
                    <el-select v-model="sendData.is_accept_order" style='width:11rem'>
                        <el-option value="0" label="全部">全部</el-option>
                        <el-option :value="true" label="是">是</el-option>
                        <el-option :value="false" label="否">否</el-option>
                    </el-select>
                </div>
                <div style='margin-bottom:50px'>
                    <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
                    <el-button  class='myButton_40 btn_width_95'>重置</el-button>
                </div>
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
<style scoped>
    .inlimeLabel{font-family: PingFangSC-Regular;font-size: 16px;color: #000000;padding-right:15px;}
</style>
<style>
nav{min-height: 528px}
</style>
<script type="text/ecmascript-6">
    import TopBar from 'components/topBar';
    import Table  from 'components/table';
    import Pagination  from 'components/pagination';
    export default {
        data() {
            return {
                isShowTop : true,
                sendData  : {
                    price_min  : '',
                    price_max  : '',
                    search     : '',
                    courseName : '',
                    is_accept_order : '',
                },
                total     : 1000,
                tableData : [
                    {
                        "id": 1,
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
                        "boxer_name": "李四", //拳手姓名
                        "mobile": "111111111", //拳手手机号
                        "is_professional_boxer": true, //是否是职业选手
                        "is_accept_order": true,  //是否可以接单
                        "course_name": "THAI_BOXING", //课程名称
                        "price": 120, //价格
                        "duration": 120, //时长
                        "validity": "2018-08-25" //有效期
                    },
                    {
                        "id": 4,
                        "boxer_name": "王五", //拳手姓名
                        "mobile": "111111111", //拳手手机号
                        "is_professional_boxer": true, //是否是职业选手
                        "is_accept_order": true,  //是否可以接单
                        "course_name": "THAI_BOXING", //课程名称
                        "price": 120, //价格
                        "duration": 120, //时长
                        "validity": "2018-08-25" //有效期
                    },
                    {
                        "id": 5,
                        "boxer_name": "赵柳", //拳手姓名
                        "mobile": "111111111", //拳手手机号
                        "is_professional_boxer": true, //是否是职业选手
                        "is_accept_order": true,  //是否可以接单
                        "course_name": "THAI_BOXING", //课程名称
                        "price": 120, //价格
                        "duration": 120, //时长
                        "validity": "2018-08-25" //有效期
                    },
                    {
                        "id": 6,
                        "boxer_name": "王依依", //拳手姓名
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
                        "boxer_name": "张三", //拳手姓名
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
                    {title:'boxer_name',       name :'拳手姓名',   width:''},
                    {title:'mobile',           name :'拳手手机号', width:''},
                    {title:'professional_boxer', name :'选手类型', width:''},
                    {title:'course_name',      name :'已开课程',   width:''},
                    {title:'price',            name :'单价（元）', width:''},
                    {title:'duration',         name :'时长（分钟）',width:''},
                    {title:'is_accept_order',  name :'接单状态',   width:''},
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
                // this.ajax('/courses','get',{},{}).then(function(res){
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
                this.$router.push({path: '/classdetail', query:{id:row.id}});

            },
            filter(){
                console.log(this.sendData)
            }
        },
    }
</script>