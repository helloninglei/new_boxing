<template>
    <div class="trends_container" :class="{hasClose: ifClose}">
        <div class="trends_container_head">
            <template v-if="info.user">
                <div class="portrait_container">
                    <img class="portrait" :src="info.user.avatar ? info.user.avatar + `${portraitQuery}` : avatar_default" />
                    <div class="sign_icon" :class="info.user.user_type"></div>
                </div>

                <span class="userName">{{info.user.nick_name}}</span>
                <span class="is_following" @click="followEv">
                    <template v-if="info.user.is_following">
                        <span class="follow"></span>
                        已关注
                    </template>
                    <template v-else>
                        <span class="no_follow"></span>
                        关注
                    </template>
                </span>
            </template>
            <GetTime :createTime="info.created_time" class="getTime"></GetTime>
            <div class="content">{{info.content}}</div>
            <template v-if="info.video">
                <Video :url="info.video" v-show="showVideo"></Video>
            </template>
            <template v-else>
                <div class="pic_wrapper" :class="getClass">
                    <img :src="item + `${compressPic}`" v-for="(item, index) in info.images" :key="index" class="pic" @click="showZoomImage(index) "/>
                </div>
            </template>
        </div>
        <TabBar :id="id" :ifShowPraise=true commentType="message" @openApp="openApp" :praiseNum="praiseNum"></TabBar>
        <div class="bottom_bar">
            <div class="bar_container">
                <div class="comment_btn" @click="openApp">
                    <div class="comment_icon"></div>
                    评论
                </div>
                <div class="line"></div>
                <div class="praise_btn"  @click="openApp">
                    <div class="praise_icon"></div>
                    点赞
                </div>
            </div>
        </div>
        <DownloadTip @closeEv="closeEv" :id="id" page="messages" @tipOpenType="tipOpenType"></DownloadTip>
        <Modal :ifShow='showModal' @modalEv="modalEv"></Modal>
        <ZoomImage @hideSwiper="hideSwiper" :showSwiper="showSwiper" :imageArr="bigPicArr" :slideIndex="slideIndex"></ZoomImage>
        <PopTip v-if="popTip" @click.native="closePopTip"></PopTip>
    </div>

</template>

<style scoped lang="stylus" type="text/stylus">
.created_time.getTime
    margin 0
    margin-left 2.2rem
.trends_container
    padding-bottom  3.5rem
    &.hasClose
        padding-bottom 0
.portrait_container
    display inline-block
    position relative
    .sign_icon
        position absolute
        right 0
        bottom 0
        width .9rem
        height .9rem
        &.boxer_icon
            background url("../assets/images/boxer_icon.png") no-repeat
            background-size contain
        &.mark_icon
            background url("../assets/images/mark_icon.png") no-repeat
            background-size contain
        &.media_icon
            background url("../assets/images/media_icon.png") no-repeat
            background-size contain
.portrait
    width 2rem
    height 2rem
    border-radius 50%
    vertical-align middle
.userName
    vertical-align middle
    color #fff
.trends_container_head
    margin-top 1.3rem
    padding 0 1rem
    line-height 1.3rem
    .is_following
        float right
        display inline-block
        width 3.3rem
        height 1.3rem
        line-height 1.3rem
        text-align center
        font-size .5rem
        color #8989A1
        border 1px solid #8989A1
        border-radius 1rem
        vertical-align middle
        .follow, .no_follow
            display inline-block
            width .7rem
            height .7rem
            vertical-align middle
        .follow
            background url("../assets/images/follow.png") no-repeat
            background-size contain
        .no_follow
            background url("../assets/images/no_follow.png") no-repeat
            background-size contain
    .content
        margin-bottom .5rem
        font-size .7rem
        color #fff
    .video_container
        width 100%
        height 10rem
    .pic_wrapper1
        .pic
            width 100%
            /*height 10rem*/
    .pic_wrapper2
        margin auto auto -.4rem -.75rem
        .pic
            margin auto auto .4rem .75rem
            width 8rem
    .pic_wrapper3
        margin auto auto -.5rem -.835rem
        .pic
            margin auto auto .5rem .835rem
            width 5rem
.bottom_bar
    width 100%
    height 2.4rem
    line-height 2.4rem
    font-size .7rem
    color #fff
    background: #31313B;
    .bar_container
        display -webkit-flex
        display flex
        .line
            display inline-block
            margin-top .7rem
            width 1px
            height 1rem
            background #484855
        .comment_btn
            flex 1
            -webkit-flex 1
            text-align center
            .comment_icon
                display inline-block
                width .7rem
                height .7rem
                background url("../assets/images/comment_icon.png")
                background-size contain
                vertical-align middle
        .praise_btn
            flex 1
            -webkit-flex 1
            text-align center
            .praise_icon
                display inline-block
                width .7rem
                height .7rem
                background url("../assets/images/praise_icon.png")
                background-size contain
                vertical-align middle
</style>

<script type="text/ecmascript-6">
    import config from 'common/my_config';
    import GetTime from 'components/getTime';
    import DownloadTip from 'components/downloadTip';
    import Video from 'components/video';
    import TabBar from 'components/tabBar';
    import Modal from 'components/modal';
    import ZoomImage from 'components/zoomImage';
    import PopTip from 'components/popTip';
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
                dataObj: '',
                wx: '',
                compressPic: '',
                thumbnail: '',
                portraitQuery: '',
                bigPicArr: [],
                showVideo: true,
                id: '',
                praiseNum: '',
                popTip: false
            }
        },

        created() {
            this.id = this.$route.params.id;
            if (this.id) {
                this.getData();
                this.sharePage();
            }
        },
        isInWeChat() {
            let u = navigator.userAgent, app = navigator.appVersion;
            return /(micromessenger|webbrowser)/.test(u.toLocaleLowerCase());
        },
        mounted(){
            setTimeout(() => {
                let baseSize = parseFloat(document.getElementsByTagName('html')[0].style.fontSize);
                this.portraitQuery = `?x-oss-process=image/resize,w_${parseInt(baseSize * 4)},m_fill`;
            },0)
        },

        components: {
            GetTime,
            DownloadTip,
            Video,
            TabBar,
            Modal,
            ZoomImage,
            PopTip
        },

        methods: {
            getData() {
                this.ajax(`/messages/${this.id}`,'get').then((res) => {
                    if (res && res.data) {
                        this.info = res.data;
                        this.praiseNum = res.data.like_count;
                        switch (this.info.user.user_type) {
                            case '拳手':
                                this.info.user.user_type = 'boxer_icon';
                                break;
                            case '自媒体':
                                this.info.user.user_type = 'media_icon';
                                break;
                            case '名人':
                                this.info.user.user_type = 'mark_icon';
                                break;
                            default:
                                this.info.user.user_type = ''
                                break;
                        };
                        let baseSize = parseFloat(document.getElementsByTagName('html')[0].style.fontSize);
                        let picArrSize = this.info.images.length;
                        let thumbnail_swiper = 18.75 * baseSize;
                        if (picArrSize === 1) {
                            this.compressPic = `?x-oss-process=image/resize,m_fill,w_${parseInt(thumbnail_swiper)}`
                        }
                        else if (picArrSize > 1 && picArrSize < 5) {
                            this.compressPic = `?x-oss-process=image/resize,m_fill,w_${parseInt(8 * baseSize)}`
                        }
                        else if (picArrSize > 5) {
                            this.compressPic = `?x-oss-process=image/resize,m_fill,w_${parseInt(5 * baseSize)}`
                        }
                        let compressPic = `?x-oss-process=image/resize,w_${parseInt(thumbnail_swiper)}/quality,q_90`;
                        this.info.images.forEach((item) => {
                            let item_pic = item + compressPic;
                            this.bigPicArr.push(item_pic);
                        })
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        console.log(errors);
                    }
                })
            },

            openApp() {
                this.showVideo = false;
                this.showModal = true;
            },

            modalEv(ifShow) {
                if (ifShow) {
                    if (this.isInWeChat()) {
                        this.popTip = true;
                        this.showVideo = false;
                    }
                    else {
                        location.href = `boxing://api.bituquanguan.com:80/messages?id=${this.id}&time=${new Date().getTime()}`;
                    }
                }
                else {
                    this.showModal = false;
                    this.showVideo = true;
                }
            },

            followEv() {
                if (!this.info.user.is_following) {
                    this.showModal = true;
                }
            },

            closeEv(val) {
                this.ifClose = val;
            },

            tipOpenType(e) {
                if (e) {
                    this.popTip = true;
                    this.showVideo = false;
                }
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
                            console.log(obj)
                            console.log(this.wx)
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
                this.showVideo = false;
            },
            hideSwiper() {
                this.showSwiper = false;
                this.showVideo = true;
            },
            closePopTip() {
                this.popTip = false;
                this.showVideo = true;
            },
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