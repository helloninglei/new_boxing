<template>
    <div class="usermanage">
        <TopBar v-if="isShowTop" firstTitle_name="约单管理" firstTitle_path="/" secondTitle_name="课程管理" secondTitle_path="/classmanage"></TopBar>
        <div class='container'>
            <header>
                <el-input v-model="sendData.keywards"  class='myInput_40 margin_rt25' placeholder='输入用户ID/用户账号/昵称/手机号' style='width:284px'></el-input>
                <el-date-picker
                v-model="sendData.startTime"
                type="datetime"
                :default-value= "new Date()"
                placeholder="注册开始时间" style='width:200px' class="margin_rt25">
                </el-date-picker>
                <el-date-picker
                v-model="sendData.endTime"
                type="datetime"
                :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                placeholder="注册结束时间" style='width:200px' class="margin_rt25">
                </el-date-picker>
                <el-select v-model="sendData.userType">
                    <el-option value="0" label="全部">全部</el-option>
                    <el-option value="1" label="普通用户">普通用户</el-option>
                    <el-option value="2" label="认证拳手">认证拳手</el-option>
                </el-select>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 margin_lf70'>查询</el-button>
                <el-button  class='myButton_40 btn_width_95'>重置</el-button>
            </header>
            <nav>
               <Table :tableColumn="tableColumn" :tableData="tableData"></Table> 
            </nav>
        </div>
    </div>
</template>
<style scoped>
    
</style>
<style>
</style>
<script type="text/ecmascript-6">
    import TopBar from 'components/topBar';
    import Table  from 'components/table';

    export default {
        data() {
            return {
                isShowTop : true,
                sendData  : {
                    startTime : '',
                    endTime   : '',
                    keywards  : '',
                    userType  : '',
                },
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
            Table
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
                }
                // this.ajax('/course','get',{},{}).then(function(res){
                //     if(res&&res.data){
                //         console.log(res.data)
                //         for(var i=0;i<res.data.results.length;i++){
                //             res.data.results[i].professional_boxer=res.data.results[i].is_professional_boxer? "职业":"非职业"
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
        },
    }
</script>