<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script type="text/ecmascript-6">
import axios from 'axios';
// import router from './router';
axios.defaults.withCredentials = true;
  export default {
    data() {
      return {}
    },
    methods: {

    },
    created() {
       
    }
  };
</script>

<style lang="stylus" type="text/stylus">
  @import "./assets/public.styl"
  @import "./assets/common.css"
</style>
