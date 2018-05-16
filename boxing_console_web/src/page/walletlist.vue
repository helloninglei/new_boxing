<template>
    <div class="classDetail">
        
    </div>
</template>
<style scoped>
</style>
<style>
nav{min-height: 528px}
</style>
<script type="text/ecmascript-6">
    import TopBar from 'components/topBar';
    import Table  from 'components/table';
    import Pagination  from 'components/pagination';
    export default {
        data() {
            return {
                res:{
                    "count": 1,
                    "next": null,
                    "previous": null,
                    "results": [
                        {
                            "id": 1,
                            "boxer_name": "张三", // 拳手姓名
                            "mobile": "111111111", // 拳手手机号
                            "is_professional_boxer": true, //是否是专业选手
                            "is_accept_order": true, // 接单状态
                            "club": "北京拓天比图拳馆拓天比图拳馆拓天比图拳馆，北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆。500字拓天比图拳馆。500字北京拓天比图拳馆拓天比图拳馆拓天比图拳馆，北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳馆拓天比图拳馆拓天比图拳馆北京拓天比图拳京拓天比图拳馆拓天比图拳馆拓天比图拳馆。500字拓天比图拳馆。500字", // 约单拳馆
                            "allowed_lessons": [ // 已通过的课程类型
                                "THAI_BOXING",
                                "BOXING",
                                "MMA"
                            ],
                            "boxer_id": 1, //拳手id
                            "course_name": "THAI_BOXING", // 课程名
                            "price": 120, // 价格
                            "duration": 120, // 时长
                            "validity": "2018-08-25" // 有效期
                        }
                    ]
                }
            }
        },
        components: {
            TopBar,
            Table ,
            Pagination
        },
        created() {
            let query = this.$route.query
            this.getDetailData(query.id);
        },
        methods: {
            getDetailData(id) {
                //获取data数据
                let $this   = this
                // this.ajax('/course','get',{},{id:id}).then(function(res){
                //     if(res&&res.data){
                //         console.log(res.data)
                //     }

                // },function(err){
                //     if(err&&err.response){
                //         let errors=err.response.data
                //         for(var key in errors){
                //             console.log(errors[key])
                //             // return
                //         } 
                //     } 
                // })
            },
            checkIdent(id){
                console.log('查看认证信息'+id)
            }
        },
    }
</script>