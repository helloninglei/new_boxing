<template>
    <div class="matchData">
        <div class="title">赛事数据</div>
        <div class="data_panel">
            <div class="total panel_item">总计5</div>
            <div class="win panel_item">胜2</div>
            <div class="ko panel_item">KO1</div>
        </div>
        <DataItem></DataItem>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
.matchData
    margin-top 2.8rem
    .title
        margin-left 1.2rem
        font-size 1rem
        color #fff
    .data_panel
        margin-top .8rem
        height 2.4rem
        line-height 2.4rem
        font-size .7rem
        color #8989A1
        background #272734
        overflow hidden
        .panel_item
            float left
            &.total
                margin auto 2.2rem auto 1.2rem
            &.win
                margin-right 1.2rem
</style>

<script type="text/ecmascript-6">
    import DataItem from 'components/dataItem';
    export default {
        data() {
            return {}
        },
        components: {
            DataItem
        }
    }
</script>