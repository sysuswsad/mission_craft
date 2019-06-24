import Vue from 'vue'
import Vuex from 'vuex'
import $backend from './backend'
import { Message } from 'element-ui'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userInfo: {
      avatar: '',
      balance: 0,
      check_man_id: '',
      email: '',
      gender: -1,
      grade: '',
      idUser: '',
      id_card_num: '',
      mission_fin_num: -1,
      mission_pub_num: -1,
      phone: '',
      qq: '',
      realname: '',
      school: '',
      sid: '',
      tag: '',
      type: '',
      university: '',
      username: '',
      wechat: ''
    },
    missionInfo: [],
    message: [],
    isLogin: false
  },

  mutations: {
    login (state, info) {
      Vue.set(state, userInfo, { ...info })
    },

    updateMessage (state, payload) {
      state.message = payload.message
    },

    addMission (state, payload) {
      state.missionInfo = state.missionInfo.concat(payload.missionInfo.reverse())
    },

    logout (state) {
      state.userInfo.avatar = ''
      state.userInfo.balance = 0
      state.userInfo.check_man_id = ''
      state.userInfo.email = ''
      state.userInfo.gender = -1
      state.userInfo.grade = ''
      state.userInfo.idUser = ''
      state.userInfo.id_card_num = ''
      state.userInfo.mission_fin_num = -1
      state.userInfo.mission_pub_num = -1
      state.userInfo.phone = ''
      state.userInfo.qq = ''
      state.userInfo.realname = ''
      state.userInfo.school = ''
      state.userInfo.sid = ''
      state.userInfo.tag = ''
      state.userInfo.type = ''
      state.userInfo.university = ''
      state.userInfo.username = ''
      state.userInfo.wechat = ''
    },

    setInRegister (state, username, studentId, email, phone, weChat, qq, other) {
      state.userInfo.username = username
      state.userInfo.sid = studentId
      state.userInfo.email = email
      state.userInfo.phone = phone
      state.userInfo.weChat = weChat
      state.userInfo.qq = qq
      state.userInfo.other = other
    },

    setUsername (state, username) {
      state.userInfo.username = username
    },

    setEmail (state, email) {
      state.userInfo.email = email
    },

    setAll (state, info) {
      state.userInfo = info
    },

    setGrade (state, grade) {
      state.userInfo.grade = grade
    },

    setSchool (state, school) {
      state.userInfo.school = school
    },

    setLogin (state, l) {
      state.isLogin = l
    },

    changeInfo (state, payload) {
      state.userInfo.username = payload.username
      state.userInfo.school = payload.school
      state.userInfo.grade = payload.grade
      state.userInfo.phone = payload.phone
      state.userInfo.qq = payload.qq
      state.userInfo.wechat = payload.wechat
    }

  },

  actions: {
    getMessageRemotely (context) {

    },

    fetchMissionRemotely ({ commit, state }, payload) {
      let personal = 0
      let noMoreMissions = false

      return $backend.getRequest('mission/', {
        params: {
          create_time: payload.create_time,
          limit: payload.limit,
          personal: personal
        }
      }).then(response => {
        if (response.data.data.missions.length > 0) {
          commit('addMission', {
            missionInfo: response.data.data.missions
          })
        }

        if (response.data.data.missions.length === 0) {
          noMoreMissions = true
        }

        return noMoreMissions
      }).catch(err => {
        console.log(err.response.data.message)
        Message.error('出错了！请刷新重试')
        return noMoreMissions
      })
    }
  }
})
