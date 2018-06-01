import Vue        from 'vue';
import VueRouter  from 'vue-router';
import VueResoure from 'vue-resource';
import App        from './App';
import axios      from './common/axios'
import config     from './common/my_config'
import routes     from './router/index.js';
import VueQuillEditor from 'vue-quill-editor'
import layer from 'vue-layer'
Vue.prototype.$layer = layer(Vue);

// require styles
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

Vue.use(VueQuillEditor);
Vue.use(VueRouter);
Vue.use(VueResoure);

let linkActiveClass = 'active';

//添加全局函数用this调用
Vue.prototype.ajax    = axios
Vue.prototype.config  = config
Vue.prototype.token   = ''

let router = new VueRouter({
  routes,
  mode:"history",
  linkActiveClass
});

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})


