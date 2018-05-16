<template>
    <div class="classDetail">
        <div class='detail_content detail_header'>已通过的课程类型 ： <span v-for="item in res.results[0].allowed_lessons">{{item}} &nbsp;&nbsp;</span></div>
        <el-row class='detail_item'>
            <el-col :span="1">
                <div class='detail_title'>姓名</div>
            </el-col>
            <el-col :span="3">
                <div class='detail_content margin_lf'>{{res.results[0].boxer_name}}</div>
            </el-col>
            <el-col :span="1">
                <div class='detail_title'>手机号</div>
            </el-col>
            <el-col :span="3">
                <div class='detail_content margin_lf'>{{res.results[0].mobile}}</div>
            </el-col>
            <el-col :span="16">
                <el-button type="danger" class='myColor_red myButton_40' style='width:200px;margin-top:-13px' @click="checkIdent(res.results[0].id)">查看拳手认证信息</el-button>
            </el-col>
        </el-row>
        <el-row class='detail_item'>
            <el-col :span="1">
                <div class='detail_title'>约单拳馆</div>
            </el-col>
            <el-col :span="24">
                <div class='detail_content' style='padding-left:17px;line-height:25px;margin-top:10px'>{{res.results[0].club}}</div>
            </el-col>
        </el-row>
        <el-row class='detail_item'>
            <el-col :span="1">
                <div class='detail_title'>约单有效期</div>
            </el-col>
            <el-col :span="10">
                <div class='detail_content margin_lf'>({{res.results[0].validity}})</div>
            </el-col>
        </el-row>
        <el-row class='detail_item'>
            <el-col :offset="1">
                <div class='detail_content margin_lf'>
                    <el-col :span="3">
                        <div class='detail_content'>{{res.results[0].course_name}}</div>
                    </el-col>
                    <el-col :span="3">
                        <div class='detail_content margin_lf'>{{res.results[0].price}} 元/小时</div>
                    </el-col>
                    <el-col :span="3">
                        <div class='detail_content margin_lf'>{{res.results[0].duration}} 分钟</div>
                    </el-col>
                    <el-col :span="3">
                        <div class='detail_content margin_lf'>{{res.results[0].is_accept_order?'已开启':'已关闭'}}</div>
                    </el-col>
                </div>
            </el-col>
        </el-row>
    </div>
</template>
<style scoped>
    .classDetail{padding:90px 20px 20px 20px;}
    .detail_header{margin-bottom:40px;padding-left:10px;}
    .detail_item{margin-bottom:40px;}
    .detail_title{width:80px;}
    .detail_content.margin_lf{margin-left:30px;}
</style>
<style>
nav{min-height: 528px}
</style>
<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                res:{
                    "count": 1,
                    "next": null,
                    "previous": null,
                    "results": [
                        {
                            "id": 1,
                            "boxer_name": "张三", // 拳手姓名
                            "mobile": "111111111", // 拳手手机号
                            "is_professional_boxer": true, //是否是专业选手
                            "is_accept_order": true, // 接单状态
                            "club": "北京拓天比图拳馆拓天比图拳馆拓天比图拳馆，北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆。500字拓天比图拳馆。500字北京拓天比图拳馆拓天比图拳馆拓天比图拳馆，北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳京拓天比图拳馆拓天比图拳馆拓天比图拳馆。500字拓天比图拳馆。500字", // 约单拳馆
                            "allowed_lessons": [ // 已通过的课程类型
                                "THAI_BOXING",
                                "BOXING",
                                "MMA"
                            ],
                            "boxer_id": 1, //拳手id
                            "course_name": "THAI_BOXING", // 课程名
                            "price": 120, // 价格
                            "duration": 120, // 时长
                            "validity": "2018-08-25" // 有效期
                        }
                    ]
                }
            }
        },
        components: {
           
        },
        created() {
            let query = this.$route.query
            this.getDetailData(query.id);
        },
        methods: {
            getDetailData(id) {
                //获取data数据
                let $this   = this
                // this.ajax('/course','get',{},{id:id}).then(function(res){
                //     if(res&&res.data){
                //         console.log(res.data)
                //     }

                // },function(err){
                //     if(err&&err.response){
                //         let errors=err.response.data
                //         for(var key in errors){
                //             console.log(errors[key])
                //             // return
                //         } 
                //     } 
                // })
            },
            checkIdent(id){
                console.log('查看认证信息'+id)
            }
        },
    }
</script>