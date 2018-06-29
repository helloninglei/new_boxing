<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="拳手认证审核管理" disNone="disNone"></TopBar>
        <div class='container'>
            <header>
                <div class="inline_item">
                    <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='昵称/姓名/手机号' style='width:18rem'></el-input>
                </div>
                <div class="inline_item">
                    <span class="inlimeLabel">选手类型</span>
                    <el-select v-model="sendData.is_professional_boxer" class="margin_rt25" style='width:11rem'>
                        <el-option value="" label="全部">全部</el-option>
                        <el-option :value="true" label="职业">职业</el-option>
                        <el-option :value="false" label="非职业">非职业</el-option>
                    </el-select>
                </div>
                <div class="inline_item">
                    <span class="inlimeLabel">审核状态</span>
                    <el-select v-model="sendData.authentication_state" class="margin_rt25" style='width:11rem'>
                        <el-option value="" label="全部">全部</el-option>
                        <el-option value="APPROVED" label="已通过">已通过</el-option>
                        <el-option value="REFUSE" label="已驳回">已驳回</el-option>
                        <el-option value="WAITING" label="待审核">待审核</el-option>
                    </el-select>
                </div>
                <div class="inline_item">
                    <span class="inlimeLabel">接单状态</span>
                    <el-select v-model="sendData.is_locked" style='width:11rem;margin-right:80px'>
                        <el-option value="" label="全部">全部</el-option>
                        <el-option :value="true" label="已锁定">已锁定</el-option>
                        <el-option :value="false" label="已解锁">已解锁</el-option>
                    </el-select>
                </div>
                <div class="inline_item">
                    <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
                    <el-button  class='myButton_40 btn_width_95' @click='refuse()'>重置</el-button>
                </div>
            </header>
            <nav>
               <Table :tableColumn="tableColumn" :tableData="tableData" @toDetail="toDetail" @btnLeftClick="changeLockType" :showBtnLeft="true"></Table> 
            </nav>
            <footer v-show="total>10">
                <Pagination :total="total" @changePage="changePage" :page='page'></Pagination>
            </footer>
        </div>
    </div>
</template>
<style scoped>
    header{clear:both;margin-bottom:21px;}
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
                issearch  : false,
                page      : 1,
                sendData  : {
                    search     : '',
                    authentication_state : '',
                    is_locked  : '',
                    is_professional_boxer : '',
                },
                total     : 1000,
                tableData : [
                    {
                        "id": 1, // 拳手ID
                        "honor_certificate_images": [], // 拳手荣誉证书
                        "competition_video": null, // 拳手参赛视频
                        "nick_name": "赵柳", // 拳手昵称
                        "allowed_lessons": [], // 可开课程
                        "created_time": "2018-05-18 00:27:43",
                        "updated_time": "2018-05-18 00:27:47",
                        "real_name": "张三", // 拳手真实姓名
                        "height": 170, // 身高
                        "weight": 65, // 体重
                        "birthday": "2018-05-17", // 出生日期
                        "identity_number": "111111111111111111", //身份证
                        "mobile": "11111111111", //手机
                        "is_professional_boxer": true, //是否是专业拳手
                        "club": "20", // 所属拳馆
                        "job": "teacher", // 职业
                        "introduction": "哈哈", //个人介绍
                        "is_locked": true, // 接单状态 true锁定，false解锁
                        "experience": null, // 个人经历
                        "authentication_state": "APPROVED", // 认证状态（APPROVED：已通过| WAITING：待审核 | REFUSE：已驳回）
                        "refuse_reason": null, // 驳回原因
                        "user": 5 // 用户ID
                    },
                    
                ],
                tableColumn:[
                    {title:'id',              name :'申请编号',   width:''},
                    {title:'updated_time',    name :'申请时间', width:'200'},
                    {title:'nick_name',       name :'昵称',   width:''},
                    {title:'real_name',       name :'姓名',   width:''},
                    {title:'mobile',          name :'手机号', width:''},
                    {title:'professional_boxer', name :'选手类型', width:''},
                    {title:'authentication_name',name :'审核状态',   width:''},
                    {title:'lock_name',       name :'接单状态',   width:''},
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
                let $this   = this
                let sendData={}
                if(this.issearch){
                   sendData=this.sendData
                }
                if(page){
                    sendData.page=page
                }
                this.ajax('/boxer/identification','get',{},sendData).then(function(res){
                    if(res&&res.data){
                        $this.tableData=res.data.results;
                        for(var i=0;i<$this.tableData.length;i++){
                            $this.tableData[i].professional_boxer=$this.tableData[i].is_professional_boxer? "职业":"非职业"
                            $this.tableData[i].lock_name=$this.tableData[i].authentication_state=='WAITING'? '--' :$this.tableData[i].is_locked? "已锁定":"已解锁"  
                            if($this.tableData[i].authentication_state=='APPROVED'){
                                $this.tableData[i].authentication_name="已通过"
                            }else if($this.tableData[i].authentication_state=='REFUSE'){
                                $this.tableData[i].authentication_name="已驳回"
                            }else{
                                $this.tableData[i].authentication_name="待审核"
                            }
                        }
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
                // 参数 ID 审核状态 authentication_state
                this.$router.push({path: '/Boxerindentdetail', query:{id:row.id,authentication_state:row.authentication_state}});

            },
            changeLockType(row,$index){
                let $this    = this; 
                let is_locked=row.is_locked? "UNLOCK":"LOCK" 
                this.ajax('/boxer/identification/'+row.id+'/'+is_locked,'post').then(function(res){
                    // console.log(res.status)
                    if(res.status==204){
                        // $this.getTableData($this.page)
                        row.is_locked = !row.is_locked
                        row.lock_name = row.is_locked? "已锁定":"已解锁" 
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
            filter(){
                this.issearch=true;
                //搜索是先看第一页
                this.page=1
                this.getTableData(1) 
            },
            refuse(){
                this.sendData={};
                this.getTableData();
            }
        },
    }
</script>