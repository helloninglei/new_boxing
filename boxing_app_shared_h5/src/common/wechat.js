import wx from 'weixin-js-sdk';
import config from 'common/my_config';
import $ from 'jquery';

let signature, noncestr, timestamp, encodeUrl;
let check = false;

function wxConfig(obj) {
    $.ajax({
        type : "GET",
        url : config.baseUrl  + "/second_share_signature",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success : function(msg) {
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
    });
}

export { wxConfig }