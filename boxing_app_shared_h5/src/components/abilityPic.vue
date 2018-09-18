<template>
    <div>
        <img class="pic" :src="imgSrc" alt="">
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .pic
        display block
        margin 1.9rem auto 1.35rem auto
        width 11rem
        height 11rem
</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                imgSrc: ''
            }
        },
        props: {
            userId: {
                type: [String,Number]
            }
        },
        created() {
            this.imgSrc = `/players/${this.userId}/ability_chart`;
//            this.imgSrc = 'http://qa2.htop.info:50000/players/10158/ability_chart'; // todo
        }
    }
</script>