<template>
    <div class="modal_bg" v-if="ifShow">
        <div class="modal">
            <div class="title">下载拳城出击APP，<br/>跟小伙伴们一起玩转拳击</div>
            <div class="cancel" @click="cancleEv">暂不下载</div>
            <div class="confirm" @click="confirmEv">立即下载</div>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .modal_bg
        position fixed
        top 0
        left 0
        z-index 9999
        width 100%
        height 100%
        background rgba(0, 0, 0, 0.40)
        .modal
            position absolute
            top 0
            bottom 0
            left 0
            right 0
            margin auto
            width 14rem
            height 7.5rem
            background #fff
            border-radius .4rem
            overflow hidden
            .title
                padding-top 1.3rem
                width 100%
                height 3.7rem
                font-size .75rem
                color #353535
                line-height 1.25rem
                text-align: center
                border-bottom .05rem solid #E5E5E5
            .cancel
                float left
                width 6.95rem
                height 2.4rem
                line-height 2.4rem
                font-size .9rem
                color #525252
                text-align center
                border-right .05rem solid #E5E5E5
            .confirm
                float right
                width 6.95rem
                height 2.4rem
                line-height 2.4rem
                font-size .9rem
                color #E60012
                text-align: center
</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {

            }
        },
        props: {
          ifShow: {
              type: Boolean,
              default: false
          }
        },
        methods: {
            cancleEv() {
                this.$emit('modalEv',false);
            },
            confirmEv() {
                this.$emit('modalEv',true);
            }
        }
    }
</script>