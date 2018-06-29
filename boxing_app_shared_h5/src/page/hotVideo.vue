<template>
    <div class="hot_video_container" :class="{hasClose: ifClose}">
        <div>
            <div class="payTip" v-if="videoObj.price && showPayTip">
                免费观看15S,看完整视频需付费{{videoObj.price / 100}}元
                <div class="close_btn" @click="closePayTipEv"></div>
            </div>
            <div class="video_info_wrapper">
                <template v-show="showVideo">
                    <div v-if="videoObj.try_url || videoObj.url" class="video">
                        <Video :url="videoObj.price ? videoObj.try_url : videoObj.url" height="11.8rem"></Video>
                    </div>
                </template>
                <div class="text">
                    <h2 class="title">{{videoObj.name}}</h2>
                    <div class="desc">{{videoObj.description}}</div>
                </div>
            </div>
            <div class="seeVideo" v-if="videoObj.price" @click="openApp">{{videoObj.price / 100}}元观看完整视频</div>
        </div>
        <TabBar :id="id" :ifShowPraise=false commentType="hot_videos" @openApp="openApp"></TabBar>
        <DownloadTip @closeEv="closeEv"></DownloadTip>
        <Modal :ifShow='showModal' @modalEv="modalEv"></Modal>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
.hot_video_container
    padding-bottom 3.5rem
    &.hasClose
        padding-bottom 0
.payTip
    width 100%
    height 1.2rem
    line-height 1.2rem
    font-size .65rem
    text-align center
    color #fff
    background #F95862
    overflow hidden
    .close_btn
        float right
        margin .3rem 1.2rem auto auto
        width .55rem
        height .55rem
        background url("../assets/images/close_btn.png") no-repeat
        background-size contain
.video
    width 100%
    height 11.8rem
.text
    margin 0 auto
    line-height 1rem
    width 16.3rem
    overflow hidden
    .title
        margin .9rem auto .3rem auto
        font-size .75rem
        color #fff
    .desc
        font-size .6rem
        color: #474955;
.seeVideo
    margin .9rem auto 1.2rem auto
    width 8.5rem
    height 2rem
    line-height 2rem
    text-align center
    font-size .8rem
    color #fff
    background-image linear-gradient(-161deg, #74398A 0%, #F84B62 56%, #FD8F61 100%);
    border-radius 5rem;

</style>

<script type="text/ecmascript-6">
    import config from 'common/my_config';
    import GetTime from 'components/getTime';
    import DownloadTip from 'components/downloadTip';
    import Video from 'components/video';
    import TabBar from 'components/tabBar';
    import Modal from 'components/modal';
    import {wxConfig} from 'common/wechat';

    export default {
        data() {
            return {
                id: '',
                ifClose: false,
                userId: 1000000,
                showPayTip: true,
                showModal: false,
                videoObj: {},
                wx: '',
                dataObj: '',
                showVideo: true
            }
        },
        components: {
            GetTime,
            DownloadTip,
            Video,
            TabBar,
            Modal
        },
        created() {
            this.id = this.$route.params.id;
            this.userId = this.$route.params.userId;
            if (this.id && this.userId) {
                this.getData();
                if (navigator.userAgent.indexOf('MicroMessenger') > -1) {
                    this.sharePage();
                }
                else {
                    this.commonShare();
                }
            }
        },
        methods: {
            getData() {
                this.ajax(`/users/${this.userId}/hot_videos/${this.id}`,'get').then((res) => {
                    if (res && res.data) {
                        this.videoObj = res.data;
                        console.log(this.videoObj)
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        console.log(errors);
                    }
                })
            },
            modalEv(ifShow) {
                if (ifShow) {
                    this.$router.push({path: '/download'})
                }
                else {
                    this.showModal = false
                    this.showVideo = true;
                }
            },
            closePayTipEv() {
                this.showPayTip = false;
            },
            closeEv(val) {
                this.ifClose = val;
            },
            openApp() {
                this.showModal = true;
                this.showVideo = false;
            },
            commonShare() {
                this.ajax(`/hot_videos/${this.id}/share`,'get').then((res) => {
                    if (res && res.data) {
                        document.title = res.data.title;
                        let metaList = document.getElementsByTagName("meta");
                        for (let i = 0; i < metaList.length; i++) {
                            if (metaList[i].getAttribute("name") == "description") {
                                metaList[i].content = res.data.sub_title;
                                return;
                            }
                        }
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        console.log(errors);
                    }
                })
            },
            sharePage() {
                let wechat = require('../common/wechat');
                this.wx = require('weixin-js-sdk');
                wechat.wxConfig();
                this.inWxShare();
                this.ajax(`/hot_videos/${this.id}/share`,'get').then((res) => {
                    if (res && res.data) {
                        this.initShare(res.data);
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        console.log(errors);
                    }
                })
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
            }
        }
    }
</script>