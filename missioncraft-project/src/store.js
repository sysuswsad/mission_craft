import Vue from 'vue'
import Vuex from 'vuex'
import $backend from 'backend'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userInfo: {
      username: '',
      sid: '',
      email: '',
      avatar: '',
      school: '',
      grade: -1,    // 0: male, 1: female
      gender: '',
      qq: '',
      wechat: '',
      mission_pub_num: -1,
      mission_fin_num: -1
    },
    message: []
  },

  mutations: {
    login (state, info) {
      Vue.set(state, userInfo, { ...info })
    },

    updateMessage (state, newMsg) {
      Vue.set(state, message, [...newMsg])
    },

    logout (state) {
      state.userInfo.username = ''
      state.userInfo.sid = ''
      state.userInfo.email = ''
      state.userInfo.avatar = ''
      state.userInfo.school = ''
      state.userInfo.grade = ''
      state.userInfo.gender = -1
      state.userInfo.qq = ''
      state.userInfo.wechat = ''
      state.userInfo.mission_pub_num = -1
      state.userInfo.mission_fin_num = -1
    }
  },

  actions: {
    getMessageRemotely (context) {

    }
  }
})
