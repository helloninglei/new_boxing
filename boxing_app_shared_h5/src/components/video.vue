<template>
    <d-player :options="options"
              ref="player"
                class="player">
    </d-player>
</template>

<style scoped lang="stylus" type="text/stylus">
    .player
        height 10rem
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
                    },
                    autoplay: false,
                    contextmenu: [
                        {
                            text: 'GitHub',
                            link: 'https://github.com/MoePlayer/vue-dplayer'
                        }
                    ]
                },
            }
        },
        props: {
            url: {
                type: String
            }
        },
        components: {
            'd-player': VueDPlayer
        }
    }
</script>