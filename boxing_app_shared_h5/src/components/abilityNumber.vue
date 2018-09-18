<template>
    <ul class="ability_table">
        <li class="item">
            <span class="item_title">防守</span>
            <span class="item_num">85</span>
        </li>
        <li class="item">
            <span class="item_title">力量</span>
            <span class="item_num">60</span>
        </li>
        <li class="item">
            <span class="item_title">技术</span>
            <span class="item_num">80</span>
        </li>
        <li class="item">
            <span class="item_title">耐力</span>
            <span class="item_num">50</span>
        </li>
        <li class="item">
            <span class="item_title">进攻</span>
            <span class="item_num">100</span>
        </li>
        <li class="item">
            <span class="item_title">意志力</span>
            <span class="item_num">12</span>
        </li>
    </ul>
</template>

<style scoped lang="stylus" type="text/stylus">
.ability_table
    margin 2.75rem auto 2.5rem auto
    width 100%
    font-size .75rem
    text-align center
    overflow hidden
    .item
        float left
        margin-bottom .5rem
        width 100%
        .item_title
            display inline-block
            width 3rem
            line-height 1rem
            text-align right
            color #8989A1
        .item_num
            display inline-block
            text-indent 1rem
            width 3rem
            text-align left
            color #fff

</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {}
        }
    }
</script>