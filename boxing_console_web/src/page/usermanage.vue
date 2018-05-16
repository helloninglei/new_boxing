<template>
    <div class="usermanage">
        <TopBar v-if="isShowTop" firstTitle_name="用户管理" firstTitle_path="/usermanage" disNone="disNone"></TopBar>
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
                <el-button  class='myButton_40 btn_width_95 myBtnHover_red'>重置</el-button>
            </header>
            <p class="showTotal">注册用户数:{{userTotal}}</p>
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
                        label="拳豆余额"
                        width="90">
                            <template slot-scope="scope">
                                <!-- <span class='colorFont' >{{"1000"}}</span> -->
                                <span class='' >{{"1000"}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                        label="钱包余额"
                        width="90">
                            <template slot-scope="scope">
                                <span class='colorFont' @click='goWalletList(scope.row.id)'>{{"2000"}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                        label="用户类别"
                        width="150">
                            <template slot-scope="scope">
                                <span class='colorFont' v-if="scope.row.user_basic_info.userType==1" @click='goUserDetail(scope.row)'>普通用户</span>
                                <span class='colorFont' v-if="scope.row.user_basic_info.userType==2" @click='checkIdent(scope.row.id)'>认证拳手</span>
                            </template>
                        </el-table-column>
                        <el-table-column
                        prop="date_joined"
                        label="注册时间"
                        width="200">
                        </el-table-column>
                        <el-table-column
                          fixed="right"
                          label="操作">
                            <template slot-scope="scope">
                                <div style='margin-bottom:9px'> 
                                    <el-button  class='myBtnHover_red myButton_20 ' @click="handleClick(scope.row.id)">增加用户余额</el-button>
                                </div>
                                <div> 
                                    <el-button class='myBtnHover_red myButton_20 '>增加用户拳豆</el-button>
                                </div>                          
                            </template>
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
</style>
<style>
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
                    startTime : '',
                    endTime   : '',
                    keywards  : '',
                    userType  : '',
                },
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
                            "userType":2,//模拟数据用户类型
                            "gaunzhu_num":100,//模拟数据关注数
                            "fensi_num":100,//模拟数据粉丝数
                            "fenxiang_num":100,//模拟数据分享数
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
                            "userType":1,//模拟数据用户类型
                            "gaunzhu_num":100,//模拟数据关注数
                            "fensi_num":100,//模拟数据粉丝数
                            "fenxiang_num":100,//模拟数据分享数
                        }
                    }
                ],
                tableColumn:[
                    {title:'id',    name :'用户ID',   width: '80'},
                    {title:'mobile',name :'用户手机号',width: ''},
                    {title:'user_basic_info.gender',   name :'性别'    ,width: '80'},
                    {title:'user_basic_info.nick_name',name :'用户昵称' ,width: '100'},
                    {title:'user_basic_info.address',  name :'居住地'   ,width: ''},
                    {title:'user_basic_info.gaunzhu_num',name :'关注数' ,width: '90'},
                    {title:'user_basic_info.fensi_num',  name :'粉丝数' ,width: '90'},
                    {title:'user_basic_info.fenxiang_num',name :'分享数' ,width: '90'},
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
                this.ajax('/users','get',{},this.sendData).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        for(var i=0;i<res.data.results.length;i++){
                            res.data.results[i].user_basic_info=res.data.results[i].user_basic_info?res.data.results[i].user_basic_info:{}
                        }
                        // $this.tableData=res.data.results;//后台没数据先不用
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
            handleClick(row){
                console.log(row.id)
            },
            changePage(val){
                // 要看第几页
                console.log(val)
            },
            goWalletList(id){
                //去钱包流水页面
                console.log(id)
                this.$router.push({path: '/walletlist', query:{id:id}});
            },
            goUserDetail(row){
                //去普通用户列表
                console.log(row)
                this.$router.push({path: '/userdetail', query:row});
            },
            checkIdent(id){
                console.log('查看认证信息'+id)
            }
        },
    }
</script>