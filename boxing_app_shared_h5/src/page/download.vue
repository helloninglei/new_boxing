<template>
    <div class="wechat-android" :class="{show: ifShow}"></div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .wechat-android
        display none
        position fixed
        width 100%
        height 100%
        top 0
        left 0
        text-align right
        background rgba(0, 0, 0, 0.8) url("../assets/images/wxDownload-new.png") center top no-repeat
        background-size contain
        &.show
            display block

</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                ifShow: false
            }
        },
        created() {
          this.getPhoneType();
        },
        methods: {
            getPhoneType() {
                let u = navigator.userAgent, app = navigator.appVersion;
                let isAndroid = u.indexOf('Android') > -1 || u.indexOf('Linux') > -1;
                let isIOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);
                let isInWeChat = /(micromessenger|webbrowser)/.test(u.toLocaleLowerCase());
                // 是微信内部webView
                // 是安卓浏览器
                if (isAndroid) {
                    if (isInWeChat) {
                        this.ifShow = true;
                        return;
                    }
                    window.location.href = 'http://api.bituquanguan.com/app/boxing.apk';
                }
                // 是iOS浏览器
                if (isIOS) {
                    window.location.href = 'https://itunes.apple.com/cn/app/id1256291812';
                }
            }
        }
    }
</script>