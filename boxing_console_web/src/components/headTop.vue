<template>
    <div :class="head_top">
        <div class="container">
            <span class="title">{{title}}</span>
            <span class="subTitle">{{subTitle}}</span>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .head_top
        width 100%
        height 88px
        line-height 88px
        font-size 32px
        color #000
        background #fff
        border-bottom 1px solid rgba(51,51,51,.3)
    .sub_head_top
        padding-top 48px
        width 100%
        height 40px
        font-size 14px
        color #000
        background #fff
        border-bottom 1px solid rgba(51,51,51,.3);
        overflow hidden;
        .title
            font-weight bold

</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {}
        },
        props: {
            title: {
                type: String
            },
            subTitle: {
                type: String,
                default: ''
            },
            head_top: {
                type: String,
                default: 'head_top'
            }
        }
    }
</script>