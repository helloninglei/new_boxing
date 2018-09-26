<template>
    <div class="list_item">
        <div class="left_player player_avatar">
            <div class="player_avatar_img_wrapper">
                <img class="player_avatar_img" :src="data.red_avatar" alt="">
                <div class="mark_icon" :class="{icon_ko: data.ko === 'red',icon_win: data.win==='red'}"></div>
            </div>
            <div class="player_name">{{data.red_name}}</div>
        </div>
        <div class="icon_vs"></div>
        <div class="right_player player_avatar">
            <div class="player_avatar_img_wrapper">
                <img class="player_avatar_img" :src="data.blue_avatar" alt="">
                <div class="mark_icon" :class="{icon_ko: data.ko === 'blue',icon_win: data.win==='blue'}"></div>
            </div>
            <div class="player_name">{{data.blue_name}}</div>
        </div>
        <div class="item_desc">
            <div class="area">{{data.schedule}}</div>
            <div class="kind">{{data.category}} <span class="level">{{data.level_min}}-{{data.level_max}}KG</span></div>
            <div class="time">{{data.time}}</div>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
.list_item
    width 16.3rem
    height 5.5rem
    margin 0 auto
    border-bottom 1px solid rgba(72,72,85,.5)
    overflow hidden
    &:last-child
        border-bottom none
    .player_avatar
        float left
        margin-top .9rem
        overflow hidden
    .player_avatar_img_wrapper
        position relative
        width 2.5rem
        height 2.5rem
        .mark_icon
            position absolute
            right 0
            bottom 0
            width 1rem
            height 1rem
            border-radius 50%
            &.icon_win
                background url("../assets/images/icon_win.png") no-repeat
                background-size contain
            &.icon_ko.icon_win
                background url("../assets/images/icon_ko.png") no-repeat
                background-size contain

    .player_avatar_img
        width 2.5rem
        height 2.5rem
        border-radius 50%
    .player_name
        margin-top .4rem
        width 2.5rem
        text-align center
        font-size .6rem
        color #fff
        overflow hidden
        text-overflow ellipsis
        white-space nowrap
    .icon_vs
        float left
        margin 2.1rem .9rem auto .9rem
        width 1.35rem
        height .7rem
        background url("../assets/images/icon_vs.png") no-repeat
        background-size contain
    .item_desc
        float left
        margin 1.15rem auto auto 1.75rem
        width 6.3rem
        line-height .8rem
        font-size .65rem
        color #8989A1
        .area
            margin-bottom .4rem
            width 6.3rem
            overflow hidden
            text-overflow ellipsis
            white-space nowrap
        .kind
            width 6.3rem
            margin-bottom .4rem

</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {}
        },
        props: {
            data: {
                type: Object,
                default: {}
            }
        }
    }
</script>