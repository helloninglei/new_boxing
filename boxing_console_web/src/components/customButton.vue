<template>
    <div type="text" class="custom_button" :class="buttonClass">{{text}}</div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .custom_button
        display inline-block
        text-align center
        cursor pointer
        height 32px
        line-height 32px
        font-size 14px
        border-radius 24px
        &.custom_button1
            width 100px
            border 1px solid #4B74FF
            color #4B74FF
        &.custom_button2
            float right
            width 120px
            background #4B74FF
            color #fff
        &.custom_button3
            float right
            width 100px
            background #4B74FF
            color #fff
            margin-top 3px
        &.custom_button4
            width 140px
            height 34px
            line-height 34px
            background #4B74FF
            color #fff
        &.custom_button5
            width 140px
            border 1px solid #4B74FF
            color #4B74FF
</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {}
        },
        props: {
            buttonClass: {
                type: String,
                default: 'custom_button1'
            },
            text: {
                type: String
            }
        },
        methods: {

        }
    }
</script>