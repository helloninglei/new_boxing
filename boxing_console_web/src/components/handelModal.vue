<template>
    <div class="pop_modal">
        <div class="content">
            <div class="top">
                <div class="icon"></div>
            </div>
            <div class="input_title">{{inputTitle}}</div>
            <div class="errorTip">{{delErrorTip}}</div>
            <div class="btn_wrapper">
                <div class="cancle btn" @click="cancle">取消</div>
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
            height 250px
            font-size 0
            background #fff
            overflow hidden
            .top
                .icon
                    margin 40px auto 20px auto
                    width 48px
                    height 48px
                    background url("../assets/images/del_icon.png") no-repeat
                    background-size contain
                    border-radius 50%
                    vertical-align middle
            .input_title
                text-align center
                font-size 14px
            .errorTip
                margin 10px auto
                width 90%
                line-height 20px
                text-align center
                font-size 14px
                color #FF635A
            .btn_wrapper
                text-align center
                .btn
                    display inline-block
                    width 104px
                    height 40px
                    line-height 40px
                    text-align center
                    font-size 14px
                    border-radius 100px
                    cursor pointer
                    &.cancle
                        margin-right 16px
                        color #5E77FF
                        border 1px solid #5E77FF
                    &.confirm
                        color #fff
                        background #5E77FF
</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {

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
                default: '用户角色'
            },
            delErrorTip: {
                type: String,
                default: ''
            }
        },
        methods: {
            cancle() {
                this.$emit('cancleModal');
            },
            confirm() {
                this.$emit('confirmModal');
            }
        },
    }
</script>