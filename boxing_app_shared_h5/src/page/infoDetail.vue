<template>
    <div class="infoDetail_container">
        <div class="infoDetail">
            <h1 class="title">{{info.title}}</h1>
            <div class="created_time">{{info.created_time}}</div>
            <img v-if="info.picture" class="picture" :src="`${config.baseUrl}` + info.picture"/>
        </div>
        <div class="preface-text ql-editor" v-html="str"></div>
        <TabBar :id="id" :ifShowPraise=false commentType="game_news" @openApp="openApp"></TabBar>
        <DownloadTip @closeEv="closeEv"></DownloadTip>
        <Modal :ifShow='showModal' @modalEv="modalEv"></Modal>
    </div>
</template>

<style  lang="stylus" type="text/stylus">
    .infoDetail_container
        padding-bottom 3.5rem
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
        color: #fff!important
        img
            width 100%
            height 10rem
            margin 0 auto
    video
        margin-bottom .5rem

</style>

<script>
    import config from 'common/my_config';
    import TabBar from 'components/tabBar';
    import Modal from 'components/modal';
    import DownloadTip from 'components/downloadTip';
    import {wxConfig} from 'common/wechat';

    export default {
        data() {
            return {
                id: '',
                showModal: false,
                info: {},
                str: '<p><img src="http://39.105.73.10:8000/uploads/65/56/1af070dca4c5a6acc00307361fea887e2f3d.png"></p><iframe class="ql-video" playsinline controls="controls" src="http://39.105.73.10:8000/uploads/b9/a2/8434d87433ef41280821942a1c70783df2a6.mp4" autoplay="false"></iframe><p><br></p><p><br></p><p><br></p><p style="color: red">按揭房拉丝机发发龙卷风拉上解放啦否</p><p>快圣诞节疯狂了世界国家</p>'
            }
        },
        components: {
            TabBar,
            DownloadTip,
            Modal
        },
        created() {
            this.id = this.$route.params.id;
            this.str = this.getSrc(this.str);
            if (this.id) {
                this.getData();
            }
        },
        methods: {
            getSrc(str) {
                var imgReg = /<iframe.*?(?:>|\/>)/gi;
                var srcReg = /src=[\'\"]?([^\'\"]*)[\'\"]?/i;
                var arr = str.match(imgReg);
                for (var i = 0; i < arr.length; i++) {
                    var src = arr[i].match(srcReg);
                    str = str.replace(arr[i],'<video class="ql-video" playsinline  controls="controls" src="' + src[1] + '"></video>')
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
                        for(var key in errors){
                            this.$layer.msg(errors[key][0]);
                        }
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
            }
        },
    }
</script>