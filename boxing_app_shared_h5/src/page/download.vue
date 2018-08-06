<template>
    <div :class="popTip ? 'wechat_pop' : 'page_bg'">
        <div class="top"></div>
        <div class="middle"></div>
        <div class="bottom"></div>
        <div class="download_btn" @click="downloadEv">下载安装</div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .wechat_pop
        position fixed
        width 100%
        height 100%
        top 0
        left 0
        text-align right
        background rgba(0, 0, 0, 0.6) url("../assets/images/popTip.png") no-repeat
        background-size contain
        .download_btn
            display none
    .page_bg
        position absolute
        width 100%
        height 100%
        background #13131b
        top 0
        left 0
        overflow hidden
        .top
            position absolute
            top 2rem
            width 100%
            height 16.9rem
            margin 0 auto
            background url("../assets/images/downPage_top.png") no-repeat
            background-size cover
        .bottom
            position absolute
            bottom 0
            width 100%
            height 3.125rem
            background url("../assets/images/downPage_bottom.png") no-repeat
            background-size cover
        .download_btn
            display block
            position absolute
            left 50%
            bottom 3rem
            transform translate(-50%,0)
            width 8.65rem
            height 2.35rem
            line-height 2.35rem
            text-align center
            font-size 1rem
            color #fff
            background #efad3f
            border-radius 2rem

</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                id: '',
                userId: '',
                page: ''
            }
        },
        props: {

        },
        created() {
            this.id = this.$route.query.id;
            this.userId = this.$route.query.userId;
            this.page = this.$route.query.page;
            this.goApp();
        },
        computed: {
            popTip() {
                return this.isInWeChat();
            }
        },
        methods: {
            downloadEv() {
                let u = navigator.userAgent, app = navigator.appVersion;
                let isAndroid = u.indexOf('Android') > -1 || u.indexOf('Linux') > -1;
                let isIOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);
                if (isAndroid) {
                    window.location.href = 'http://api.bituquanguan.com/app/boxing.apk';
                }
                else if (isIOS) {
                    window.location.href = 'https://itunes.apple.com/cn/app/id1256291812';
                }
            },
            isInWeChat() {
                let u = navigator.userAgent, app = navigator.appVersion;
                return /(micromessenger|webbrowser)/.test(u.toLocaleLowerCase());
            },
            isIos() {
                let u = navigator.userAgent, app = navigator.appVersion;
                return !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);
            },
            goApp() {
                if (this.page === 'hot_videos') {
                    location.href = `boxing://api.bituquanguan.com:80/${this.page}?id=${this.id}&userId=${this.userId}&time=${new Date().getTime()}`;
                }
                else {
                    location.href = `boxing://api.bituquanguan.com:80/${this.page}?id=${this.id}&time=${new Date().getTime()}`;
                }
            }
        }
    }
</script>