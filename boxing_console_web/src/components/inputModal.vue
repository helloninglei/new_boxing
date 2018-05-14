<template>
    <div class="pop_modal">
        <div class="content">
            <div class="top">
                <div class="icon"></div>
                <div class="title">{{title}}</div>
            </div>
            <div class="input_title">{{inputTitle}}</div>
            <input type="text" class="input" v-model="inputText" @input="inputEv" :maxlength="maxlength">
            <div class="errorTip">{{errorTip}}</div>
            <div class="btn_wrapper">
                <div class="cancle btn" @click="cancle">取消</div>
                <div class="confirm btn" @click="confirm">{{btnText}}</div>
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
            height 300px
            font-size 0
            background #fff
            overflow hidden
            .top
                .icon
                    display inline-block
                    margin 30px 15px 30px 30px
                    width 48px
                    height 48px
                    background url("../assets/images/add_icon.png") no-repeat
                    background-size contain
                    border-radius 50%
                    vertical-align middle
                .title
                    display inline-block
                    font-size 18px
                    font-weight bold
                    vertical-align middle
            .input_title
                margin-left 30px
                margin-bottom 6px
                font-size 14px
            .input
                width 325px
                height 40px
                margin 0 auto 0 30px
                padding-left 10px
                font-size 14px
                border 1px solid #C6CBD4
                outline none
            .errorTip
                width 100%
                height 40px
                line-height 40px
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
                inputText: ''
            }
        },
        props: {
            input: {
                type: String
            },
            title: {
                type: String,
            },
            inputTitle: {
                type: String,
                default: '用户角色'
            },
            errorTip: {
                type: String
            },
            btnText: {
                type: String,
                default: '确定'
            },
            maxlength: {
                type: String,
                default: '9999999999999'
            }
        },
        methods: {
            cancle() {
                this.$emit('cancleModal');
            },
            confirm() {
                this.$emit('confirmModal',this.inputText)
            },
            inputEv() {
                this.$emit('inputEv')
            }
        },
        created() {

        },
        watch: {
            input(){
                console.log(this.inputText)
                this.inputText = this.input;
            }
        }

    }
</script>