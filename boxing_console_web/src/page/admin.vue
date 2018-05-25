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
                            <el-button class='myBtnHover_red myButton_20'  @click="openConfirm(scope.row.id)">删除</el-button>                        
                        </template>
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <footer>
            <Pagination :total="total" @changePage="changePage"></Pagination>
        </footer>
        <DialogLabel :isshow="dialog_label_data.isshow" @confirm="confirm" @cancel="cancel"  :type="'phone'"></DialogLabel> 
        <Confirm :isshow="confirmData.isshow" @confirm="conform1" @cancel="cancel1()" :content="confirmData.content" :id='confirmData.id'></Confirm>
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
                    {
                        "id": 5,
                        "mobile": "16600000000"
                    },
                    {
                        "id": 3,
                        "mobile": "19900000002"
                    },
                    {
                        "id": 2,
                        "mobile": "19900000001"
                    },
                    {
                        "id": 1,
                        "mobile": "19990000000"
                    }
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
            conform1(id){
                console.log(id)
                this.deleteAdmin(id)
            },
            getData(){
                var $this=this;
                this.ajax('/admins/','get',{},{}).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        $this.tableData = res.data.results
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
            },
            cancel(val){
                this.dialog_label_data.isshow=val;
            },
            confirm(val){
                var $this = this;
                this.ajax('/admins/','post',{mobile:val},{}).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        $this.tableData.push(res.data);
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
                this.dialog_label_data.isshow=false;
            },
            openConfirm(id){
                this.confirmData.id=id
                this.confirmData.isshow=true
            },
            deleteAdmin(id){
                let $this=this;
                this.ajax('/admins/'+id+'/','delete').then(function(res){
                    if(res&&res.status==204){
                        for(var i=0;i<$this.tableData.length;i++){
                            if($this.tableData[i].id==id){
                                $this.tableData.splice(i,1)
                                $this.confirmData.isshow=false;
                            }
                        } 
                    }else{
                      console.log(res)  
                    }

                },function(err){
                    if(err&&err.response){
                        console.log(err.response)
                        if(err.response.status==204){
                            alert('已删除')
                        }
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