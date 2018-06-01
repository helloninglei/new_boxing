<template>
    <div class="banner_manage" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/bannermanage" disNone="disNone"></TopBar>
        <div class="container">
            <header>
                <el-date-picker
                        class="margin_rt25"
                        v-model="dateArr"
                        type="datetimerange"
                        range-separator="至"
                        start-placeholder="起始日期"
                        end-placeholder="结束日期"
                        @change="getDateTime"
                        value-format="yyyy-MM-dd hh:mm:ss">
                </el-date-picker>
                <el-input v-model="search"  class='myInput_40 margin_rt20' placeholder='请输入关键词' style='width:280px' @keyup.enter.native="searchEv"></el-input>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 margin_lf70' @click.native="searchEv">查询</el-button>
            </header>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_tp30 margin_bt20' @click.native="addMatchEv">新增</el-button>
            <template>
                <el-table
                        :data="tableData"
                        style="width: 100%">
                    <el-table-column
                            prop="id"
                            label="ID">
                    </el-table-column>
                    <el-table-column
                            prop="title"
                            label="资讯标题">
                    </el-table-column>
                    <el-table-column
                            prop="author"
                            label="发布作者">
                    </el-table-column>
                    <el-table-column
                            prop="views_count"
                            label="阅读人数">
                    </el-table-column>
                    <el-table-column
                            prop="initial_views_count"
                            label="真实阅读量">
                    </el-table-column>
                    <el-table-column
                            prop="comment_count"
                            label="评论">
                    </el-table-column>
                    <el-table-column
                            prop="start_time"
                            label="发布时间"
                            width="200">
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
                <Pagination :total="total" @changePage="changePage"></Pagination>
            </footer>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">

</style>

<script >
    import TopBar from 'components/topBar';
    import Pagination  from 'components/pagination';

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
                    {
                        "id": 1,
                        "author": "lerry",
                        "comment_count": 0,
                        "title": "111",
                        "sub_title": "22",
                        "views_count": 0,
                        "initial_views_count": 22,
                        "picture": "/uploads/aa/67/959ce5a33a6984b10e1d44c965b03c84230f.jpg",
                        "stay_top": true,
                        "push_news": true,
                        "start_time": "2018-12-31 12:59:00",
                        "end_time": "2018-12-31 23:59:00",
                        "app_content": "222",
                        "share_content": null
                    },
                    {
                        "id": 2,
                        "author": "lerry",
                        "comment_count": 0,
                        "title": "111",
                        "sub_title": "22",
                        "views_count": 0,
                        "initial_views_count": 22,
                        "picture": "/uploads/aa/67/959ce5a33a6984b10e1d44c965b03c84230f.jpg",
                        "stay_top": true,
                        "push_news": true,
                        "start_time": "2018-12-31 12:59:00",
                        "end_time": "2018-12-31 23:59:00",
                        "app_content": "222",
                        "share_content": null
                    },
                    {
                        "id": 3,
                        "author": "lerry",
                        "comment_count": 0,
                        "title": "111",
                        "sub_title": "22",
                        "views_count": 0,
                        "initial_views_count": 22,
                        "picture": "/uploads/aa/67/959ce5a33a6984b10e1d44c965b03c84230f.jpg",
                        "stay_top": true,
                        "push_news": true,
                        "start_time": "2018-12-31 12:59:00",
                        "end_time": "2018-12-31 23:59:00",
                        "app_content": "222",
                        "share_content": null
                    },
                ]
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
                let param = {page: this.page, search: this.search, start_date: this.start_date, end_date: this.end_date};
                !this.hasSearch && (param = {page: this.page});
                this.ajax('/game_news','get',{},param).then((res) => {
                    if(res&&res.data){
                        // this.tableData = res.data.results;
                        // this.total = res.data.count;
                        ifBtn && (this.hasSearch = true);
                    }
                })
            },
            deleteData(id) {
                this.ajax(`/game_news/${id}`,'delete').then((res) => {
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
            addMatchEv() {
                this.$router.push({path: '/infodetail'});
            },
            handleEdit(index, row) {
                this.$router.push({path: '/infodetail', query:row});
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
            getDateTime() {
                this.start_date = this.dateArr[0];
                this.end_date = this.dateArr[1];
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