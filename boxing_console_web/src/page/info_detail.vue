<template>
    <div id="info_detail">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/infolist" secondTitle_name="资讯"></TopBar>
        <div class="container">
            <el-row> 
                <el-col :span="12">
                    <el-form :model="form" label-width="110px" :rules="rules" ref="ruleForm">
                        <el-form-item label="主标题" prop="title">
                            <el-input v-model="form.title" placeholder="限制20字" :maxlength="20"></el-input>
                        </el-form-item>
                        <el-form-item label="副标题" prop="sub_title">
                            <el-input v-model="form.sub_title" placeholder="请输入"></el-input>
                        </el-form-item>
                        <el-form-item label="初始阅读量" prop="initial_views_count" style='width:284px'>
                            <el-input v-model="form.initial_views_count" placeholder="请输入"></el-input>
                        </el-form-item>
                        <el-form-item label="资讯主题图">
                            <el-upload
                                    class="avatar-uploader"
                                    :action=action
                                    :show-file-list="false"
                                    :on-success="handleAvatarSuccess"
                                    style="position: relative;width: 375px;border: 1px solid #d9d9d9;overflow: hidden;cursor: pointer;">
                                <template v-if="picture">
                                    <i class="el-icon-circle-close close_btn" @click.stop="removeImageEv"></i>
                                    <img  :src="picture" class="avatar">
                                </template>
                                <template v-else>
                                    <i class="el-icon-plus avatar-uploader-icon"></i>
                                    <div class="upload_tip_text">尺寸大小：750*340</div>
                                </template>
                            </el-upload>
                            <div class="el-form-item__error" v-if="showError">
                                请上传资讯主题图
                            </div>
                        </el-form-item>
                        <el-form-item label="是否置顶" prop="stay_top">
                            <el-radio-group v-model="form.stay_top">
                                <el-radio :label="true">是</el-radio>
                                <el-radio :label="false">否</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-checkbox-group v-model="form.push_news" style='margin-bottom:22px'>
                          <el-checkbox label="创建推送" name="push_news"></el-checkbox>
                        </el-checkbox-group>
                        <el-form-item label="发送时间" prop="stay_top">
                            <el-date-picker
                                    class="margin_rt25"
                                    v-model="dateArr"
                                    type="datetimerange"
                                    range-separator="至"
                                    start-placeholder="起始日期"
                                    end-placeholder="结束日期"
                                    @change="getDateTime"
                                    value-format="yyyy-MM-dd hh:mm:ss">
                            </el-date-picker>
                        </el-form-item>
                        <p>App内正文（必填），如未填写App外分享正文，App内和App外都显示App内正文。</p>
                        <el-form-item class="handle_btn">
                            <el-button class="cancel" @click="cancelEv">取消</el-button>
                            <el-button type="danger" @click="submitForm('ruleForm')">发布</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<style lang="stylus" type="text/stylus" scoped>

    .el-icon-circle-close {
        position absolute
        right  0
        top 0
        font-size 20px
    }
    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 375px;
        height: 170px;
        line-height: 170px;
        text-align: center;
    }
    .avatar {
        display: block;
        width: 375px;
        height 170px
    }
    .handle_btn {
        margin-top 60px
        .cancel {
            margin-right 30px
        }
    }
    .upload_tip_text {
        width 100%
        text-align center
        position absolute
        bottom 0
        color #909399
    }
</style>
<style>
    #info_detail .el-checkbox__label,#info_detail .el-radio__label,#info_detail .el-form-item__label{
        font-family: PingFangSC-Regular;
        font-size: 16px;
        color: #000000;
    }
</style>
<script>
    import TopBar from 'components/topBar';
    import config from 'common/my_config'

    export default {
        data() {
            return {
                id: '',
                isShowTop: true,
                showError: false,
                action: `${config.baseUrl}/upload`,
                checkType: 'voteId',
                dateArr: [],
                form: {
                    title: '',
                    sub_title: '',
                    initial_views_count: 1,
                    picture: '',
                    picture_change: '',
                    stay_top: '',
                    push_news: '',
                    start_time: '',
                    end_time: '',
                    app_content: '',
                    share_content: '',
                },
                picture: '',
                rules: {
                    title    : [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    sub_title: [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    picture_change: [
                        { validator: (rule, value, callback) => {
                            if (this.picture === ''&&value==='') {
                                callback(new Error('请选择主题图片'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur', required: true}
                    ],
                    stay_top: [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    push_news: [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    start_time: [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    end_time: [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    app_content: [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    share_content: [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    initial_views_count: [
                        { validator: (rule, value, callback) => {
                            if (value === '') callback(new Error('请输入初始阅读量'))
                            else {
                                if (value < 0 || !/^[0-9]*$/.test(value)) {
                                    callback(new Error('只能输入正整数'));
                                    return;
                                }
                                callback();
                            }
                        }, trigger: 'blur',required: true }
                    ],
                    
                }
            }
        },

        components: {
            TopBar
        },

        created() {
            this.query = this.$route.query;
            console.log(this.query)
        },

        methods: {

            handleAvatarSuccess(res, file) {
                let picUrl = `${config.baseUrl}/${res.url}`;
                let image = new Image();
                image.src = picUrl;
                image.onload = () => {
                    if (image.width !== 750 || image.height != 340) {
                        this.showErrorTip('请上传符合尺寸的商品详情图');
                    }
                    else {
                        this.picture = picUrl
                        this.showError = false;
                    }
                };
            },

            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (!this.picture) {
                        this.showError = true;
                        return false;
                    }
                    if (valid) {
                        this.bannerEv();
                    }
                });
            },

            getDateTime() {
                this.form.start_time = this.dateArr[0];
                this.form.end_time = this.dateArr[1];
            },

            removeImageEv() {
                this.picture = '';
            },

            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            },

            cancelEv() {
                this.$router.push({path: '/infolist'});
            },

        }
    }
</script>