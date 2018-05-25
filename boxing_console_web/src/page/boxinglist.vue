<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="拳馆管理" firstTitle_path="/boxingmanage" secondTitle_name="拳馆列表" secondTitle_path="/boxinglist"></TopBar>
        <BigImg v-if="showImg" @clickit="viewImg" :imgSrc="imgSrc"></BigImg>
        <nav style='margin-top:60px'>
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
                            <span class='colorFont' @click='clickImg(scope.row.images[0])'>查看</span>
                        </template>
                    </el-table-column>
                    <el-table-column
                      fixed="right"
                      label="操作">
                        <template slot-scope="scope">
                            <el-button class='myBtnHover_red myButton_20' style='margin-right:20px' @click=''>删除</el-button>
                            <el-button class='myColor_red myButton_20' style='margin-right:20px' @click=''>修改</el-button>                         
                        </template>
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <footer>
            <Pagination :total="total" @changePage="changePage"></Pagination>
        </footer>
        
    </div>
</template>

<style scoped>
    .myColor_red{color:#fff;border-color:#F95862;}
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
                    {title:'club_name',name :'拳馆名称',    width:''},
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
            
        },
        methods: {
            changePage(val){
                // 要看第几页
                // console.log(val)
                this.getTableData(this.sendData,val);
            },
            clickImg(img) {
                // 获取当前图片地址
                console.log(img)
                // this.imgSrc ='http://'+ img;
                this.imgSrc ="http://img.zcool.cn/community/010f87596f13e6a8012193a363df45.jpg@1280w_1l_2o_100sh.jpg";
                this.showImg=true;
            },
            viewImg(){
                this.showImg = false;
            },
        },
    }
</script>