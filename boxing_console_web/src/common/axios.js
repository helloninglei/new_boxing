import axios from 'axios'


export default function(url='',data={},params={},headers={},method='get'){
    // console.log(localStorage.token)
    let token=localStorage.token,baseURL=this.config.baseUrl;
    if(token==undefined||token==''){
        //回到首页
    }else{
        if(method=='post'){
            data.user_token=token;
        }
        if(method=='get'){
            params.user_token=token;
        }
    }
    return axios({
        url:url,
        baseURL:baseURL,
        responseType:'json',
        data:data,
        params:params,
        headers: headers,
        method:method,  
        withCredentials:false
    })
}