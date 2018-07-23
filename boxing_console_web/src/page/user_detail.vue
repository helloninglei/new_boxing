<template>
    <div>
         <TopBar v-if="isShowTop" firstTitle_name="用户管理" firstTitle_path="/usermanage" :secondTitle_name="user_type" secondTitle_path="/userdetail"></TopBar>
         <div class='userDetail'>
            <el-row class='detail_item'>
                <el-col :span="2">
                    <div class='detail_title'>姓名</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.name?result.user_basic_info.name:'&nbsp;&nbsp;'}}</div>
                </el-col>
                <el-col :span="2">
                    <div class='detail_title'>民族</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.nation?result.user_basic_info.nation:'&nbsp;&nbsp;'}}</div>
                </el-col>
                <el-col :span="2">
                    <div class='detail_title'>身高</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.height?result.user_basic_info.height+'cm':'&nbsp;&nbsp;'}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item'>
                <el-col :span="2">
                    <div class='detail_title'>体重</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.weight?result.user_basic_info.weight+'kg':'&nbsp;&nbsp;'}}</div>
                </el-col>
                <el-col :span="2">
                    <div class='detail_title'>出生日期</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf' style='width:100px'>{{result.user_basic_info.birthday?result.user_basic_info.birthday:'&nbsp;&nbsp;'}}</div>
                </el-col>
                <el-col :span="2">
                    <div class='detail_title'>职业</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_basic_info.profession}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item' v-if='user_type!=="普通用户"'>
                <el-col :span="2">
                    <div class='detail_title'>认证称号</div>
                </el-col>
                <el-col :span="13">
                    <div class='detail_content margin_lf'>{{title}}</div>
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
    .detail_content.margin_lf{margin-left:39px;}
    .detail_content{min-width: 100px}
</style>
<style>
nav{min-height: 528px}
</style>
<script>
    import TopBar from 'components/topBar';
    export default {
        data() {
            return {
                isShowTop: true,
                result   : {
                    user_basic_info : {}
                },
                user_type:'',
                title:'',
            }
        },
        components: {
            TopBar,
        },
        created() { 
            //刷新后对象里面都变成字符串
            let query   = this.$route.query
            this.user_type = query.user_type
            this.title = query.title
            this.result.user_basic_info = query.user_basic_info;
            console.log(query)
        },
        mounted(){
        },
        methods: {
            getDetailData(id) {
                
            }
        },
    }
</script>