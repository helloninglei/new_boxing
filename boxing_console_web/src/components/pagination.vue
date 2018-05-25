<template>
    <div id='footer'>
        <template>
              <div class="block">
                <el-pagination
                  @current-change="handleCurrentChange"
                  :current-page.sync="currentPage"
                  prev-text="上一页"
                  next-text="下一页"
                  background
                  layout="prev, pager, next"
                  :total="total">
                </el-pagination>
              </div>
        </template>
    </div>
</template>

<style>
    .el-pager .number{
        background: #fff!important;
        border:1px solid rgba(0,0,0,0.1);
        border-left:1px solid rgba(0,0,0,0.1)!important;
        height:32px;
        box-sizing: border-box;
    }
    .el-pager .number.active{
        background: #F95862!important;
        border:1px solid #F95862!important;
    }
    .btn-prev,.btn-next{
        height:32px!important;
        width:94px;
        background:#fff!important;
        border:1px solid rgba(0,0,0,0.1)!important;
    }
</style>
<script>
    export default {
        data() {
            return {
                user_name: 'admin',
                currentPage: 1,
                
            }
        },
        props: {
            total: {
                type: [String, Number],
            },
        },
        watch: {
        
        },
        components: {
        },
        created() {
            //事件委托
            let $this=this
            document.addEventListener('click',function(event){
                var target = event.target;
                if(target.id == "firstPage"){
                    $this.currentPage=1;
                }
                if(target.id == "lastPage"){
                    $this.currentPage=($this.total%10>0)?parseInt($this.total/10)+1:parseInt($this.total/10);
                }
            })
        },
        mounted(){
            var  firstBtn     = document.createElement('button');
            var  lastBtn      = document.createElement('button');
            var  span         = document.createElement('span');
            firstBtn.className= "btn-prev";
            firstBtn.id       = "firstPage";
            firstBtn.innerText= "首页";
            lastBtn.className = "btn-prev";
            lastBtn.id        = "lastPage";
            lastBtn.innerText = "末页"
            span.innerText    = '每页10条'
            span.className    = 'el-pagination__total'
            let pagination=document.getElementsByClassName("el-pagination")[0]
            pagination.appendChild(lastBtn);
            pagination.appendChild(span);
            pagination.insertBefore(firstBtn,pagination.childNodes[0]);

        },
        methods: {
            handleCurrentChange(val){
                this.$emit('changePage',val)
            }
        },
    }
</script>