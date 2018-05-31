<template>
    <div class="created_time">{{getTime}}</div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .created_time
        margin .35rem auto .6rem 1.2rem
        font-size .6rem
        color  #474955
</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {

            }
        },
        props: {
            createTime: {
                type: String
            }
        },
        computed: {
            getTime() {
                let currentTime = new Date().getTime();
                let oldTime =  new Date(this.createTime).getTime();
                let diff = currentTime - oldTime;
                let minute = 60000;
                if (diff < minute) {
                    return '刚刚';
                }
                else if (diff >= minute && diff < minute * 60) {
                    let text = Math.floor(diff / minute)
                    return text + '分钟以前';
                }
                else if (diff >= minute * 60 && diff < minute * 60 * 24) {
                    let text = Math.floor(diff / (minute * 60));
                    return text + '小时以前';
                }
                else {
                    return this.createTime;
                }
            }
        }
    }
</script>