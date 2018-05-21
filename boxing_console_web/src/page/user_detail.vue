<template>
    <div>
         <TopBar v-if="isShowTop" firstTitle_name="用户管理" firstTitle_path="/usermanage" secondTitle_name="普通用户" secondTitle_path="/userdetail"></TopBar>
         <div class='userDetail'>
            <el-row class='detail_item'>
                <el-col :span="1">
                    <div class='detail_title'>姓名</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.name}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>民族</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.nation?result.user_basic_info.nation:'汉'}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>身高</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.height}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item'>
                <el-col :span="1">
                    <div class='detail_title'>体重</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.weight}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>出生日期</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.birthday}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>职业</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.profession}}</div>
                </el-col>
            </el-row>
        </div>
    </div>
</template>
<style scoped>
    .userDetail{padding:70px 20px 20px 10px;}
    .detail_header{margin-bottom:40px;padding-left:10px;}
    .detail_item{margin-bottom:20px;}
    .detail_title{width:80px;}
    .detail_content.margin_lf{margin-left:30px;}
</style>
<style>
nav{min-height: 528px}
</style>
<script type="text/ecmascript-6">
    import TopBar from 'components/topBar';
    export default {
        data() {
            return {
                isShowTop: true,
                result   : {
                    user_basic_info : {}
                }
            }
        },
        components: {
            TopBar,
        },
        created() { 
            //刷新后对象里面都变成字符串
            let query   = this.$route.query
            this.result.user_basic_info = query;
        },
        mounted(){
        },
        methods: {
            getDetailData(id) {
                
            }
        },
    }
</script>