<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="拳手认证" firstTitle_path="" disNone="disNone"></TopBar>

        拳手认证ss
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