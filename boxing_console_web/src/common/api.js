import axios from 'axios'
axios.interceptors.request.use(config => {

return config

}, error => {

return Promise.reject(error)

})



// http response拦截器

axios.interceptors.response.use(

response => {

// console.log(response)//正确响应

return response

},

error => {

if(error.request){

console.log(error.request.response)
let errors=error.request.response
 for(var key in errors){
 	console.log(errors[key])
 	return
 }

} else if(error.response){

console.log(error.response.data);

console.log(error.response.status);

console.log(error.response.headers);

}



if (error && error.response) {

switch (error.response.status) {

case 400: error.message = '请求错误(400)' ; break;

case 401: error.message = '未授权，请重新登录(401)'; break;

case 403: error.message = '拒绝访问(403)'; break;

case 404: error.message = '请求出错(404)'; break;

case 408: error.message = '请求超时(408)'; break;

case 500: error.message = '服务器错误(500)'; break;

case 501: error.message = '服务未实现(501)'; break;

case 502: error.message = '网络错误(502)'; break;

case 503: error.message = '服务不可用(503)'; break;

case 504: error.message = '网络超时(504)'; break;

case 505: error.message = 'HTTP版本不受支持(505)'; break;

default: error.message = `连接出错(${error.response.status})!`;

}

}else{

error.message = '连接服务器失败!'

}

return Promise.reject(error)

}

)

