<template>
    <div class="banner_manage" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/dynamic" secondTitle_name="反馈建议"></TopBar>
        <div class="container">
            <header style='margin:20px 0 50px'>
                <el-input v-model="search"  class='myInput_40 margin_rt25' placeholder='输入用户昵称/用户手机号搜索' style='width:280px' @keyup.enter.native="searchEv"></el-input>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25' @click.native="searchEv">查询</el-button>
            </header>
            <template>
                <el-table
                        :data="tableData"
                        style="width: 100%">
                    <el-table-column
                            prop="id"
                            label="id">
                    </el-table-column>
                    <el-table-column
                            prop="user_nick_name"
                            label="用户昵称">
                    </el-table-column>
                    <el-table-column
                            prop="user_mobile"
                            label="用户手机号">
                    </el-table-column>
                    <el-table-column
                            prop="created_time"
                            label="提交时间">
                    </el-table-column>
                    <el-table-column label="操作" width='200'>
                        <template slot-scope="scope">
                            <el-button
                                    size="mini"
                                    @click="toDetail(scope.$index, scope.row)">查看详情</el-button>
                            <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleEdit(scope.$index, scope.row)">标记</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </template>
            <footer>
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
                stay_top: '',
                hasSearch: false,
                tableData: [
                    
                ],
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
                this.ajax('/feedback','get',{},param).then((res) => {
                    if(res&&res.data){
                        console.log(res.data)
                        this.tableData = res.data.results;
                        this.total = res.data.count;
                        ifBtn && (this.hasSearch = true);
                    }
                })
            },
            toDetail(){

            },
            handleEdit(index, row) {
                this.$router.push({path: '/boxerdetail', query:{id:row.id}});
            },
            toDetail(index, row) {
                
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
