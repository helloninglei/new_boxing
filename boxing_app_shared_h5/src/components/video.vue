<template>
    <d-player :options="options"
              ref="player"
              class="player" :style="{height: height}">
    </d-player>
</template>

<style scoped lang="stylus" type="text/stylus">

</style>

<script type="text/ecmascript-6">
    import config from 'common/my_config';
    import VueDPlayer from 'vue-dplayer'
    import '../../node_modules/vue-dplayer/dist/vue-dplayer.css'

    export default {
        data() {
            return {
                options: {
                    hotkey: false,
                    screenshot: false,
                    preload: true,
                    video: {
                        url: `${config.baseUrl}` + this.url,
                        pic: `${config.baseUrl}` + this.url + '?x-oss-process=video/snapshot,t_0,f_jpg,w_0,h_0,m_fast',
                    },
                    autoplay: false,
                },
            }
        },
        props: {
            url: {
                type: String
            },
            height: {
                type: String,
                default: '10rem'
            }
        },
        components: {
            'd-player': VueDPlayer
        }
    }
</script>