<template>
    <div class="banner_manage" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="Banner管理" firstTitle_path="/bannermanage" disNone="disNone"></TopBar>
        <div class="container">
            <header>
                <el-input v-model="search"  class='myInput_40 margin_rt20' placeholder='请输入名称' style='width:280px' @keyup.enter.native="searchEv"></el-input>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 margin_lf70' @click.native="searchEv">查询</el-button>
            </header>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_tp30 margin_bt20' @click.native="addBannerEv">新增</el-button>
            <template>
                <el-table
                        :data="tableData"
                        style="width: 100%">
                    <el-table-column
                            prop="id"
                            label="ID"
                            width="180">
                    </el-table-column>
                    <el-table-column
                            prop="name"
                            label="名称"
                            width="180">
                    </el-table-column>
                    <el-table-column
                            prop="order_number"
                            label="序号">
                    </el-table-column>
                    <el-table-column label="操作">
                        <template slot-scope="scope">
                            <el-button
                                    size="mini"
                                    @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                            <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleEdit(scope.$index, scope.row)">修改</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </template>
            <footer>
                <Pagination :total="total" @changePage="changePage" :page="page"></Pagination>
            </footer>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">

</style>

<script type="text/ecmascript-6">
    import TopBar from 'components/topBar';
    import Pagination  from 'components/pagination';

    export default {
        data() {
            return {
                isShowTop: true,
                search: '',
                total: 1,
                page: 1,
                hasSearch: false,
                tableData: []
            }
        },
        components: {
            TopBar,
            Pagination
        },
        created() {
            this.getData();
        },
        methods: {
            getData(ifBtn) {
                ifBtn && (this.page = 1);
                let param = {page: this.page, search: this.search};
                !this.hasSearch && (param = {page: this.page});
                this.ajax('/banners','get',{},param).then((res) => {
                    if(res&&res.data){
                        this.tableData = res.data.results;
                        this.total = res.data.count;
                        ifBtn && (this.hasSearch = true);
                    }
                })
            },
            deleteData(id) {
                this.ajax(`/banners/${id}`,'delete').then((res) => {
                    res && String (res.status).indexOf('2') > -1 && this.getData();
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            this.showErrorTip(errors[key][0])
                        }
                    }
                })
            },
            addBannerEv() {
                this.$router.push({path: '/bannercontent'});
            },
            handleEdit(index, row) {
                this.$router.push({path: '/bannercontent', query:{id: row.id}});
            },
            handleDelete(index, row) {
                let id = row.id;
                this.deleteData(id);
            },
            changePage(page) {
                this.page = page;
                this.getData();
            },
            searchEv() {
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