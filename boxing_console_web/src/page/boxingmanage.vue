<template>
    <div class="upload-img">

        <h2>上传封面<span class="mark">上传视频缩略图封面，建议上传16:9的图片，仅支持JPEG,BMP,PNG格式，图像小于2M</span></h2>

        <div class="select-button clearfix">

        <el-upload :show-file-list="false" :auto-upload="false" :data="{token:token}" action="http://up-z2.qiniu.com/" :http-request="upload"  name="file" ref="coverImg"  list-type="picture-card" class="upload-plus clearfix" :on-change="handleChange" :on-preview="handlePictureCardPreview" :before-upload="handleBefore">

            <i class="el-icon-plus add-img">点击添加图片</i>

        </el-upload>
        <div class="file" v-if="showCover">
            <div class="file-box">
                <span class="tag" :style="{backgroundColor:tagObj.color}">{{tagObj.label}}</span>
                <img :src="item.coverUrl" alt="">
                <div class="cover-bar">
                    <a href="javascript:;" class="el-icon-view" @click="handleCheckView"></a>
                    <a href="javascript:;" class="el-icon-delete2" @click="handleDelete"></a>
                </div>
            </div>
        </div>
        <cropper :panel="panel" :url="url" v-if="panel" @handleShow="handleShow" @handleGetUrl="handleGetUrl" @upload="upload"></cropper>
        <el-dialog v-model="dialogVisible" size="tiny">

            <img width="100%" :src="dialogImageUrl" alt="">

        </el-dialog>

        </div>

    </div>
</template>
<script>
import url from '../urls/index'
import EditVideo from '../api/service/videoEdit'
import cropper from '@/components/common/cropper.vue'
    export default {

        data() {

            return {
                dialogImageUrl: '',//查看缩略图弹框的图片url
                dialogVisible: false,//查看缩略图弹框显示
                uploadUrl:'',//上传的url
                fileName:"",//文件名
                showCover:false,//上传缩略图成功控制是否显示
                // coverUrl:"" //上传成功后的url地址
                panel:false,
                url:''
            }

        },
        components: {
          cropper
        },
        computed:{
            item:{
                get:function(){
                    return JSON.parse(window.localStorage.getItem('item'))
                },
                set:function(value){
                    window.localStorage.setItem('item',JSON.stringify(value))
                }
            },
            tagObj:{
                get:function(){
                    return this.$store.getters.GET_TAG_OBJ
                },
                set:function(value){
                    this.$store.commit('UPDATE_TAG_OBJ',value)
                }
            },
            token:{
                get:function(){
                    return this.$store.getters.GET_TOKEN
                },
                set:function(value){
                    return this.$store.commit('UPDATE_TOKEN',value)
                }
            }
        },
        mounted(){
            this.uploadUrl = url['Upload'];
            //页面加载完成  判断localStorage是否存在
            try {
              if(this.item.coverUrl != "" && this.item.coverUrl){
                this.showCover=true
              }else{
                this.showCover=false
              }
            } catch (error) {
              this.showCover = false
              return this.file=[]
              this.postData.token = ''
            }
        },
        methods: {
            handleChange:function (files) {
              if (!files) return;
              this.panel = true;
              this.picValue = files.raw;
              this.url = files.url;
              this.panel = true;
            },
            //生成图片链接
            getObjectURL (file) {
              var url = null ;
              if (window.createObjectURL!=undefined) { // basic
                url = window.createObjectURL(file) ;
              } else if (window.URL!=undefined) { // mozilla(firefox)
                url = window.URL.createObjectURL(file) ;
              } else if (window.webkitURL!=undefined) { // webkit or chrome
                url = window.webkitURL.createObjectURL(file) ;
              }
              return url ;
            },
            //子组件修改弹出层显示和隐藏状态
            handleShow:function (data) {
              this.panel = data
            },
            //子组件剪裁过后的bese64图片
            handleGetUrl:function (data) {
              this.item.coverUrl = data
            },
            upload:function(e){
              const self = this
              var pic = this.item.coverUrl.replace('data:image/png;base64,','');
              var url = "http://up-z2.qiniu.com/putb64/-1"; //非华东空间需要根据注意事项 1 修改上传域名
              var xhr = new XMLHttpRequest();
              xhr.onreadystatechange=function(){
                if (xhr.readyState==4){
                  // document.getElementById("myDiv").innerHTML=xhr.responseText;

                  const fileName = xhr.responseText ? JSON.parse(xhr.responseText) : ""
                  EditVideo.DownloadUrl({fileName:fileName.key,type:20}).then((data)=>{
                      const item=JSON.parse(window.localStorage.getItem('item'))
                      item.coverUrl = data.fileUrl
                      self.item.coverUrl = data.fileUrl//返回的封面url
                      self.dialogImageUrl = data.fileUrl//查看大图的url地址
                      self.showCover = true //上传成功控制列表显示
                      window.localStorage.setItem('item',JSON.stringify(item))
                  })
                }
              }
              xhr.open("POST", url, true);
              xhr.setRequestHeader("Content-Type", "application/octet-stream");
              xhr.setRequestHeader("Authorization", "UpToken "+this.token);
              xhr.send(pic);
            },
            //上传之前 文件类型判断
            handleBefore:function(file){
                const extension = file.name.split('.')[1] === 'jpeg'
                const extension1 = file.name.split('.')[1] === 'bmp'
                const extension2 = file.name.split('.')[1] === 'png'
                const extension3 = file.name.split('.')[1] === 'jpg'
                const isLt2M = file.size / 1024 / 1024 < 2
                if(!extension && !extension1 && !extension2 && !extension3){
                    this.$notify({
                        type: 'error',
                        message: '上传图片格式不正确!'
                    });
                    return false
                }
                if(!isLt2M){
                    this.$notify({
                        type: 'error',
                        message: '上传缩略图不能超过2M!'
                    });
                    return false
                }
                return extension || extension1 || extension2 ||  extension3
            },
            //查看图片
            handlePictureCardPreview(file) {
                this.dialogImageUrl = this.item.coverUrl
                this.dialogVisible = true;
            },
            //查看大图
            handleCheckView:function(){
                this.dialogImageUrl = this.item.coverUrl
                this.dialogVisible = true
            },
            //删除已上传的缩略图
            handleDelete:function(){
                this.file = {}
                this.showCover = false
                this.item.coverUrl = ""
                const item=JSON.parse(window.localStorage.getItem('item'))
                item.coverUrl = ""
                window.localStorage.setItem('item',JSON.stringify(item))
                window.localStorage.removeItem('coverFile')
            }
        }

    }
</script>
<style scoped>
    .upload-img {

        width: 1000px;

        margin: 20px auto 10px;

        box-shadow: 0 6px 10px 0 rgba(212, 212, 212, 0.50);

        background: #ffffff;

    }



    .upload-img h2 {

        padding: 10px;

        text-align: left;

        border-bottom: 1px solid #f4f4f4;

        font-size: 16px;

        color: #38424b;

    }



    .mark {

        font-size: 12px;

        color: #69717a;

        margin-left: 20px;

    }



    .select-button {

        text-align: left;

        padding: 20px 10px;

    }


    .add-img{
        font-size:14px;
        color:#38424b;
        position: relative;
    }
    .add-img::before{
        position: absolute;
        top: -25px;
        left: 50%;
        margin-left: -10px;
        border-radius: 50%;
        background: #000;
        color: #fff;
        padding: 3px;
    }
    .upload-plus{
        float: left;
    }
    .file{
        float: left;
        position: relative;
    }
    .file-box{
        position: relative;
        line-height: 150px;
        float: left;
        margin-right: 20px;
        width: 235px;
        height: 132px;
        background: #f4f4f4;
        /* border: 1px dashed #c0ccda; */
        /* border-radius: 6px; */
    }
    .file-box img{
        width: 235px;
        height: 132px;
        /* border-radius: 6px; */
    }
    .cover-bar{
        position: absolute;
        top: 0;
        left: 0;
        width: 235px;
        height: 132px;
        text-align: center;
        display: none;
        /* border-radius: 6px; */
        background: rgba(0, 0, 0, 0.50)
    }
    .file:hover .cover-bar{
        display: block;
    }
    .cover-bar a{
        color: #fff;
        text-decoration: none;
        font-size: 20px;
        margin: 0 10px;
    }
    .tag{
        position: absolute;
        left: 0;
        top: 0;
        z-index: 99;
        width: 34px;
        height: 17px;
        display: block;
        font-size: 14px;
        color: #fff;
        line-height: 17px;
        text-align: center;
    }

</style>
