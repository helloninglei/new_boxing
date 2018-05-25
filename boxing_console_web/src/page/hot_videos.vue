<template>
    <div class="usermanage">
        <TopBar v-if="isShowTop" firstTitle_name="热门视频" firstTitle_path="/usermanage" disNone="disNone"></TopBar>
        <div class='container'>
            <header>
                 <el-row>
                    <el-col :span="5" style='width:314px'>
                        <el-input v-model="sendData.keywards"  class='myInput_40 margin_rt25' placeholder='用户ID/视频名称' style='width:284px'></el-input>
                    </el-col> 
                    <el-col :span="7" style='width:460px'>
                        <el-date-picker
                        v-model="sendData.start_time"
                        type="datetime"
                        value-format="yyyy-MM-dd hh:mm:ss"
                        :default-value= "new Date()"
                        placeholder="发布开始时间" style='width:200px' class="margin_rt25">
                        </el-date-picker>
                        <el-date-picker
                        v-model="sendData.end_time"
                        type="datetime"
                        value-format="yyyy-MM-dd hh:mm:ss"
                        :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                        placeholder="发布结束时间" style='width:200px' class="margin_rt25">
                        </el-date-picker>
                    </el-col>      
                    <el-col :span='6'>
                        <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
                        <el-button  class='myButton_40 btn_width_95 myBtnHover_red'>重置</el-button>
                    </el-col>     
                </el-row>
            </header>
            <p class="showTotal">付费人数:{{userTotal}} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;付费金额(元)：{{moneyTotal}}</p>
            <nav class='myTable'>
                <Table :tableColumn="tableColumn" :tableData="tableData" @toDetail="toDetail" :showBtn1="true"></Table>
            </nav>
            <footer>
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
                sendData  : {
                    start_time : '',
                    end_time   : '',
                    keywards  : '',
                },
                userTotal : 1000000,//付费人数
                moneyTotal : 1000000,//付费金额
                total     : 1000,//数据的总条数
                tableData : [
                    {
                        "id": 1,
                        "user_id": 1,
                        "name": "test",
                        "description": "test",
                        "sales_count": 0,
                        "price_amount": null,
                        "url": "1111",
                        "try_url": "1111",
                        "price": 111,
                        "is_show": true,
                        "created_time": "2018-05-10 18:51:03"
                    },
                    {
                        "id": 2,
                        "user_id": 1,
                        "name": "2",
                        "description": "9992",
                        "sales_count": 0,
                        "price_amount": null,
                        "url": "http://127.0.0.1:8000/hot_videos",
                        "try_url": "http://127.0.0.1:8000/hot_videos",
                        "price": 22222,
                        "is_show": true,
                        "created_time": "2018-05-10 18:34:43"
                    },
                    {
                        "id": 3,
                        "user_id": 1,
                        "name": "2",
                        "description": "999",
                        "sales_count": 0,
                        "price_amount": null,
                        "url": "http://127.0.0.1:8000/hot_videos",
                        "try_url": "http://127.0.0.1:8000/hot_videos",
                        "price": 22222,
                        "is_show": false,
                        "created_time": "2018-05-10 18:23:49"
                    }
                ],
                tableColumn:[
                    {title:'id',    name :'ID',   width: '80'},
                    {title:'name',name :'视频名称',width: ''},
                    {title:'user_id',   name :'用户ID'    ,width: '80'},
                    {title:'price',name :'价格（元）' ,width: '100'},
                    {title:'sales_count',  name :'付费人数'   ,width: ''},
                    {title:'price_amount',name :'付费金额（元）' ,width: '90'},
                    {title:'created_time',  name :'发布时间' ,width: '200'},
                    {title:'is_show',name :'显示状态' ,width: '90'},
                ],
            }
        },
        components: {
            TopBar,
            Table,
            Pagination
        },
        created() {
            this.getTableData();
        },
        methods: {
            getTableData() {
                //获取data数据
                let $this   = this
                this.ajax('/hot_videos','get',{},this.sendData).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        for(var i=0;i<res.data.results.length;i++){
                            res.data.results[i].price_amount = res.data.results[i].price_amount  ?res.data.results[i].price_amount  :0
                            res.data.results[i].is_show      = res.data.results[i].is_show?'显示':'隐藏'
                        }
                        $this.tableData=res.data.results;//后台没数据先不用
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
                console.log(this.sendData)
            },
            toDetail(){

            }
        },
    }
</script>