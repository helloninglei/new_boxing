<template>
    <div class="homePage_container" :class="{hasClose: ifClose}">
        <div class="header_info" v-if="userInfo">
            <img class="avatar" :src="userInfo.avatar ? userInfo.avatar : avatar_default" />
            <div class="info_container">
                <div class="name_info">
                    <div class="name">{{userInfo.nick_name}}</div>
                    <div class="sex" :class="userInfo.gender ? 'lady' : 'gentleman'"/>
                </div>
                <div class="desc">{{userInfo.bio}}</div>
                <div class="sub_desc" v-if="userInfo.boxer_info.introduction">{{userInfo.boxer_info.introduction}}</div>
            </div>
        </div>
        <div class="middle_info">
            <div class="middle_item attentions">
                <div class="num">{{userInfo.followers_count}}</div>
                <div class="item_name">关注</div>
            </div>
            <div class="middle_item fans">
                <div class="num">{{userInfo.following_count}}</div>
                <div class="item_name">粉丝</div>
            </div>
        </div>
        <div class="fight">
            <div class="title">战绩</div>
            <component :is="tabView" class="content_wrapper" :user-id="userId"></component>
            <div class="handle_btn_wrapper">
                <span v-for="(tab ,index) in tabs" class="tab" :class="{current:current==index,current_tab: index ===0}" @click="tabChange(index)">
                    <span class="tab_name">{{tab.name}}</span>
                    <span v-if="index == 0" class="vertical_line"></span>
                </span>
            </div>
        </div>
        <MatchData></MatchData>
        <DownloadTip @closeEv="closeEv" :id="userId" page="home_page_match"></DownloadTip>
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
.homePage_container
    padding-bottom 3.5rem
    &.hasClose
        padding-bottom 0
.header_info
    position relative
    height 2.9rem
    margin-top .75rem
    font-size 0
    .avatar
        position absolute
        top 0
        left 1.2rem
        width 2.5rem
        height 2.5rem
        border-radius 50%
        vertical-align middle
    .info_container
        position absolute
        top 0
        left 4.3rem
        font-size .6rem
        overflow hidden
        .name_info
            margin-bottom .2rem
            overflow hidden
            .name
                display inline-block
                line-height 1rem
                font-size .7rem
                color #fff
                vertical-align middle
            .sex
                display inline-block
                vertical-align middle
                &.lady
                    width .6rem
                    height .65rem
                    background url("../assets/images/woman_icon.png") no-repeat
                    background-size contain
                &.gentleman
                    width .65rem
                    height .6rem
                    background url("../assets/images/man_icon.png") no-repeat
                    background-size contain
        .desc
            margin-bottom .25rem
            width 13.8rem
            line-height .6rem
            color #474955
            overflow hidden
            text-overflow ellipsis
            white-space nowrap
        .sub_desc
            line-height .85rem
            width 13.8rem
            color #fff
            overflow hidden
            text-overflow ellipsis
            white-space nowrap
.middle_info
    display flex
    margin-top 1.4rem
    .middle_item
        flex 1
        text-align center
        .num
            line-height 1rem
            font-size 1rem
            color #fff
        .item_name
            margin-top .1rem
            line-height .7rem
            font-size .55rem
            color #9DA3B4
.fight
    overflow hidden
    .title
        margin 1.7rem auto auto 1.2rem
        line-height 1.5rem
        color #fff
        font-size 1rem
    .handle_btn_wrapper
        width 100%
        text-align center
        font-size 0
        color #8989A1
        .tab_name
            font-size .8rem
        .vertical_line
            display inline-block
            margin 0 .55rem
            width .1rem
            height .6rem
            background #474955
        .current
            .tab_name
                color #fff
</style>

<script type="text/ecmascript-6">
    import AbilityPic from 'components/abilityPic';
    import AbilityNumber from 'components/abilityNumber';
    import MatchData from 'components/matchData';
    import DownloadTip from 'components/downloadTip';
    import {wxConfig} from 'common/wechat';
    import { mapState, mapMutations } from 'vuex';
    export default {
        data() {
            return {
                userId: '',
                userInfo: '',
                tabs: [{name: "能力图"}, {name: "数值"}],
                current: 0,
                tabView: 'AbilityPic',
                ifClose: false,
                dataObj: {},
                avatar_default: require('../assets/images/portrait_default.png'),
            }
        },
        components: {
            AbilityPic,
            AbilityNumber,
            MatchData,
            DownloadTip
        },
        created() {
            this.userId = this.$route.params.userId;
            if (this.userId) {
                this.storeHomePageId(this.userId);
                this.getUserInfo();
                this.sharePage();
            }

        },
        methods: {
            getUserInfo() {
                this.ajax(`/user_profile/${this.userId}`,'get').then((res) => {
                    if (res && res.data) {
                        let userInfo = res.data;
                        if (userInfo.followers_count >= 10000 && userInfo.followers_count < 1000000) {
                            userInfo.followers_count = Math.round(userInfo.followers_count / 1000) /10 + 'W';
                        }
                        else if (userInfo.followers_count >= 1000000) {
                            userInfo.followers_count = Math.round(userInfo.followers_count / 10000) + 'W';
                        }
                        if (userInfo.following_count >= 10000 && userInfo.following_count < 1000000) {
                            userInfo.following_count = Math.round(userInfo.following_count / 1000) /10 + 'W';
                        }
                        else if (userInfo.following_count >= 1000000) {
                            userInfo.following_count = Math.round(userInfo.following_count / 10000) + 'W';
                        }

                        this.userInfo = userInfo;
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        console.log(errors);
                    }
                })
            },
            ...mapMutations(["storeHomePageId"]),
            tabChange(e) {
                this.tabView = e == 0 ? 'AbilityPic' : 'AbilityNumber';
                this.current = e;
            },
            closeEv(val) {
                this.ifClose = val;
            },
            sharePage() {
                if (navigator.userAgent.indexOf('MicroMessenger') > -1) {
                    let wechat = require('../common/wechat');
                    this.wx = require('weixin-js-sdk');
                    wechat.wxConfig();
                    this.inWxShare();
                    let url = `/players/${this.userId}/share`;
                    url = 'http://qa2.htop.info:50000/players/10158/share';
                    this.ajax(url,'get').then((res) => {
                        if (res && res.data) {
                            this.initShare(res.data);
                        }
                    },(err) => {
                        if(err&&err.response){
                            let errors=err.response.data;
                            console.log(errors);
                        }
                    })
                }
            },
            initShare(data) {
                let title = data.title;
                let desc = data.sub_title;
                let imgUrl = data.picture;
                let url = data.url;
                this.dataObj = {title, desc, url, imgUrl};
            },
            inWxShare () {
                let Timer = '';
                this.dataObj = '';
                this.wx.ready(() => {
                    Timer = setInterval(() => {
                        if (this.dataObj) {
                            clearInterval(Timer);
                            let obj = this.dataObj;
                            this.wx.onMenuShareAppMessage({
                                title: obj.title,
                                desc: obj.desc,
                                link: obj.url,
                                imgUrl: obj.imgUrl,
                            });
                            this.wx.onMenuShareTimeline({
                                title: obj.title,
                                link: obj.url,
                                imgUrl: obj.imgUrl,
                            });
                        }
                        else {
                            clearInterval(Timer);
                        }
                    },300)
                })

            },
        },

    }
</script>