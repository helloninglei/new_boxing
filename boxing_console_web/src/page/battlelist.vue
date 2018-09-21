<template>
    <div class="battlelist" style="calc(100vw - 230px)">
        <TopBar v-if="isShowTop" firstTitle_name="赛事管理" firstTitle_path="/infolist" secondTitle_path="/metchlist" secondTitle_name="赛程管理" thirdTitle_name="对战表"></TopBar>
        <div class="container">
            <header>
                <p class='battle_title'>赛事信息 <span class='edit_icon' @click="editMetch"></span></p>
                <p class="battle_content"><span style='color:#909399;margin-right:20px'>比赛日期</span><span style='color:#1D1D27;'>{{editmetch.race_date}}</span></p>
                <p class="battle_content" style="margin-bottom:35px"><span style='color:#909399;margin-right:20px'>赛事名称</span><span style='color:#1D1D27;'>{{editmetch.name}}</span></p>
                <p class='battle_title'>对战信息</p>
                <!-- <img :src="src" alt=""> -->
            </header>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_bt20' @click.native="addBattleEv">添加对战</el-button>
            <template>
                <el-table
                        :data="tableData"
                        style="width: 100%">
                    <el-table-column
                            prop="id"
                            label="ID">
                    </el-table-column>
                    <el-table-column
                            prop="red_player"
                            label="红方姓名">
                    </el-table-column>
                    <el-table-column
                            prop="blue_player"
                            label="蓝方姓名">
                    </el-table-column>
                    <el-table-column
                            prop="category"
                            label="项目类型">
                    </el-table-column>
                    <el-table-column
                            label="项目级别">
                            <template slot-scope="scope">
                                <span>{{scope.row.level_min+'-'+scope.row.level_max+'KG'}}</span>
                            </template>
                    </el-table-column>
                    <el-table-column
                            prop="result"
                            label="胜负">
                    </el-table-column>
                    <el-table-column label="操作" width='220'>
                        <template slot-scope="scope">
                            <el-button
                                    size="mini"
                                    @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                            <el-button
                                    size="mini"
                                    type="danger"
                                    @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </template>
            <footer v-if='total>10'>
                <Pagination :total="total" @changePage="changePage" :page="page"></Pagination>
            </footer>
        </div>
        <Confirm :isshow="confirmData.isshow" @confirm="conform1" @cancel="cancel()" :content="confirmData.content" :id='confirmData.id' :index='confirmData.index'></Confirm>
        <Metchdialog :isshow="editmetch.isshow" @confirm="conform" @cancel="cancel()" content_title="编辑赛程" :id="form.schedule" :name="editmetch.name" :race_date="editmetch.race_date"></Metchdialog>
        <el-dialog  :visible.sync="showBattleDialog" class='myDialog'>
            <div class="dialog_title">编辑对战表</div>
            <div class="dialog_content" >
                <el-form ref="form" :model="form" label-width="76px" :rules="rules">
                    <el-row>
                        <el-col :span="11">
                            <el-form-item label="红方姓名" prop="red_player">
                                <!-- <el-input v-model="form.red_player" placeholder="请输入姓名" ></el-input> -->
                                <template>
                                      <el-select v-model="form.red_player" filterable placeholder="请输入姓名">
                                        <el-option
                                          v-for="item in players"
                                          :key="item.id"
                                          :label="item.name+'  '+item.mobile"
                                          :value="item.id">
                                        </el-option>
                                      </el-select>
                                </template>
                            </el-form-item>
                        </el-col>
                        <el-col :span="11" :offset="2">
                            <el-form-item label="蓝方姓名" prop="blue_player">
                                <template>
                                      <el-select v-model="form.blue_player" filterable placeholder="请输入姓名">
                                        <el-option
                                          v-for="item in players"
                                          :key="item.id"
                                          :label="item.name+'  '+item.mobile"
                                          :value="item.id">
                                        </el-option>
                                      </el-select>
                                </template>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-form-item label="项目类型" prop="category">
                        <el-radio-group v-model="form.category">
                            <el-radio :label="1" name="category" value="1">自由搏击</el-radio>
                            <el-radio :label="2"    name="category" value="2">拳击</el-radio>
                            <el-radio :label="3"    name="category" value='3'>MMA</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-row>
                        <el-form-item label="项目级别">
                            <el-col :span="6">
                              <el-form-item prop="level_min">
                                <el-input type="number"  v-model="form.level_min" style="width: 100%;"></el-input>
                              </el-form-item>
                            </el-col>
                            <el-col class="line" :span="2" style='text-align: center'>—</el-col>
                            <el-col :span="6">
                              <el-form-item prop="level_max">
                                <el-input type="number" v-model="form.level_max" style="width: 100%;"></el-input>
                              </el-form-item>
                            </el-col>
                        </el-form-item>
                    </el-row>
                    <el-form-item label="赛事结果" prop="result">
                        <el-radio-group v-model="form.result">
                            <el-radio :label="1"     name="result" >红方胜</el-radio>
                            <el-radio :label="2"     name="result" >蓝方胜</el-radio>
                            <el-radio :label="3" name="result" >红方KO蓝方</el-radio>
                            <el-radio :label="4" name="result" >蓝方KO红方</el-radio>
                        </el-radio-group>
                    </el-form-item>
                </el-form>
            </div>
            <div slot="footer" class="dialog-footer" style='text-align:center'>
                <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="showBattleDialog=false">取消</el-button>
                <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="saveBettle()">确定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<style scoped lang="stylus">
    .battle_title{
        font-family: PingFangSC-Medium;
        font-size: 22px;
        color: #000000;
        letter-spacing: 0;
        margin-bottom:20px;
    }
    .battle_content{
        font-family: PingFangSC-Regular;
        font-size: 14px;
        margin-bottom:20px;
    }
    .edit_icon{
        display:inline-block;
        width:14px;
        height:14px;
        background:url('./img/edit.png') no-repeat center center;
        background-size:contain;
        cursor:pointer;
    }
    .font_14{
        font-size:14px
    }
</style>
<style lang="stylus">
    .battlelist .myDialog .el-dialog{
        width:700px;
        height:380px;
        .el-dialog__body{
            padding:0 50px;
            .dialog_title{
                font-family: PingFangSC-Regular;
                font-size: 16px;
                color: #000000;
                margin-bottom:25px;
            }
            .el-form-item__label{
                font-family: PingFangSC-Regular;
                font-size: 14px!important;
                color: #606266;
                text-align:left;
            }
            .el-form-item{
                margin-bottom:16px!important;
                height:40px;
            }
            .el-dialog__footer{margin-top:0!important}
            .el-checkbox:first-child{margin-left:0}
        }
    }
</style>
<script >
    import TopBar from 'components/topBar';
    import Pagination  from 'components/pagination';
    import Confirm from "components/confirm"
    import Metchdialog from "components/metch_add_dialog"
    export default {
        data() {
            return {
                showBattleDialog:false,
                battleDialogTitle:'添加对战表',
                src:'',
                isShowTop: true,
                search: '',
                total: 1,
                page: 1,
                dateArr: [],
                start_date: '',
                end_date: '',
                stay_top: '',
                hasSearch: false,
                tableData: [
                    {
                        id:1,
                        red_player:1,
                        blue_player:2,
                        category:2,
                        level_min:'55',
                        level_max:'60',
                        result:1,
                    },
                    {
                        id:2,
                        red_player:2,
                        blue_player:2,
                        category:1,
                        level_min:'55',
                        level_max:'60',
                        result:3,
                    }
                ],
                players:[
                    {
                        "id": 1,
                        "name": "红方1",
                        "mobile": "19280909898"
                    },
                    {
                        "id": 2,
                        "name": "红方2",
                        "mobile": "19980909899"
                    }
                ],
                confirmData:{
                    isshow: false,
                    id    :'',
                    content:'确认删除该条资讯？'
                },
                editmetch:{
                    isshow:false,
                    race_date:'',
                    name:''
                },
                form:{
                    red_player:'',
                    blue_player:'',
                    schedule:'',
                    category:'',
                    level_min:'',
                    level_max:'',
                    result:'',
                },
                rules:{
                    red_player: [
                        { validator: (rule, value, callback) => {
                            if(value===''){
                                callback(new Error('请输入红方姓名'));
                            } else {
                                callback();
                            }
                        }, trigger: 'blur'}
                    ],
                    blue_player: [
                        { validator: (rule, value, callback) => {
                            if(value===''){
                                callback(new Error('请输入蓝方姓名'));
                            }else {
                                callback();
                            }
                        }, trigger: 'blur'}
                    ],
                    category: [
                        { validator: (rule, value, callback) => {
                            if(value===''){
                                callback(new Error('请选择项目类型'));
                            }else {
                                callback();
                            }
                        }, trigger: 'blur'}
                    ],
                    level_min: [
                        { validator: (rule, value, callback) => {
                            if(value===''){
                                callback(new Error('请输入项目级别最小值'));
                            }else if(!/^[0-9]*$/.test(value)||value>100||value==0){
                                callback(new Error('请输入1-100的正整数'));
                            }else{
                                callback();
                            }
                        }, trigger: 'blur'}
                    ],
                    level_max: [
                        { validator: (rule, value, callback) => {
                            if(value===''){
                                callback(new Error('请输入项目级别最大值'));
                            }else if(!/^[0-9]*$/.test(value)||value>100||value==0){
                                callback(new Error('请输入1-100的正整数'));
                            }else if(parseInt(value)<parseInt(this.form.level_min)||parseInt(value)==parseInt(this.form.level_min)){
                                callback(new Error('最大值要大于最小值'));
                            }else {
                                callback();
                            }
                        }, trigger: 'blur'}
                    ],
                    result: [
                        { validator: (rule, value, callback) => {
                            if(value===''){
                                callback(new Error('请选择赛事结果'));
                            }else {
                                callback();
                            }
                        }, trigger: 'blur'}
                    ],
                }
            }
        },
        components: {
            TopBar,
            Pagination,
            Confirm,
            Metchdialog
        },
        created() {
            this.form.schedule = this.$route.query.id
            this.editmetch.race_date = this.$route.query.race_date
            this.editmetch.name = this.$route.query.name
            this.getData();
            this.getUsers();
        },
        watch:{
            showBattleDialog(isshow){
                if(isshow==false){
                    this.$refs['form'].resetFields();
                    this.form={
                        red_player:'',
                        blue_player:'',
                        schedule:this.$route.query.id,
                        category:'',
                        level_min:'',
                        level_max:'',
                        result:'',
                    }
                }
            }
        },
        methods: {
            getData() {
                this.ajax('/matches?schedule='+this.form.schedule,'get',{},{page:this.page}).then((res) => {
                    if(res&&res.data){
                        this.tableData = res.data.results;
                        this.total = res.data.count;
                    }
                })
            },
            deleteData(id,index) {
                let $this = this;
                this.ajax(`/matches/${id}`,'delete').then((res) => {
                    $this.tableData.splice(index,1)
                    $this.confirmData.isshow=false;
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            this.showErrorTip(errors[key][0])
                        }
                    }
                })
            },
            saveBettle(){
                this.$refs["form"].validate((valid) => {
                    if (valid) {
                        let url = this.form.id?'/matches/'+this.form.id:'/matches'
                        let type = this.form.id?'put':'post'
                        this.ajax(`${url}`,type,this.form).then((res) => {
                            if(res&&res.data){
                                this.showBattleDialog = false
                                this.getData();
                            }
                        },(err) => {
                            if(err&&err.response){
                                let errors=err.response.data
                                for(var key in errors){
                                    this.showErrorTip(errors[key][0])
                                }
                            }
                        })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            addBattleEv() {
                this.battleDialogTitle = '添加对战表';
                this.showBattleDialog=true;
            },
            handleEdit(index, row) {
                this.battleDialogTitle = '编辑对战表';
                this.form={
                    red_player:row.red_player_id,
                    blue_player:row.blue_player_id,
                    schedule:this.form.schedule,
                    category:row.category=='自由搏击'?1:row.category=='拳击'?2:row.category=='MMA'?3:'',
                    level_min:row.level_min,
                    level_max:row.level_max,
                    result:row.result=='红方胜'?1:row.result=='蓝方胜'?2:row.result=='红方KO蓝方'?3:row.result=='蓝方KO红方'?4:'',
                    id:row.id
                };
                this.showBattleDialog=true;
            },
            editMetch(){
                this.editmetch.isshow=true
            },
            handleDelete(index, row) {
                this.confirmData.id = row.id;
                this.confirmData.index = index;
                this.confirmData.isshow=true;
            },
            cancel(val){
                this.confirmData.isshow=val;
                this.editmetch.isshow=val;
            },
            conform1(id,index){
                this.deleteData(id,index);
            },
            conform(data){
                 this.editmetch={
                    isshow:false,
                    race_date:data.race_date,
                    name:data.name
                }
            },
            changePage(page) {
                this.page = page;
                this.getData();
            },
            showErrorTip(text) {
                this.$message({
                    message: text,
                    type: 'error'
                });
            },
            getUsers(){
                this.ajax('/players').then((res) => {
                    if(res&&res.data){
                        this.players=res.data.results;
                    }
                },(err) => {
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            this.showErrorTip(errors[key][0])
                        }
                    }
                })
            }
        }
    }
</script>
