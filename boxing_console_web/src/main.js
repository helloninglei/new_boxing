import Vue        from 'vue';
import VueRouter  from 'vue-router';
import VueResoure from 'vue-resource';
import App        from './App';
import store      from './store/index'
import axios      from './common/axios'
import config     from './common/my_config'
import ElementUI  from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import routes     from './router/index.js';
// import $          from 'jquery'
import Cropper    from "cropper"
// import VueCropper from "vue-cropper"
// 富文本框所用的引入
import VueQuillEditor from 'vue-quill-editor'


// 富文本框所用的引入
    import 'quill/dist/quill.core.css'
    import 'quill/dist/quill.snow.css'
    import 'quill/dist/quill.bubble.css'

Vue.use(VueRouter);
Vue.use(VueResoure);
Vue.use(ElementUI);
Vue.use(VueQuillEditor)


let linkActiveClass = 'active';

//添加全局函数用this调用
Vue.prototype.ajax    = axios
Vue.prototype.config  = config
Vue.prototype.token   = ''

let router = new VueRouter({
  routes,
  linkActiveClass
});
// console.log(window.PYDATA);
// let userInfo = window.PYDATA.user;
// let ifSetPassword = userInfo.has_changed_password;
// let arr = [];
// userInfo.roles.forEach((item) => {
//     arr.push(item.name)
// });

// router.beforeEach ((to, from, next) => {
//     if (!ifSetPassword) {
//         next();
//     }
//     else {
//         if (to.path == '/') {
//             if (arr.indexOf('ADMIN') > -1) {
//                 next({
//                     path: '/login',
//                 })
//             }
//             else if (arr.indexOf('WATCHER') > -1) {
//                 next({
//                     path: '/viewer',
//                 })
//             }
//             else {
//                 next({
//                     path: '/login',
//                 })
//             }
//         }
//         else {
//             next();
//         }
//     }
// })

new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})


