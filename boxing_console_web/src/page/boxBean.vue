<template>
    <div class="usermanage">
        <TopBar v-if="isShowTop" firstTitle_name="公司拳豆记录"  disNone="disNone"></TopBar>
        <div class='container'>
            <p class="showTotal">公司账户拳豆汇总:{{moneyTotal}}</p>
            <header>
                 <el-row>
                    <el-col :span="5" style='width:314px'>
                        <el-input v-model="keywards"  class='myInput_40 margin_rt25' placeholder='用户ID/视频名称' style='width:284px'></el-input>
                    </el-col> 
                    <el-col :span='6'>
                        <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
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
                        prop="id"
                        label="ID"
                        >
                        </el-table-column>
                        <el-table-column
                        label="收入/支出"
                        >
                            <template slot-scope="scope">
                                <span>{{scope.row.derection=='in'?'+':'-'}} {{scope.row.account}}</span>                 
                            </template>
                        </el-table-column>
                        <el-table-column
                        prop="time"
                        label="时间"
                        >
                        </el-table-column>
                        <el-table-column
                        prop="description"
                        label="备注"
                        >
                        </el-table-column>
                    </el-table>
                </template>
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
                moneyTotal : 1000000,//付费金额
                total     : 1000,//数据的总条数
                keywards  :'',
                tableData : [
                    {
                        "id": 1,
                        "account": 100,
                        "time": "2017-11-03 19:00:00",
                        "description": "test",
                        "derection":'in'
                    },
                    {
                        "id": 2,
                        "account": 100,
                        "time": "2017-11-03 19:00:00",
                        "description": "test",
                        "derection":'in'
                    },
                    {
                        "id": 3,
                        "account": 100,
                        "time": "2017-11-03 19:00:00",
                        "description": "test",
                        "derection":'in'
                    },
                    {
                        "id": 4,
                        "account": 100,
                        "time": "2017-11-03 19:00:00",
                        "description": "test",
                        "derection":'out'
                    }
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
            getTableData() {
                //获取data数据
                let $this   = this
                this.ajax('/hot_videos','get',{},this.sendData).then(function(res){
                    if(res&&res.data){
                        // console.log(res.data)
                        for(var i=0;i<res.data.results.length;i++){
                            res.data.results[i].price_amount = res.data.results[i].price_amount  ?res.data.results[i].price_amount  :0
                            res.data.results[i].is_show_name = res.data.results[i].is_show?'显示':'隐藏'
                        }
                        // $this.tableData=res.data.results;
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
            toDetail(row){
                //修改详情页
                this.$router.push({path: '/hotvideodetail', query:row});
            },
            changeShow(id){
                // 显示隐藏
                console.log(id)
                let $this = this;
                this.ajax('/','get',{},this.sendData).then(function(res){
                    if(res&&res.data){
                        // console.log(res.data)
                        for(var i=0;i<res.data.results.length;i++){
                            res.data.results[i].price_amount = res.data.results[i].price_amount  ?res.data.results[i].price_amount  :0
                            res.data.results[i].is_show_name = res.data.results[i].is_show?'显示':'隐藏'
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
            openConfirm(id){
                this.confirmData.id    = id
                this.confirmData.isshow= true
            },
            deleteClick(id){
                // 删除
                console.log(id)
                this.ajax('/hot_videos/'+id,'delete').then(function(res){
                    if(res&&res.status==204){
                        for(var i=0;i<$this.tableData.length;i++){
                            if($this.tableData[i].id==id){
                                $this.tableData.splice(i,1)
                                $this.confirmData.isshow=false;
                            }
                        } 
                    }else{
                      console.log(res)  
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
            cancel(val){
                this.confirmData.isshow= val
            }
        },
    }
</script>