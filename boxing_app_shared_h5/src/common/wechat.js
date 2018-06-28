import wx from 'weixin-js-sdk';
import config from 'common/my_config';
// import axios from 'axios'
import $ from 'jquery';

let signature, noncestr, timestamp, appId, debug;
let check = false;
let url = window.location.href;

function wxConfig(obj) {
    // axios.get(config.baseUrl  + "/second_share_signature?url=" + encodeURIComponent(url))
    //     .then(function (msg) {
    //         debug = msg.debug;
    //         appId = msg.app_id
    //         signature = msg.signature;
    //         noncestr = msg.nonceStr;
    //         timestamp = msg.timestamp;
    //         //微信JS-SDK权限验证
    //         wx.config({
    //             debug : debug,
    //             appId : appId,
    //             timestamp : timestamp,
    //             nonceStr : noncestr,
    //             signature : signature,
    //             jsApiList : ['onMenuShareTimeline','onMenuShareAppMessage','onMenuShareQQ','onMenuShareWeibo','onMenuShareQZone','startRecord','stopRecord','onVoiceRecordEnd','playVoice','pauseVoice','stopVoice','onVoicePlayEnd','uploadVoice','downloadVoice','chooseImage','previewImage','uploadImage','downloadImage','translateVoice','getNetworkType','openLocation','getLocation','hideOptionMenu','showOptionMenu','hideMenuItems','showMenuItems','hideAllNonBaseMenuItem','showAllNonBaseMenuItem','closeWindow','scanQRCode','chooseWXPay','openProductSpecificView','addCard','chooseCard','openCard']
    //         });
    //         check=true;
    //         if(!(obj==undefined)){
    //             obj();
    //         }
    //     })
    //     .catch(function (error) {
    //         console.log(error);
    //     });

    $.ajax({
        type : "GET",
        url : config.baseUrl  + "/second_share_signature?url=" + encodeURIComponent(url),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success : function(msg) {
            debug = msg.debug;
            appId = msg.app_id
            signature = msg.signature;
            noncestr = msg.nonceStr;
            timestamp = msg.timestamp;
            //微信JS-SDK权限验证
            wx.config({
                debug : debug,
                appId : appId,
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