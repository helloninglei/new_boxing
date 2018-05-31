<template>
    <div>
        <div class="tab_bar">
        <span class="item comment" :class="{active: checked === 'comment'}" @click="tab('comment')">
            评论 {{comments.length}}
            <span class="underline"></span>
        </span>
        <span class="item praise" :class="{active: checked === 'praise'}" @click="tab('praise')" v-if="ifShowPraise">
            点赞
            <span class="underline"></span>
        </span>
        </div>
        <div class="tab_content">
            <template v-if="checked === 'comment'">
                <div class="comments_container" v-for="(item, index) in comments" :key="index">
                    <template v-if="item.user">
                        <img class="portrait" :src="item.user.avatar ? `${config.baseUrl}/` + item.user.avatar : avatar_default" />
                        <span class="userName">{{item.user.nick_name}}</span>
                    </template>
                    <GetTime :createTime="item.created_time"></GetTime>
                    <div class="topic">{{item.content}}</div>
                    <div :class="{replay_container: item.replies.results.length}">
                        <div v-for="(replay,index_replay) in item.replies.results" :key="index_replay" v-if="index_replay < 3">
                            <span class="replay_user_name">{{replay.user.nick_name}}</span>
                            <template v-if="replay.to_user">
                                回复
                                <span class="to_user">{{replay.to_user.nick_name}}</span>
                                {{replay.content}}
                            </template>
                            <template v-else>：</template>
                        </div>
                        <div class="replay_count" v-if="item.replies.count > 2" @click="openApp">共{{item.replies.count}}条回复 ></div>
                    </div>
                </div>

            </template>
            <template v-else-if="checked === 'praise'">
                <div class="praises_container" v-for="(item, index) in praises" :key="index">
                    <template v-if="item.user">
                        <img class="portrait" :src="item.user.avatar ? `${config.baseUrl}/` + item.user.avatar : avatar_default" />
                        <span class="userName">{{item.user.nick_name}}</span>
                    </template>
                </div>
            </template>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .portrait
        width 1.1rem
        height 1.1rem
        border-radius 50%
        vertical-align middle
    .userName
        vertical-align middle
        color #fff
    .tab_bar
        margin .5rem auto 1.3rem auto
        width 100%
        height 2.4rem
        line-height 2.4rem
        font-size 0
        color rgba(157, 163, 180, .75)
        background #272734
        overflow hidden
        .item
            display inline-block
            box-sizing border-box
            font-size .75rem
            &.comment
                margin auto 2.1rem auto 1.4rem
            &.active
                color #fff
                .underline
                    display block
                    margin -.15rem auto auto auto
                    width .75rem
                    height .15rem
                    background #F95862
    .tab_content
        padding 0 1rem
        font-size .65rem
        .comments_container
            color  #9DA3B4
            .topic
                margin .35rem auto .6rem 1.2rem
            .replay_container
                width 15.4rem
                margin 0 auto 1.2rem 1.2rem
                padding .5rem
                box-sizing border-box
                line-height 1rem
                background: #31313B;
                .replay_user_name, .to_user
                    color #DDDDEC
                .replay_count
                    margin-top .3rem
                    color #fff
    .praises_container
        margin-bottom 1rem
        .portrait
            width 2rem
            height 2rem
        .userName
            margin-left .3rem
            font-size .8rem
</style>

<script type="text/ecmascript-6">
    import GetTime from 'components/getTime';
    export default {
        data() {
            return {
                checked: 'comment',
                comments: [],
                praises: []
            }
        },
        props: {
            id: {
                type: String
            },
            ifShowPraise: {
                type: Boolean
            }
        },
        components: {
            GetTime
        },
        created() {
            if (this.id) {
                this.getComments();
            }
        },
        methods: {
            tab(val) {
                if (this.checked !== val) {
                    this.checked = val;
                    val === 'praise' ? this.getPraises() : this.getComments();
                }
            },

            getComments() {
                this.ajax(`/messages/${this.id}/comments`,'get').then((res) => {
                    if (res && res.data) {
                        this.comments = res.data.results;
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        for(var key in errors){
                            console.log(errors[key][0]);
                        }
                    }
                })
            },

            getPraises() {
                this.ajax(`/messages/${this.id}/like`,'get').then((res) => {
                    if (res && res.data) {
                        this.praises = res.data.results;
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        for(var key in errors){
                            console.log(errors[key][0]);
                        }
                    }
                })
            },
            openApp() {
                this.$router.push({path: '/download'})
            },
        }

    }
</script>