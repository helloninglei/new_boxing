<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios';
//axios.defaults.withCredentials = true;

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
  @import "../static/css/reset.css"
  @import "./assets/common.css"
</style>
