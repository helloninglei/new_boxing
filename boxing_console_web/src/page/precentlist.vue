<template>
    <div id='report'>
        <TopBar v-if="isShowTop" firstTitle_name="财务管理" firstTitle_path="/boxingmanage" secondTitle_name="用户提现记录" secondTitle_path="/addBoxing"></TopBar>
        <header style='padding:30px'>
            <div class="inline_item">
                <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='提现单号、用户ID、用户手机号' style='width:26rem'></el-input>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
            </div>
            <div style='margin:10px 0 40px 0'>
                <template>
                    <el-radio-group v-model="sendData.statusTab">
                        <el-radio-button label="waiting">未审核</el-radio-button>
                        <el-radio-button label="finished">已审核</el-radio-button>
                    </el-radio-group>
                </template>
            </div>
            <el-row v-show="sendData.statusTab=='finished'">
                <el-col :span="5" style='width:314px;margin-bottom:30px'>
                    <el-select v-model="sendData.statusSel" class="margin_rt25">
                        <el-option value="" label="全部"></el-option>
                        <el-option value="approved" label="审核通过">审核通过</el-option>
                        <el-option value="rejected" label="审核未通过">审核未通过</el-option>
                    </el-select>
                </el-col> 
            </el-row>  
        </header>
        <nav v-show="sendData.statusTab=='waiting'">
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
                      width='200'
                      label="操作" >
                        <template slot-scope="scope">
                            <el-button class='myBtnHover_red myButton_20' style='margin-right:20px' @click='openConfirm(scope.row.id,false)'>不通过</el-button>
                            <el-button class='myColor_red myButton_20' style='margin-right:20px' @click='openConfirm(scope.row.id,true)'>通过</el-button>                         
                        </template>
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <nav v-show="sendData.statusTab=='finished'">
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
                    label="审核状态"
                    prop="status"
                    width="200"
                    >
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <footer v-show="total>10">
            <Pagination :total="total" @changePage="changePage" :page='page'></Pagination>
        </footer>
        <Confirm :isshow="confirmData.isshow" @confirm="conform1" @cancel="cancel1()" :content="confirmData.content" :id='confirmData.id'></Confirm>
    </div>
</template>

<style scoped>
    .myColor_red{color:#fff;border-color:#F95862;}
    .header_tab{border:1px solid #F0F2F5;height:36px;line-height:36px;text-align: center;cursor:pointer;}
    .header_tab.active{background:#F0F2F5;}
    
</style>
<style>
    #report .el-radio-group .el-radio-button__orig-radio:checked+.el-radio-button__inner{
        background-color:#F0F2F5;
        color: #303133;
        border-color:#F0F2F5;
        -webkit-box-shadow: -1px 0 0 0 #F0F2F5;
        box-shadow: -1px 0 0 0 #F0F2F5;
    }
    #report .el-radio-button:last-child .el-radio-button__inner{
        border-left-color:#F0F2F5;
    }
    #report .el-radio-group .el-radio-button__inner{
        font-family: PingFangSC-Regular;
        font-size: 14px;
        color: #303133;
        height:36px;
        line-height:36px;
        width:180px;
        padding:0px;
    }
</style>
<script >
    import TopBar  from 'components/topBar';
    import Pagination    from 'components/pagination';
    import Confirm       from "components/confirm"
    export default {
        data() {
            return {
                isShowTop : true,
                total     : 1000,
                issearch  :false,
                page      :1,
                sendData  :{
                    search:'',
                    statusTab:'waiting',
                    statusSel:'',
                },
                detailData:{
                    allData:{},
                    isshow :false,
                },
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'',
                    isDel :true,
                },
                tableData : [
                    {
                        "id": 30,
                        "order_number": "2018052800021",
                        "user_id": "7",
                        "user_nickname": "nick_name",
                        "user_mobile": "19900000000",
                        "created_time": "2018-05-28 17:23:59",
                        "amount": 200,
                        "withdraw_account": "aaaaaa",
                        "status": "审核中"
                    },
                    {
                        "id": 29,
                        "order_number": "2018052800020",
                        "user_id": "7",
                        "user_nickname": "nick_name",
                        "user_mobile": "19900000000",
                        "created_time": "2018-05-28 16:19:44",
                        "amount": 10000,
                        "withdraw_account": "aaaaaa",
                        "status": "审核中"
                    }
                ],
                tableColumn:[
                    {title:'id',       name :'ID',  width:''},
                    {title:'order_number',     name :'提现单号',    width:''},
                    {title:'user_id',  name :'用户ID',   width:'120'},
                    {title:'user_mobile',   name :'用户手机号', width:''},
                    {title:'created_time',   name :'提现时间', width:'200'},
                    {title:'amount',   name :'提现金额（元）', width:'120'},
                    {title:'withdraw_account',   name :'到账支付宝账户', width:''},
                ],
            }
        },
        components: {
            TopBar,
            Pagination,
            Confirm
        },
        watch:{
           'sendData.statusTab'(val){
                if(this.issearch){
                    let data ={ 
                        status:val,
                        search:this.sendData.search,
                    }
                    this.getData(data);  
                }else{
                    this.getData({status:val});
                }
           } ,
           'sendData.statusSel'(val){
                if(this.issearch){
                    let data ={ 
                        status:val,
                        search:this.sendData.search,
                    }
                    this.getData(data);  
                }else{
                    this.getData({status:val});
                }
           } 
        },
        created() {
            this.getData({status:this.sendData.statusTab});
        },
        methods: {
            getData(data){
                let $this=this
                this.ajax('/withdraw_logs','get',{},data).then(function(res){
                    if(res&&res.data){
                        $this.tableData = res.data.results
                        for (var i=0;i<$this.tableData.length;i++){
                            $this.tableData[i].amount = $this.tableData[i].amount /100;
                        }
                        $this.total = res.data.count;
                    }

                },function(err){
                    console.log(err.response.status)
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            console.log(errors[key])
                            // return
                        } 
                    } 
                })
            },
            openContent(val){
                this.detailData.allData = val;
                this.detailData.isshow  = true
            },
            openConfirm(id,isDel){
                this.confirmData.id    = id
                this.confirmData.isDel = isDel;
                if(isDel){
                    // 通过
                    this.confirmData.content = '您确定审核通过'
                }else{
                     // 不通过
                    this.confirmData.content = '您确定审核不通过'
                }
                this.confirmData.isshow= true
            },
            changePage(val){
                // 要看第几页
                // console.log(val)
                let data = {
                    status : this.sendData.statusTab == 'waiting' ? 'waiting' :(this.sendData.statusSel?this.sendData.statusSel:this.sendData.statusTab)
                }
                if(this.issearch){
                    data.search=this.sendData.search
                }
                data.page=val
                this.getData(data);
            },
            filter(){
                let data = {
                    search : this.sendData.search,
                    status : this.sendData.statusTab == 'waiting' ? 'waiting' :(this.sendData.statusSel?this.sendData.statusSel:this.sendData.statusTab)
                }
                this.page = 1;
                data.page = 1;
                this.issearch=true;
                this.getData(data);
            },
            cancel(val){
                this.detailData.isshow  = val ;
            },
            cancel1(val){
                this.confirmData.isshow=val;
            },
            update(id){
                this.confirmData.isshow=false;
                for(var i=0;i<this.tableData.length;i++){
                    if(this.tableData[i].id==id){
                        this.tableData.splice(i,1)
                    }
                } 
            },
            conform1(id){
                let $this=this;
                if(this.confirmData.isDel){
                    //通过
                    this.ajax('withdraw_logs/'+id+'/approved','put').then(function(res){
                        if(res&&res.status==200){
                            // alert('审核通过')
                            $this.update(id);
                        }else{
                          console.log(res)  
                        }

                    },function(err){
                        console.log(err.response.status)
                        if(err&&err.response){
                            let errors=err.response.data
                            for(var key in errors){
                                console.log(errors[key])
                                // return
                            } 
                        } 
                    })
                }else{
                    //不通过
                    this.ajax('withdraw_logs/'+id+'/rejected','put').then(function(res){
                        if(res&&res.status==200){
                            // alert('审核驳回')
                            $this.update(id);
                        }else{
                          console.log(res)  
                        }

                    },function(err){
                        console.log(err.response.status)
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