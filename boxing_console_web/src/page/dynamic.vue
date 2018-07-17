<template>
    <div id='report'>
        <TopBar v-if="isShowTop" firstTitle_name="动态管理" firstTitle_path="/dynamic" secondTitle_name="动态列表" secondTitle_path="/dynamic"></TopBar>
        <header style='padding:30px'>
            <div class="inline_item">
                <el-row>
                    <el-col :span="4" style='width:280px'>
                        <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='请输入用户昵称/手机号' style='width:250px'></el-input>
                    </el-col>
                    <!-- <el-col :span="4" style='width:280px'>
                        <el-input v-model="sendData.content"  class='myInput_40 margin_rt25' placeholder='请输入关键字' style='width:250px'></el-input>
                    </el-col>   -->
                    <el-col :span="7" style='width:500px'>
                        <el-date-picker
                        v-model="sendData.start_date"
                        type="datetime"
                        value-format="yyyy-MM-dd HH:mm:ss"
                        :default-value= "new Date()"
                        placeholder="起始时间" style='width:220px' class="margin_rt25 margin_tp_30">
                        </el-date-picker>
                        <el-date-picker
                        v-model="sendData.end_date"
                        type="datetime"
                        value-format="yyyy-MM-dd HH:mm:ss"

                        :default-value= "(new Date()).setTime((new Date()).getTime()+30*60*1000)"
                        placeholder="结束时间" style='width:220px' class="margin_rt25">
                        </el-date-picker>
                    </el-col> 
                </el-row> 
                <el-row> 
                    <el-col :span="2">
                        <div class="inlimeLabel margin_tp30">用户类别</div>
                    </el-col>
                    <el-col :span="5">
                        <el-select v-model="sendData.user_type" class="margin_tp30">
                            <el-option value="1" label="认证拳手">认证拳手</el-option>
                            <el-option value="2" label="名人">名人</el-option>
                            <el-option value="3" label="自媒体">自媒体</el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="10">
                        <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 margin_lf70 margin_tp30' @click="filter()">查询</el-button>
                        <el-button  class='myButton_40 btn_width_95 myBtnHover_red' @click='reset()'>重置</el-button>
                    </el-col> 
                </el-row>
                <!-- <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button> -->
            </div>
        </header>
        <nav>
            <template>
                <el-table
                  :data="tableData"
                  style="width: 100%"
                  :highlight-current-row="true">
                    <el-table-column
                    label="ID"
                    prop="id"
                    width="80"
                    >
                    </el-table-column>
                    <el-table-column
                    label="内容"
                    width="90">
                        <template slot-scope="scope">
                            <span class='colorFont' @click='openContent(scope.row.id)'>查看内容</span>
                        </template>
                    </el-table-column>
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
                            <el-button class='myBtnHover_red myButton_20'  @click='openConfirm(scope.row)'>编辑</el-button>                         
                        </template>
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <footer v-show="total>10">
            <Pagination :total="total" @changePage="changePage"></Pagination>
        </footer>
        <ReportContent :getData="detailData.allData" :isshow="detailData.isshow" @cancel="cancel"></ReportContent>
        <DialogLabel :isshow="confirmData.isshow" @confirm="confirm1" @cancel="cancel1"  :type="'forward'" :row='confirmData.row'></DialogLabel> 
    </div>
</template>

<style scoped>
    .myColor_red{color:#fff;border-color:#F95862;}
    .header_tab{border:1px solid #F0F2F5;height:36px;line-height:36px;text-align: center;cursor:pointer;}
    .header_tab.active{background:#F0F2F5;}
    .inlimeLabel{font-family: PingFangSC-Regular;font-size: 16px;color: #000000;padding-right:15px;height:40px;line-height:40px;width:100px;}
    @media screen and (max-width: 1349px){
        .margin_tp_30{
            margin-top:30px;
        }
    }
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
    import TopBar        from 'components/topBar';
    import Pagination    from 'components/pagination';
    import ReportContent from 'page/dynamic_detail';
    import DialogLabel   from "components/dialog_label"
    export default {
        data() {
            return {
                isShowTop : true,
                total     : 0,
                issearch  : false,
                page      : 1,
                sendData  :{
                    search:'',
                    content:'',
                    start_date:'',
                    end_date:'',
                    user_type:'',
                },
                detailData:{
                    allData:{},
                    isshow :false,
                },
                confirmData:{
                    isshow: false,
                    row:{},
                    id    :'',
                    content:'',
                    isDel :true,
                },
                tableData : [
                    {
                        "id": 157,
                        "like_count": 1,   // 真实点赞数
                        "user_id": 1181,  
                        "forward_count": 0,  // 真实转发数
                        "images": [
                            "/uploads/1a/38/78ecb0a6ac4f9509fdcef35f2691b1a7105b.jpg",
                            "/uploads/71/a1/5f60610897faa8319c90410a4f733caef765.jpg"
                        ],
                        "nick_name": "5553扣扣了",  // 用户昵称
                        "user_type": "普通用户", // 用户类型
                        "mobile": "13260125553",
                        "content": "",  
                        "video": null,
                        "created_time": "2018-06-29 17:54:12",
                        "initial_like_count": 10,   // 初始点赞数
                        "initial_forward_count": 10 // 初始转发数
                    },
                    {
                        "id": 158,
                        "like_count": 12,   // 真实点赞数
                        "user_id": 1181,  
                        "forward_count": 22,  // 真实转发数
                        "images": [
                            "/uploads/1a/38/78ecb0a6ac4f9509fdcef35f2691b1a7105b.jpg",
                            "/uploads/71/a1/5f60610897faa8319c90410a4f733caef765.jpg"
                        ],
                        "nick_name": "5553扣扣了",  // 用户昵称
                        "user_type": "普通用户", // 用户类型
                        "mobile": "13260125553",
                        "content": "",  
                        "video": null,
                        "created_time": "2018-06-29 17:54:12",
                        "initial_like_count": 0,   // 初始点赞数
                        "initial_forward_count": 0 // 初始转发数
                    },
                ],
                tableColumn:[
                    {title:'nick_name',  name :'昵称',   width:'100'},
                    {title:'mobile',   name :'手机号', width:'95'},
                    {title:'user_type',   name :'用户类型', width:''},
                    {title:'forward_count',   name :'真实转发量', width:''},
                    {title:'initial_forward_count',   name :'初始转发量', width:''},
                    {title:'like_count',   name :'真实点赞数', width:''},
                    {title:'initial_like_count',   name :'初始点赞数', width:''},
                    {title:'created_time',   name :'发布时间', width:'150'},
                ],
            }
        },
        components: {
            TopBar,
            Pagination,
            ReportContent,
            DialogLabel
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
            this.getData();
        },
        methods: {
            getData(page){
                let $this   = this
                let sendData={}
                if(this.issearch){
                   sendData=this.sendData
                }
                if(page){
                    sendData.page=page
                }
                this.ajax('/messages','get',{},sendData).then(function(res){
                    if(res&&res.data){
                        // console.log(res.data)
                        $this.tableData = res.data.results
                        for(var i=0;i<$this.tableData.length;i++){
                            
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
            openContent(id){
                let $this = this
                this.ajax('/messages/'+id,'get',{}).then(function(res){
                    if(res&&res.data){
                        if(res.data.images&&res.data.images.length>0){
                           for (var i=0;i<res.data.images.length;i++){
                                res.data.images[i] = $this.config.baseUrl + res.data.images[i]
                            } 
                        }
                        $this.detailData.allData = res.data;
                        $this.detailData.isshow  = true
                    }

                },function(err){
                    console.log(err.response.status)
                    if(err.response.status==404){
                        $this.$message({
                            message: '该动态已被删除，无法查看',
                            type: 'warning'
                        });
                    }
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            console.log(errors[key])
                            // return
                        } 
                    } 
                })
                
            },
            openConfirm(row,isDel){
                this.confirmData.row    = row
                this.confirmData.isshow= true
            },
            changePage(val){
                // 要看第几页
                // console.log(val)
                this.page=val
                this.getData(val)
                
            },
            filter(){
                this.issearch=true;
                //搜索是先看第一页
                this.page=1
                this.getData(1) 
            },
            cancel(val){
                this.detailData.isshow  = val ;
            },
            cancel1(val){
                this.confirmData.isshow=val;
            },
            reset(){
                this.sendData={};
                this.getData();
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
            confirm1(data){
                
            },
        },
    }
</script>