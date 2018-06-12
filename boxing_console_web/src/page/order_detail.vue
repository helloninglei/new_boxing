<template>
    <div class="classDetail">
        <div class='detail_header'>{{result.status_name}}</div>
        <BigImg v-if="showImg" @clickit="viewImg" :imgSrc="imgSrc"></BigImg>
        <div class='detail_item'>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>用户信息</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>ID</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_id}}</div>
                </el-col>
                 <el-col :span="1">
                    <div class='detail_title'>昵称</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_nickname}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>手机号</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.user_mobile}}</div>
                </el-col>
            </el-row>
        </div>
        <div class="detail_item">
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>拳手信息</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>姓名</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.boxer_name}}</div>
                </el-col>
                <el-col :span="1">
                    <div class='detail_title'>手机号</div>
                </el-col>
                <el-col :span="3">
                    <div class='detail_content margin_lf'>{{result.boxer_mobile}}</div>
                </el-col>
                <el-col :span="15" :offset='1'>
                    <el-button type="danger" class='myColor_red myButton_40 ' style='width:200px;margin-top:-13px' @click="checkIdent(result.boxer_id)">查看拳手认证信息</el-button>
                </el-col>
            </el-row>
        </div>
        <div class="detail_item">
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>订单信息</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>订单号</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.out_trade_no}}  (约单有效期至{{result.course_validity}})</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>课程</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.course_name}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>支付金额</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'> {{result.amount}}元/次</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>时长</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.course_duration}}分钟</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>约单拳馆</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.club_name}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub' v-if="result.status>1">
                <el-col :span="1">
                    <div class='detail_title'>保险</div>
                </el-col>
                <el-col :span="23" v-if="result.insurance_amount==0||result.insurance_amount>0? false : true">
                    <div class='detail_content margin_lf'>请购买保险 
                        <el-button  class='myBtnHover_red myButton_20' size='mini' style='width:100px;height:25px!important;margin-top:-4px' @click="addCount()">标记保险</el-button>
                    </div>
                </el-col>
                <el-col :span="23" v-else>
                    <div class='detail_content margin_lf'>{{(result.insurance_amount/100).toFixed(2)}}元</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub' v-if="result.status==1">
                <el-col :span="1">
                    <div class='detail_title'>下单时间</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.order_time}}</div>
                </el-col>
            </el-row>
        </div>
        <div class="detail_item" v-if="result.status>1">
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>下单时间</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.order_time}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>支付时间</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.pay_time}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>支付方式</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.payment_type_name}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="1">
                    <div class='detail_title'>支付金额</div>
                </el-col>
                <el-col :span="23">
                    <div class='detail_content margin_lf'>{{result.amount}}元</div>
                </el-col>
            </el-row>
        </div>
        <div class="detail_item" v-if="result.status>1&&result.status!=5">
            <el-row class='detail_item_sub'>
                <el-col :span="2">
                    <div class='detail_title width_160'>拳手确认完成时间</div>
                </el-col>
                <el-col :span="22">
                    <div class='detail_content margin_lf50'>{{result.boxer_confirm_time}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub' v-if="result.user_confirm_time">
                <el-col :span="2">
                    <div class='detail_title width_160'>用户确认完成时间</div>
                </el-col>
                <el-col :span="22">
                    <div class='detail_content margin_lf50'>{{result.user_confirm_time}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub' v-else-if="result.boxer_confirm_time&&(new Date()-new Date(result.boxer_confirm_time)-7*24*60*60*1000>0)" style='background: #ebebeb;padding:10px 0;width:600px'>
                <el-col :span="4">
                    <div class='detail_title width_160'>用户确认完成时间</div>
                </el-col>
                <el-col :span="20">
                    <div class='detail_content margin_lf50' style='margin-left:54px'>{{result.user_moren_time}} （过期默认确认）</div>
                </el-col>
            </el-row>
        </div>
        <div class="detail_item" v-if="result.status==4">
            <el-row class='detail_item_sub'>
                <el-col :span="2">
                    <div class='detail_title width_160'>用户评论</div>
                </el-col>
                <el-col :span="22">
                    <div class='detail_content margin_lf50'>
                        <el-rate
                          v-model="starValue"
                          disabled
                          :colors="['#F95862', '#F95862', '#F95862']"
                          :allow-half="false"
                          >
                        </el-rate>
                    </div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="22" :offset="2">
                    <div class='detail_content margin_lf50'>{{result.comment_time}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="22" :offset="2">
                    <div class='detail_content margin_lf50' style='line-height: 25px'>{{result.comment_content}}</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="22" :offset="2">
                    <div class='detail_content margin_lf50' v-show='result.comment_images&&result.comment_images.length>0'>
                        <div class='addImage' v-for='value in result.comment_images'>
                            <img :src="config.baseUrl+value" alt="" height='100%' @click='clickImg(value)' style='cursor:pointer'>
                        </div>
                    </div>
                </el-col>
            </el-row>
        </div>
        <DialogLabel :isshow="dialog_label_data.isshow" @confirm="confirm" @cancel="cancel3()" :content_title="dialog_label_data.content_title" :content_foot="dialog_label_data.content_foot" :type="'number'"></DialogLabel>
    </div>
</template>
<style scoped>
    .classDetail{padding:75px 20px 20px 60px;}
    .detail_header{font-size: 32px;color: #000000;margin-bottom:40px; }
    .detail_item_sub{margin-bottom:22px;}
    .detail_item{margin-bottom:50px;}
    .detail_title{width:80px;text-align: right;}
    .detail_content.margin_lf{margin-left:40px;}
    .detail_content.margin_lf50{margin-left:60px;}
    .width_160{width:145px!important;}
    .addImage{height:65px;float:left;margin-right:14px;}
    .classDetail .el-rate__icon{color:#F95862!important}
</style>
<style>
   
</style>
<script>
    import DialogLabel from "components/dialog_label"
    import BigImg  from 'components/bigImg';
    export default {
        data() {
            return {
                starValue:4,
                dialog_label_data:{
                    isshow:false,
                    content_title:"",
                },
                showImg   : false,
                imgSrc    : '',
                addData : {},
                orderId :'',
                result:{
                    // "id": 1, //订单id
                    // "status": 4, //订单状态（1:待付款/未支付；2:待使用; 3:待评论; 4:已完成; 5:已过期）
                    // "out_trade_no": 11111111, //订单号
                    // "payment_type": 1,//支付方式（1:支付宝；2:微信；3:余额）
                    // "amount": 120, //金额
                    // "comment_score": null, //订单评分
                    // "comment_time": '2015-03-08 12:34:44', //订单评论时间
                    // "comment_content": '评论内容评论内容评论内容评论内容品论内容评论内容评论内容评论内容', //订单评论内容
                    // "comment_images": [
                    //     "/uploads/a2/ab/da7f76418372eacd8c3410d53a5a6a0e79d4.png",
                    //     "/uploads/1c/c3/fbeb379b103be64b4ff74e99f61846386eb2.png",
                    //     "/uploads/1c/c3/fbeb379b103be64b4ff74e99f61846386eb2.png",

                    // ], //订单评论图片
                    // "order_time": "2018-05-16 08:29:56",//下单时间
                    // "pay_time": null, //支付时间
                    // "course_name": "THAI_BOXING",//课程名
                    // "course_duration": 120, //课程时长
                    // "course_validity": "2018-08-25", //课程有效期
                    // "user_mobile": "10000000000", //用户手机号
                    // "user_id": 5, //用户id
                    // "user_nickname": "赵柳", //用户昵称
                    // "boxer_name": "张三", //拳手姓名
                    // "boxer_mobile": "111111111", //拳手手机号
                    // "object_id": 1, //课程id
                    // "club_name": "club01" //拳手所在拳馆
                }
            }
        },
        components: {
           DialogLabel,
           BigImg
        },
        created() {
            let query = this.$route.query
            this.getDetailData(query.id);
            this.orderId = query.id
        },
        methods: {
            getDetailData(id) {
                //获取data数据
                let $this   = this
                this.ajax('/course/order/'+id,'get',{},{}).then(function(res){
                    if(res&&res.data){
                        $this.result=res.data;
                        $this.starValue = res.data.comment_score;
                        // 用户确认默认时间
                        $this.result.user_moren_time = new Date($this.result.boxer_confirm_time)
                        $this.result.user_moren_time.setDate($this.result.user_moren_time.getDate()+7)
                        $this.result.user_moren_time = $this.result.user_moren_time.Format("yyyy-MM-dd hh:mm:ss")
                        if($this.result.course_name=='BOXING'){
                            $this.result.course_name='拳击'
                        }else if($this.result.course_name=='THAI_BOXING'){
                            $this.result.course_name='泰拳'
                        }
                        if($this.result.payment_type==1){
                            $this.result.payment_type_name='支付宝'
                        }else if($this.result.payment_type==2){
                            $this.result.payment_type_name='微信'
                        }else{
                            $this.result.payment_type_name='余额'
                        }
                        $this.result.amount = ($this.result.amount/100).toFixed(2)
                        // $this.result.insurance_amount = ($this.result.insurance_amount/100).toFixed(2)
                        switch ($this.result.status){
                            case 1 :
                            $this.result.status_name='待付款';
                            break;
                            case 2 :
                            $this.result.status_name='待使用';
                            break;
                            case 3:
                            $this.result.status_name='待评论';
                            break;
                            case 4 :
                            $this.result.status_name='已完成';
                            break;
                            case 5 :
                            $this.result.status_name='已过期';
                            break;
                        }
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
            checkIdent(id){
                // 参数 ID 审核状态ident_type
                this.$router.push({path: '/Boxerindentdetail', query:{id:id}});
            },
            confirm(val){
                let $this = this;
                this.addData.insurance_amount=val*100;
                this.ajax('/order/'+this.orderId+'/mark_insurance','post',this.addData).then(function(res){
                    if(res&&res.status==204){
                        $this.result.insurance_amount = val
                        $this.getDetailData($this.orderId);
                        $this.dialog_label_data.isshow=false
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
            addCount(id){
                this.dialog_label_data.isshow=true
            },
            cancel3(val){
                this.dialog_label_data.isshow=val;
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