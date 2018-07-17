
import axios from 'axios'
//回调参数的捕获
let $this = this;
axios.interceptors.response.use(function (response) {
    return response;
  }, function (error) {
    if(error.response.status==401){
        localStorage.token='';
        $this.$router.push({path:'/login'});
    }
    return Promise.reject(error);
  });
export default function(url='',method='get',data={},params={},headers={},successfun){
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
        onUploadProgress(progressEvent){
            if (progressEvent.lengthComputable) {
              let val = (progressEvent.loaded / progressEvent.total * 100).toFixed(0);
              if(successfun){
                successfun(val)
              }
              
            }
        },
        headers: headers,
        method:method,
        withCredentials:false
    })
}