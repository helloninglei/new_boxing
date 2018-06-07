<template>
    <div>
        <div class="boxer_container">
            <template v-if="info.user">
                <img class="portrait" :src="boxer.avatar ? `${config.baseUrl}` + boxer.avatar : avatar_default" />
                <div class="boxer_info">
                    <div class="boxerName">{{boxer.real_name}}</div>
                    <div class="allowed_course">
                        <span v-for="(item, index) in boxer.allowed_course" :key="index">{{item}}<span v-if="index < boxer.allowed_course.length - 1"> / </span></span>
                    </div>
                </div>
                <div class="order_count">约单：{{boxer.order_count}}次</div>
            </template>
            <!--<template v-if="info.video">-->
                <!--<Video :url="info.video"></Video>-->
            <!--</template>-->
            <!--<template v-else>-->
                <!--<div class="pic_wrapper" :class="getClass">-->
                    <!--<img :src="`${config.baseUrl}` + item" v-for="(item, index) in info.images" :key="index" class="pic" @click="showZoomImage(index) "/>-->
                <!--</div>-->
            <!--</template>-->
        </div>
        <div class="separate_line"></div>
        <div class="order_info">
            <div class="order_time">
                <span class="time_icon"></span>
                <span class="text">约单有效期至：2018-05-20</span>
            </div>
            <div class="order_place">
                <span class="place_icon"></span>
                <span class="text">约单拳馆：拓天必图拳馆（马家堡天路蓝图金源...</span>
                <span class="go_in"></span>
            </div>
        </div>
        <div class="separate_line"></div>
        <div class="course_info">
            <div class="title">课程</div>
            <div class="course_item">

            </div>
        </div>
        <DownloadTip @closeEv="closeEv"></DownloadTip>
        <Modal :ifShow='showModal' @modalEv="modalEv"></Modal>
        <ZoomImage @hideSwiper="hideSwiper" :showSwiper="showSwiper" :imageArr="info.images" :slideIndex="slideIndex"></ZoomImage>
    </div>

</template>

<style scoped lang="stylus" type="text/stylus">
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
        .text
            display inline-block
            line-height .75rem
            font-size .65rem
            color #DDDDEC
            vertical-align middle
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

    .boxer_container
        margin-bottom .6rem
        padding .9rem 1rem 0 1rem
        line-height 1.3rem
        box-sizing border-box
        .pic_wrapper1
            .pic
                width 100%
                height 10rem
        .pic_wrapper2
            margin auto auto -.4rem -.75rem
            .pic
                margin auto auto .4rem .75rem
                width 8rem
                height 8rem
        .pic_wrapper3
            margin auto auto -.5rem -.835rem
            .pic
                margin auto auto .5rem .835rem
                width 5rem
                height 5rem
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
                slideIndex: 1,
                ifClose: false,
                showModal: false,
                showSwiper: false,
                avatar_default: require('../assets/images/portrait_default.png'),
                info: {},
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
            const Qs = require('qs');
            let url = 'method=query_sql_dataset_data&projectId=85&appToken=7d22e38e-5717-11e7-907b-a6006ad3dba0';
            let b = Qs.parse(url);
            console.log(Qs.stringify({...b, a: '1'}))
            this.id = this.$route.params.id;
            if (this.id) {
                this.getData();
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

            getData() {
                this.ajax(`/messages/${this.id}`,'get').then((res) => {
                    if (res && res.data) {
                        this.info = res.data;
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
                    Timer = setInterval(function () {
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
                if (this.info.images) {
                    let len = this.info.images.length;
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