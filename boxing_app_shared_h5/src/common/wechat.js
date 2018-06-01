import wx from 'weixin-js-sdk';
import {config} from 'my_config';

let signature, noncestr, timestamp, encodeUrl;
let check = false;

function wxConfig(obj) {
    this.ajax(`/token/jsSignature`,'post').then((res) => {
        if (res && res.data) {
            signature = msg.signature;
            noncestr = msg.noncestr;
            timestamp = msg.timestamp;
            //微信JS-SDK权限验证
            wx.config({
                debug : false,
                appId : appid,
                timestamp : timestamp,
                nonceStr : noncestr,
                signature : signature,
                jsApiList : ['onMenuShareTimeline','onMenuShareAppMessage','onMenuShareQQ','onMenuShareWeibo','onMenuShareQZone','startRecord','stopRecord','onVoiceRecordEnd','playVoice','pauseVoice','stopVoice','onVoicePlayEnd','uploadVoice','downloadVoice','chooseImage','previewImage','uploadImage','downloadImage','translateVoice','getNetworkType','openLocation','getLocation','hideOptionMenu','showOptionMenu','hideMenuItems','showMenuItems','hideAllNonBaseMenuItem','showAllNonBaseMenuItem','closeWindow','scanQRCode','chooseWXPay','openProductSpecificView','addCard','chooseCard','openCard']
            });
            check=true;
            if(!(obj==undefined)){
                obj();
            }
        }
    },(err) => {
        if(err&&err.response){
            let errors=err.response.data;
            for(var key in errors){
                this.$layer.msg(errors[key][0]);
            }
        }
    })
}

export { wxConfig }