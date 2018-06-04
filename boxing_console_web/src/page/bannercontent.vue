<template>
    <div class="banner_content">
        <TopBar v-if="isShowTop" firstTitle_name="Banner管理" firstTitle_path="/usermanage" disNone="disNone"></TopBar>
        <div class="container">
            <el-form :model="form" label-width="100px" :rules="rules" ref="ruleForm">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name" placeholder="限制20字" maxlength="20"></el-input>
                </el-form-item>
                <el-form-item label="序号" prop="order_number" required>
                    <el-input v-model="form.order_number" placeholder="请输入正整数，数字越大，排序越靠前"></el-input>
                </el-form-item>
                <el-form-item label="打开方式" prop="link_type" required>
                    <el-radio-group v-model="form.link_type" @change="changeType">
                        <el-radio :label="1">app内网页跳转</el-radio>
                        <el-radio :label="2">app外网页跳转</el-radio>
                        <el-radio :label="3">app内本地跳转</el-radio>
                    </el-radio-group>
                </el-form-item>
                <template v-if="form.link_type != 3">
                    <el-form-item label="链接地址" prop="link">
                        <el-input v-model="form.link"></el-input>
                    </el-form-item>
                </template>
                <template v-else>
                    <el-radio-group v-model="checkType" @change="changeCheckType" style="width: 100%">
                        <el-radio label="voteId" class="vertical_radio" style="display: block">
                            <el-form-item label="投票ID" prop="voteId">
                                <el-input v-model="form.voteId"></el-input>
                            </el-form-item>
                        </el-radio>
                        <el-radio label="enrollId" style="display: block;margin-left: 0" class="vertical_radio">
                            <el-form-item label="报名ID" prop="enrollId">
                                <el-input v-model="form.enrollId"></el-input>
                            </el-form-item>
                        </el-radio>
                        <el-radio label="contentId" style="display: block;margin-left: 0" class="vertical_radio">
                            <el-form-item label="资讯ID" prop="contentId">
                                <el-input v-model="form.contentId"></el-input>
                            </el-form-item>
                        </el-radio>
                    </el-radio-group>
                </template>
                <el-form-item label="展示图片" required>
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
                        请上传展示图片
                    </div>
                </el-form-item>
                <el-form-item class="handle_btn">
                    <el-button class="cancel" @click="cancelEv">取消</el-button>
                    <el-button type="danger" @click="submitForm('ruleForm')">发布</el-button>
                </el-form-item>
            </el-form>
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

<script type="text/ecmascript-6">
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
                form: {
                    name: '',
                    order_number: '',
                    link_type: 1,
                    link: '',
                    voteId: '',
                    enrollId: '',
                    contentId: '',
                },
                picture: '',
                pictureUrl: '',
                rules: {
                    name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
                    order_number: [
                        { validator: (rule, value, callback) => {
                            if (value === '') callback(new Error('请输入序号'))
                            else {
                                if (value < 0 || !/^[0-9]*$/.test(value)) {
                                    callback(new Error('只能输入正整数'));
                                    return;
                                }
                                callback();
                            }
                        }, trigger: 'blur', }
                    ],
                    link: [
                        { validator: (rule, value, callback) => {
                            if (value === '') callback(new Error('请输入链接地址'));
                            else {
                                if (!this.checkUrl(value)) {
                                    callback(new Error('请输入正确的链接地址'));
                                    return;
                                }
                                callback();
                            }
                        }, trigger: 'change',required: true }
                    ],
                    voteId: [
                        { validator: (rule, value, callback) => {
                            if (this.checkType !== 'voteId') callback();
                            if (value === '') {
                                callback(new Error('请输入投票ID'));
                            } else {
                                if (value < 0 || !/^[0-9]*$/.test(value)) {
                                    callback(new Error('投票ID必须为数字'));
                                    return;
                                }
                                callback();
                            }
                        }, trigger: 'change',required: true }
                    ],
                    enrollId: [
                        { validator: (rule, value, callback) => {
                            if (this.checkType !== 'enrollId') callback();
                            if (value === '') {
                                callback(new Error('请输入报名ID'));
                            } else {
                                if (value < 0 || !/^[0-9]*$/.test(value)) {
                                    callback(new Error('报名ID必须为数字'));
                                    return;
                                }
                                callback();
                            }
                        }, trigger: 'change',required: true }
                    ],
                    contentId: [
                        { validator: (rule, value, callback) => {
                            if (this.checkType !== 'contentId') callback();
                            if (value === '') {
                                callback(new Error('请输入资讯ID'));
                            } else {
                                if (value < 0 || !/^[0-9]*$/.test(value)) {
                                    callback(new Error('资讯ID必须为数字'));
                                    return;
                                }
                                callback();
                            }
                        }, trigger: 'change',required: true }
                    ]
                }
            }
        },

        components: {
            TopBar
        },

        created() {
            this.id = this.$route.query.id || '';
            this.id && this.getPageInfo();
        },

        methods: {

            handleAvatarSuccess(res, file) {
                let picUrl = `${config.baseUrl}/${res.urls[0]}`;
                let image = new Image();
                image.src = picUrl;
                image.onload = () => {
                    if (image.width !== 750 || image.height != 340) {
                        this.showErrorTip('请上传符合尺寸的商品详情图');
                    }
                    else {
                        this.picture = picUrl
                        this.pictureUrl = res.urls[0];
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

            removeImageEv() {
                this.picture = this.pictureUrl = '';
            },

            changeType() {
                this.$refs['ruleForm'].clearValidate();
                this.showError = false;
            },

            changeCheckType(val) {
                this.checkType = val;
                this.showError = false;
                this.$refs['ruleForm'].clearValidate();
            },

            bannerEv() {
                let obj = Object.assign(this.form,{picture: this.pictureUrl});
                if (obj.link_type == 3) {
                    let linkObj = {
                        'voteId': 'game_votes',
                        'enrollId': 'game_apply',
                        'contentId': 'game_news'
                    }
                    obj['link'] = linkObj[this.checkType] + ':' + obj[this.checkType];
                }
                delete obj['voteId'];
                delete obj['enrollId'];
                delete obj['contentId'];

                !this.id ? this.createBannerEv(obj) : this.modifyBannerEv(obj);

            },

            createBannerEv(obj) {
                console.log(obj)
                this.ajax('/banners','post',obj).then((res) => {
                    res && res.data && this.$router.push({path: '/bannermanage'});
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        for(var key in errors){
                            this.showErrorTip(errors[key][0]);
                        }
                    }
                })
            },

            modifyBannerEv(obj) {
                this.ajax(`/banners/${this.id}`,'put',obj).then((res) => {
                    res && res.data && this.$router.push({path: '/bannermanage'});
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data;
                        for(var key in errors){
                            this.showErrorTip(errors[key][0]);
                        }
                    }
                })
            },

            getPageInfo() {
                this.ajax(`/banners/${this.id}`,'get').then((res) => {
                    if (res && res.data ) {
                        this.form = res.data;
                        this.picture = this.form.picture;
                        delete this.form['picture'];

                        this.form.link_type !== 3
                            ? (this.form['voteId'] = this.form['enrollId'] = this.form['contentId'] = '') : this.setCheckType(res.data.link);
                    }

                    console.log(this.form)
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            this.showErrorTip(errors[key][0]);
                        }
                    }
                })
            },

            checkUrl(url) {
                let Expression=/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/;
                return new RegExp(Expression).test(url);
            },

            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            },

            cancelEv() {
                this.$router.push({path: '/bannermanage'});
            },

            setCheckType(data) {
                let checkType = data.split(':');
                let obj = {
                    'game_votes': 'voteId',
                    'game_apply': 'enrollId',
                    'game_news': 'contentId'
                }
                for (let key in obj) {
                    let val = obj[key];
                    this.form[val] = '';
                    if (key === checkType[0]) {
                        this.form[val] = checkType[1];
                        this.form.link = '';
                        this.checkType = val;
                    }
                }
            }

        }
    }
</script>