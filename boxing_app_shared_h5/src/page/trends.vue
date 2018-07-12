<template>
    <div class="trends_container" :class="{hasClose: ifClose}">
        <div class="trends_container_head">
            <template v-if="info.user">
                <img class="portrait" :src="info.user.avatar ? info.user.avatar + `${portraitQuery}` : avatar_default" />
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
            <GetTime :createTime="info.created_time"></GetTime>
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
        <TabBar :id="id" :ifShowPraise=true commentType="message" @openApp="openApp"></TabBar>
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
        <DownloadTip @closeEv="closeEv"></DownloadTip>
        <Modal :ifShow='showModal' @modalEv="modalEv"></Modal>
        <ZoomImage @hideSwiper="hideSwiper" :showSwiper="showSwiper" :imageArr="bigPicArr" :slideIndex="slideIndex"></ZoomImage>
    </div>

</template>

<style scoped lang="stylus" type="text/stylus">
.trends_container
    padding-bottom  3.5rem
    &.hasClose
        padding-bottom 0
.portrait
    width 1.1rem
    height 1.1rem
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
                showVideo: true
            }
        },

        created() {
            this.id = this.$route.params.id;
            if (this.id) {
                this.getData();
                this.sharePage();
            }
        },

        mounted(){
            setTimeout(() => {
                let baseSize = parseFloat(document.getElementsByTagName('html')[0].style.fontSize);
                this.portraitQuery = `?x-oss-process=image/resize,w_${parseInt(baseSize)},m_fill`;
            },0)
        },

        components: {
            GetTime,
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
                    this.$router.push({path: '/download'})
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