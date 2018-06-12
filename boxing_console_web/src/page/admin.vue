<template>
    <div >
        <TopBar v-if="isShowTop" firstTitle_name="管理员" firstTitle_path="/boxingmanage" disNone="disNone"></TopBar>
        <nav  id="admin">
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95' @click="dialog_label_data.isshow=true">新增</el-button>            
            <template>
                <el-table
                  :data="tableData"
                  style="width: 100%"
                  :highlight-current-row="true">
                    <el-table-column
                    prop="mobile"
                    label="手机号">
                    </el-table-column>
                    <el-table-column
                      fixed="right"
                      label="操作">
                        <template slot-scope="scope">
                            <el-button class='myBtnHover_red myButton_20'  @click="openConfirm(scope.row.id,scope.$index)">删除</el-button>                        
                        </template>
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <footer v-show='total>10'>
            <Pagination :total="total" @changePage="changePage"></Pagination>
        </footer>
        <DialogLabel :isshow="dialog_label_data.isshow" @confirm="confirm" @cancel="cancel"  :type="'phone'"></DialogLabel> 
        <Confirm :isshow="confirmData.isshow" @confirm="conform1" @cancel="cancel1()" :content="confirmData.content" :id='confirmData.id' :index='confirmData.index'></Confirm>
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
                total     : 1000,
                showImg   : false,
                imgSrc    : '',
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
                this.ajax('/admins/','get',{},{page:page}).then(function(res){
                    if(res&&res.data){
                        // console.log(res.data)
                        $this.tableData = res.data.results
                        $this.total = res.data.total
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
            cancel(val){
                this.dialog_label_data.isshow=val;
            },
            confirm(val){
                var $this = this;
                this.ajax('/admins/','post',{mobile:val},{}).then(function(res){
                    if(res&&res.data){
                        // console.log(res.data)
                        $this.tableData.push(res.data);
                        $this.dialog_label_data.isshow=false;
                    }

                },function(err){
                    console.log(err.response.status)
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            $this.$message({
                                message: errors[key][0],
                                type: 'error'
                            });
                        } 
                    } 
                })
                
            },
            openConfirm(id,index){
                this.confirmData.id=id
                this.confirmData.index=index
                this.confirmData.isshow=true
                $('.v-modal').addClass('addIndex')
                console.log($('.v-modal'))
            },
            deleteAdmin(id,index){
                let $this=this;
                // console.log(index)
                this.ajax('/admins/'+id+'/','delete').then(function(res){
                    if(res&&res.status==204){
                        $this.tableData.splice(index,1)
                        $this.confirmData.isshow=false;
                    }else{
                      console.log(res)  
                    }

                },function(err){
                    if(err&&err.response){
                        console.log(err.response)
                        let errors=err.response.data
                        for(var key in errors){
                            console.log(errors[key])
                            // return
                        } 
                    }else if(err.request){
                        console.log(err.request)
                    }else{
                        console.log('Error', err.message);
                    }

                })
            }
        },
    }
</script>