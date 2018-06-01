<template>
    <div>
        <div>
            <div class="payTip" v-if="showPayTip">
                可免费观看15S,看完整视频需付费99元
                <div class="close_btn" @click="closePayTipEv"></div>
            </div>
            <div class="video_info_wrapper">
                <div v-if="videoObj.try_url" class="video">
                    <Video :url="videoObj.try_url" height="11.8rem"></Video>
                </div>
                <div class="text">
                    <h2 class="title">{{videoObj.name}}</h2>
                    <div class="desc">{{videoObj.description}}</div>
                </div>
            </div>
            <div class="seeVideo" @click="openApp">99元观看完整视频</div>
        </div>
        <TabBar :id="id" :ifShowPraise=false commentType="hot_videos"></TabBar>
        <DownloadTip @closeEv="closeEv"></DownloadTip>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
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

    export default {
        data() {
            return {
                id: '',
                userId: 1000000,
                showPayTip: true,
                videoObj: {}
            }
        },
        components: {
            GetTime,
            DownloadTip,
            Video,
            TabBar
        },
        created() {
            this.id = this.$route.params.id;
            this.userId = this.$route.params.userId;
            if (this.id && this.userId) {
                this.getData();
            }
        },
        methods: {
            getData() {
                this.ajax(`/users/${this.userId}/hot_videos/${this.id}`,'get').then((res) => {
                    if (res && res.data) {
                        this.videoObj = res.data;
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
            closePayTipEv() {
                this.showPayTip = false;
            },
            closeEv(val) {
                this.ifClose = val;
            },
            openApp() {
                this.$router.push({path: '/download'})
            },
        }
    }
</script>