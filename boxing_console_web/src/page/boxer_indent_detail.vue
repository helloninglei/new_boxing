<template>
    <div class="classDetail">
        <div class='detail_header' v-if="authentication_state=='APPROVED'">审核通过 
            <span class='detail_content'>已通过的课程类型 ： <span v-for="item in result.allowed_course">{{item}} &nbsp;&nbsp;</span>
                <el-button type="danger" class='myColor_red myButton_40' style='width:95px;margin-top:-13px' @click="openApprove()">修改</el-button>
            </span>
        </div>
        <div class='detail_header' v-else-if="authentication_state=='REFUSE'">已驳回</div>
        <div class='detail_header' v-else>待审核</div>
        <div class='detail_item'>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>姓名</div>
                </el-col>
                <el-col :span="4">
                    <div class='detail_content margin_lf'>{{result.real_name}}</div>
                </el-col>
                 <el-col :span="1">
                    <div class='detail_title'>性别</div>
                </el-col>
                <el-col :span="4">
                    <div class='detail_content margin_lf'>{{result.gender}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>身高</div>
                </el-col>
                <el-col :span="4">
                    <div class='detail_content margin_lf'>{{result.height}}cm</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>体重</div>
                </el-col>
                <el-col :span="4">
                    <div class='detail_content margin_lf'>{{result.weight}}kg</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>出生日期</div>
                </el-col>
                <el-col :span="4">
                    <div class='detail_content margin_lf'>{{result.birthday}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>身份证号</div>
                </el-col>
                <el-col :span="4">
                    <div class='detail_content margin_lf'>{{result.identity_number}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>手机号</div>
                </el-col>
                <el-col :span="4">
                    <div class='detail_content margin_lf'>{{result.mobile}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>职业</div>
                </el-col>
                <el-col :span="4">
                    <div class='detail_content margin_lf'>{{result.job}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>选手类型</div>
                </el-col>
                <el-col :span="4">
                    <div class='detail_content margin_lf' v-if="result.is_professional_boxer">职业</div>
                    <div class='detail_content margin_lf' v-if="!result.is_professional_boxer">非职业</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>所事拳馆</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.club}}</div>
                </el-col>
            </el-row>
        </div>
        <hr style="height:1px;border:none;border-top:1px solid rgba(187,187,187,0.2);margin-left:-60px;margin-right:-20px;margin-bottom:30px" >
    
        <div class="detail_item">
            <el-row class='detail_item_sub'>
                <div class='detail_title'>自我介绍</div>
            </el-row>
            <el-row class='detail_item_sub'>
                <div class='detail_content_p detail_content'>{{result.introduction?result.introduction:'无'}}</div>
            </el-row>
        </div>
        <div class="detail_item">
            <el-row class='detail_item_sub'>
                <div class='detail_title' style='width:176px'>参赛、获奖及执教经历</div>
            </el-row>
            <el-row class='detail_item_sub'>
                <div class='detail_content_p detail_content'>{{result.experience?result.experience:'无'}}</div>
            </el-row>
        </div>
        <div class="detail_item">
            <el-row class='detail_item_sub'>
                <div class='detail_title'>荣誉证明</div>
            </el-row>
            <el-row class='detail_item_sub'>
                <div class='detail_content_p detail_content'>
                    <div class='addImage' v-for="item in result.honor_certificate_images">
                        <img :src="config.baseUrl+item" alt="" width='100%' height='100%'>
                    </div>
                    <!-- <div class='addImage'>图片</div> -->
                </div>
            </el-row>
        </div>
        <div class="detail_item">
            <el-row class='detail_item_sub'>
                <div class='detail_title'>参赛视频</div>
            </el-row>
            <el-row class='detail_item_sub'>
                <div class='detail_content_p detail_content'>
                    <div style='width:193px;height:132px;border:1px solid #ccc'>
                        <!-- {{result.competition_video}} -->
                        <video :src="config.baseUrl+result.competition_video" controls="controls" width="100%" height="100%">
                            您的浏览器不支持该视频。
                        </video>
                    </div>
                </div>
            </el-row>
        </div>
        <!-- <div style='text-align:center' v-if="authentication_state=='WAITING'"> -->
        <div style='text-align:center'>
            <el-button  class='myButton_40 myBtnHover_red btn_width_200 margin_rt60' @click="refuseData.isshow1=true">驳回</el-button>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_200 ' @click="openApprove()">审核通过</el-button>
        </div>

        <Dialog :isshow="refuseData.isshow1" @confirm="refuse()" @cancel="cancel()" :content_title="refuseData.content_title" :content_foot="refuseData.content_foot" :type="1"></Dialog> 
        <Dialog :isshow="refuseData.isshow2" @confirm="approve" @cancel="cancel()" :content_title="refuseData.content_title2" :content_foot="refuseData.content_foot" :type="2"></Dialog> 
        <!-- <Dialog :isshow="refuseData.isshow2" @confirm="conform2()" @cancel="cancel2()" :content_title="refuseData.content_title" :content_foot="refuseData.content_foot" :type="2"></Dialog>  -->
    </div>
</template>
<style scoped>
    .classDetail{padding:75px 20px 20px 60px;}
    .detail_header{font-size: 32px;color: #000000;margin-bottom:40px; }
    .detail_item_sub{margin-bottom:22px;}
    .detail_item{margin-bottom:30px;}
    .detail_title{width:80px;}
    .detail_content.margin_lf{margin-left:39px;}
    .detail_content.detail_content_p{margin-left:16px;line-height:25px;}
    .width_160{width:145px!important;}
    .addImage{width:95px;height:65px;float:left;margin-right:14px;border:1px solid #ccc;}
    .classDetail .el-rate__icon{color:#F95862!important}
</style>
<style>
   
</style>
<script >
    import Dialog  from "components/dialog"
    import Confirm from "components/confirm"
    export default {
        data() {
            return {
                starValue   : 4,
                indent_type : '',
                authentication_state : '',
                result:{
                    "id": 1, // 拳手ID
                    "honor_certificate_images": [], // 拳手荣誉证书
                    "competition_video": null, // 拳手参赛视频
                    "nick_name": "赵柳", // 拳手昵称
                    "allowed_course": ["泰拳","MMA","拳击"], // 可开课程
                    "created_time": "2018-05-18 00:27:43",
                    "updated_time": "2018-05-18 00:27:47",
                    "real_name": "张三", // 拳手真实姓名
                    "height": 170, // 身高
                    "weight": 65, // 体重
                    "birthday": "2018-05-17", // 出生日期
                    "identity_number": "111111111111111111", //身份证
                    "mobile": "11111111111", //手机
                    "is_professional_boxer": true, //是否是专业拳手
                    "club": "20", // 所属拳馆
                    "job": "teacher", // 职业
                    "gender":"男",
                    "introduction": "哈哈", //个人介绍
                    "is_locked": true, // 接单状态 true锁定，false解锁
                    "experience": '北京拓天比图拳馆拓天比图拳馆拓天比图拳馆，北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆。500字拓天比图拳馆。500字北京拓天比图拳馆拓天比图拳馆拓天比图拳馆，北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳京拓天比图拳馆拓天比图拳馆拓天比图拳馆。500字拓天比图拳馆。500字', // 个人经历
                    "authentication_state": "APPROVED", // 认证状态（APPROVED：已通过| WAITING：待审核 | REFUSE：已驳回）
                    "refuse_reason": null, // 驳回原因
                    "user": 5 // 用户ID
                },
                refuseData:{
                    isshow1: false,
                    isshow2: false,
                    content_title:"请输入驳回原因：",
                    content_title2:"请选择此用户可开通的课程类型（选填）：",
                    content_foot:""
                },
                approveData:{
                    isshow: false,
                },
            }
        },
        components: {
           Dialog,
           Confirm
        },
        created() {
            let query = this.$route.query
            if(query.authentication_state){
                this.authentication_state = query.authentication_state;
            }
            this.getDetailData(query.id);
        },
        methods: {
            getDetailData(id) {
                //获取data数据
                let $this   = this
                this.ajax('/boxer/identification/'+id,'get').then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        $this.result=res.data
                        $this.authentication_state = res.data.authentication_state
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
            openApprove(){
                this.refuseData.isshow2=true
            },
            approve(val){
                console.log(val.class_name)
                // this.refuseData.isshow2=false;
                let sendData = {
                        "authentication_state": this.result.authentication_state,    //认证状态
                        "allowed_course": val.class_name  //可开通课程，选项为THAI_BOXING/BOXING/MMA
                    }
                //通过
                this.ajax('boxer/identification/'+this.result.id+'/approve','post',sendData).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
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
            refuse(){
                //驳回
                this.refuseData.isshow1=false;
            },
            cancel(val){
                this.refuseData.isshow1=val;
                this.refuseData.isshow2=val;
            },
            conform(){
            },

        },
    }
</script>