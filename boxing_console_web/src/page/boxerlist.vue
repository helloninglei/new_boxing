<template>
    <div class="banner_manage" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/infoList" secondTitle_name="参赛选手管理"></TopBar>
        <div class="container">
            <header style='margin:20px 0'>
                <el-input v-model="search"  class='myInput_40 margin_rt25' placeholder='请输入拳手姓名／手机号' style='width:280px' @keyup.enter.native="searchEv"></el-input>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click.native="searchEv">查询</el-button>
            </header>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_tp30 margin_bt20' @click.native="addMatchEv">新增</el-button>
            <template>
                <el-table
                        :data="tableData"
                        style="width: 100%">
                    <el-table-column
                            prop="name"
                            label="拳手名称">
                    </el-table-column>
                    <el-table-column
                            prop="mobile"
                            label="拳手手机号">
                    </el-table-column>
                    <el-table-column
                            width="350"
                            label="拳手能力值">
                            <template slot-scope="scope">
                                <span>{{`耐力：${scope.row.stamina}，技术：${scope.row.skill}，进攻：${scope.row.attack}，防守：${scope.row.defence}，力量：${scope.row.strength}`}}</span>
                            </template>
                    </el-table-column>
                    <el-table-column label="操作" width='200'>
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
            <footer v-if='total>10'>
                <Pagination :total="total" @changePage="changePage" :page="page"></Pagination>
            </footer>
        </div>
        <Confirm :isshow="confirmData.isshow" @confirm="conform1" @cancel="cancel1()" :content="confirmData.content" :id='confirmData.id' :index='confirmData.index'></Confirm>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">

</style>

<script >
    import TopBar from 'components/topBar';
    import Pagination  from 'components/pagination';
    import Confirm from "components/confirm"
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
                hasSearch: false,
                tableData: [

                ],
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'参赛拳手资料删除后不可恢复，是否确认删除？？'
                },
            }
        },
        components: {
            TopBar,
            Pagination,
            Confirm
        },
        created() {
            this.getData();
        },
        methods: {
            getData(ifBtn) {
                ifBtn && (this.page = 1);
                let param = {page: this.page, search: this.search};
                !this.hasSearch && (param = {page: this.page});
                this.ajax('/player','get',{},param).then((res) => {
                    if(res&&res.data){
                        console.log(res.data)
                        this.tableData = res.data.results;
                        this.total = res.data.count;
                        ifBtn && (this.hasSearch = true);
                    }
                })
            },
            deleteData(id,index) {
                let $this = this;
                this.ajax(`/player/${id}`,'delete').then((res) => {
                    $this.confirmData.isshow=false;
                    $this.tableData.splice(index,1)
                    $this.confirmData.isshow=false;
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data
                        if((typeof errors=='string')&&errors.constructor==String){
                            this.showErrorTip(errors)
                        }else{
                           for(var key in errors){
                                this.showErrorTip(errors[key][0])
                            } 
                        }
                    }

                })
            },
            addMatchEv() {
                this.$router.push({path: '/boxerdetail'});
            },
            handleEdit(index, row) {
                this.$router.push({path: '/boxerdetail', query:{id:row.id}});
            },
            handleDelete(index, row) {
                this.confirmData.id = row.id
                // 点击删除，则判断该拳手是否还有赛程记录，若有赛程，则弹窗提示用户：“请先删除该参赛拳手的所有赛程再删除拳手记录“，按钮只有一个“我知道了”，
                this.confirmData.index = row.index
                this.confirmData.isshow=true;
            },
            cancel1(val){
                this.confirmData.isshow=val;
            },
            conform1(id,index){
                this.deleteData(id,index);
            },
            changePage(page) {
                this.page = page;
                this.getData();
            },
            searchEv() {
                this.hasSearch = true
                this.getData(true);
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
