<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="用户管理" firstTitle_path="/usermanage" disNone="disNone"></TopBar>

        财务管理ss
    </div>
</template>

<style scoped lang="stylus" type="text/stylus">
    
</style>

<script type="text/ecmascript-6">
    import TopBar from 'components/topBar';

    export default {
        data() {
            return {
                isShowTop : true,
            }
        },
        components: {
            TopBar
        },
        created() {
            
        },
        methods: {
            
        },
    }
</script>