<template>
    <div id="table">
        <template>
            <el-table
              :data="tableData"
              style="width: 100%">
               <el-table-column
                :prop="value.title"
                :label="value.name"
                :width="value.width"
                v-for="value in tableColumn">
               </el-table-column>
               <el-table-column
                  fixed="right"
                  label="操作">
                  <template slot-scope="scope">
                    <el-button class='myBtnHover_red myButton_20' style='margin-right:20px' v-if="showBtnLeft" @click='btnLeftClick(scope.row)'>{{scope.row.is_locked?"解锁":"锁定"}}</el-button>
                    <span class='colorFont' @click="handleClick(scope.row)">{{operaname}}</span>
                  </template>
                </el-table-column>
            </el-table>
        </template>
    </div>
</template>

<style scoped>
    .myButton_20{padding:3px 10px;}
</style>
<style>
.el-table .cell{text-align:center!important;}
</style>
<script type="text/ecmascript-6">
    export default {
        data() {
            return {
                user_name: 'admin',
                
            }
        },
        props: {
            tableData: {
                type: Array,
                default: function (value) {
                    return value
                }
            },
            tableColumn:{
                type: Array,
                default: function (value) {
                    return value
                }
            },
            operaname :{
                type : String,
                default:'详情'
            },
            showBtnLeft : {
                type :Boolean,
                default:false,
            },
            btnLeftName :{
                type : String,
                default:''
            }
        },
        watch: {
        // 监测路由变化,只要变化了就调用获取路由参数方法将数据存储本组件即可
          '$route': 'getParams'
        },
        components: {
        },
        created() {
            
        },
        methods: {
            getParams(){
                let routerParams = this.$route.params.dataobj
                this.getMsg      = routerParams
            },
            handleClick(row){
                this.$emit('toDetail',row)
            },
            btnLeftClick(row){
                this.$emit('btnLeftClick',row)
            },
        },
    }
</script>