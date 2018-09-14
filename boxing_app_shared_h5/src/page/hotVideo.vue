<template>
    <div class="hot_video_container" :class="{hasClose: ifClose}">
        <div>
            <div class="payTip" v-if="videoObj.price && showPayTip">
                免费观看15S,看完整视频需付费{{videoObj.price / 100}}元
                <div class="close_btn" @click="closePayTipEv"></div>
            </div>
            <div class="video_info_wrapper">

                <div v-if="videoObj.try_url || videoObj.url" class="video">
                    <Video :url="videoObj.price ? videoObj.try_url : videoObj.url" height="11.8rem" v-show="showVideo"></Video>
                </div>
                <div class="user-wrap clearfix" v-if="videoObj.bind_user">
                    <div class="portrait"><img :src="videoObj.bind_user.avatar" alt=""></div>
                    <div class="user-info">
                        <div class="user-name">{{videoObj.bind_user.nick_name}}</div>
                        <div class="create-time" v-if="videoObj.bind_user.created_time">
                            {{videoObj.bind_user.created_time.substr(0,11)}}发布<span
                                class="see">{{videoObj.bind_user.forward_count}}人观看</span></div>
                    </div>
                    <div v-if="videoObj.is_like" class="follow already" @click="openApp"></div>
                    <div v-else class="follow" @click="openApp"></div>
                </div>
                <div class="text">
                    <h2 class="title">{{videoObj.name}}</h2>
                    <div class="desc">{{videoObj.description}}</div>
                </div>
                <div class="relevant-recommendations" v-if="videoObj.other_users&&videoObj.other_users.length">
                    <div class="title">相关推荐</div>
                    <swiper :options="swiperOption" ref="mySwiper" class="user-list">
                        <swiper-slide v-for="(item,index) in videoObj.other_users" :key="index">
                            <div class="user-item">
                                <div class="portrait"><img :src="item.avatar" alt=""></div>
                                <p>{{item.nick_name}}</p>
                            </div>
                        </swiper-slide>
                    </swiper>

                </div>

            </div>
            <div class="seeVideo" v-if="videoObj.price" @click="openApp">{{videoObj.price / 100}}元观看完整视频</div>
        </div>

        <TabBar :id="id" :ifShowPraise=true :praiseNum="videoObj.like_count" commentType="hot_videos"></TabBar>
        <div class="more-recommend" v-if="videoObj.recommend_videos&&videoObj.recommend_videos.length">
            <div class="title">更多推荐</div>
            <div class="video-list">
                <div class="recommend-video" v-for="(item,index) in videoObj.recommend_videos" :key="index">
                    <div class="is-pay">{{item.price?'付费':'免费'}}</div>
                    <div class="play-btn" @click="playVideoEv(item.id,item.user_id)"></div>
                    <img :src="item.url+'?x-oss-process=video/snapshot,t_0,f_jpg,w_0,h_0,m_fast'" :alt="item.name">
                    <div class="video-name">{{item.name}}</div>
                </div>

            </div>
        </div>
        <DownloadTip @closeEv="closeEv" :id="id" :userId="userId" page="hot_videos"></DownloadTip>
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

    .user-wrap
        width 16.3rem
        margin: 0 auto
        color #ffffff
        margin-top: 1.2rem
        margin-bottom: 1.3rem
        .portrait
            float: left
        .user-info
            float: left
            width: 10rem
            margin-left: 0.5rem
        .user-name
            color #fff
            margin-top: 0.3rem
        .create-time
            color #8989A1
            margin-top: 0.3rem
            .see
                margin-left: 0.6rem

        .follow
            height: 1.3rem
            width 3.2rem
            float: right
            line-height 1.3rem
            background url("../assets/images/icon_plus.png") no-repeat
            background-size contain
            &.already
                background url("../assets/images/icon_right.png") no-repeat
                background-size contain


    .relevant-recommendations
        width 16.3rem
        margin: 0 auto
        font-size: 0.75rem
        color #fff
        margin-top: 0.18rem
        .title
        .user-list
            margin-top: 1rem
            .user-item
                .portrait
                    margin: 0 auto
                    img {
                        width: 100%

                    }
                p {
                    width: 3.3rem
                    margin-top: 0.5rem
                    text-align center
                    overflow: hidden;
                    text-overflow:ellipsis;
                    white-space: nowrap;
                }

    .portrait
        width 2rem
        height 2rem
        border-radius 50%
        vertical-align middle
        img {
            width: 100%
            height 100%
            border-radius 50%
        }

    .more-recommend
        margin-top: 1.4rem
        .title
            width 16.3rem
            margin: 0 auto
            color #ffffff
        .video-list
            .recommend-video
                width: 100%
                overflow hidden
                height: 10rem
                margin-top: 1rem
                position relative
                text-align center
                .is-pay
                    position absolute
                    left: 0.6rem
                    top: 0.6rem
                    opacity 0.6
                    background rgba(29,29,39,1)
                    border-radius: 0.1rem;
                    color #DDDDEC
                    font-size: 0.7rem
                    width: 2.4rem
                    height 1.2rem
                    line-height 1.2rem
                    text-align center
                    box-sizing border-box
                .video-name
                    width: 100%
                    position absolute
                    bottom: 0.5rem
                    color #fff
                    font-size: 0.6rem
                    padding-left: 1.4rem
                    padding-right: 1.4rem
                    line-height 0.8rem
                    text-align left
                    box-sizing border-box
                    overflow: hidden;
                    text-overflow:ellipsis;
                    white-space: nowrap;
                img {
                    height: 100%
                }
                .play-btn
                    position absolute
                    width: 2.6rem
                    height: 2.6rem
                    background url("../assets/images/icon_play.png") no-repeat
                    background-size contain
                    left: 50%
                    top: 50%
                    margin-left: -1.3rem
                    margin-top: -1.3rem


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
                swiperOption: {
                    slidesPerView: 5
                },
                id: '',
                ifClose: false,
                userId: 1000000,
                showPayTip: true,
                showModal: false,
                videoObj: {},
                wx: '',
                dataObj: '',
                showVideo: true,
                userInfo: {}
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
        mounted(){
        },
        computed: {
            swiper() {
                return this.$refs.mySwiper.swiper
            }

        },
        methods: {
            isIos() {
                let u = navigator.userAgent, app = navigator.appVersion;
                return !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);
            },
            playVideo(){
                if(this.isIos()){
                    document.querySelector('video').play();
                }

            },
            playVideoEv(videoId,userId){
                this.id = videoId.toString();
                this.userId = userId.toString();
                window.scrollTo(0,0)
                this.getData(()=>{
                    this.playVideo()
                });
            },
            getData(callback) {
                this.ajax(`/users/${this.userId}/hot_videos/${this.id}`, 'get').then((res) => {
                    if (res && res.data) {
                        this.videoObj = res.data;
                        this.$nextTick(()=>{
                            callback&&callback()
                        })


                    }
                }, (err) => {
                    if (err && err.response) {
                        let errors = err.response.data;
                        console.log(errors);
                    }
                })
            },
            isIos() {
                let u = navigator.userAgent, app = navigator.appVersion;
                return !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);
            },
            modalEv(ifShow) {
                if (ifShow) {
                    if (this.isIos()) {
                        window.location.href = `/share/#/download?id=${this.id}&page=hot_videos&userId=${this.userId}`
                    }
                    else {
                        this.$router.push({
                            path: '/download',
                            query: {id: this.id, page: 'hot_videos', userId: this.userId}
                        });
                    }
                }
                else {
                    this.showModal = false
                    this.showVideo = true;
                }
            },
            isInWeChat() {
                let u = navigator.userAgent, app = navigator.appVersion;
                return /(micromessenger|webbrowser)/.test(u.toLocaleLowerCase());
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
                this.ajax(`/hot_videos/${this.id}/share`, 'get').then((res) => {
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
                }, (err) => {
                    if (err && err.response) {
                        let errors = err.response.data;
                        console.log(errors);
                    }
                })
            },
            sharePage() {
                let wechat = require('../common/wechat');
                this.wx = require('weixin-js-sdk');
                wechat.wxConfig();
                this.inWxShare();
                this.ajax(`/hot_videos/${this.id}/share`, 'get').then((res) => {
                    if (res && res.data) {
                        this.initShare(res.data);
                    }
                }, (err) => {
                    if (err && err.response) {
                        let errors = err.response.data;
                        console.log(errors);
                    }
                })
            },
            inWxShare() {
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
                    }, 300)
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