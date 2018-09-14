<template>
    <div class="banner_manage" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/infolist" secondTitle_path="/metchlist" secondTitle_name="赛程管理" thirdTitle_name="对战表"></TopBar>
        <div class="container">
            <header>
                <p class='battle_title'>赛事信息 <span class='edit_icon' @click="editMetch"></span></p>
                <p class="battle_content"><span style='color:#909399;margin-right:20px'>比赛日期</span><span style='color:#1D1D27;'>{{editmetch.race_date}}</span></p>
                <p class="battle_content" style="margin-bottom:35px"><span style='color:#909399;margin-right:20px'>赛事名称</span><span style='color:#1D1D27;'>{{editmetch.name}}</span></p>
                <p class='battle_title'>对战信息</p>
            </header>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_bt20' @click.native="addBattleEv">添加对战</el-button>
            <template>
                <el-table
                        :data="tableData"
                        style="width: 100%">
                    <el-table-column
                            prop="id"
                            label="ID">
                    </el-table-column>
                    <el-table-column
                            prop="hongfangxingming"
                            label="红方姓名">
                    </el-table-column>
                    <el-table-column
                            prop="lanfangxingming"
                            label="蓝方姓名">
                    </el-table-column>
                    <el-table-column
                            prop="xiangmuleixing"
                            label="项目类型">
                    </el-table-column>
                    <el-table-column
                            prop="xiangmujibie"
                            label="项目级别">
                    </el-table-column>
                    <el-table-column
                            prop="shengfu"
                            label="胜负">
                    </el-table-column>
                    <el-table-column label="操作" width='220'>
                        <template slot-scope="scope">
                            <el-button
                                    size="mini"
                                    @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                            <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </template>
            <footer>
                <Pagination :total="total" @changePage="changePage" :page="page"></Pagination>
            </footer>
        </div>
        <Confirm :isshow="confirmData.isshow" @confirm="conform1" @cancel="cancel()" :content="confirmData.content" :id='confirmData.id' :index='confirmData.index'></Confirm>
        <Metchdialog :isshow="editmetch.isshow" @confirm="conform" @cancel="cancel()" content_title="编辑赛程" :name="editmetch.name" :race_date="editmetch.race_date"></Metchdialog>
    </div>
</template>

<style scoped lang="stylus">
    .battle_title{
        font-family: PingFangSC-Medium;
        font-size: 22px;
        color: #000000;
        letter-spacing: 0;
        margin-bottom:20px;
    }
    .battle_content{
        font-family: PingFangSC-Regular;
        font-size: 14px;
        margin-bottom:20px;
    }
    .edit_icon{
        display:inline-block;
        width:14px;
        height:14px;
        background:red;
    }
    .font_14{
        font-size:14px
    }
</style>

<script >
    import TopBar from 'components/topBar';
    import Pagination  from 'components/pagination';
    import Confirm from "components/confirm"
    import Metchdialog from "components/metch_add_dialog"
    export default {
        data() {
            return {
                isShowTop: true,
                search: '',
                total: 1,
                page: 1,
                dateArr: [],
                start_date: '',
                end_date: '',
                stay_top: '',
                hasSearch: false,
                tableData: [
                    {
                        id:1,
                        hongfangxingming:'张大胜',
                        lanfangxingming:'李世民',
                        xiangmuleixing:'泰拳',
                        xiangmujibie:'55-60kg',
                        shengfu:'红方胜',
                    },
                    {
                        id:2,
                        hongfangxingming:'张大胜',
                        lanfangxingming:'李世民',
                        xiangmuleixing:'拳击',
                        xiangmujibie:'55-60kg',
                        shengfu:'蓝方ko红方',
                    }
                ],
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'确认删除该条资讯？'
                },
                editmetch:{
                    isshow:false,
                    race_date:'2018-3-4',
                    name:'lalal'
                }
            }
        },
        components: {
            TopBar,
            Pagination,
            Confirm,
            Metchdialog
        },
        created() {
            this.getData();
        },
        methods: {
            getData() {
                // this.ajax('/schedules','get',{},{page:this.page}).then((res) => {
                //     if(res&&res.data){
                //         this.tableData = res.data.results;
                //         this.total = res.data.count;
                //     }
                // })
            },
            deleteData(id,index) {
                let $this = this;
                this.ajax(`//${id}`,'delete').then((res) => {
                    $this.confirmData.isshow=false;
                    // res && String (res.status).indexOf('2') > -1 && this.getData();
                    $this.tableData.splice(index,1)
                    $this.confirmData.isshow=false;
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            this.showErrorTip(errors[key][0])
                        }
                    }
                })
            },
            addBattleEv() {
            },
            editMetch(){
                this.editmetch.isshow=true
            },
            handleEdit(index, row) {
            },
            handleDelete(index, row) {
                this.confirmData.id = row.id
                this.confirmData.index = row.index
                this.confirmData.isshow=true;
            },
            cancel(val){
                this.confirmData.isshow=val;
                this.editmetch.isshow=val;
            },
            conform1(id,index){
                this.deleteData(id,index);
            },
            conform(data){
                 this.editmetch={
                    isshow:false,
                    race_date:data.race_date,
                    name:data.name
                }
            },
            changePage(page) {
                this.page = page;
                this.getData();
            },
            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            }
        }
    }
</script>
