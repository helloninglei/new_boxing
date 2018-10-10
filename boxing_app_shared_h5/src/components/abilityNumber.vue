<template>
    <ul class="ability_table" v-if="data">
        <li class="item">
            <span class="item_title">防守</span>
            <span class="item_num">{{data.defence}}</span>
        </li>
        <li class="item">
            <span class="item_title">力量</span>
            <span class="item_num">{{data.strength}}</span>
        </li>
        <li class="item">
            <span class="item_title">技术</span>
            <span class="item_num">{{data.skill}}</span>
        </li>
        <li class="item">
            <span class="item_title">耐力</span>
            <span class="item_num">{{data.stamina}}</span>
        </li>
        <li class="item">
            <span class="item_title">进攻</span>
            <span class="item_num">{{data.attack}}</span>
        </li>
        <li class="item">
            <span class="item_title">意志力</span>
            <span class="item_num">{{data.willpower}}</span>
        </li>
    </ul>
</template>

<style scoped lang="stylus" type="text/stylus">
.ability_table
    margin 2.75rem auto 2.5rem auto
    width 100%
    font-size .75rem
    text-align center
    overflow hidden
    .item
        float left
        margin-bottom .5rem
        width 100%
        .item_title
            display inline-block
            width 3rem
            line-height 1rem
            text-align right
            color #8989A1
        .item_num
            display inline-block
            text-indent 1rem
            width 3rem
            text-align left
            color #fff

</style>

<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                data: {}
            }
        },
        props: {
            userId: {
                type: [String,Number]
            }
        },
        created() {
          this.getData();
        },
        methods: {
           getData() {
               let url = `/players/${this.userId}/ability_detail`;
//               url = 'http://qa2.htop.info:50000/players/10158/ability_detail'; // todo
               this.ajax(url,'get').then((res) => {
                   this.data = res.data;
                   console.log(this.data)
               },(err) => {
                   if(err&&err.response){
                       let errors=err.response.data;
                       console.log(errors);
                   }
               })
           }
        }
    }
</script>