<template>
    <div id='report'>
        <TopBar v-if="isShowTop" firstTitle_name="举报处理" disNone="disNone"></TopBar>
        <header style='padding:30px'>
            <div style='margin:20px 0 40px 0'>
                <!-- <el-row>
                    <el-col :span="3" class='header_tab active' @click="changeTab()">未处理</el-col>
                    <el-col :span="3" class='header_tab' @click="changeTab()">已处理</el-col>
                </el-row>   -->
                <template>
                    <el-radio-group v-model="sendData.status">
                        <el-radio-button label="unprocessed">未处理</el-radio-button>
                        <el-radio-button label="processed">已处理</el-radio-button>
                    </el-radio-group>
                </template>
            </div>
            <div class="inline_item">
                <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='用户ID' style='width:18rem'></el-input>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
            </div>
        </header>
        <nav v-show="sendData.status=='unprocessed'">
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
                    label="举报内容"
                    width="90">
                        <template slot-scope="scope">
                            <span class='colorFont' @click='openContent(scope.row.content)'>查看</span>
                        </template>
                    </el-table-column>
                    <el-table-column
                    label="内容类型"
                    prop="content_type"
                    >
                    </el-table-column>
                    <el-table-column
                    label="举报时间"
                    prop="created_time"
                    width="200"
                    >
                    </el-table-column>
                    <!-- <el-table-column
                    label="状态"
                    prop="status"
                    >
                    </el-table-column> -->
                    <el-table-column
                      fixed="right"
                      width='200'
                      label="操作" >
                        <template slot-scope="scope">
                            <el-button class='myBtnHover_red myButton_20' style='margin-right:20px' @click='openConfirm(scope.row.id,false)'>核实为假</el-button>
                            <el-button class='myColor_red myButton_20' style='margin-right:20px' @click='openConfirm(scope.row.id,true)'>删除内容</el-button>                         
                        </template>
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <nav v-show="sendData.status=='processed'">
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
                    label="举报内容"
                    width="90">
                        <template slot-scope="scope">
                            <span class='colorFont' @click='openContent(scope.row.content)'>查看</span>
                        </template>
                    </el-table-column>
                    <el-table-column
                    label="内容类型"
                    prop="content_type"
                    >
                    </el-table-column>
                    <el-table-column
                    label="举报时间"
                    prop="created_time"
                    width="200"
                    >
                    </el-table-column>
                    <!-- <el-table-column
                    label="状态"
                    prop="status"
                    >
                    </el-table-column> -->
                    <el-table-column
                    label="处理结果"
                    prop="result"
                    >
                    </el-table-column>
                    <el-table-column
                    label="处理人"
                    prop="operator"
                    >
                    </el-table-column>
                    <el-table-column
                    label="处理时间"
                    prop="created_time"
                    width="200"
                    >
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <footer v-show="total>10">
            <Pagination :total="total" @changePage="changePage"></Pagination>
        </footer>
        <ReportContent :getData="detailData.allData" :isshow="detailData.isshow" @cancel="cancel"></ReportContent>
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
    import ReportContent from 'page/report_content'
    import Confirm       from "components/confirm"
    export default {
        data() {
            return {
                isShowTop : true,
                total     : 1000,
                issearch  :false,
                sendData  :{
                    search:'',
                    status:'unprocessed',
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
                        "id": 1,
                        "reason": "淫秽色情",
                        "reported_user": 1000008,
                        "content_type": "动态",
                        "status": "未处理",
                        "content": {
                            "id": 1,
                            "user": 1000001,
                            "content": "动态1234",
                            "images": [],
                            "video": null,
                            "is_deleted": true
                        },
                        "created_time": "2018-05-21 15:18:21",
                        "object_id": 1,
                        "remark": null,
                        "user": 1000001
                    },
                    {
                        "id": 2,
                        "reason": "淫秽色情",
                        "reported_user": 1000009,
                        "content_type": "动态",
                        "status": "未处理",
                        "content": {
                            "id": 1,
                            "user": 1000001,
                            "content": "动态1234",
                            "images": [],
                            "video": null,
                            "is_deleted": true
                        },
                        "created_time": "2018-05-21 15:18:21",
                        "object_id": 1,
                        "remark": null,
                        "user": 1000001
                    },
                ],
                tableColumn:[
                    {title:'id',       name :'ID',  width:''},
                    {title:'user',     name :'举报用户ID',    width:''},
                    {title:'reported_user',  name :'被举报用户',   width:''},
                    {title:'reason',   name :'举报理由', width:''},
                ],
            }
        },
        components: {
            TopBar,
            Pagination,
            ReportContent,
            Confirm
        },
        watch:{
           'sendData.status'(val){
                if(this.issearch){
                    this.getData(this.sendData);  
                }else{
                    this.getData({status:val});
                }
           } 
        },
        created() {
            this.getData({status:this.sendData.status});
        },
        methods: {
            getData(data){
                let $this=this
                this.ajax('/report','get',{},data).then(function(res){
                    if(res&&res.data){
                        // console.log(res.data)
                        $this.tableData = res.data.results
                        for(var i=0;i<$this.tableData.length;i++){
                            $this.tableData[i].content_type=$this.tableData[i].content_type=='comment'?'评论':'动态';
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
                console.log(val)
                if(val.pictures&&val.pictures.length>0){
                    for (var i=0;i<val.pictures.length;i++){
                        val.pictures[i] = this.config.baseUrl + val.pictures[i]
                    }
                }
                this.detailData.allData = val;
                this.detailData.isshow  = true
                // console.log(this.detailData.allData)
            },
            openConfirm(id,isDel){
                this.confirmData.id    = id
                this.confirmData.isDel = isDel;
                if(isDel){
                    this.confirmData.content = '您确定核实这条内容，并做删除内容处理'
                }else{
                    this.confirmData.content = '您确定核实这条内容，并做核实为假处理'
                }
                this.confirmData.isshow= true
            },
            changePage(val){
                // 要看第几页
                // console.log(val)
                this.sendData.page=val;
                if(this.issearch){
                   this.getData(this.sendData); 
               }else{
                    this.getData({page:val});
               }
                
            },
            filter(){
                this.issearch=true;
                this.page = 1;
                this.sendData.page = 1;
                this.getData(this.sendData);
            },
            cancel(val){
                this.detailData.isshow  = val ;
            },
            cancel1(val){
                this.confirmData.isshow=val;
            },
            update(id){
                this.confirmData.isshow=false;
                console.log(this.tableData)
                for(var i=0;i<this.tableData.length;i++){
                    console.log(this.tableData[i].id)
                    if(this.tableData[i].id==id){
                        this.tableData.splice(i,1)
                    }
                } 
            },
            conform1(id){
                console.log(id,this.confirmData.isDel)
                let $this=this;
                if(this.confirmData.isDel){
                    //删除
                    this.ajax('/report/'+id+'/do_delete','post').then(function(res){
                        if(res&&res.status==200){
                            // alert('删除成功')
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
                    //核实为假
                    this.ajax('/report/'+id+'/proved_false','post').then(function(res){
                        if(res&&res.status==200){
                            // alert('核实为假')
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