<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="约单管理" firstTitle_path="/classall" secondTitle_name="课程管理" secondTitle_path="/classmanage"></TopBar>
        <div class='container'>
            <header>
                <div class="inline_item">
                    <span class="inlimeLabel">拳手</span>
                    <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='姓名/手机号' style='width:18rem'></el-input>
                </div>
                <div class="inline_item">
                    <span class="inlimeLabel">价格区间</span>
                    <el-input v-model="sendData.price_min_int"  class='myInput_40' type='number' style='width:9rem' placeholder='请输入'></el-input>
                    <span>-</span>
                    <el-input v-model="sendData.price_max_int"  class='myInput_40 margin_rt25' type='number' style='width:9rem' placeholder='请输入'></el-input>
                </div>
                <div class="inline_item">
                    <span class="inlimeLabel">已开课程</span>
                    <el-select v-model="sendData.course_name" class="margin_rt25" style='width:11rem'>
                        <el-option value="" label="全部">全部</el-option>
                        <el-option value="拳击" label="拳击">拳击</el-option>
                        <el-option value="自由搏击" label="自由搏击">自由搏击</el-option>
                        <el-option value="MMA" label="MMA">MMA</el-option>
                    </el-select>
                </div>
                <div class="inline_item">
                    <span class="inlimeLabel">接单状态</span>
                    <el-select v-model="sendData.is_accept_order" style='width:11rem'>
                        <el-option value="" label="全部">全部</el-option>
                        <el-option :value="1" label="是">是</el-option>
                        <el-option :value="0" label="否">否</el-option>
                    </el-select>
                </div>
                <div style='margin-bottom:50px;margin-left:52px'>
                    <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
                    <el-button  class='myButton_40 btn_width_95' @click="refresh()">重置</el-button>
                </div>
            </header>
            <nav>
               <Table :tableColumn="tableColumn" :tableData="tableData" @toDetail="toDetail" :showBtn1="true"></Table> 
            </nav>
            <footer v-show='total>10'>
                <Pagination :total="total" @changePage="changePage" :page='page'></Pagination>
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
<script>
    import TopBar from 'components/topBar';
    import Table  from 'components/table';
    import Pagination  from 'components/pagination';
    export default {
        data() {
            return {
                isShowTop : true,
                page      : 1,
                issearch  : false,
                sendData  : {
                    price_min_int  : '',
                    price_max_int  : '',
                    price_min  : '',
                    price_max  : '',
                    search     : '',
                    course_name : '',
                    is_accept_order : '',
                },
                total     : 20,
                tableData : [
                    
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
            getTableData(page) {
                //获取data数据
                let $this    = this
                let sendData={}
                if(this.issearch){
                   sendData=this.sendData
                   sendData.price_min = this.sendData.price_min_int?this.sendData.price_min_int*100:'';
                   sendData.price_max = this.sendData.price_max_int?this.sendData.price_max_int*100:'';
                }
                if(page){
                    sendData.page=page
                }
                this.ajax('/courses','get',{},sendData).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        for(var i=0;i<res.data.results.length;i++){
                            res.data.results[i].professional_boxer=res.data.results[i].is_professional_boxer? "职业":"非职业"
                            res.data.results[i].is_accept_order=res.data.results[i].is_accept_order? "是":"否"
                            res.data.results[i].price=(res.data.results[i].price/100).toFixed(2);
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
                this.getTableData(val) 
            },
            toDetail(row){
                this.$router.push({path: '/classdetail', query:{id:row.id}});

            },
            filter(){
                this.issearch=true;
                //搜索是先看第一页
                this.page=1
                this.getTableData(1) 
            },
            refresh(){
                this.sendData={};
                this.getTableData() 
            }
        },
    }
</script>