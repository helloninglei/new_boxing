<template>
    <div class="banner_manage" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/infoList" disNone="disNone"></TopBar>
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
                        :clearable=false
                        :editable=false
                        value-format="yyyy-MM-dd HH:mm:ss">
                </el-date-picker>
                <el-input v-model="search"  class='myInput_40 margin_rt25' placeholder='请输入关键词' style='width:280px' @keyup.enter.native="searchEv"></el-input>
                <el-select v-model="stay_top" class="margin_tp30 margin_rt60">
                    <el-option value="all" label="全部">全部</el-option>
                    <el-option :value="true" label="置顶">置顶</el-option>
                    <el-option :value="false" label="不置顶">不置顶</el-option>
                </el-select>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 margin_tp30' @click.native="searchEv">查询</el-button>
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
                            prop="stay_top_name"
                            label="是否置顶">
                    </el-table-column>
                    <el-table-column
                            prop="pub_time"
                            label="发布时间"
                            width="170">
                    </el-table-column>
                    <el-table-column label="操作" width='220'>
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
                tableData: [],
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'确认删除该条资讯？'
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
                let param = {page: this.page, search: this.search, start_date: this.start_date, end_date: this.end_date,stay_top: this.stay_top};
                !this.hasSearch && (param = {page: this.page});
                this.ajax('/game_news','get',{},param).then((res) => {
                    if(res&&res.data){
                        this.tableData = res.data.results;
                        for(var i=0;i<res.data.results.length;i++){
                            res.data.results[i].stay_top_name = res.data.results[i].stay_top ? '是' : '否'
                        }
                        this.total = res.data.count;
                        ifBtn && (this.hasSearch = true);
                    }
                })
            },
            deleteData(id,index) {
                let $this = this;
                this.ajax(`/game_news/${id}`,'delete').then((res) => {
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
            addMatchEv() {
                this.$router.push({path: '/infodetail'});
            },
            handleEdit(index, row) {
                this.$router.push({path: '/infodetail', query:row});
            },
            handleDelete(index, row) {
                this.confirmData.id = row.id
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
            getDateTime() {
                console.log(this.dateArr)
                if (this.dateArr) {
                    this.start_date = this.dateArr[0];
                    this.end_date = this.dateArr[1];
                }
                else {
                    this.start_date = '';
                    this.end_date = '';
                }
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
