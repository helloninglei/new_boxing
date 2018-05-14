<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="拳馆管理" firstTitle_path="/boxingmanage" secondTitle_name="拳馆列表" secondTitle_path="/boxinglist"></TopBar>
    </div>
</template>

<style scoped>
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