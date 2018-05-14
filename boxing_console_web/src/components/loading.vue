<template>
    <div class="loading_box">
        <span class="text">拼命加载中</span>
        <i class="el-icon-loading loading"></i>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .loading_box
        color #fff
        margin 20px auto
        z-index 111
        width 300px
        height 40px
        line-height 40px
        text-align center
        background rgba(0,0,0,.5)
        .text
            color #fff
        .loading
            vertical-align middle
            font-size 30px
</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {}
        }
    }
</script>