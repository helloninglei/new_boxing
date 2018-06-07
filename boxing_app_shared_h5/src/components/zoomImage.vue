<template>
    <div class="zoom-container" v-if="showSwiper" ref="a">
        <swiper :options="swiperOption" ref="mySwiper" class="swiper-container">
            <swiper-slide class="swiper-slide" v-for="(item, index) in imageArr" :key="index">
                <div class="swiper-zoom-container" @click="closeSwiper(index)">
                    <img :src="`${config.baseUrl}` + item" />
                </div>
            </swiper-slide>
            <div class="swiper-pagination pagination_wrapper_zoom" slot="pagination"></div>
        </swiper>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
.zoom-container
    position: fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:#fff;
    overflow: hidden;
    z-index 9999
    .swiper-container
        width 100%
        height 100%
        .swiper-slide
            text-align center
            display -webkit-box
            display -ms-flexbox
            display -webkit-flex
            display flex
            -webkit-box-pack center
            -ms-flex-pack center
            -webkit-justify-content center
            justify-content center
            -webkit-box-align center
            -ms-flex-align center
            -webkit-align-items center
            align-items center
            img
                width: 100%
    .pagination_wrapper_zoom
        position fixed
        top 4rem
        left 0
        right 0
        width 2.5rem
        height 1.5rem
        line-height 1.5rem
        text-align center
        margin 0 auto
        font-size 1rem
        color #a2a2a2
</style>

<script type="text/ecmascript-6">
    import Vue from 'vue';
    import {wxConfig} from 'common/wechat';
    export default {
        name: 'carrousel',
        data() {
            return {
                swiperOption: {
                    notNextTick: true,
                    pagination: {
                        el: '.swiper-pagination',
                        type: 'fraction',
                    },
                    observer: true,
                    observeParents: true,
                    zoom: true
                },
                index: 1,
                slidesPerView : 1,
                slidesPerGroup: 1
            }
        },
        props: {
            showSwiper: {
                type: Boolean,
                default: false
            },
            imageArr: {
                type: Array,
                default: () => []
            },
            slideIndex: {
                type: [Number, String],
                default: 1
            }
        },

        computed: {
            swiper() {
                return this.$refs.mySwiper.swiper
            },

        },

        updated() {
            if (this.showSwiper) this.$refs.mySwiper.swiper.slideTo(this.slideIndex, 500, false);
        },

        methods: {
            closeSwiper(index) {
                this.$emit('hideSwiper');
            }
        }
    }
</script>