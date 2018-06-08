<template>
    <div class="course_detail">
        <div class="boxer_container">
            <template>
                <img class="portrait" :src="boxer.avatar ? `${config.baseUrl}` + boxer.avatar : avatar_default" @click="openApp" />
                <div class="boxer_info">
                    <div class="boxerName">{{boxer.real_name}}<span :class="boxer.gender ? 'man_icon' : 'woman_icon'"></span></div>
                    <div class="allowed_course">
                        <span v-for="(item, index) in boxer.allowed_course" :key="index">{{item}}<span v-if="index < boxer.allowed_course.length - 1"> / </span></span>
                    </div>
                </div>
                <div class="order_count">约单：{{boxer.order_count}}次</div>
            </template>
        </div>
        <div class="separate_line"></div>
        <div class="order_info">
            <div class="order_time">
                <span class="time_icon"></span>
                <span class="text">约单有效期至：{{courseInfo.validity}}</span>
            </div>
            <div class="order_place">
                <span class="place_icon"></span>
                <span class="text" @click="openApp">约单拳馆：{{courseInfo.club_name}} {{courseInfo.club_address}}</span>
                <span class="go_in"></span>
            </div>
        </div>
        <div class="separate_line"></div>
        <div class="course_info">
            <div class="title">课程</div>
            <div class="course_item" v-for="(item, index) in courseInfo.results" :key="index">
                <div class="item_title">
                    <span class="course_name">{{item.course_name}}</span>
                    <span class="evaluate">（{{item.order_count}}个人约过 {{item.score}}分)</span>
                </div>
                <div class="item_time">
                    <span class="name">课程时长</span>
                    <span class="info">{{item.duration}}分钟</span>
                </div>
                <div class="item_charge">
                    <span class="name">课程时长</span>
                    <span class="info">{{item.price/100}}元/次</span>
                </div>
            </div>
        </div>
        <div class="separate_line"></div>
        <div class="introduce">
            <div class="title">自我简介</div>
            <div class="desc">在擂台上播求以犀利的膝法、灵活有力的扫腿、毒蛇吐信般的正蹬技惊四座。</div>
        </div>
        <div class="award_experience_text">
            <div class="title">参赛、获奖及执教经历</div>
            <div class="desc">umpini 拳场 135 lbs 级别排名第一</div>
            <div class="desc">2001 泰国职业拳击协会次轻量级的冠军</div>
            <div class="desc">Omnoi运动场次轻量级的冠军</div>
            <div class="desc">Omnoi运动场轻量级的冠军</div>
        </div>
        <div class="award_experience_pic">
            <div class="title">参赛、获奖及执教经历</div>
            <div class="pic_wrapper" :class="getClass">
                <img :src="`${config.baseUrl}` + item" v-for="(item, index) in images" :key="index" class="pic" @click="showZoomImage(index) "/>
            </div>
        </div>
        <div class="match_video" v-if="video">
            <div class="title">参赛视频</div>
            <Video :url="video"></Video>
        </div>
        <div class="comments_container">
            <span class="comments">评论</span>
            <span v-if="courseInfo.avg_score" class="score">综合得分：<span class="num">{{courseInfo.avg_score}}分</span></span>
            <span class="count">共{{courseInfo.comments_count}}条</span>
        </div>
        <div class="separate_line"></div>
        <div class="see_more" @click="openApp">查看更多>></div>
        <div class="go_order" @click="openApp">去下单</div>
        <DownloadTip @closeEv="closeEv"></DownloadTip>
        <Modal :ifShow='showModal' @modalEv="modalEv"></Modal>
        <ZoomImage @hideSwiper="hideSwiper" :showSwiper="showSwiper" :imageArr="images" :slideIndex="slideIndex"></ZoomImage>
    </div>

</template>

<style scoped lang="stylus" type="text/stylus">
    .course_detail
        margin-bottom 3.5rem
        overflow hidden
    .portrait
        margin-right .6rem
        width 2.5rem
        height 2.5rem
        border-radius 50%
        vertical-align top
    .boxer_info
        display inline-block
        vertical-align middle
        color #fff
        .boxerName
            font-size .75rem
            .man_icon
                display inline-block
                margin-left .4rem
                width .65rem
                height .6rem
                background url("../assets/images/man_icon.png") no-repeat
                background-size contain
            .woman_icon
                display inline-block
                margin-left .4rem
                width .6rem
                height .65rem
                background url("../assets/images/woman_icon.png") no-repeat
                background-size contain
        .allowed_course
            font-size .6rem
            color #cccce3
    .order_count
        float right
        font-size .6rem
        color #8989A1
    .separate_line
        margin 0 auto
        width 16.4rem
        height 1px
        background rgba(72, 72, 85, .5)
    .order_info
        font-size .65rem
        color #DDDDEC
        overflow hidden
        .text
            display inline-block
            width 15rem
            line-height .75rem
            font-size .65rem
            color #DDDDEC
            vertical-align middle
            overflow hidden
            text-overflow ellipsis
            white-space nowrap
        .order_time
            margin 1.1rem auto .45rem 1.2rem
            .time_icon
                display inline-block
                width .6rem
                height .6rem
                background url("../assets/images/time.png") no-repeat
                background-size contain
                vertical-align middle
        .order_place
            margin 0 auto 1.1rem 1.2rem
            .place_icon
                display inline-block
                width .5rem
                height .6rem
                background url("../assets/images/place.png") no-repeat
                background-size contain
                vertical-align middle
            .go_in
                display inline-block
                width .4rem
                height .65rem
                background url("../assets/images/go_in.png") no-repeat
                background-size contain
                vertical-align middle
    .course_info
        margin .9rem auto
        padding 0 1rem
        color #8989A1
        .title
            font-size .75rem
        .course_item
            margin-top .7rem
            .item_title
                margin-bottom .5rem
                .course_name
                    font-size .75rem
                    color #fff
                .evaluate
                    font-size .65rem
            .item_time
                margin-bottom .5rem
                overflow hidden
            .item_charge
                overflow hidden
            .name
                float left
                font-size .65rem
            .info
                float right
                font-size .65rem
                color #fff
    .introduce
        margin 1rem auto
        padding 0 1rem
        overflow hidden
        .title
            margin-bottom .5rem
            font-size .75rem
            color #9DA3B4
        .desc
            line-height 1rem
            font-size .65rem
            color #474955
    .award_experience_text, .award_experience_pic, .match_video
        margin 1rem auto auto auto
        padding 0 1rem
        overflow hidden
        .title
            margin-bottom .5rem
            font-size .75rem
            color #9DA3B4
        .desc
            line-height 1rem
            font-size .65rem
            color #474955
    .comments_container
        margin-top 1rem
        padding 0 1rem
        height 2rem
        line-height 2rem
        font-size .75rem
        color #8989A1
        .comments
            margin-right 3.35rem
        .score
            margin-right 3.35rem
            .num
                color #F95962
        .count
            font-size .65rem
    .see_more
        margin 1rem auto
        width 4rem
        font-size .65rem
        color #8989A1
    .go_order
        margin 0 auto 1rem auto
        width 15rem
        height 2.4rem
        line-height 2.4rem
        text-align center
        font-size .8rem
        color #fff
        background url("../assets/images/go_order.png") no-repeat
        background-size contain
    .boxer_container
        margin-bottom .6rem
        padding .9rem 1rem 0 1rem
        line-height 1.3rem
        box-sizing border-box
    .pic_wrapper1
        margin-top .6rem
        .pic
            width 100%
            height 10rem
    .pic_wrapper2
        margin .6rem auto -.4rem -.75rem
        .pic
            margin auto auto .4rem .75rem
            width 8rem
    .pic_wrapper3
        margin .6rem auto -.5rem -.835rem
        .pic
            margin auto auto .5rem .835rem
            width 5rem
</style>

<script type="text/ecmascript-6">
    import config from 'common/my_config';
    import DownloadTip from 'components/downloadTip';
    import Video from 'components/video';
    import TabBar from 'components/tabBar';
    import Modal from 'components/modal';
    import ZoomImage from 'components/zoomImage';
    import {wxConfig} from 'common/wechat';

    export default {
        data() {
            return {
                video: '/uploads/7a/0c/5e7615519c323324e8667495e77e7adb2cf3.mp4',
                images:[
                    "/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png",
                    "/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png",
                    "/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png",
                    "/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png",
                    "/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png",
                    "/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png",
                    "/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png",
                    "/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png",
                    "/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png",
                ],
                slideIndex: 1,
                ifClose: false,
                showModal: false,
                showSwiper: false,
                avatar_default: require('../assets/images/portrait_default.png'),
                courseInfo:  {},
                dataObj: {},
                wx: '',
                boxer: {
                    "id": 3,
                    "longitude": 120.385763,
                    "latitude": 30.308592,
                    "course_min_price": 150,
                    "order_count": 11,
                    "gender": true,
                    "avatar": "/uploads/31/9e/838678d0449140e5262832eb6361b0b5edaf.jpg",
                    "real_name": "李四",
                    "allowed_course": [
                        "拳击",
                        "泰拳",
                        "MMA"
                    ],
                    "city": "杭州市",
                    "user_id": 1000010
                },

            }
        },

        created() {
            this.id = this.$route.params.id;
            if (this.id) {
                this.getCourseData();
                this.sharePage();
            }
        },

        components: {
            DownloadTip,
            Video,
            TabBar,
            Modal,
            ZoomImage
        },

        methods: {

            getCourseData() {
                this.ajax(`/boxer/${this.id}/course`,'get').then((res) => {
                    if (res && res.data) {
                        this.courseInfo = res.data;
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        console.log(errors);
                    }
                })
            },

            openApp() {
                this.showModal = true;
            },

            modalEv(ifShow) {
                ifShow ?  this.$router.push({path: '/download'}) : this.showModal = false;
            },

            closeEv(val) {
                this.ifClose = val;
            },

            sharePage() {
                if (navigator.userAgent.indexOf('MicroMessenger') > -1) {
                    let wechat = require('../common/wechat');
                    this.wx = require('weixin-js-sdk');
                    wechat.wxConfig();
                    this.inWxShare();
                    this.ajax(`/messages/${this.id}/share`,'get').then((res) => {
                        if (res && res.data) {
                            this.initShare(res.data);
                        }
                    },(err) => {
                        if(err&&err.response){
                            let errors=err.response.data;
                            console.log(errors);
                        }
                    })
                }
            },

            inWxShare () {
                let Timer = '';
                this.dataObj = '';
                this.wx.ready(() => {
                    Timer = setInterval(() => {
                        if (this.dataObj) {
                            clearInterval(Timer);
                            let obj = this.dataObj;
                            this.wx.onMenuShareAppMessage({
                                title: obj.title,
                                desc: obj.desc,
                                link: obj.url,
                                imgUrl: obj.imgUrl,
                            });
                            this.wx.onMenuShareTimeline({
                                title: obj.title,
                                link: obj.url,
                                imgUrl: obj.imgUrl,
                            });
                        }
                        else {
                            clearInterval(Timer);
                        }
                    },300)
                })

            },

            initShare(data) {
                let title = data.title;
                let desc = data.sub_title;
                let imgUrl = data.picture;
                let url = data.url;
                this.dataObj = {title, desc, url, imgUrl};
            },

            showZoomImage(index) {
                this.slideIndex = index;
                this.showSwiper = true;
            },

            hideSwiper() {
                this.showSwiper = false;
            }
        },

        computed: {
            getClass() {
                if (this.images) {
                    let len = this.images.length;
                    if (len) {
                        if (len === 1) return 'pic_wrapper1';
                        else if (len <= 4 && len > 1) return 'pic_wrapper2';
                        else {
                            return 'pic_wrapper3'
                        };
                    }
                    else {
                        return '';
                    }
                }
            }
        }
    }
</script>