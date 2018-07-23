<template>
    <div >
        <TopBar v-if="isShowTop" firstTitle_name="拳城BB敏感词" firstTitle_path="/sensitiveword" disNone="disNone"></TopBar>
        <header>
            <div class="inline_item">
                <el-input v-model="sendData.search"  class='myInput_40 margin_rt25' placeholder='敏感词' style='width:18rem'></el-input>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click="filter()">查询</el-button>
            </div>
        </header>
        <nav  id="admin">
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95' @click="openDialog()">新增词汇</el-button>            
            <template>
                <el-table
                  :data="tableData"
                  style="width: 100%"
                  :highlight-current-row="true">
                    <el-table-column
                    prop="sensitive_word"
                    label="敏感词">
                    </el-table-column>
                    <el-table-column
                      fixed="right"
                      label="操作">
                        <template slot-scope="scope">
                            <el-button class='myBtnHover_red myButton_20'  @click="openConfirm(scope.row.id,scope.$index)">删除</el-button>                        
                            <el-button class='myBtnHover_red myButton_20'  @click="openDialog(scope.row,scope.$index)">修改</el-button>                        
                        </template>
                    </el-table-column>
                </el-table>
            </template>
        </nav>
        <footer v-show='total>10'>
            <Pagination :total="total" @changePage="changePage"></Pagination>
        </footer>
        <DialogLabel :isshow="dialog_label_data.isshow" @confirm="confirm" @cancel="cancel"  :type="'sensitive'" :sensitive_name='sensitive_word'></DialogLabel> 
        <Confirm :isshow="confirmData.isshow" @confirm="conform1" @cancel="cancel1()" :content="confirmData.content" :id='confirmData.id' :index='confirmData.index'></Confirm>
    </div>
</template>

<style scoped>
    .myColor_red{color:#fff;border-color:#F95862;}
    #admin{padding:30px;}
    .inline_item{padding:30px 30px 0 30px;}
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
                sensitive_word : '',
                page:1,
                issearch:false,
                sendData  :{
                    search:'',
                },
                dialog_label_data:{
                    isshow:false,
                    content_title:"增加钱包余额",
                    sensitive:''
                },
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'确认删除这条敏感词？'
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
                this.deleteSensitive(id,index)
            },
            getData(page){
                var $this=this;
                let sendData={}
                if(this.issearch){
                   sendData=this.sendData
                }
                if(page){
                    sendData.page=page
                }
                this.ajax('/word_filters/','get',{},sendData).then(function(res){
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
            filter(){
                this.issearch=true;
                this.page=1;
                this.getData();
            },
            changePage(val){
                // 要看第几页
                this.page = val
                this.getData(val);
            },
            cancel(val){
                this.dialog_label_data.isshow=val;
                this.sensitive_word = ''
            },
            confirm(val){
                var $this = this;
                if(this.confirmData.row&&this.confirmData.row.id){
                    this.ajax('/word_filters/'+this.confirmData.row.id+'/','put',{sensitive_word:val}).then(function(res){
                        if(res&&res.data){
                            // console.log(res.data)
                            $this.confirmData.row. sensitive_word= res.data.sensitive_word;
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
                }else{
                    this.ajax('/word_filters/','post',{sensitive_word:val},{}).then(function(res){
                        if(res&&res.data){
                            // console.log(res.data)
                            $this.tableData.unshift(res.data);
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
                }
                
                
            },
            openConfirm(id,index){
                this.confirmData.id=id
                this.confirmData.index=index
                this.confirmData.isshow=true
                $('.v-modal').addClass('addIndex')
                console.log($('.v-modal'))
            },
            openDialog(row,index){
                this.confirmData.row=row
                console.log(row)
                if(row){
                    this.sensitive_word = row.sensitive_word
                }else{
                    this.sensitive_word = ''
                }
                
                this.dialog_label_data.isshow=true
            },
            deleteSensitive(id,index){
                let $this=this;
                // console.log(index)
                this.ajax('/word_filters/'+id+'/','delete').then(function(res){
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