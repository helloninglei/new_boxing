<template>
    <div>
        <div class="trends_container_head">
            <template v-if="info.user">
                <img class="portrait" :src="info.user.avatar ? `${config.baseUrl}/` + info.user.avatar : avatar_default" />
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
            <div class="content">那些沉浸在海底的人，终于付出了水面.新世纪最新拳王出炉，快看看采访火爆现场吧。 </div>
            <template v-if="info.video">
                <Video :url="url"></Video>
            </template>
            <template v-else>
                <div class="pic_wrapper" :class="getClass">
                    <img :src="item" v-for="(item, index) in images" :key="index" class="pic"/>
                </div>
            </template>
        </div>
        <TabBar :id="id" :ifShowPraise=true :commentType="message"></TabBar>
        <div class="bottom_bar" :class="{hasClose: ifClose}">
            <div class="bar_container">
                <div class="comment_btn">
                    <div class="comment_icon"></div>
                    评论
                </div>
                <div class="line"></div>
                <div class="praise_btn">
                    <div class="praise_icon"></div>
                    点赞
                </div>
            </div>
        </div>
        <DownloadTip @closeEv="closeEv"></DownloadTip>
    </div>

</template>

<style scoped lang="stylus" type="text/stylus">
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
.bottom_bar
    margin-bottom 3.5rem
    width 100%
    height 2.4rem
    line-height 2.4rem
    font-size .7rem
    color #fff
    background: #31313B;
    &.hasClose
        margin-bottom 0
    .bar_container
        display: -webkit-flex;
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

    export default {
        data() {
            return {
                images: [
                    require('../assets/images/video_default.png'),
                    require('../assets/images/video_default.png'),
                    require('../assets/images/video_default.png'),
                    require('../assets/images/video_default.png'),
                    require('../assets/images/video_default.png'),
                ],
                ifClose: false,
                avatar_default: require('../assets/images/portrait_default.png'),
                info: {},
                url: '',
            }
        },

        created() {
            this.id = this.$route.params.id;
            if (this.id) {
                this.getData();
            }
        },

        components: {
            GetTime,
            DownloadTip,
            Video,
            TabBar
        },

        methods: {

            getData() {
                this.ajax(`/messages/${this.id}`,'get').then((res) => {
                    if (res && res.data) {
                        this.info = res.data;
                        if (this.info.video) {
                            this.url = this.info.video;
                        }
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
                this.$router.push({path: '/download'})
            },

            followEv() {
                if (!this.info.user.is_following) {
                    this.$router.push({path: '/download'});
                }
            },

            closeEv(val) {
                this.ifClose = val;
            }

        },
        computed: {
            getClass() {
                let len = this.images.length;
                if (len) {
                    if (len === 1) return 'pic_wrapper1';
                    else if (len <= 4 && len > 1) return 'pic_wrapper2';
                    else {
                        return 'pic_wrapper3'
                    };
                }
            }
        }

    }
</script>