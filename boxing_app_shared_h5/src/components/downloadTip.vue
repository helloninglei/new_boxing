<template>
    <div class="download_app_container" v-show="show">
        <div class="container_position">
            <div class="logo_container"></div>
            <div class="text_desc">拳城出击APP</div>
            <div class="open_app" @click="openApp"></div>
            <div class="close_btn" @click="closeEv"></div>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .download_app_container {
        position: fixed;
        left -.125rem
        bottom: 0;
        width: 100%;
        height: 3.5rem;
        color: #525252;
        background: rgba(0, 0, 0, 0.7);
        z-index: 99;
        overflow: hidden;
        .container_position {
            position: relative;
            width: 100%;
            height: 100%;
            .logo_container {
                position: absolute;
                top: .5rem;
                left: .65rem;
                width: 2.5rem;
                height: 2.5rem;
                background: url("../assets/images/logo.jpg") no-repeat;
                background-size: contain;
                vertical-align: middle;
            }
            .text_desc {
                position: absolute;
                top: 1.2rem;
                left: 3.8rem;
                font-size: .8rem;
                color: #fff;
            }
            .open_app {
                position: absolute;
                top: 1rem;
                right: 1.6rem;
                width: 4rem;
                height: 1.5rem;
                line-height: 1.5rem;
                text-align: center;
                font-size: .75rem;
                color: #fff;
                background: url("../assets/images/download.png") no-repeat;
                background-size contain
            }
            .close_btn {
                position: absolute;
                top: .5rem;
                right: .5rem;
                width: .6rem;
                height: .6rem;
                background: url("../assets/images/close_btn.png") no-repeat;
                background-size: contain;
            }
        }
    }

</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                show: true
            }
        },
        props: {
            id: {
              type: [String,Number]
            },
            page: {
                type: String
            },
            userId: {
                type: [String,Number],
                default: 1
            }
        },
        methods: {
            isIos() {
                let u = navigator.userAgent, app = navigator.appVersion;
                return !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);
            },
            openApp() {
                if (this.isIos()) {
                    if (this.page === 'hot_videos') {
                        window.location.href = `/share/#/download?id=${this.id}&page=${this.page}&userId=${this.userId}`
                    }
                    else {
                        window.location.href = `/share/#/download?id=${this.id}&page=${this.page}`
                    }

                }
                else {
                    if (this.page === 'hot_videos') {
                        this.$router.push({path: '/share/download',query: {id: this.id, page: this.page, userId: this.userId}});
                    }
                    else {
                        this.$router.push({path: '/share/download',query: {id: this.id, page: this.page}});
                    }
                }
            },
            closeEv() {
                this.show = false;
                this.$emit('closeEv',true);
            }
        }
    }
</script>