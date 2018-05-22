<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="拳馆管理" firstTitle_path="/boxingmanage" secondTitle_name="添加拳馆" secondTitle_path="/addBoxing"></TopBar>
        <div>添加拳馆</div>
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