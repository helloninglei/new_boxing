<template>
    <div >
        <TopBar v-if="isShowTop" firstTitle_name="相册管理" firstTitle_path="/admin" disNone="disNone"></TopBar>
        <nav  id="admin">
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95' style="margin-bottom: 20px" @click="addAlbum">新增相册</el-button>            
            <template>
                <el-table
                  :data="tableData"
                  style="width: 100%"
                  :highlight-current-row="true">
                    <el-table-column
                    prop="name"
                    label="相册名称">
                    </el-table-column>
                    <el-table-column
                    prop="nick_name"
                    label="关联账号">
                    </el-table-column>
                    <el-table-column
                    prop="release_time"
                    label="发布时间">
                    </el-table-column>
                    <el-table-column
                      fixed="right"
                      label="显示状态">
                        <template slot-scope="scope">
                            <span>{{scope.row.is_show?'显示':'隐藏'}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column
                      fixed="right"
                      label="操作">
                        <template slot-scope="scope">
                            <el-button  class='myBtnHover_red myButton_20' @click="toDetail(scope.row)">修改</el-button>                       
                            <el-button class='myBtnHover_red myButton_20 ' @click="changeShow(scope.row,scope.$index)">{{scope.row.is_show?'隐藏':'显示'}}</el-button> 
                        </template>
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <footer v-show='total>10'>
            <Pagination :total="total" @changePage="changePage"></Pagination>
        </footer>
    </div>
</template>

<style scoped>
    .myColor_red{color:#fff;border-color:#F95862;}
    #admin{padding:30px;}
</style>

<script >
    import TopBar      from 'components/topBar';
    import Pagination  from 'components/pagination';
    import DialogLabel from "components/dialog_label"
    import Confirm     from "components/confirm"
    export default {
        data() {
            return {
                isShowTop : true,
                total     : 0,
                showImg   : false,
                imgSrc    : '',
                page      :1,
                dialog_label_data:{
                    isshow:false,
                    content_title:"增加钱包余额",
                },
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'确认删除管理员？'
                },
                tableData : [
                    
                ],
            }
        },
        components: {
            TopBar,
            Pagination,
            DialogLabel,
            Confirm
        },
        created() {
           this.getData() 
        },
        methods: {
            cancel1(val){
                this.confirmData.isshow=val;
            },
            conform1(id,index){
                this.deleteAdmin(id,index)
            },
            getData(page){
                var $this=this;
                this.ajax('/albums','get',{},{page:page}).then(function(res){
                    if(res&&res.data){
                        $this.tableData = res.data.results
                        $this.total = res.data.count
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
                console.log(val)
                this.getData(val)
            },
            toDetail(row){
                //修改详情页
                this.$router.push({path: '/albumdetail', query:row});
            },
            addAlbum(){
                this.$router.push({path: '/albumdetail'});
            },
            changeShow(row,index){
                // 显示隐藏
                let $this = this;
                this.ajax('/albums/'+row.id,'patch',{is_show:!row.is_show}).then(function(res){
                    if(res&&res.data){
                        row.is_show= res.data.is_show
                        row.is_show_name = res.data.is_show?'显示':'隐藏'
                        // $this.tableData.splice(index,1,row);
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
        },
    }
</script>