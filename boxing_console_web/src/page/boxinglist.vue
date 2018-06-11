<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="拳馆管理" firstTitle_path="/boxinglist" disNone="disNone"></TopBar>
        <BigImg v-if="showImg" @clickit="viewImg" :imgSrc="imgSrc"></BigImg>
        <header>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_120 margin_rt25'  @click='goTodetail()' style='margin-top:30px;float:right;'>添加</el-button>
            <div class="inline_item">
                <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='拳馆名称' style='width:18rem'></el-input>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
            </div>
        </header>
        <nav style='padding:30px'>
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
                    label="宣传图"
                    width="90">
                        <template slot-scope="scope">
                            <span class='colorFont' @click='clickImg(scope.row.avatar)'>查看</span>
                        </template>
                    </el-table-column>
                    <el-table-column
                      fixed="right"
                      label="操作">
                        <template slot-scope="scope">
                            <el-button class='myBtnHover_red myButton_20' style='margin-right:20px' @click='deleteClub(scope.row)'>停用</el-button>
                            <el-button class='myColor_red myButton_20' style='margin-right:20px' @click='goTodetail(scope.row)'>修改</el-button>                         
                        </template>
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <footer v-show='total>10'>
            <Pagination :total="total" @changePage="changePage" :page='page'></Pagination>
        </footer>
        
    </div>
</template>

<style scoped>
    .myColor_red{color:#fff;border-color:#F95862;}
    .inline_item{padding:30px;}
</style>

<script >
    import TopBar  from 'components/topBar';
    import Pagination  from 'components/pagination';
    import BigImg  from 'components/bigImg';
    export default {
        data() {
            return {
                isShowTop : true,
                total     : 1000,
                showImg   : false,
                imgSrc    : '',
                issearch  :false,
                page      :1,
                sendData  :{
                    search:'',
                },
                tableData : [
                    {
                        "id": 20,
                        "images": [
                            "www.baidu.com",
                            "www.sina.com.cn"
                        ],
                        "created_time": "2018-05-12 08:08:11",
                        "updated_time": "2018-05-12 08:08:11",
                        "club_name": "拳王06",
                        "address": "丰台区角门东洋桥",
                        "longitude": "111.222222",
                        "latitude": "11.222223",
                        "phone": "11111111111",
                        "opening_hours": "10:00--20:00",
                        "introduction": "最牛逼的拳馆"
                    },
                    {
                        "id": 22,
                        "images": [
                            "www.baidu.com",
                            "www.sina.com.cn"
                        ],
                        "created_time": "2018-05-12 09:28:16",
                        "updated_time": "2018-05-12 09:28:16",
                        "club_name": "拳王08",
                        "address": "丰台区角门东洋桥",
                        "longitude": "111.444444",
                        "latitude": "11.444444",
                        "phone": "11111111111",
                        "opening_hours": "10:00--20:00",
                        "introduction": "最牛逼的拳馆"
                    }
                ],
                tableColumn:[
                    {title:'id',       name :'ID',  width:''},
                    {title:'name',name :'拳馆名称',    width:''},
                    {title:'address',  name :'地址',   width:''},
                    {title:'opening_hours',name :'营业时间', width:''},
                ],
            }
        },
        components: {
            TopBar,
            Pagination,
            BigImg
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
                this.ajax('/club','get',{},sendData).then(function(res){
                    if(res&&res.data){
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
                this.page = val
                this.getTableData(val);
            },
            filter(){
                this.issearch=true;
                this.page=1;
                this.getTableData();
            },
            clickImg(img) {
                // 获取当前图片地址
                this.imgSrc =this.config.baseUrl+ img;
                this.showImg=true;
            },
            viewImg(){
                this.showImg = false;
            },
            goTodetail(row){
                this.$router.push({path: '/addboxing', query:row});

            },
            deleteClub(row){
                //停用的接口
                this.ajax('/club/'+row.id+'/close','post').then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
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
    }
</script>