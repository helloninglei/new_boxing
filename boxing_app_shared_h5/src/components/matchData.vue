<template>
    <div class="matchData">
        <div class="title">赛事数据</div>
        <div class="data_panel">
            <div class="total panel_item">总计{{total}}</div>
            <div class="win panel_item">胜{{win}}</div>
            <div class="ko panel_item">KO{{ko}}</div>
        </div>
        <DataItem v-for="(item,index) in data" :data="item" :key="index"></DataItem>
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
    import { mapState } from 'vuex';
    export default {
        data() {
            return {
                data: [],
                total: '',
                win: '',
                ko: ''
            }
        },
        components: {
            DataItem
        },
        created() {
            this.getData();
        },
        methods: {
            getData() {
                let id = this.getUserId;
                let url = `/players/${id}/match`;
//                url = 'http://qa2.htop.info:50000/players/10158/match';
                this.ajax(url,'get').then((res) => {
                    this.total = res.data.total;
                    this.win = res.data.win;
                    this.ko = res.data.ko;
                    this.data = res.data.results;
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        console.log(errors);
                    }
                })
            }
        },
        computed: {
            ...mapState({
                getUserId: state => state.home_page_id
            })
        }
    }
</script>