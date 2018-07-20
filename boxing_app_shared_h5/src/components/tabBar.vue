<template>
    <div>
        <div class="tab_bar">
        <span class="item comment" :class="{active: checked === 'comment'}" @click="tab('comment')">
            评论 {{commentNum}}
            <span class="underline"></span>
        </span>
        <span class="item praise" v-if="ifShowPraise">
            点赞 {{praises.length}}
            <span class="underline"></span>
        </span>
        </div>
        <div class="tab_content">
            <template v-if="checked === 'comment'">
                <div class="comments_container" v-for="(item, index) in comments" :key="index">
                    <template v-if="item.user">
                        <div class="portrait_container">
                            <img class="portrait" :src="item.user.avatar ? item.user.avatar + `${portraitQuery}` : avatar_default" />
                            <div class="sign_icon" :class="item.user.user_type"></div>
                        </div>

                        <div class="portrait_right_wrapper">
                            <span class="userName">{{item.user.nick_name}}</span>
                            <GetTime :createTime="item.created_time" class="getTime"></GetTime>
                        </div>
                    </template>

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
                            {{replay.content}}
                        </div>
                        <div class="replay_count" v-if="item.replies.count > 2" @click="openApp">共{{item.replies.count}}条回复 ></div>
                    </div>
                </div>

            </template>
            <template v-else-if="checked === 'praise'">
                <div class="praises_container" v-for="(item, index) in praises" :key="index">
                    <template v-if="item.user">
                        <img class="portrait" :src="item.user.avatar ? item.user.avatar + `${portraitQuery}` : avatar_default" />
                        <span class="userName">{{item.user.nick_name}}</span>
                    </template>
                </div>
            </template>
        </div>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    .portrait_container
        position relative
        display inline-block
        .sign_icon
            position absolute
            right 0
            bottom 0
            width .9rem
            height .9rem
            &.boxer_icon
                background url("../assets/images/boxer_icon.png") no-repeat
                background-size contain
            &.mark_icon
                background url("../assets/images/mark_icon.png") no-repeat
                background-size contain
            &.media_icon
                background url("../assets/images/media_icon.png") no-repeat
                background-size contain

    .portrait_right_wrapper
        display inline-block
        vertical-align middle
        .getTime
            margin .5rem auto auto auto
    .portrait
        width 2rem
        height 2rem
        border-radius 50%
        vertical-align middle
    .userName
        /*vertical-align middle*/
        color #fff
    .tab_bar
        margin .5rem auto auto auto
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
        margin-top 1.3rem
        padding 0 1rem
        font-size .65rem
        .comments_container
            color  #9DA3B4
            .topic
                line-height 1rem
                margin .35rem auto .6rem 2.2rem
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
    import config from 'common/my_config'
    export default {
        data() {
            return {
                checked: 'comment',
                comments: [],
                praises: [],
                commentNum: '',
                portraitQuery: ''
            }
        },
        props: {
            id: {
                type: String
            },
            ifShowPraise: {
                type: Boolean
            },
            commentType: {
                type: String,
                default: 'message'
            }
        },
        components: {
            GetTime
        },
        created() {
            if (this.id) {
                this.getComments();
                if (this.commentType == 'message') {
                    this.getPraises();
                }
            }
        },
        mounted(){
            setTimeout(() => {
                let baseSize = parseFloat(document.getElementsByTagName('html')[0].style.fontSize);
                this.portraitQuery = `?x-oss-process=image/resize,w_${parseInt(baseSize * 5)},m_fill`;
            },0)
        },
        methods: {
            tab(val) {
                if (this.checked !== val) {
                    this.checked = val;
                    val === 'praise' ? this.getPraises() : this.getComments();
                }
            },

            getComments() {
                this.ajax(`/${this.commentType}/${this.id}/comments`,'get').then((res) => {
                    if (res && res.data) {
                        this.comments = res.data.results;
                        this.comments.forEach((item) => {
                            switch (item.user.user_type) {
                                case '拳手':
                                    item.user.user_type = 'boxer_icon';
                                    break;
                                case '自媒体':
                                    item.user.user_type = 'media_icon';
                                    break;
                                case '名人':
                                    item.user.user_type = 'mark_icon';
                                    break;
                                default:
                                    item.user.user_type = ''
                                    break;
                            }
                        })
                        this.commentNum = res.data.comment_count;
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
                this.$emit('openApp', true);
            },
        }

    }
</script>