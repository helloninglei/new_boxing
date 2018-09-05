<template>
    <div id="addHotvideo">
        <TopBar v-if="isShowTop" firstTitle_name="视频管理" firstTitle_path="/hotvideo" :secondTitle_name="secondTitle_name" ></TopBar>
        <div class='container'>
            <el-row> 
                <el-col :span="12">
                    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="200px" class="demo-ruleForm">
                        <el-form-item label="视频名称" prop="name">
                            <el-input v-model="ruleForm.name"  :maxlength="40" placeholder='限制40字数'></el-input>
                        </el-form-item>
                        <el-form-item label="视频介绍" prop="description">
                            <el-input type="textarea" v-model="ruleForm.description" :rows="6" placeholder='限制140字数'></el-input>
                        </el-form-item>
                        <el-form-item label="付费金额" prop="price_int">
                            <el-input v-model="ruleForm.price_int" :span="5" placeholder="付费金额为自然数" type='number'></el-input>
                        </el-form-item>
                        <el-form-item label="完整视频" prop="tsurl">
                            <el-button class='myButton_40 btn_width_95 myBtnHover_red'  @click="addFullVideo()" v-if="!(tsurl)">添加视频</el-button>
                            <p v-if="(tsurl)">
                                <span class='video_name'>{{tsurl}} </span>
                                <span ><i class="el-icon-error" style='cursor:pointer' @click='deleteUrl(1)'></i></span>
                            </p>
                            <el-progress type="circle" :percentage="tsurlProgress" :width='70' style='position:absolute;right:-69px;top:-14px' v-show='tsurlProgress>0&&tsurlProgress<100'></el-progress>
                            <el-input v-model="ruleForm.tsurl" type='file' id='full_video' @change='getFullVideo' style='display: none'></el-input>
                        </el-form-item>
                        <el-form-item label="不完整视频" prop="try_ts_url">
                            <el-button class='myButton_40 btn_width_95 myBtnHover_red' @click="addLittleVideo()" v-if="!(try_ts_url)">添加视频</el-button>
                            <p v-if="(try_ts_url)">
                                <span class='video_name'>{{try_ts_url}}</span> 
                                <span ><i class="el-icon-error" style='cursor:pointer' @click='deleteUrl(2)'></i></span>
                            </p>
                            <el-progress type="circle" :percentage="tryTsurlProgress" :width='70' style='position:absolute;right:-69px;top:-14px' v-show='tryTsurlProgress>0&&tryTsurlProgress<100'></el-progress>
                            <el-input v-model="ruleForm.try_ts_url" type='file' id='little_video' @change='getLittleVideo' style='display: none'></el-input>
                        </el-form-item>
                        <el-form-item label="视频封面" prop="cover" class='my_avatar'>
                            <el-row>
                                <Cropper @getUrl='getUrl' :url_f='url_f' :changeUrl='changeUrl' :imgId='imgId' :width='1242' :height='663'></Cropper>
                                <div>  
                                    <div class='showImg' @click="addImg('inputId3','src_avatar')">  
                                      <img :src="src_avatar" alt="" width='100%' id='src_avatar'> 
                                      <div class='noImg' v-if="!src_avatar"> 
                                          <p>添加视频封面</p>
                                          <p>1242*663</p>
                                      </div>
                                    </div>
                                    <div style="margin-top:63px;float:left;margin-left:20px">  
                                      <input type="file" id="inputId3" style='display:none' accept="image" @change="change">  
                                      <label for="inputId1"></label>  
                                    </div>  

                                </div> 
                            </el-row>
                            <el-input v-model="ruleForm.avatar" type='hidden'></el-input>
                        </el-form-item>
                        <el-form-item label="视频标签" prop="tag">
                            <el-select v-model="ruleForm.tag" placeholder="请选择视频标签">
                                <el-option :value="item.id" :label="item.name" v-for="item in videoTags">{{item.name}}</el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="关联用户" prop='users'>
                            <ul>
                                <li class='lf'>
                                    <p style='border-radius: 50%;width:50px;height:50px;overflow: hidden;margin-left:15px;cursor: pointer' @click='showChangeUser=true'>
                                        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAABGdBTUEAALGPC/xhBQAAFKRJREFUeAHtXXtwHdV9Pmfv3ZVlkNNCWh7BTkI6yOlfyaQ10we1/CDQhCZp3FBJfgDSxdPSOpS6xZ0MZBzSUkISTNHgUFmSjWzZCi0ltM2EJGBI0pRgpilp2sGigTiyHZyQxokFtnX3ak+/71zt1dm9u7oP7b26knVn7ux57Xl8357375yfFA3+U93dF+ROq1YlRatSohXZbZVKXCSkaIG9ReIp8NTFkGIMbmNwG4PbGN75EdxHYB/BOyPpxXJE9vf/tJGLLBstc6q969KstFZL4a0GuKuQv7clnMcjIOhpJayDjvIOyuGBHyYc/4yiawhC1Iau1mzO2iSkWieUYi2o30/KEaHko07aG5T7Bkbql3B0SrNGiNr0Jxe6ubMdaFo2KqVWRGevvq5SykNoCvfa6UUH5OCD/1ff1POp1Z0QtT5zmeuJ24XyMkqI5lKFlkKOo+a8pIQ8DLD4NY9Ylvq+J1KnHNsaE15qTFz+S2M6nldeaxHWREvW9VosMbHE8+Tb8W4rSG+VQi3Hu1cooZpKpynOCGn12Za4Vw71HSsVPkn/uhGibtj8Djc78VdokjaBCCeuECAgJ4Q6pCx50BLqYNpZ9qzcs/1sXPhK3NWN2xflsqO/4Qm5WnpqtRByBQhKx8UBcLJCykHbSd0jH+59OS5cku41J0R1dbW4Z8Rd+Eq3gIhUVOaRCVQA+QwA2mtbzY/KoZ5TUeGSdlPrtyxxvTPrkPxGfChtyF8kHnCcgE+P3Sw+LgcG8rUx6cxMxheZgaTSGu/sbgfU96Gwl8TEedyyxM50Or1PDvaOxoSpi7PatHlZLpfb4HniFiT4lshEpfwhiNnatL9/ONI/AceaEKI6u9+KfqIfzcGayDxK8YqU1qfsKy7bI7dvz0aGmSVHtX2747507EalvG34mC6Pygaa1afQv3TL/f0/iPKfiVvihOQ6Mx/0lNqNkdMvFmdMjkpL3GFfsfQAiEBf0bg/EJN2XzraoTzx12jSloVzihHZSUvKm9L7+x4P+83EnhghavNm23194lPKU7eFM4TMu6gtn3Va0p+Uvb2nw/6NbEe5FmfHcneiVmzFR2aH8yotucM+P7UN5XLDftXYEyFEdWQucoX3OGbWV4YzgYI8Y9vyFrm378Ww31yyq42Zd7qu2okPqy2cb8z8n7OF9UF5oI9LNTP6zZgQ1fnHl2e97FdQrd9h5oTDVzZP6aG+e1FDMICZ+z/UEJlbn7mdzVjxcFm+7FjOe+X+z70yk5LOiJBs583vwgTvCWT0okAmpDyG0VO7PdT/zYD7PLG467t/C6OxYYweLzOLhA/vR5hQXuvs3/WC6V6J2aoksBnW3ZC5SqiJr4XJQPV90rEXvWu+kkEMWDaWkWU1MdFYABONjelRgbkqQlgz1IT3r+gzlphp4QsZtluXvX+21oHMvNTazDLqsqLMZlrEhNjo1sP0KNNccZPFPsNV2X8vrhlWj71/163zpb8oEz+0Wkq6nTf/HeYtW8x32HzZ0vnNSvuUimoIR1PswMNkCMv6hHOg76PnGhkkgGVm2YmBSQgx0lgBM9O9lLnsGqLnGWO5b4SHthhJPeDsH7i1VELngn+2I/NAcU3BkLglfVW585Sya4g7lru3iAz2GUP9f3YugF1OGSeb7HCfciUnzOW8zzBlEcLlEJARAJ4jDLt16Q3nYjMVBy6xyGMSGn1h9YIYxr1nupdssvRCoRL/iTZxam0K8ww97JulXTWzAI1o5m5o1j37gjlPAVknbSneXWpBsmQN0au2BhmcgXPSdy4Mbaslm9hojPRmWz4WftDEslSc0xLC/YzwErperZ2nM/BSYFXiz8kjsTLfIZZ6j8h0DJljmyzu9GXPUCJjanNJLxQe6Fs9V/uN/Ip0bj3WotZhvPoeqdSF2HD6GTD5LwxgH7MvXrJb7thxJoRR1VbUCul2ZA4GFiSlfNVpVq1xO4+xNSS/7WqQgSV0vWo7RxcKs53dK7KnJl4EGbuB8HX80LDi6WCw8sv4rwV4D2ZPnPoeALy6agZCL+pOnivdwK7ghXQ1tgWHoCGSEAokYLcsMPMEy5+dq0vouY6udcITXw+vSAehgE2pSzGP+NJ4Z9f6Ir8qHYgZsQu8TvkCYhzxiySE0iH4egyBBDnKzaWI9xveaXx95g89JYcBSknxHxaG5Zae7M+2d787qcLlsZOjfnxMQ0vg+A7Gs4gQyk3hS9lkhMGKsrhjru30Mf/sQOWENwQyYkV9zHL6Zk2eVJ/x7TN9ErtwB0+MNdahyIsIoRAb29ZCOAgkcA+8YJ9DBrTdR9BZv15NltGvrI5rVqqJT2MILP13iTGx9u3+M0AIJzSUKPQ9+aR0SKMLJJj5Nc3OUN+3RMq6GsScNN3LNbuut6bcsKXCEUNiGQhH6U1ibvwChFDWFsyZ4p3HKapjhJ9zRmdo1/MilVqLIXvFxxAw8oqWz6oShUksj/uvE2st3+w74BkgRHjBvoNCbI0mN2XkvcioNnT/SpEjHJx9vd8W6TTnTz+J8o9zs4RMVGaMWBLTQHoQNjftBUJ4JACM/brviRmjokShb2/0J+YZt7o58WLckNXZ9/ffQde+CouiPy63LJ5UicvzailNPZjL5wK1cAWx9/NUIESfz/Bd+YSs7WyLd5rZmc6MydxWyIPdz9GUVHIw29F9Q1T4pr39/22nrTb4nYjyN924Zuc0C0jTJPvTmGo55ql4TewLhOjDMlNhQIgaNK2NanY7u7d5yisMUfHFsUwD2c5Md1SeOVFz0qINH9z0J6ek6K/d8Te5N5A3HlSa/GlCeIwM4+JCteHXYcvz/skP1KhPt737Ds9T94Tzp0nxvF3Z9q4/CvvRzpNSTkqsBCnHovwRYtRetPjOaL+Zu2oJf2MlmNhrDhC1JoRn+oLJqEP1OhIQTLd823hH9yc8oWJXD9AfcuF0J/qWP42KVe7r/54jnZUE3/TXozEpf0/u7nnNdE/SnMdWHTLj9DnQhPCApenJwzKmvdHM4+2Zv8FX9fFS+SIp6Ft6sNcd2O3036NEiLPIBiniCN30KAyjsaYDfVj9re0vjLHPgSYEp2UChPDkUm2zU33s4x2Ze4XwPlZJDFgw3IG+5i+i3pF7HjriNC/6HZDxLEdhHI1FhUvaLYwxVgZWMQ3Jc+DZN1ThgCOq7Li9aOkvJHWMLMmCoPm5L0q6vtw0cHzgY/aB/r8tN3wtw/F4nXv26M/MRU/nPHmhxUP5gYR5yD6hM32BeGdoweprz3RkoMP4jkyn34NvLHbugHMrd7udmZp11pUUUWPMQ6zGj1xYvCHBcOPycyCQ6TcbZoyYJIawn8OXFNk5M08g49v2eXI1Z+SOgz5Biv+Ny6vneXeNt3fdFedfT/cw1uTCQtsVIASFaRhCSAa+6F7leZHDV4IHMp63raa1/pxBDj503EmlV5ZYJrkzrk+pJyFhrMkFO/UgITgHXtdMxSSGI2UWZuADICUTEwTlkd+yl6SvxmgpsJqLw5ub8d6b494Djd9PC/EP8f518inGutVCoS42k+ehfNM+G2b1yCMpd+TYIJqpG+PSR76/aS9W78Xmz8/NMNiU+qQnxHbTLWjGwZrmppWl5KOC79TGFsaaXKCGqPPN5HhDgmmvt1kftnzsy/swVI3d10Zz9HX7gqZrw5Ib4+3d92DFOiB6E8g/+hb2MXL3zqMB91myFGOtzmcf0mLmR19XYTrU0UwxnezI6AE0N+1xyYKMp+2W1O/KnTsDO4HZji6sZ6ltce+hfTus+xb0MbFh6uwRxppcYGgeJETfHVLnjDE5ng/Pjk08gmHeH8QlDzK+Ctmp94f397OdXTifIbZO897/OMJqk/t6X40LMyvuvKfF+JELTBhDhPgXuRgBa21UW7Y0ZQ+PPorlkA/FpiXlE3bT0g+YgmwchWGp/UHIWn007j0U8rtYKFyVxAnZuDSqdg9jzRpSdWQJvcgZa/Ynp7+A6K6LjVLKLzpvXvwhc8JKMtyO7ofw5FUYkT/UqBdsu3lVLRcKIxOegSN2KXEdnvnjFUd1+qnbbmt2x4/+M2rGtfFJysed1qUflj09434YPSTuzPRhYrXZdws/QcZ/2IvFmoYWCg9jDS7YqQcJwX1T4cLVwq5BPXHqi/jC40U3JW56W5L6iLmvr98bGd2N97ri8gUyDtlNLYXJYly4WXcPYU0u2KkHCOHlX/XIKO4R+TWAqlc4o9JDvh5BzWhHB+76/np+cvjoXmR8k+8WfoKMZ21r8dVyz/0Uom7oXxhrcpFGpx4ghDex1aMUmARdg4lfZFLw22///jWb5PXXT/gBUDPS7mNPQApRXO+7hZ8o0L/Zzep9cqAnUKZwuEax61vvzMywhkxepVpw1tfiFWy1M2Dl9pqo2PGFD9vLl24MkMH5yeGjn0fNmI6Mr9npC4omi1FpNIpbGGtywVFWcO2KdxTW+IcJ4JuQxJVRySgrdTf6DKx+5H+oGQ6OEWDdSX3Ydws/UTMO4qTr++Tez7wR9mtoezHWI+xDgoSEV39rUKKJ1701aK6wvhf6QRKkaaj3u76rnp+MHIWwhZrmwKT8in3xm64LTxb9OBr6GcKaXECOSYyYLTmWs2teQ7AnEd1cqbwcFIfDuR///Cr3tdMQRo65lS6P9JecRRgS70jmksx6k8ebUgPYgwuL128HMgLWOFkLuCVsUVJGEqKkugRrUk+5r5466U2IL6MWrYlNWsp/cZYvC0wWY8M2oIfGGNfWmlkjF5be2JHyB74HQGjiVaq+PemnFptU6q2R8SpxDTru1cxDpL/vKOUXnJbUOnN+4nvNlScxDpXzCLnQSyeoOgEpE95rW6uCuTkrsnaUnZ4U/4j5yUfM+UnZ7zZQwDDG6D+eZvY0IbyY3sxr/pJh0yU5M5qlqgnhkNhpXdaBmpFLLkezE1MYY58DTYhjpzU7U1nDjc+4ZHjKnoyJoyYMItoqjQ0TxRwGG/2YLG6YD2TksZUrTByoqYF2TQgFAyC2V+jc0balXfVG7LjfjKgSc+6np38bcS8u7x35Is7lPZCS8gPYqr3AGR7ImJPF8uJozFC8TZsYF3IH7H21GVOOUNmAIeaURKCSm/DCnsJLCRgwM0VzZQ70ApGeQJP0JFyetJX6qhzun146PfDqXLPganPzp7HPO6AlyP/yOjzEYd8OD2U76bdVekYEMk/H/DjCT3RcF2IUVTSkBhEeaDqBZfhYtsJxVWeXp5qG+3816t3p8m2GbxoeuMy0V2rmleZuNncEBS1gj+MRy33dJYUaQgeI7z+PgPoUFV/gXehI8O4KE409lxcHN3hg03lphelUHBwIBAQ6QhHE5jsUbkZWYmqSgY/xECTxC92F7kMKKVhysGCGgRfTcy3JdFswV48AsZy87H8qEiiQmbKEDn1qzTICykymfm/hxfRT1gXTTBCYxLJQE1FjzxBzM85ADdHbndAsYwaAfNQ27kWYbgvmyhEghsQy8CawDm8xBwhhYHuR82kwly28CJUN1BJQsC8YqkJAY2iovyDGVKkUjgzuxT+I1uxCR5uZ8sHlM0tS75yTS9xThZg1E/Z/FvNqKAxcl/mZQGfe5xzov9m3+8+iGkIPrXOJan4KP7WMKhsK1gVDRQjksTPIALbEOCqSSEK0AizoXDJfwPLFVqpsMN0WzKURIGbELhAS2MYpGYskhC9TARaWU171I0ITZmv9GRBQ890WntMjAMzkJGZ2ISR2RTW2BYegIZYQLVkuxZ+bwbH+0kb9GabbgjkeAa1rBJgFQkCpWFhq3/Qv+bXjbN+TIKKwc6dXXlOibT6rozABqtZMHSNqQjxjLiICu6ec4f6108UZW0P8l7Q2MuO+KSZAZSbhe5788AtPjKVwB5bGyFjRxajqJLEshU9JQnjSCKIpNwUigmYZ1z0zvLCsEkBFW4gJscFCaWARkhiWc2qrJCFMharhqI3MTB4LhWvdkaMPs+My3c9ls+7ENSYi0CwRu3LV65VFCEHWquGkeM4EHBlopzIT0+1cNucVuwRPf2HL4TliVy4uZRNCoQKqhsOq/Mtm5Fif2TLemdluup2LZmJALIJlly9rdXqGwHjQv9hWcXOzoPIoCKJuphJUeVQxIcxOXl0eNbRFKQWDTpEG028bhDA5m+7A8/1o4JAqmqlTQqZWVqM+rypCWCSqhovW1IY9cbt53quz4NDWzZ79vDlHIy4kQ6as6+x9fd+gvdJf1YQwoQXFksGhLeYas6dYkoSwSlI1XLij5xics1TehzifhsX5/gJlQtnC8wxiQCyqaaaIpf+bUQ3xI1lQTtxAyokLpFB9d16TW9F1eqjK81d9txT347DQ7UnJGidSQ3xS+FxQcG+iUbk5cUKYBa3ZDQqwwiOQQvagJYAX0/Mu9EYbIuuhLCRttECCsQdeyDsMXLXVi65Y5zPdkzDXhBA/Y1oBlhL3oQO8xHcLPY/zLnR9/fZg72jIr65WShRSiG1SbqogqhPIBDfssEfUtL9/OOCeoKWmhDCfVC6W12cFNT8BrT1TpUAmcDGqfIa3afMC53rdGUwpdC1UTjlmpdpMicKp3LFGQL4A267c6Ztuc8l8p1pzzQnxM0blKFrNDzXLmApj/ACTT26AgZ9DvNeWV6mmnWXPmnechIJXZOUxMp5c4mGZ/PkMHLsw9izCkQGcLD6UQS308XBvYA0vHDYpe90I8TOsbrplqXs2+5dUHANiTF0lfpDAEwSN4+vkwdQRPgWuxeNNbLz8S983xSuO/Ft1eHcIrqvgDQn6UL4n345a14r614qC6icIaAokEGFB2DPQ89RHuSk51HcsIkjNnOpOiF8SvfQABTLUWQKwC2oyfP/ZeAKM5wXkm7VI7SyplZ01QkzAVcfm5VnlbcTXvA5teavpV3MzDyrhfIaT9gb9IwE1T3OaBBqCEDN/1BLAi+l5F7q+Aj3uxK75UiVmnDjmIVee6eMxMv/kUiVR1DJswxESLiyvQueNz9gobsVyP2sP+gPepKrOh70Fq6st6CPyNxjhNh24jcENl8/I19FfnED4EdhHeEECz4H79/uG02kU+/8DEJC7SrcsPJwAAAAASUVORK5CYII=" alt="" width="100%">
                                    </p>
                                    <p style='text-align: center'>编辑关联用户</p>
                                </li>
                                <li class='lf' v-for="item in userImgIds" style='width:80px'>
                                    <p style='border-radius: 50%;overflow: hidden;width:50px;height:50px;margin-left:15px'>
                                        <img :src="config.baseUrl+item.avatar" alt="" width="100%">
                                        <!-- <img src="/static/img/edit_user_img.png" alt="" width="100%"> -->
                                    </p>
                                    <p style='text-align: center'>{{item.nick_name}}</p>
                                </li>
                            </ul>
                        </el-form-item>
                        <el-form-item label="是否同步热门视频" prop="push_to_hotvideo">
                            <el-radio-group v-model="ruleForm.push_to_hotvideo">
                                <el-radio :label="true" >是</el-radio>
                                <el-radio :label="false">否</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="是否置顶" prop="stay_top" v-if='ruleForm.push_to_hotvideo'>
                            <el-radio-group v-model="ruleForm.stay_top">
                                <el-radio :label="true" >是</el-radio>
                                <el-radio :label="false">否</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-checkbox-group v-model="ruleForm.push_hot_video" style='margin-bottom:22px;width:200px;text-align: right;' v-if='ruleForm.push_to_hotvideo'>
                          <el-checkbox label="创建推送" name="push_hot_video"></el-checkbox>
                        </el-checkbox-group>
                        <el-form-item label="发送时间" :class="isRequired" style='margin-left:32px' id='addTime' v-if='ruleForm.push_to_hotvideo'>
                            <el-date-picker
                                    class="margin_rt25"
                                    v-model="dateArr"
                                    type="datetimerange"
                                    range-separator="至"
                                    start-placeholder="起始日期"
                                    end-placeholder="结束日期"
                                    @change="getDateTime"
                                    :default-value='new Date()'
                                    value-format="yyyy-MM-dd HH:mm:ss">
                            </el-date-picker>
                        </el-form-item>
                        <el-form-item style='margin-left:30px;margin-top:-30px'>
                            <el-form-item prop="end_time" >
                                <el-input v-model="ruleForm.end_time" style='display: none'></el-input>
                            </el-form-item>
                        </el-form-item>
                        <el-form-item>
                            <!-- <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button> -->
                             <el-button type="danger" class='myColor_red myButton_40 btn_width_95' @click="submitForm('ruleForm')">{{btn_name}}</el-button>
                             <el-button class='myButton_40 btn_width_95 myBtnHover_red' @click="resetForm('ruleForm')">取消</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>
        </div>
        <el-dialog  :visible.sync="showChangeUser" class='myDialog' title="编辑关联用户">
          <!-- <div class="dialog_title">编辑关联用户</div> -->
          <div class="dialog_content myUser" >
            <template>
              <el-transfer 
                filterable
                :filter-method="filterMethod"
                filter-placeholder="请输入用户名称"
                :titles="['待选择', '已选择']"
                :props="{
                  key: 'id',
                  label: 'nick_name',

                }"
                v-model="ruleForm.users" 
                :data="userIds"></el-transfer>
            </template>
          </div>
          <div slot="footer" class="dialog-footer" style='text-align:center'>
            <el-button type="danger" class='myColor_red myButton_40 btn_width_95 margin_rt25 border_raduis_100' @click="confirm()">确定</el-button>
            <el-button  class='myButton_40 btn_width_95 border_raduis_100' @click="close()">取消</el-button>
          </div>
        </el-dialog>

    </div>
</template>

<style>
    #addHotvideo .el-checkbox__label,#addHotvideo .el-radio__label,#addHotvideo .el-form-item__label,#addHotvideo .el-checkbox__input.is-checked+.el-checkbox__label{
        font-family: PingFangSC-Regular;
        font-size: 16px;
        color: #000000!important;
    }
    #addHotvideo .el-form-item{margin-bottom:30px;}
    #addHotvideo .button{height:37px;width:45px;border:none;border-right:1px solid #ccc;margin-top:2px;margin-left:2px!important;font-size:20px;padding-top:8px;padding-left:12px;}
    #addHotvideo .myAddress input{padding-left:50px;}
    .el-checkbox__inner:hover,.el-checkbox__input.is-focus .el-checkbox__inner,.el-input__inner:focus,.el-select .el-input__inner:focus,.el-select .el-input.is-focus .el-input__inner{
        border-color:#F95862!important;
    }
    .el-checkbox__input.is-checked+.el-checkbox__label,.el-select-dropdown__item.selected{
        color:#F95862!important;
    }
    .el-transfer-panel__item.el-checkbox {
        color: #606266;
    }
</style>
<style scope>
    .myDialog .el-dialog{position:fixed;left:50%;margin-left:-302px;width:604px;}
    .myUser .el-checkbox:first-child{margin-left:0px!important;}
    .myDialog .el-dialog__body{padding-top:10px;}
    .image{height:140px;width:140px;border:1px solid #ccc;vertical-align: middle}
    .image img{height:100%;}
    .myUser .el-button--primary{
        background:#F95862!important;
        border-color:#F95862!important;
    }
    .video_name{
        width:90%;
        display: inline-block;
        vertical-align: middle;
        margin-right:20px;
        white-space:nowrap;
        overflow:auto;
        /*text-overflow:ellipse;*/
    }
    .showImg{
        width:207px;
        height:111px;
        overflow: hidden;
        position: relative;
        float: left;
        /* border-radius: 50%; */
        border: 1px solid #d5d5d5;
    }
    .noImg{
        text-align: center;
        font-size: 14px;
        line-height: 25px;
        margin:15px auto;
    }
    .my_avatar .el-form-item__content{
        line-height: 0
    }
</style>
<script>
    import TopBar from 'components/topBar';
    import $      from 'jquery' 
    import Cropper from 'components/cropper';
    export default {
        data() {
            var validateUrl = (rule, value, callback) => {
                // console.log(this.tsurl,value)
              if ((!this.tsurl )&&(!value)) {
                callback(new Error('选择完整视频'));
              } else {
                
                callback();
              }
            };
            var validateTryUrl = (rule, value, callback) => {
              if ((!this.try_ts_url) &&(!value)) {
                callback(new Error('选择不完整视频'));
              } else {
                
                callback();
              }
            };
            return {
                isShowTop   : true,
                tsurl       : '',
                try_ts_url  : '',
                secondTitle_name:'添加视频',
                id          :'',
                btn_name    : '发布',
                userIds     : [],
                userHash    : [],
                userImgIds  : [
                    
                ],
                videoTags   :[],
                dateArr:[],
                isRequired:'',
                tryTsurlProgress:0,
                tsurlProgress:0,
                showChangeUser:false,
                ruleForm: {
                    users   : [],
                    name    : '',
                    description: '',
                    price_int  : 0,
                    price   : '',
                    tsurl   :'',
                    try_ts_url: '',
                    push_to_hotvideo:false,
                    stay_top:false,
                    push_hot_video:false,
                    start_time:'',
                    end_time:'',
                    tag:''
                },
                rules:{
                    users:[
                        { required:true,message:'请选择用户id', trigger:'blur' }
                    ],
                    cover:[
                        { required:true,message:'请添加视频封面', trigger:'blur' }
                    ],
                    name:[
                        { required:true,message:'请输入视频名称', trigger:'blur' }
                    ],
                    tag:[
                        { required:true,message:'请选择视频标签', trigger:'blur' }
                    ],
                    description:[
                        { validator: (rule, value, callback) => {
                                if(!value){
                                    callback(new Error('请输入视频介绍'));
                                }else if (value&&value.length>140) {
                                    callback(new Error('限制140字数'));
                                } else {
                                
                                    callback();
                                }
                        }, trigger: 'blur' ,required:true}
                    ],
                    price_int:[
                        { validator: (rule, value, callback) => {
                              if (!/^[0-9]*$/.test(value)) {
                                callback(new Error('付费金额为自然整数'));
                              } else {
                                
                                callback();
                              }
                        }, trigger: 'blur',required:true }
                    ],
                    push_to_hotvideo:[
                        { trigger: 'blur',required:true }
                    ],
                    stay_top:[
                        { trigger: 'blur',required:true }
                    ],
                    tsurl:[
                        { validator: validateUrl, trigger: 'blur',required:true }
                    ],
                    try_ts_url:[
                        { validator: validateTryUrl, trigger: 'blur',required:true }
                    ],
                    end_time: [
                        { validator: (rule, value, callback) => {
                            console.log(this.ruleForm.push_hot_video)
                            if(this.ruleForm.push_hot_video){
                               if(this.ruleForm.start_time===''){
                                callback(new Error('请选择发送的开始时间'));
                                }else if (value==='') {
                                    callback(new Error('请选择发送的结束时间'));
                                }else if(new Date(this.ruleForm.start_time)-new Date()<0){
                                    callback(new Error('开始发送时间不能小于当前时间'));
                                }else if(new Date(value)-new Date(this.ruleForm.start_time)<0){
                                    callback(new Error('结束时间不能早于开始时间'));
                                }else if(new Date(value)-new Date(this.ruleForm.start_time)> 60*60*24*14*1000){
                                    callback(new Error('推送有效时间不能超过14天'));
                                } else {
                                    callback();
                                } 
                            }else{
                               callback(); 
                            }
                            
                        }, trigger: 'blur', required: true}
                    ],
                },
                inputId:'',
                url_f:'',
                changeUrl:false,
                imgId :'',
                src_avatar:'',
            }
        },
        components: {
            TopBar,
            Cropper
        },
        created() {
            let query     = this.$route.query
            this.id = query.id
            if(this.id){
                this.secondTitle_name = '修改视频'
                this.btn_name = '修改'
                this.getData(this.id)
                let tsurl = query.url
                this.tsurl=query.url
                let try_ts_url = query.try_url
                this.try_ts_url= query.try_url
                this.ruleForm.tag = query.tag.id
                this.ruleForm.push_hot_video = query.push_hot_video
                $('#full_video').val(tsurl) 
                $('#little_video').val(try_ts_url) 
                this.dateArr=[query.start_time?query.start_time:'',query.end_time?query.end_time:'']
                console.log(query)
                console.log(this.dateArr)
            }else{
                // 2018-06-12 08:06:08
                let startDate = new Date();
                let endDate   = new Date();
                startDate.setMinutes(startDate.getMinutes()+5);
                endDate.setDate(endDate.getDate()+1);
                this.dateArr=[startDate.Format("yyyy-MM-dd hh:mm:ss"),endDate.Format("yyyy-MM-dd hh:mm:ss")]
            }
            this.getDateTime();
            this.getUserIds();
            this.getVideoTags();
            
        },
        watch:{
            "ruleForm.push_hot_video":function(val){
                this.isRequired = val?'is-required':''
            }
        },
        methods: {
            getFullVideo(){
                var _this=this
                var file=event.target.files;
                var $this=this
                this.upload(file[0],function(url){
                    $this.tsurl = url
                },2);
            },
            getUserIds(){
                let $this = this;
                this.ajax('/hot_videos/users','get').then(function(res){
                    if(res&&res.data){
                        res.data.forEach((val, index) => {
                          $this.userHash[val.id]=val
                        });
                        $this.userIds = res.data
                    }

                },function(err){
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            $this.$message({
                                message: errors[key][0],
                                type: 'error'
                            });
                        } 
                    } 
                })
            },
            getData(id){
                let $this = this;
                this.ajax('/hot_videos/'+id,'get').then(function(res){
                    if(res&&res.data){
                        $this.ruleForm.name    = res.data.name;
                        $this.ruleForm.price_int   = parseInt(res.data.price);
                        $this.ruleForm.description = res.data.description;
                        $this.ruleForm.cover = res.data.cover;
                        $this.ruleForm.stay_top = res.data.stay_top
                        $this.userImgIds = res.data.user_list;
                        for(var i=0;i<$this.userImgIds.length;i++){
                            $this.ruleForm.users.push($this.userImgIds[i].id)
                            if($this.userImgIds[i].id==10){
                               $this.ruleForm.push_to_hotvideo = true;
                            }
                        }
                        $this.src_avatar = $this.config.baseUrl + res.data.cover;

                    }

                },function(err){
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            $this.$message({
                                message: errors[key][0],
                                type: 'error'
                            });
                        } 
                    } 
                })
            },
            getVideoTags(){
                let $this = this;
                this.ajax('/hot_videos_tags','get').then(function(res){
                    if(res&&res.data){
                        $this.videoTags = res.data.result;
                    }

                },function(err){
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            $this.$message({
                                message: errors[key][0],
                                type: 'error'
                            });
                        } 
                    } 
                })
            },
            filterMethod(query, item){
                return item.nick_name.indexOf(query) > -1;

            },
            getLittleVideo(){
                var _this=this
                var file=event.target.files;
                var $this=this
                this.upload(file[0],function(url){
                    $this.try_ts_url = url
                },1);
            },
            upload(file,fun,type){
                // console.log(file)
                let formData = new FormData() 
                let $this = this;
                formData.append('file', file) 
                this.ajax('/upload','post',formData,{},{},function(val){
                    if(type==1){
                        $this.tryTsurlProgress = parseFloat(val)
                    }
                    if(type==2){
                        $this.tsurlProgress = parseFloat(val)
                    }
                    
                }).then(function(res){
                    if(res&&res.data){
                        fun(res.data.urls[res.data.urls.length-1])
                    }

                },function(err){
                    if(err&&err.response){
                        let errors=err.response.data
                        for(var key in errors){
                            $this.$message({
                                message: errors[key][0],
                                type: 'error'
                            });
                        } 
                    } 
                })
            },
            close(){
                this.showChangeUser = false;
            },
            confirm(){
                this.showChangeUser = false;
                // console.log(this.ruleForm.users)
                let userImgIds = []
                for(var i=0;i<this.ruleForm.users.length;i++){
                    userImgIds.push(this.userHash[this.ruleForm.users[i]])
                }
                this.userImgIds = userImgIds
            },
            submitForm(formName) {
                let $this = this
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let sendData = this.ruleForm;
                        sendData.try_url = this.try_ts_url;
                        sendData.url = this.tsurl;
                        sendData.price = parseInt(sendData.price_int)*100
                        console.log(sendData)
                        let $this = this
                        if(this.id){
                            //编辑
                            this.ajax('/hot_videos/'+this.id,'put',sendData).then(function(res){
                                if(res&&res.data){
                                    $this.resetForm(formName)
                                }

                            },function(err){
                                if(err&&err.response){
                                    let errors=err.response.data
                                    for(var key in errors){
                                        $this.$message({
                                            message: errors[key][0],
                                            type: 'error'
                                        });
                                    } 
                                } 
                            })
                        }else{
                            //新建
                            this.ajax('/hot_videos','post',sendData).then(function(res){
                                if(res&&res.data){
                                    $this.resetForm(formName)
                                }

                            },function(err){
                                if(err&&err.response){
                                    let errors=err.response.data
                                    for(var key in errors){
                                        $this.$message({
                                            message: errors[key][0],
                                            type: 'error'
                                        });
                                    } 
                                } 
                            })
                        }
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$router.push({path: '/hotvideo'});
                this.$refs[formName].resetFields();
            },
            addFullVideo(){
                $('#full_video').click();
            },
            addLittleVideo(){
                $('#little_video').click();
            },
            deleteUrl(type){
                if(type==1){
                    this.tsurl=''
                    this.ruleForm.tsurl=''
                }else{
                    this.try_ts_url=''
                    this.ruleForm.try_ts_url=''
                }
                
            },
            deleteTryUrl(){
                this.try_ts_url=''
                this.ruleForm.try_ts_url=''
            },
            //宣传图
            getUrl(url,imgId){
                this.changeUrl=false
                this.src_avatar = this.config.baseUrl+url
                this.ruleForm.cover = url
            },
            addImg(ele,imgId){
                this.imgId=imgId;
                $("#"+ele).click();
            },
            change(e){
                let files = e.target.files || e.dataTransfer.files;  
                if (!files.length) return;  
                let picValue = files[0];  
                this.url_f = this.getObjectURL(picValue); 
                this.changeUrl=true
            },
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
            getDateTime() {
                this.ruleForm.start_time = this.dateArr?this.dateArr[0]:'';
                this.ruleForm.end_time = this.dateArr?this.dateArr[1]:'';
            },
        },
    }
</script>
