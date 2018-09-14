<template>
    <div>
        <div class="header_info">
            <image class="avatar"></image>
            <div class="info_container">
                <div class="name_info">
                    <div class="name">拳皇</div>
                    <div class="sex"></div>
                </div>
                <div class="desc">我参加很多比赛，比赛让我兴奋…</div>
                <div class="sub_desc">国内首个全国业余搏击赛事</div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
.header_info
    font-size 0
    .avatar
        width 2.5rem
        height 2.5rem
        background red
        border-radius 50%
        vertical-align middle
    .info_container
        display inline-block

</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {}
        }
    }
</script>