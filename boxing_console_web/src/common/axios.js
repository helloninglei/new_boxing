import axios from 'axios'


export default function(url='',method='get',data={},params={},headers={}){
    // console.log(localStorage.token)
    let token=localStorage.token,baseURL=this.config.baseUrl;
    // console.log(token)
    if(token==undefined||token==''){
        this.$router.push({path:'/login'});
        //回到首页
    }else{
        headers['Authorization'] = 'Token '+token;
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