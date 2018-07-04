<template>
    <div class="classDetail">
        <BigImg v-if="showImg" @clickit="viewImg" :imgSrc="imgSrc"></BigImg>
        <div class='detail_header' v-if="authentication_state=='APPROVED'">审核通过 
            <span class='detail_content'>已通过的课程类型 ： <span v-for="item in result.allowed_course">{{item}} &nbsp;&nbsp;</span>
                <el-button type="danger" class='myColor_red myButton_40' style='width:95px;margin-top:-13px' @click="openApprove(false)">修改</el-button>
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
                    <div class='detail_content margin_lf'>{{result.gender?'男':'女'}}</div>
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
                    <div class='detail_title'>所属拳馆</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.club}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub' v-show='result.authentication_state=="APPROVED"'>
                <el-col :span="1">
                    <div class='detail_title'>认证称号</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.title}}</div>
                </el-col>
            </el-row>
        </div>
        <hr style="height:1px;border:none;border-top:1px solid rgba(187,187,187,0.2);margin-left:-60px;margin-right:-20px;margin-bottom:30px" >
    
        <div class="detail_item">
            <el-row class='detail_item_sub'>
                <div class='detail_title_lf detail_title'>自我介绍</div>
            </el-row>
            <el-row class='detail_item_sub'>
                <div class='detail_content_p detail_content'>{{result.introduction?result.introduction:'无'}}</div>
            </el-row>
        </div>
        <div class="detail_item">
            <el-row class='detail_item_sub'>
                <div class='detail_title_lf detail_title' style='width:176px'>参赛、获奖及执教经历</div>
            </el-row>
            <el-row class='detail_item_sub' v-show='result.experience'>
                <div class='detail_content_p detail_content'>{{result.experience}}</div>
            </el-row>
        </div>
        <div class="detail_item">
            <el-row class='detail_item_sub'>
                <div class='detail_title_lf detail_title'>荣誉证明</div>
            </el-row>
            <el-row class='detail_item_sub'>
                <div class='detail_content_p detail_content' v-if='result.honor_certificate_images&&result.honor_certificate_images.length>0'>
                    <div class='addImage' v-for="item in result.honor_certificate_images">
                        <img :src="config.baseUrl+item" alt="" width='100%' height='100%' style="cursor:pointer;" @click='clickImg(item)'>
                    </div>
                    <!-- <div class='addImage'>图片</div> -->
                </div>
            </el-row>
        </div>
        <div class="detail_item" >
            <el-row class='detail_item_sub'>
                <div class='detail_title_lf detail_title'>参赛视频</div>
            </el-row>
            <el-row class='detail_item_sub'>
                <div class='detail_content_p detail_content' v-if='result.competition_video'>
                    <div style='width:193px;height:132px;border:1px solid #ccc'>
                        <!-- {{result.competition_video}} -->
                        <video :src="config.baseUrl+result.competition_video" controls="controls" width="100%" height="100%">
                            您的浏览器不支持该视频。
                        </video>
                    </div>
                </div>
            </el-row>
        </div>
        <div style='text-align:center' v-if="authentication_state=='WAITING'">
            <el-button  class='myButton_40 myBtnHover_red btn_width_200 margin_rt60' @click="refuseData.isshow1=true">驳回</el-button>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_200 ' @click="openApprove(true)">审核通过</el-button>
        </div>

        <Dialog :isshow="refuseData.isshow1" @confirm="refuse" @cancel="cancel()" :content_title="refuseData.content_title" :content_foot="refuseData.content_foot" :type="1"></Dialog> 
        <Dialog :isshow="refuseData.isshow2" @confirm="approve" @cancel="cancel()" :content_title="refuseData.content_title2" :content_foot="refuseData.content_foot" :type="2" :showIndenTitle="showIndenTitle"></Dialog> 
        
    </div>
</template>
<style scoped>
    .classDetail{padding:75px 20px 20px 60px;}
    .detail_header{font-size: 32px;color: #000000;margin-bottom:40px; }
    .detail_item_sub{margin-bottom:22px;}
    .detail_item{margin-bottom:30px;}
    .detail_title{width:80px;}
    .detail_title_lf{width:80px;text-align: left}
    .detail_content.margin_lf{margin-left:50px;}
    .detail_content.detail_content_p{margin-left:16px;line-height:25px;}
    .width_160{width:145px!important;}
    .addImage{width:95px;height:65px;float:left;margin-right:14px;}
    .classDetail .el-rate__icon{color:#F95862!important}
</style>
<style>
   
</style>
<script >
    import Dialog  from "components/dialog"
    import Confirm from "components/confirm"
    import BigImg  from 'components/bigImg';
    export default {
        data() {
            return {
                starValue   : 4,
                indent_type : '',
                authentication_state : '',
                showImg   : false,
                imgSrc    : '',
                result:{
                    
                },
                showIndenTitle:true,
                refuseData:{
                    isshow1: false,
                    isshow2: false,
                    content_title:"请输入驳回原因：",
                    content_title2:"请选择可开通的课程类型（最少选一个）：",
                    content_foot:""
                },
                approveData:{
                    isshow: false,
                },
            }
        },
        components: {
           Dialog,
           Confirm,
           BigImg
        },
        created() {
            let query = this.$route.query
            if(query.authentication_state){
                this.authentication_state = query.authentication_state;
            }
            this.boxerId = query.id
            this.getDetailData(this.boxerId);
        },
        methods: {
            getDetailData(id) {
                //获取data数据
                let $this   = this
                this.ajax('/boxer/identification/'+id,'get').then(function(res){
                    if(res&&res.data){
                        // console.log(res.data)
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
            openApprove(showIndenTitle){
                this.showIndenTitle= showIndenTitle;
                this.refuseData.isshow2=true
            },
            approve(val){
                console.log(val.class_name)
                let $this    = this;
                let sendData = {
                        "authentication_state": 'APPROVED',    //认证状态
                        "allowed_course": val.class_name  //可开通课程，选项为THAI_BOXING/BOXING/MMA
                    }
                if(this.showIndenTitle){
                    sendData.title = val.title
                }
                //通过
                this.ajax('boxer/identification/'+this.result.id+'/approve','post',sendData).then(function(res){
                    if(res&&res.data){
                        console.log(res.data)
                        $this.refuseData.isshow2=false;
                        
                        $this.getDetailData($this.boxerId);
                    }

                },function(err){
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            $this.$message({
                                message: errors[key][0],
                                type: 'error'
                            });
                        } 
                    } 
                })
            },
            refuse(val){
                //驳回
                let $this    = this;
                let sendData = {
                        "authentication_state": 'REFUSE',    //认证状态
                        "refuse_reason": val.textarea_val  //可开通课程，选项为THAI_BOXING/BOXING/MMA
                    }
                this.ajax('boxer/identification/'+this.result.id+'/refuse','post',sendData).then(function(res){
                    console.log(res)
                    if(res&&res.data){
                        // console.log(res.data)
                        $this.refuseData.isshow1=false;
                        $this.getDetailData($this.boxerId);
                    }

                },function(err){
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            $this.$message({
                                message: errors[key][0],
                                type: 'error'
                            });
                        } 
                    } 
                })
            },
            cancel(val){
                this.refuseData.isshow1=val;
                this.refuseData.isshow2=val;
            },
            clickImg(img) {
                // 获取当前图片地址
                this.imgSrc =this.config.baseUrl+ img;
                // this.imgSrc ="http://img.zcool.cn/community/010f87596f13e6a8012193a363df45.jpg@1280w_1l_2o_100sh.jpg";
                this.showImg=true;
            },
            viewImg(){
                this.showImg = false;
            },

        },
    }
</script>