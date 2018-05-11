<template>
    <div class="pop_modal">
        <div class="content">
            <div class="top">
                <div class="icon"></div>
                <div class="title">{{title}}</div>
            </div>
            <div class="input_title">{{inputTitle}}</div>
            <div class="btn_wrapper">
                <div class="confirm btn" @click="confirm">确定</div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .pop_modal
        position fixed
        left 0
        top 0
        width 100%
        height 100%
        background rgba(0,0,0,.3)
        z-index 99999
        .content
            position absolute
            top 0
            left 0
            bottom 0
            right 0
            margin auto
            width 400px
            height 230px
            font-size 0
            background #fff
            overflow hidden
            .top
                .icon
                    display inline-block
                    margin 30px 15px 20px 30px
                    width 48px
                    height 48px
                    background url("../assets/images/tip_icon.png") no-repeat
                    background-size contain
                    border-radius 50%
                    vertical-align middle
                .title
                    display inline-block
                    font-size 18px
                    font-weight bold
                    vertical-align middle
            .input_title
                width 320px
                line-height 20px
                margin 0 auto 5px auto
                font-size 14px
            .btn_wrapper
                text-align right
                .btn
                    display inline-block
                    margin-right 50px
                    width 104px
                    height 40px
                    line-height 40px
                    text-align center
                    font-size 14px
                    border-radius 100px
                    cursor pointer
                    color #fff
                    background #5E77FF
</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                inputText: this.input
            }
        },
        props: {
            input: {

            },
            title: {
                type: String,
            },
            inputTitle: {
                type: String,
            }
        },
        methods: {
            confirm() {
                this.$emit('confirmTip')
            }
        },
    }
</script>