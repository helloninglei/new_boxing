<template>
    <div class="infoDetail_container" :class="{hasClose: ifClose}">
        <div class="infoDetail">
            <h1 class="title">{{info.title}}</h1>
            <div class="created_time">{{info.pub_time}}</div>
            <!--<img v-if="info.picture" class="picture" :src="`${config.baseUrl}` + info.picture"/>-->
            <!--<div class="content">{{info.content}}</div>-->
        </div>
        <div class="preface-text ql-editor" v-html="str" v-if="showVideo"></div>
        <TabBar :id="id" :ifShowPraise=false commentType="game_news" @openApp="openApp" v-if="inApp == 0"></TabBar>
        <DownloadTip @closeEv="closeEv" v-if="inApp == 0" page="game_news" :id="id"></DownloadTip>
        <Modal :ifShow='showModal' @modalEv="modalEv"></Modal>
        <ZoomImage @hideSwiper="hideSwiper" :showSwiper="showSwiper" :imageArr="imgs" :slideIndex="slideIndex"></ZoomImage>
    </div>
</template>

<style lang="stylus" type="text/stylus">
    .infoDetail_container
        margin 0 auto
        width 17.25rem
        padding-bottom  3.5rem
        &.hasClose
            padding-bottom 0
        p
            line-height 1.5rem!important
            color #fff!important
            img
                display block
                width 17.25rem!important
                margin .5rem auto auto auto!important
        span
            color #fff!important
            background none!important
        video
            width 100%!important
            height 10rem!important
            margin-bottom .5rem
    .ql-editor {
        white-space: inherit!important
        img {
            width 17.25rem!important
            margin .5rem auto auto auto!important
            display block
        }
        iframe {
            width 100%!important
            height 10rem!important
        }
    }
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
            line-height 1.5rem
            font-size .75rem
            color #E9E9EA

    video::-internal-media-controls-download-button
        display none

    video::-webkit-media-controls-enclosure
        overflow hidden

</style>
<style>
    .el-carousel__item h3 {
        color: #475669;
        font-size: 14px;
        opacity: 0.75;
        line-height: 150px;
        margin: 0;
      }

      .el-carousel__item:nth-child(2n) {
         background-color: #99a9bf;
      }
      
      .el-carousel__item:nth-child(2n+1) {
         background-color: #d3dce6;
      }
      .imgsblock{
        width: 100%;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        background: #ccc;
      }
      .infoDetail_container .zoom-container{
        background:#000;
      }
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
                inApp: 1,
                id: '',
                ifClose: false,
                showModal: false,
                info: {},
                wx: '',
                dataObj: '',
                str: '',
                showVideo: true,
                showSwiper:false,
                slideIndex:1,
                imgs:[]
            }
        },
        components: {
            TabBar,
            DownloadTip,
            Modal,
            ZoomImage,
            Video,
        },
        created() {
            this.id = this.$route.params.id;
            this.inApp = this.$route.params.inApp;
            if (this.id) {
                this.getData();
                this.sharePage();
            };
        },
        updated(){
            let ele = document.getElementsByClassName('myImg')
            let $this = this
            if(ele){
                for(var i=0;i<ele.length;i++){
                    ele[i].onclick = function(e){
                        // $this.showZoomImage(e.currentTarget.dataset.index)
                        let u = navigator.userAgent, app = navigator.appVersion;
                        let isAndroid = u.indexOf('Android') > -1 || u.indexOf('Linux') > -1;
                        let isIOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);
                        if(isAndroid||isIOS){
                            boxing.previewImage(this.imgs,e.currentTarget.dataset.index)
                        }else{
                            $this.showZoomImage(e.currentTarget.dataset.index)
                        }
                        
                    }
                } 
            }
        },
        methods: {
            getSrc(str) {
                var iframeReg = /<iframe.*?(?:>|\/>)/gi;
                var imgReg = /<img.*?(?:>|\/>)/gi;
                var srcReg = /src=[\'\"]?([^\'\"]*)[\'\"]?/i;
                var arr = str.match(iframeReg);
                var imgArr = str.match(imgReg);
                if (arr) {
                    for (var i = 0; i < arr.length; i++) {
                        var src = arr[i].match(srcReg);

                        if (src[1].indexOf('http') == -1 && src[1].indexOf('https') == -1) {
                            str = str.replace(arr[i],'<div class="video_container"><video class="ql-video" playsinline  controlsList="nodownload" controls="controls" src="' + src[1] + '" poster="' + src[1] + '?x-oss-process=video/snapshot,t_0,f_jpg,w_0,h_0,m_fast"></video></div>')
                        }
                    }
                }
                if (imgArr) {
                    var baseSize = parseFloat(document.getElementsByTagName('html')[0].style.fontSize);
                    for (var i = 0; i < imgArr.length; i++) {
                        var src = imgArr[i].match(srcReg);
                        if (src[1].indexOf('http') == -1 && src[1].indexOf('https') == -1) {
                            str = str.replace(imgArr[i],'<img src="'+config.baseUrl + src[1] + `?x-oss-process=image/resize,w_${parseInt(baseSize * 34.5)}"  @click="showZoomImage" class="myImg" data-index="${i}"/>`)
                        }
                        this.imgs[i] = `${src[1]}?x-oss-process=image/resize,w_${parseInt(baseSize * 37.5)}`
                    }                }

                return str
            },
            getData() {
                this.ajax(`/game_news/${this.id}?in_app=${this.inApp}`,'get').then((res) => {
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
            isInWeChat() {
                let u = navigator.userAgent, app = navigator.appVersion;
                return /(micromessenger|webbrowser)/.test(u.toLocaleLowerCase());
            },
            openApp() {
                this.showModal = true;
                this.showVideo = false;
            },
            isIos() {
                let u = navigator.userAgent, app = navigator.appVersion;
                return !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);
            },
            modalEv(ifShow) {
                if (ifShow) {
                    if (this.isIos()) {
                        window.location.href = `/share/#/download?id=${this.id}&page=game_news`
                    }
                    else {
                        this.$router.push({path: '/download',query: {id: this.id, page: 'game_news'}});
                    }
                }
                else {
                    this.showModal = false;
                    this.showVideo = true;
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
            },
            showZoomImage(index) {
                console.log(1111)
                this.slideIndex = index;
                this.showSwiper = true;
                this.showVideo = false;
            },

            hideSwiper() {
                this.showVideo = true;
                this.showSwiper = false;
            },
        },
    }
</script>
