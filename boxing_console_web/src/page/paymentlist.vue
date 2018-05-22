<template>
    <div class="">
        <TopBar v-if="isShowTop" firstTitle_name="财务管理" firstTitle_path="/boxingmanage" secondTitle_name="用户支付流水" secondTitle_path="/addBoxing"></TopBar>
        <div>支付流水ss</div>
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