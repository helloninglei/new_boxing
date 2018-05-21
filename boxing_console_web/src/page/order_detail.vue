<template>
    <div class="classDetail">
        <div class='detail_header'>{{result.status_name}}</div>
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
                <el-col :span="16">
                    <el-button type="danger" class='myColor_red myButton_40' style='width:200px;margin-top:-13px' @click="checkIdent(result.id)">查看拳手认证信息</el-button>
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
                    <div class='detail_content margin_lf'>单价元/次</div>
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
                <el-col :span="23" v-if="result.status==2">
                    <div class='detail_content margin_lf'>请购买保险 
                        <el-button  class='myBtnHover_red myButton_20' size='mini' style='width:100px;height:25px!important;margin-top:-4px'>标记保险</el-button>
                    </div>
                </el-col>
                <el-col :span="23" v-if="result.status>2">
                    <div class='detail_content margin_lf'>20元</div>
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
                    <div class='detail_content margin_lf'>{{result.payment_type}}</div>
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
                    <div class='detail_content margin_lf'>aaaaa</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub' v-if="result.status>2">
                <el-col :span="2">
                    <div class='detail_title width_160'>用户确认完成时间</div>
                </el-col>
                <el-col :span="22">
                    <div class='detail_content margin_lf'>aaaaa</div>
                </el-col>
            </el-row>
        </div>
        <div class="detail_item" v-if="result.status==4">
            <el-row class='detail_item_sub'>
                <el-col :span="2">
                    <div class='detail_title width_160'>用户评论</div>
                </el-col>
                <el-col :span="22">
                    <div class='detail_content margin_lf'>
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
                    <div class='detail_content margin_lf'>2018-02-10 12:12:12</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="22" :offset="2">
                    <div class='detail_content margin_lf' style='line-height: 25px'>300字我在遇见冬哥了，看他在这里！我在遇见冬哥了，看他在这里！我在遇见冬哥了，看他在这里！我在遇见冬哥了，看他在这里！我在遇见冬哥了，看他在这里！300字我在遇见冬哥了，看他在这里！我在遇见冬哥了，看他在这里！我在遇见冬哥了，看他在这里！我在遇见冬哥了，看他在这里！我在遇见冬哥了，看他在这里！</div>
                </el-col>
            </el-row>
            <el-row class='detail_item_sub'>
                <el-col :span="22" :offset="2">
                    <div class='detail_content margin_lf'>
                        <div class='addImage'></div>
                        <div class='addImage'></div>
                        <div class='addImage'></div>
                        <div class='addImage'></div>
                    </div>
                </el-col>
            </el-row>
        </div>
    </div>
</template>
<style scoped>
    .classDetail{padding:75px 20px 20px 60px;}
    .detail_header{font-size: 32px;color: #000000;margin-bottom:40px; }
    .detail_item_sub{margin-bottom:22px;}
    .detail_item{margin-bottom:50px;}
    .detail_title{width:80px;}
    .detail_content.margin_lf{margin-left:30px;}
    .width_160{width:145px!important;}
    .addImage{width:95px;height:65px;float:left;margin-right:14px;border:1px solid #ccc;}
    .classDetail .el-rate__icon{color:#F95862!important}
</style>
<style>
   
</style>
<script>
    export default {
        data() {
            return {
                starValue:4,
                result:{
                    "id": 1, //订单id
                    "status_name":'待付款',
                    "status": 1, //订单状态（1:待付款/未支付；2:待使用; 3:待评论; 4:已完成; 5:已过期）
                    "out_trade_no": 11111111, //订单号
                    "payment_type": 1,//支付方式（1:支付宝；2:微信；3:余额）
                    "amount": 120, //金额
                    "order_time": "2018-05-16 08:29:56",//下单时间
                    "pay_time": null, //支付时间
                    "course_name": "THAI_BOXING",//课程名
                    "course_duration": 120, //课程时长
                    "course_validity": "2018-08-25", //课程有效期
                    "user_mobile": "10000000000", //用户手机号
                    "user_id": 5, //用户id
                    "user_nickname": "赵柳", //用户昵称
                    "boxer_name": "张三", //拳手姓名
                    "boxer_mobile": "111111111", //拳手手机号
                    "object_id": 1, //课程id
                    "club_name": "club01" //拳手所在拳馆
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
                this.ajax('/course/order/'+id,'get',{},{}).then(function(res){
                    if(res&&res.data){
                        $this.result=res.data;
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
                console.log('查看认证信息'+id)
            }
        },
    }
</script>