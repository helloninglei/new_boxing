import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex)

// const getAdminInfo = () =>  axios.get(`${site}/roles`);

const state = {
    // userInfo: window.PYDATA.user,
}

const mutations={
    setUserInfo(state,a){
        state.userInfo = a;
    }
}

const actions ={
    setInfoAction(context,a){
        context.commit('setUserInfo',a)
    }
}

export default new Vuex.Store({
    state,
    actions,
    mutations,
})

