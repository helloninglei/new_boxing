<template>
    <div class="infoDetail_container" :class="{hasClose: ifClose}">
        <div class="infoDetail">
            <h1 class="title">{{info.title}}</h1>
            <div class="created_time">{{info.created_time}}</div>
            <!--<img v-if="info.picture" class="picture" :src="`${config.baseUrl}` + info.picture"/>-->
        </div>
        <div class="preface-text ql-editor" v-html="str"></div>
        <TabBar :id="id" :ifShowPraise=false commentType="game_news" @openApp="openApp"></TabBar>
        <ZoomImage @hideSwiper="hideSwiper" :showSwiper="showSwiper" :imageArr="imageArr" :slideIndex="slideIndex"></ZoomImage>
        <DownloadTip @closeEv="closeEv"></DownloadTip>
        <Modal :ifShow='showModal' @modalEv="modalEv"></Modal>
        <div style="display: none" class="beauty_video">
            <template v-if="videoSrc">
                <Video :url="videoSrc"></Video>
            </template>
        </div>

    </div>
</template>

<style  lang="stylus" type="text/stylus">
    .infoDetail_container
        margin-bottom  3.5rem
        &.hasClose
            margin-bottom 0
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
        .preface-text
            margin-bottom 1.2rem
    p
        margin-top .5rem
        line-height 1rem
        color #fff!important
        img
            width 100%
            height 10rem
            margin 0 auto
    video
        width 100%
        margin-bottom .5rem

</style>

<script>
    import config from 'common/my_config';
    import TabBar from 'components/tabBar';
    import Modal from 'components/modal';
    import DownloadTip from 'components/downloadTip';
    import ZoomImage from 'components/zoomImage';
    import Video from 'components/video';
    import {wxConfig} from 'common/wechat';
    import $ from 'jquery'

    export default {
        data() {
            return {
                videoSrc: '',
                imageArr:[],
                slideIndex: 1,
                showSwiper: false,
                id: '',
                ifClose: false,
                showModal: false,
                info: {},
                str: '<p><img src="/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png"></p><iframe class="ql-video" playsinline controls="controls" src="/uploads/b9/a2/8434d87433ef41280821942a1c70783df2a6.mp4" autoplay="false"></iframe><p><br></p><p><br></p><p><br></p><p style="color: red">按揭房拉丝机发发龙卷风拉上解放啦否</p><p><img src="/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png"></p><p><br></p><p><br></p><p><br></p><p style="color: red">按揭房拉丝机发发龙卷风拉上解放啦否</p><p>快圣诞节疯狂了世界国家</p>\'\n<p>快圣诞节疯狂了世界国家</p>'
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
            this.str = this.getSrc(this.str);
            if (this.id) {
                this.getData();
            }
        },
        mounted() {
            let This = this;
            $('p').find('img').addClass('img');
            $('.img').on('click',function () {
                This.slideIndex = $('.img').index(this);
                This.showSwiper = true;
            });
            $('.video_container').html('');
            $('.video_container').append($('.beauty_video'));
            $('.beauty_video').show();
            this.getImgSrc();

        },
        methods: {
            getSrc(str) {
                var imgReg = /<iframe.*?(?:>|\/>)/gi;
                var srcReg = /src=[\'\"]?([^\'\"]*)[\'\"]?/i;
                var arr = str.match(imgReg);
                for (var i = 0; i < arr.length; i++) {
                    var src = arr[i].match(srcReg);
                    this.videoSrc = src[1];
                    str = str.replace(arr[i],'<div class="video_container"><video class="ql-video" playsinline  controls="controls" src="' + `${config.baseUrl}` + src[1] + '" poster="' + `${config.baseUrl}` + src[1] + '?x-oss-process=video/snapshot,t_0,f_jpg,w_0,h_0,m_fast"></video></div>')
                }
                return str
            },
            getData() {
                this.ajax(`/game_news/${this.id}`,'get').then((res) => {
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
            getImgSrc() {
                let arr = $('img');
                let imageArr = [];
                for (let i = 0;i < arr.length;i++) {
                    imageArr.push($(arr[i]).attr('src'));
                    $(arr[i]).attr('src',`${config.baseUrl}` + $(arr[i]).attr('src'));
                }
                this.imageArr = imageArr;
            },
            hideSwiper() {
                this.showSwiper = false;
            },
        },
    }
</script>