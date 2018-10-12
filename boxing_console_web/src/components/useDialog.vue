<template>
	<div>
		<el-button type="danger" class='myColor_red myButton_40 btn_width_200 ' @click="confirmData.isshow=true">弹出确认框</el-button>
		<el-button type="danger" class='myColor_red myButton_40 ' @click="refuseData.isshow1=true">弹出输入框textarea（拒绝打款1、驳回1）</el-button>
		<el-button type="danger" class='myColor_red myButton_40 ' @click="refuseData.isshow2=true">弹出输入框textarea（审核通过2）</el-button>
		<el-button type="danger" class='myColor_red myButton_40 ' @click="dialog_label_data.isshow1=true">手机号</el-button>
		<el-button type="danger" class='myColor_red myButton_40 ' @click="dialog_label_data.isshow2=true">增加钱包余额</el-button>
		<el-button type="danger" class='myColor_red myButton_40 ' @click="weight_range.isshow=true">体重范围</el-button>


		
		<Confirm :isshow="confirmData.isshow" @confirm="conform1()" @cancel="cancel1()" :content="confirmData.content"></Confirm>
		<Dialog :isshow="refuseData.isshow1" @confirm="conform2()" @cancel="cancel2()" :content_title="refuseData.content_title" :content_foot="refuseData.content_foot" :type="1"></Dialog> 
		<Dialog :isshow="refuseData.isshow2" @confirm="conform2()" @cancel="cancel2()" :content_title="refuseData.content_title" :content_foot="refuseData.content_foot" :type="2"></Dialog> 
		<DialogLabel :isshow="dialog_label_data.isshow1" @confirm="conform3()" @cancel="cancel3()"  :type="'phone'"></DialogLabel> 
		<DialogLabel :isshow="dialog_label_data.isshow2" @confirm="conform3()" @cancel="cancel3()" :content_title="dialog_label_data.content_title" :content_foot="dialog_label_data.content_foot" :type="'number'"></DialogLabel>
		<WeightRange :isshow="weight_range.isshow" @confirm="conform4()" @cancel="cancel4()"></WeightRange> 
	</div>
</template>
<script>
	import Dialog  from "components/dialog"
    import Confirm from "components/confirm"
    import DialogLabel from "components/dialog_label"
    import WeightRange from "components/weight_range"
    export default {
        data() {
            return {
                confirmData:{
                	isshow: false,
                	content:'确认审核通过？'
                },
                refuseData:{
                	isshow1: false,
                	isshow2: false,
                	content_title:"拒绝打款原因（必填）",
                	content_foot:"确定不给用户打款？"
                },
                dialog_label_data:{
                	isshow1:false,
                	isshow2:false,
                	content_title:"增加钱包余额",
                },
                weight_range:{
                	isshow:false,
                }
            }
        },
        components: {
           Dialog,
           Confirm,
           DialogLabel,
           WeightRange
        },
        created() {
           
        },
        methods: {
            cancel1(val){
                this.confirmData.isshow=val;
            },
            conform1(){
                this.confirmData.isshow=false;
            },
            cancel2(val){
                this.refuseData.isshow1=val;
                this.refuseData.isshow2=val;
            },
            conform2(){
                this.refuseData.isshow1=false;
                this.refuseData.isshow2=false;
            },
            cancel3(val){
                this.dialog_label_data.isshow1=val;
                this.dialog_label_data.isshow2=val;
            },
            conform3(){
                this.dialog_label_data.isshow1=false;
                this.dialog_label_data.isshow2=false;
            },
            cancel4(val){
                this.weight_range.isshow=val;
            },
            conform4(){
                this.weight_range.isshow=false;
            },

        },
    }
</script>
