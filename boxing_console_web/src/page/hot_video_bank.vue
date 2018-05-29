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
                    <el-col :span='24'>
                        <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25'  @click="toDetail()" style='margin-top:30px'>新增视频</el-button>
                    </el-col>   
                </el-row>
            </header>
            <p class="showTotal">付费人数:{{userTotal}} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;付费金额(元)：{{moneyTotal}}</p>
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
                        <el-table-column
                          fixed="right"
                          label="操作">
                            <template slot-scope="scope">
                                    <el-button  class='myBtnHover_red myButton_20' @click="toDetail(scope.row)">修改</el-button>
                                    <el-button class='myBtnHover_red myButton_20 ' @click="openConfirm(scope.row.id)">删除</el-button>                          
                                    <el-button class='myBtnHover_red myButton_20 ' @click="changeShow(scope.row.id,!scope.row.is_show,scope.$index)">{{scope.row.is_show?'隐藏':'显示'}}</el-button>                          
                            </template>
                        </el-table-column>
                    </el-table>
                </template>
            </nav>
            <footer>
                <Pagination :total="total" @changePage="changePage"></Pagination>
            </footer>
        </div>
        <Confirm :isshow="confirmData.isshow" @confirm="deleteClick" @cancel="cancel()" :content="confirmData.content" :id='confirmData.id'></Confirm>
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
    import Confirm     from "components/confirm"
    export default {
        data() {
            return {
                isShowTop : true,
                issearch  :false,
                sendData  : {
                    start_time : '',
                    end_time   : '',
                    keywards  : '',
                },
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'确定删除这条记录？',
                    isDel :true,
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
                        "try_url": "11111222",
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
                        "try_url": "http://127.0.0.1:8000/hot_videos1",
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
                        "try_url": "http://127.0.0.1:8000/hot_videos1",
                        "price": 22222,
                        "is_show": false,
                        "created_time": "2018-05-10 18:23:49"
                    }
                ],
                tableColumn:[
                    {title:'id',    name :'ID',   width: '80'},
                    {title:'name',  name :'视频名称',width: ''},
                    {title:'user_id',name :'用户ID' ,width: '80'},
                    {title:'price',name :'价格（元）',width: '100'},
                    {title:'sales_count', name :'付费人数'   ,width: ''},
                    {title:'price_amount',name :'付费金额（元）',width: '90'},
                    {title:'created_time',name :'发布时间' ,width: '200'},
                    {title:'is_show_name',name :'显示状态' ,width: '90'},
                ],
            }
        },
        components: {
            TopBar,
            Table,
            Pagination,
            Confirm
        },
        created() {
            this.getTableData();
        },
        methods: {
            getTableData(page) {
                //获取data数据
                let $this   = this
                if(this.issearch){
                    let sendData=this.sendData
                }else{
                    let sendData={}
                }
                if(page){
                    sendData.page=page
                }
                this.ajax('/hot_videos','get',{},this.sendData).then(function(res){
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
            changePage(val){
                // 要看第几页
                this.getTableData(val) 
            },
            filter(){
                this.issearch=true;
                //搜索是先看第一页
                this.getTableData(1) 
            },
            toDetail(row){
                //修改详情页
                this.$router.push({path: '/hotvideodetail', query:row});
            },
            changeShow(id,isshow,index){
                // 显示隐藏
                console.log(index)
                let $this = this;
                // this.gc[0] ={name:'lisi',age:22} //这样直接修改不能被vue监听到
                let resData = {
                                    "id": 1,
                                    "user_id": 1000000,
                                    "name": "222",
                                    "description": "333",
                                    "sales_count": 0,
                                    "price_amount": null,
                                    "url": "/uploads/a1/ff/7fb7421ef9b445bae16be8f7a96820723e7d.mp4",
                                    "try_url": "/uploads/a1/ff/7fb7421ef9b445bae16be8f7a96820723e7d.mp4",
                                    "price": 222,
                                    "is_show": isshow,
                                    "created_time": "2018-05-11 18:15:36"
                                }
                resData.is_show_name = resData.is_show?'显示':'隐藏'
                $this.tableData.splice(index,1,resData);
                // this.ajax('/hot_videos/'+id,'patch',{isshow:isshow}).then(function(res){
                //     if(res&&res.data){
                //         console.log(res.data)
                //         $this[index] = res.data
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
            openConfirm(id){
                this.confirmData.id    = id
                this.confirmData.isshow= true
            },
            deleteClick(id){
                // 删除
                let $this=this
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