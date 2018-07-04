<template>
    <div class="usermanage">
        <TopBar v-if="isShowTop" firstTitle_name="用户管理" firstTitle_path="/usermanage" disNone="disNone"></TopBar>
        <div class='container'>
            <header>
                 <el-row>
                    <el-col :span="5" style='width:314px'>
                        <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='请输入用户ID/昵称/手机号' style='width:284px'></el-input>
                    </el-col> 
                    <el-col :span="7" style='width:560px'>
                        <el-date-picker
                        v-model="sendData.start_time"
                        type="datetime"
                        value-format="yyyy-MM-dd HH:mm:ss"
                        :default-value= "new Date()"
                        placeholder="注册开始时间" style='width:250px' class="margin_rt25">
                        </el-date-picker>
                        <el-date-picker
                        v-model="sendData.end_time"
                        type="datetime"
                        value-format="yyyy-MM-dd HH:mm:ss"

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
                    <el-col :span="5">
                        <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 margin_lf70 margin_top_30' @click="filter()">查询</el-button>
                        <el-button  class='myButton_40 btn_width_95 myBtnHover_red' @click='reset()'>重置</el-button>
                    </el-col> 
                </el-row>
                <!-- <el-row>     
                    <el-col :md="24" :xl='5'>
                        <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 margin_lf70 margin_top_30' @click="filter()">查询</el-button>
                        <el-button  class='myButton_40 btn_width_95 myBtnHover_red' @click='reset()'>重置</el-button>
                    </el-col>     
                </el-row> -->
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
                        width="70">
                            <template slot-scope="scope">
                                <span class='colorFont' v-if="scope.row.is_boxer" @click='checkIdent(scope.row.boxer_id)'>认证拳手</span>
                                <span class='colorFont' v-else @click='goUserDetail(scope.row)'>{{scope.row.user_type}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                        label="认证称号"
                        width="100">
                            <template slot-scope="scope">
                                <span>{{scope.row.title?scope.row.title:'--'}}</span>
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
                                    <el-button  class='myBtnHover_red myButton_20 ' @click="addCount(scope.row,scope.$index)">编辑</el-button>
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
        <DialogLabel :isshow="dialog_label_data.isshow" @confirm="confirm" @cancel="cancel3()" :nick_name="dialog_label_data.nick_name" :row="addData.row" :index='addData.index'></DialogLabel>
    </div>
</template>
<style scoped>
    .myTable{font-size:14px!important;}
    .inlimeLabel{font-family: PingFangSC-Regular;font-size: 16px;color: #000000;padding-right:15px;height:40px;line-height:40px;}
    .margin_top_30{margin-top:30px;margin-left:0!important;} 
</style>
<style>
</style>
<script>
    import TopBar from 'components/topBar';
    import Table  from 'components/table';
    import Pagination  from 'components/pagination';
    import DialogLabel from "components/dialog_manage"
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
                    nick_name:"",
                },
                addData :{
                    row:{},
                    index:''
                },
                page:1,
                userTotal : 1000000,//注册人数
                total     : 1000,//数据的总条数
                tableData : [
                    {
                        "id": 1,  // 用户id
                        "mobile": "19990000000",  //手机号
                        "following_count": 0,  // 关注数
                        "follower_count": 0,  // 粉丝数
                        "share_count": 0,  // 分享数
                        "money_balance": 0,  // 钱包余额
                        "is_boxer": false,  // 是否认证拳手  true，拳手，false，普通用户
                        "user_basic_info": {
                            "nick_name": "我是是个汉子哈哈哈哈",  // 昵称
                            "gender": true,    // 性别   true，男，false，女
                            "address": null,  // 地址
                            "name": "哈哈",// 姓名
                            "nation": "汉子",  //民族
                            "birthday": "2018-09-09",// 生日
                            "height": 170,  // 身高
                            "weight": 45,  // 体重
                            "profession": "医生" // 职业
                        },
                        user_type:'普通用户',
                        title:'北京拳首',
                        "date_joined": "2018-05-11 16-49-10",  // 注册时间
                        "boxer_id": null  // 拳手id
                    },
                    {
                        "id": 2,  // 用户id
                        "mobile": "19990000000",  //手机号
                        "following_count": 0,  // 关注数
                        "follower_count": 0,  // 粉丝数
                        "share_count": 0,  // 分享数
                        "money_balance": 0,  // 钱包余额
                        "is_boxer": false,  // 是否认证拳手  true，拳手，false，普通用户
                        "user_basic_info": {
                            "nick_name": "我是是个汉子哈哈哈哈",  // 昵称
                            "gender": true,    // 性别   true，男，false，女
                            "address": null,  // 地址
                            "name": "哈哈",// 姓名
                            "nation": "汉子",  //民族
                            "birthday": "2018-09-09",// 生日
                            "height": 170,  // 身高
                            "weight": 45,  // 体重
                            "profession": "医生" // 职业
                        },
                        user_type:'认证拳手',
                        title:'北京拳首',
                        "date_joined": "2018-05-11 16-49-10",  // 注册时间
                        "boxer_id": null  // 拳手id
                    },
                    {
                        "id": 3,  // 用户id
                        "mobile": "19990000000",  //手机号
                        "following_count": 0,  // 关注数
                        "follower_count": 0,  // 粉丝数
                        "share_count": 0,  // 分享数
                        "money_balance": 0,  // 钱包余额
                        "is_boxer": false,  // 是否认证拳手  true，拳手，false，普通用户
                        "user_basic_info": {
                            "nick_name": "我是是个汉子哈哈哈哈",  // 昵称
                            "gender": true,    // 性别   true，男，false，女
                            "address": null,  // 地址
                            "name": "哈哈",// 姓名
                            "nation": "汉子",  //民族
                            "birthday": "2018-09-09",// 生日
                            "height": 170,  // 身高
                            "weight": 45,  // 体重
                            "profession": "医生" // 职业
                        },
                        user_type:'自媒体',
                        title:'北京拳首',
                        "date_joined": "2018-05-11 16-49-10",  // 注册时间
                        "boxer_id": null  // 拳手id
                    },
                ],
                tableColumn:[
                    {title:'id',    name :'用户ID',   width: '45'},
                    {title:'mobile',name :'用户手机号',width: '120'},
                    {title:'user_basic_info.gender',   name :'性别'    ,width: '30'},
                    {title:'user_basic_info.nick_name',name :'用户昵称' ,width: '100'},
                    {title:'user_basic_info.address',  name :'居住地'   ,width: ''},
                    {title:'following_count',name :'关注数' ,width: '60'},
                    {title:'follower_count',  name :'粉丝数' ,width: '60'},
                    {title:'share_count',name :'分享数' ,width: '60'},
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
                for(var i=0;i<this.tableData.length;i++){
                    this.tableData[i].user_basic_info=this.tableData[i].user_basic_info?this.tableData[i].user_basic_info:{}
                    this.tableData[i].user_basic_info.gender=this.tableData[i].user_basic_info.gender?'男':'女'
                }


                //获取data数据
                let $this   = this
                let sendData={}
                if(this.issearch){
                   sendData=this.sendData
                }
                if(page){
                    sendData.page=page
                }
                
                // this.ajax('/users','get',{},sendData).then(function(res){
                //     if(res&&res.data){
                //         for(var i=0;i<res.data.results.length;i++){
                //             res.data.results[i].user_basic_info=res.data.results[i].user_basic_info?res.data.results[i].user_basic_info:{}
                //             res.data.results[i].user_basic_info.gender=res.data.results[i].user_basic_info.gender?'男':'女'
                //         }
                //         $this.tableData=res.data.results;//后台没数据先不用
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
            addCount(row,index){
                // console.log(row)
                this.addData.row = row
                this.addData.index = index
                this.dialog_label_data.nick_name=row.user_basic_info.nick_name
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
                this.$router.push({path: '/userdetail', query:row});
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
                // console.log(val)
                // this.ajax('','post',this.addData).then(function(res){
                //     if(res&&res.data){
                //         $this.tableData[$this.addData.index].coin_balance = res.data.remain_amount
                //         $this.dialog_label_data.isshow=false;
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