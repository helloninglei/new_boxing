<template>
    <div class="usermanage">
        <TopBar v-if="isShowTop" firstTitle_name="用户管理" firstTitle_path="/usermanage" disNone="disNone"></TopBar>
        <div class='container'>
            <header>
                 <el-row>
                    <el-col :span="5" style='width:314px'>
                        <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='输入用户/昵称/手机号' style='width:284px'></el-input>
                    </el-col> 
                    <el-col :span="7" style='width:560px'>
                        <el-date-picker
                        v-model="sendData.start_time"
                        type="datetime"
                        value-format="yyyy-MM-dd hh:mm:ss"
                        :default-value= "new Date()"
                        placeholder="注册开始时间" style='width:250px' class="margin_rt25">
                        </el-date-picker>
                        <el-date-picker
                        v-model="sendData.end_time"
                        type="datetime"
                        value-format="yyyy-MM-dd hh:mm:ss"
                        :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                        placeholder="注册结束时间" style='width:250px' class="margin_rt25">
                        </el-date-picker>
                    </el-col> 
                </el-row> 
                <el-row> 
                    <el-col :span="2">
                        <div class="inlimeLabel margin_tp30">用户类别</div>
                    </el-col>
                    <el-col :span="5">
                        <el-select v-model="sendData.is_boxer" class="margin_tp30">
                            <el-option value="" label="全部">全部</el-option>
                            <el-option :value="false" label="普通用户">普通用户</el-option>
                            <el-option :value="true" label="认证拳手">认证拳手</el-option>
                        </el-select>
                    </el-col>
                </el-row>
                <el-row>     
                    <el-col :md="24" :xl='5'>
                        <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 margin_lf70 margin_top_30' @click="filter()">查询</el-button>
                        <el-button  class='myButton_40 btn_width_95 myBtnHover_red' @click='reset()'>重置</el-button>
                    </el-col>     
                </el-row>
            </header>
            <p class="showTotal">注册用户数:{{total}}</p>
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
                        <!-- <el-table-column
                        label="拳豆余额"
                        width="90">
                            <template slot-scope="scope">
                                <span class='colorFont' @click='goboxbeanList(scope.row.id)'>{{scope.row.coin_balance/100}}</span>
                            </template>
                        </el-table-column> -->
                        <el-table-column
                        label="钱包余额"
                        width="90">
                            <template slot-scope="scope">
                                <span class='colorFont' @click='goWalletList(scope.row.id)'>{{(scope.row.money_balance/100).toFixed(2)}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                        label="用户类别"
                        width="150">
                            <template slot-scope="scope">
                                <span class='colorFont' v-if="scope.row.is_boxer" @click='checkIdent(scope.row.boxer_id)'>认证拳手</span>
                                <span class='colorFont' v-else @click='goUserDetail(scope.row)'>普通用户</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                        prop="date_joined"
                        label="注册时间"
                        width="200">
                        </el-table-column>
                        <el-table-column
                          fixed="right"
                          label="操作"
                          width='120'>
                            <template slot-scope="scope">
                                <div style='margin-bottom:9px'> 
                                    <el-button  class='myBtnHover_red myButton_20 ' @click="addCount(scope.row.id,'addCount',scope.$index)">增加用户余额</el-button>
                                </div>
                                <!-- <div> 
                                    <el-button class='myBtnHover_red myButton_20 ' @click="addCount(scope.row.id,'addBean',scope.$index)">增加用户拳豆</el-button>
                                </div>   -->                        
                            </template>
                        </el-table-column>
                    </el-table>
                </template>
            </nav>
            <footer v-show="total>10">
                <Pagination :total="total" @changePage="changePage" :page='page'></Pagination>
            </footer>
        </div>
        <DialogLabel :isshow="dialog_label_data.isshow" @confirm="confirm" @cancel="cancel3()" :content_title="dialog_label_data.content_title" :content_foot="dialog_label_data.content_foot" :type="'number'"></DialogLabel>
    </div>
</template>
<style scoped>
    .myTable{font-size:14px!important;}
    .inlimeLabel{font-family: PingFangSC-Regular;font-size: 16px;color: #000000;padding-right:15px;height:40px;line-height:40px;}
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
    import DialogLabel from "components/dialog_label"
    export default {
        data() {
            return {
                isShowTop : true,
                issearch  :false,
                sendData  : {
                    start_time : '',
                    end_time   : '',
                    search  : '',
                    is_boxer  : '',
                },
                dialog_label_data:{
                    isshow:false,
                    content_title:"",
                },
                addData :{
                    addType:''
                },
                page:1,
                userTotal : 1000000,//注册人数
                total     : 1000,//数据的总条数
                tableData : [
                    {
                        "id": 1, 
                        "mobile": "111111111111", 
                        "date_joined": "2018-01-01 10-11-11", 
                        "user_basic_info": {
                            "name": "王毅", 
                            "weight": "120kg", 
                            "nick_name": "小王", 
                            "gender": '男', 
                            "profession": "计算机", 
                            "nation": "", 
                            "birthday": "1996-2-4", 
                            "address": "上海市普陀区金沙江路 1518 弄", 
                            "height": "188",
                            "is_boxer":true,//模拟数据用户类型
                            "following_count":100,//模拟数据关注数
                            "follower_count":100,//模拟数据粉丝数
                            "share_count":100,//模拟数据分享数
                        }
                    }, 
                    {
                        "id": 2, 
                        "mobile": "111111111111", 
                        "date_joined": "2018-01-01 10-11-11", 
                        "user_basic_info": {
                            "name": "王毅", 
                            "weight": "120kg", 
                            "nick_name": "小王", 
                            "gender": '男', 
                            "profession": "计算机", 
                            "nation": "", 
                            "birthday": "1996-2-4", 
                            "address": "上海市普陀区金沙江路 1518 弄", 
                            "height": "188",
                            "is_boxer":false,//模拟数据用户类型
                            "following_count":100,//模拟数据关注数
                            "follower_count":100,//模拟数据粉丝数
                            "share_count":100,//模拟数据分享数
                        }
                    }
                ],
                tableColumn:[
                    {title:'id',    name :'用户ID',   width: '80'},
                    {title:'mobile',name :'用户手机号',width: '120'},
                    {title:'user_basic_info.gender',   name :'性别'    ,width: '80'},
                    {title:'user_basic_info.nick_name',name :'用户昵称' ,width: '100'},
                    {title:'user_basic_info.address',  name :'居住地'   ,width: ''},
                    {title:'following_count',name :'关注数' ,width: '90'},
                    {title:'follower_count',  name :'粉丝数' ,width: '90'},
                    {title:'share_count',name :'分享数' ,width: '90'},
                ],
            }
        },
        components: {
            TopBar,
            Table,
            Pagination,
            DialogLabel
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
                   sendData=this.sendData
                }
                if(page){
                    sendData.page=page
                }
                
                this.ajax('/users','get',{},sendData).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        for(var i=0;i<res.data.results.length;i++){
                            res.data.results[i].user_basic_info=res.data.results[i].user_basic_info?res.data.results[i].user_basic_info:{}
                            res.data.results[i].user_basic_info.gender=res.data.results[i].user_basic_info.gender?'男':'女'
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
            addCount(id,addType,index){
                this.addData.addType=addType
                this.addData.user=id
                this.addData.index=index
                if(addType=='addBean'){
                    this.dialog_label_data.content_title='增加拳豆余额'
                }else{
                    this.dialog_label_data.content_title='增加钱包余额'
                }
                
                this.dialog_label_data.isshow=true
            },

            changePage(val){
                // 要看第几页
                this.page=val
                this.getTableData(val)
            },
            filter(){
                this.issearch=true;
                //搜索是先看第一页
                this.page=1
                this.getTableData(1) 
            },
            goWalletList(id){
                //去钱包流水页面
                console.log(id)
                this.$router.push({path: '/walletlist', query:{id:id}});
            },

            goboxbeanList(id){
                //去拳豆余额页面
                console.log(id)
                this.$router.push({path: '/boxbeanlist', query:{id:id}});
            },
            goUserDetail(row){
                //去普通用户列表
                console.log(row.user_basic_info)
                this.$router.push({path: '/userdetail', query:row.user_basic_info});
            },
            checkIdent(id){
                // console.log('查看认证信息'+id)
                this.$router.push({path: '/Boxerindentdetail', query:{id:id}});
            },
            reset(){
                this.sendData={};
                this.getTableData();
            },
            cancel3(val){
                this.dialog_label_data.isshow=val;
            },
            confirm(val){
                let $this = this;
                if(this.addData.addType=='addBean'){
                    //增加拳豆
                    this.addData.change_amount=val;
                    this.addData.change_type='INCREASE_COIN_OFFICIAL_RECHARGE';

                    this.ajax('/coin/change','post',this.addData).then(function(res){
                        if(res&&res.data){
                            $this.tableData[$this.addData.index].coin_balance = res.data.remain_amount
                            $this.dialog_label_data.isshow=false;
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
                }else{
                    //增加钱包余额
                    this.addData.change_amount=val*100;
                    this.addData.change_type='INCREASE_MONEY_OFFICIAL_RECHARGE';
                    this.ajax('/money/change','post',this.addData).then(function(res){
                        if(res&&res.data){
                            $this.tableData[$this.addData.index].money_balance = res.data.remain_amount
                            $this.dialog_label_data.isshow=false;
                            
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
                }

            },
        },
    }
</script>