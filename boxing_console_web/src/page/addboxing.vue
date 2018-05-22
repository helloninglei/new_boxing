<template>
    <div id="addBoxing">
        <TopBar v-if="isShowTop" firstTitle_name="拳馆管理" firstTitle_path="/boxingmanage" secondTitle_name="添加拳馆" secondTitle_path="/addBoxing"></TopBar>
        <div class='container'>
            <el-row> 
                <el-col :span="9">
                    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                        <el-form-item label="拳馆名称" prop="club_name">
                            <el-input v-model="ruleForm.club_name"></el-input>
                        </el-form-item>
                        <el-form-item label="宣传图" prop="club_name">
                            <el-row>
                                <el-col :span="8">
                                    <el-button type="danger" class='myColor_red myButton_40 btn_width_95'>上传</el-button>
                                </el-col>
                                <el-col :span="10">
                                    <div class='image'>
                                        <img src="" alt="">
                                    </div>
                                </el-col>
                            </el-row>
                        </el-form-item>
                        <el-form-item label="地址" prop="address">
                            <el-input v-model="ruleForm.address"></el-input>
                        </el-form-item>
                        <el-form-item label="电话" prop="phone">
                            <el-input v-model="ruleForm.phone"></el-input>
                        </el-form-item>
                        <el-form-item label="营业时间" prop="opening_hours">
                            <el-input v-model="ruleForm.opening_hours"></el-input>
                        </el-form-item>
                        <el-form-item label="拳馆简介" prop="introduction">
                            <el-input type="textarea" v-model="ruleForm.introduction" :rows="6"></el-input>
                        </el-form-item>
                        <el-form-item label="展示图" prop="club_name">
                            <el-input v-model="ruleForm.club_name"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
                            <el-button @click="resetForm('ruleForm')">重置</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<style>
#addBoxing .el-form-item__label{
    font-family: "PingFangSC-Regular";
    font-size: 16px;
    color: #000000;
}
#addBoxing .el-form-item{margin-bottom:30px;}
</style>
<style scope>
    .image{height:140px;width:140px;border:1px solid #ccc;vertical-align: middle}
    .image img{height:100%;}
</style>
<script>
    import TopBar from 'components/topBar';
    export default {
        data() {
            return {
                isShowTop : true,
                ruleForm: {
                    club_name: '',
                    address: '',
                    phone: '',
                    opening_hours: '',
                    introduction: '',
                    type: [],
                    resource: '',
                    desc: ''
                },
                rules:{
                    club_name:[
                        { required:false, message:'请输入拳馆', trigger:'change' }
                    ],
                    address:[
                        { required:true, message:'请输入拳馆地址', trigger:'blur' },
                    ],
                    phone:[
                        { required:true, message:'请输入电话', trigger:'change' }
                    ],
                    opening_hours:[
                        { required:true, message:'请输入营业时间', trigger:'change' }
                    ],
                    introduction:[
                        { required:true, message:'请输入拳馆简介', trigger:'blur' }
                    ]
                }
                
            }
        },
        components: {
            TopBar
        },
        created() {
            
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        alert('submit!');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            }
        },
    }
</script>