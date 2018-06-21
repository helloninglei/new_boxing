<template>
    <div class="infoDetail_container" :class="{hasClose: ifClose}">
        <div class="infoDetail">
            <h1 class="title">{{info.title}}</h1>
            <div class="created_time">{{info.created_time}}</div>
            <!--<img v-if="info.picture" class="picture" :src="`${config.baseUrl}` + info.picture"/>-->
            <!--<div class="content">{{info.content}}</div>-->
        </div>
        <div class="preface-text ql-editor" v-html="str"></div>
        <TabBar :id="id" :ifShowPraise=false commentType="game_news" @openApp="openApp" v-if="inApp != 0"></TabBar>
        <DownloadTip @closeEv="closeEv" v-if="inApp != 0"></DownloadTip>
        <Modal :ifShow='showModal' @modalEv="modalEv"></Modal>
    </div>
</template>

<style lang="stylus" type="text/stylus">
    .infoDetail_container
        margin-bottom  3.5rem
        &.hasClose
            margin-bottom 0
        p
            margin-top .5rem!important
            line-height 1rem!important
            color #fff!important
        img
            width 100%
            height 10rem
            margin 0 auto
        video
            width 100%
            margin-bottom .5rem
    .infoDetail
        margin 0 auto
        width 17.25rem
        .title
            margin .6rem auto .5rem auto
            line-height 1.75rem
            font-size 1.1rem
            color #DBDBEA
        .created_time
            margin-bottom .5rem
            font-size .6rem
            color: #7D7D93
        .picture
            width 100%
            height 10rem
            margin 0 auto
        .content
            line-height 1rem
            font-size .75rem
            color #E9E9EA

</style>

<script>
    import config from 'common/my_config';
    import TabBar from 'components/tabBar';
    import Modal from 'components/modal';
    import DownloadTip from 'components/downloadTip';
    import ZoomImage from 'components/zoomImage';
    import Video from 'components/video';

    export default {
        data() {
            return {
                inApp: 0,
                id: '',
                ifClose: false,
                showModal: false,
                info: {},
                wx: '',
                dataObj: '',
                str: ''
            }
        },
        components: {
            TabBar,
            DownloadTip,
            Modal,
            ZoomImage,
            Video
        },
        created() {
            this.id = this.$route.params.id;
            this.inApp = this.$route.params.inApp;
            if (this.id) {
                this.getData();
                this.sharePage();
            }
        },
        methods: {
            getSrc(str) {
                var imgReg = /<iframe.*?(?:>|\/>)/gi;
                var srcReg = /src=[\'\"]?([^\'\"]*)[\'\"]?/i;
                var arr = str.match(imgReg);
                if (arr) {
                    for (var i = 0; i < arr.length; i++) {
                        var src = arr[i].match(srcReg);
                        str = str.replace(arr[i],'<div class="video_container"><video class="ql-video" playsinline  controls="controls" src="' + `${config.baseUrl}` + src[1] + '" poster="' + `${config.baseUrl}` + src[1] + '?x-oss-process=video/snapshot,t_0,f_jpg,w_0,h_0,m_fast"></video></div>')
                    }
                }

                return str
            },
            getData() {
                this.ajax(`/game_news/${this.id}?inApp=${this.inApp}`,'get').then((res) => {
                    if (res && res.data) {
                        this.info = res.data;
                        this.str = this.getSrc(res.data.content);
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
                    this.ajax(`/game_news/${this.id}/share`,'get').then((res) => {
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
            }
        },
    }
</script>