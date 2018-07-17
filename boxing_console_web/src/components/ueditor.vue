        <style >
        .quill-editor{
            min-height: 300px;
            background:#fff;
        }

        .ql-container{
            min-height: 300px;

        }

        .ql-snow .ql-editor img{
            max-width: 280px;
        }


        .ql-editor .ql-video{
            max-width: 280px;
        }

        </style>

        <template>
            <div style='position:relative'>
                <!-- quill-editor插件标签 分别绑定各个事件-->
                <quill-editor v-model="content" ref="myQuillEditor" :options="editorOption1" @change="onEditorChange($event)">
                </quill-editor>
                <!-- 文件上传input 将它隐藏-->
                <el-upload class="upload-demo" :action="qnLocation" :before-upload='beforeUpload' :data="uploadData" :on-success='upScuccess'
                ref="upload" style="display:none">
                    <el-button size="small" type="primary" :id="imgInput" element-loading-text="插入中,请稍候">点击上传</el-button>
                </el-upload>
                
            </div>
        </template>

        <script>
        import Quill from 'quill'

        export default {
        data () {
          return {
            content: '', // 文章内容
            img_url:'./static/img/upload_img.png',
            editorOption1: {
              placeholder: '请输入内容',
              name : '',
              modules: { // 配置富文本
                toolbar: [
                  ['bold', 'italic', 'underline', 'strike'],
                  ['blockquote', 'code-block'],
                  [{ 'header': 1 }, { 'header': 2 }],
                  [{ 'direction': 'rtl' }],
                  [{ 'size': ['small', false, 'large', 'huge'] }],
                  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                  [{ 'color': [] }, { 'background': [] }],
                  [{ 'font': [] }],
                  [{ 'align': [] }],
                  ['clean'],
                  ['link', 'image', 'video']
                ]
              }
            },
            addRange: [],
            uploadData: {},
            photoUrl: '', // 上传图片地址
            uploadType: '' // 上传的文件类型（图片、视频）
          }
        },
        props:{
          myQuillEditor :{
                type : String,
                default:''
            },
          imgInput:{
            type : String,
            default:''
          },
          appContent:{
            type : String,
            default:''
          }
        },
        computed: {
        // 上传七牛的actiond地址，http 和 https 不一样
        qnLocation () {
          return this.config.baseUrl+'/upload'
        }
        },
        methods: {
            // 图片上传之前调取的函数
            // 这个钩子还支持 promise
            beforeUpload (file) {
                // 对文件格式的要求
                // let Xls = file.name.split('.');
                // if(Xls[1] === 'xls'||Xls[1] === 'xlsx'){
                //     return file
                // }else {
                //     this.$message.error('上传文件只能是 xls/xlsx 格式!')
                //     return false
                // }
                return this.qnUpload(file)
            },
            // 图片上传前获得数据token数据
            qnUpload (file) {
                // console.log(file)
                this.fullscreenLoading = true
                const suffix = file.name.split('.')
                const ext = suffix.splice(suffix.length - 1, 1)[0]
                // console.log(this.uploadType)
                this.uploadData={
                  file:file
                }
            },

            // 图片上传成功回调 插入到编辑器中
            upScuccess (e, file, fileList) {
                this.fullscreenLoading = false
                let vm = this
                let url = ''
                url = this.config.baseUrl+e.urls[e.urls.length-1]
                if (url != null && url.length > 0) { // 将文件上传后的URL地址插入到编辑器文本中
                let value = url
                // API: https://segmentfault.com/q/1010000008951906
                // this.$refs.myTextEditor.quillEditor.getSelection();
                // 获取光标位置对象，里面有两个属性，一个是index 还有 一个length，这里要用range.index，即当前光标之前的内容长度，然后再利用 insertEmbed(length, 'image', imageUrl)，插入图片即可。
                vm.addRange = vm.$refs.myQuillEditor.quill.getSelection()
                value = value.indexOf('http') !== -1 ? value : 'http:' + value
                vm.$refs.myQuillEditor.quill.insertEmbed(vm.addRange !== null ? vm.addRange.index : 0, vm.uploadType, value, Quill.sources.USER) // 调用编辑器的 insertEmbed 方法，插入URL
                } else {
                this.$message.error(`${vm.uploadType}插入失败`)
                }
                this.$refs['upload'].clearFiles() // 插入成功后清除input的内容
            },

            // 点击图片ICON触发事件
            imgHandler (state) {
                this.addRange = this.$refs.myQuillEditor.quill.getSelection()
                if (state) {
                let fileInput = document.getElementById(this.imgInput)
                fileInput.click() // 加一个触发事件
                }
                this.uploadType = 'image'
            },
            onEditorChange ({ editor, html, text }) {
                this.content = html
                this.$emit('changeEditor',html)
            },
            // 点击视频ICON触发事件
            videoHandler (state) {
                this.addRange = this.$refs.myQuillEditor.quill.getSelection()
                if (state) {
                    let fileInput = document.getElementById(this.imgInput)
                    fileInput.click() // 加一个触发事件
                }
                this.uploadType = 'video'
            }
        },
        created () {
            this.$refs = {
            myQuillEditor: HTMLInputElement,
            imgInput1: HTMLInputElement,
            imgInput2: HTMLInputElement
            }
            this.content = this.appContent;
            // this.editorOption.name=this.myQuillEditor
        },
        // 页面加载后执行 为编辑器的图片图标和视频图标绑定点击事件
        mounted () {
            // 为图片ICON绑定事件 getModule 为编辑器的内部属性
            // console.log(this.$refs.myQuillEditor.quill)
            let $this = this
            this.$refs.myQuillEditor.quill.getModule('toolbar').addHandler('image', this.imgHandler)
            // this.$refs.myQuillEditor.quill.getModule('toolbar').addHandler('video', this.videoHandler) // 为视频ICON绑定事件
            $('.ql-toolbar').find('.ql-formats').last().append("<button type='button' style='width:28px;height:25px;cursor:pointer' class='local_video "+$this.imgInput+"'><img src='"+$this.img_url+"' width='100%'></button>")
            $('.ql-toolbar').on('click','.local_video.'+$this.imgInput,function(e){
                $this.addRange = $this.$refs.myQuillEditor.quill.getSelection()
                let fileInput = document.getElementById($this.imgInput)
                fileInput.click() // 加一个触发事件
                
                $this.uploadType = 'video'
            })
        }
    }
</script>

