<template>
  <div id="app">
    <el-container>
      <el-aside v-bind:width="sideWidth" v-if="isLogin" class="sidebar-container">
        <side-bar v-bind:is-collapsed="sidebarCollapsed" v-bind:unread="unreadMsgNum"></side-bar>
      </el-aside>
      <el-container>
        <el-header id="top-menu" v-show="isLogin">
          <top-menu v-on:barCollapse="changeBarWidth"></top-menu>
        </el-header>
        <el-main class="inner-container">
          <transition name="fade" mode="out-in">
            <router-view v-on:markMessage="markMessage" v-on:login="login"/>
          </transition>
        </el-main>
      </el-container>
    </el-container>
    <vue-fab
      mainBtnColor="#2FA9F5"
      id="float-button"
      size="big"
      fabAnimateBezier="ease"
      fabItemAnimate="alive"
      v-bind:hidden="!showMenu"
      v-bind:globalOptions="{spacing: 70, delay: 0.1}">
      <fab-item v-on:clickItem="toMissionPublicPage(0)" v-bind:idx="0" title="发布问卷" icon="assignment"/>
      <fab-item v-on:clickItem="toMissionPublicPage(1)" v-bind:idx="1" title="发布其他" icon="directions_run"/>
    </vue-fab>
  </div>
</template>

<script>
import TopMenu from './components/TopMenu'
import SideBar from './components/SideBar'
import backend from './backend'

export default {
  components: { SideBar, TopMenu },
  data () {
    return {
      sideWidth: '64px',
      isLogin: false, // 根据登录情况判断是否展示侧栏
      sidebarCollapsed: true,
      unreadMsgNum: 7 // temp
    }
  },

  created: function () {
    if (this.$cookies.isKey('u-token')) {
      let token = this.$cookies.get('u-token')
      console.log(token)
      backend.getRequest('user/',
        {
          token: token
        })
        .then((response) => {
          this.isLogin = true
          this.$store.commit('setAll', response.data.data)
          console.log(response.data.data)
        })
        .catch((error) => {
          console.log(error)
        })
    }
  },

  methods: {
    changeBarWidth () {
      if (parseInt(this.sideWidth) < 100) {
        this.sideWidth = '240px'
        this.sidebarCollapsed = false
      } else {
        this.sideWidth = '64px'
        this.sidebarCollapsed = true
      }
    },

    toMissionPublicPage (idx) {
      if (idx === 0) {
        this.$router.push({ name: 'questionnaire' })
      } else {
        this.$router.push({ name: 'publishMission' })
      }
    },

    markMessage (count) {
      this.unreadMsgNum -= count
    },

    login () {
      this.isLogin = true
      this.$router.push({ name: 'square' })
    }
  },

  computed: {
    showMenu () {
      return !(this.$route.path === '/questionnaire' || this.$route.path === '/publishMission' ||
          this.$route.path === '/login' || this.$route.path === '/register' || this.$route.path === '/answerQuestionnaire' || this.$route.path === '/')
    }
  }
}
</script>

<style lang="scss" scoped>
  #top-menu {
    padding: 0;
  }

  .sidebar-container {
    transition: all .3s ease;
    box-shadow: 2px 0 4px rgba(0, 0, 0, .12)
  }

  .inner-container {
    height: calc(100vh - 60px);
  }

  .fade-enter, .fade-leave-to {
    transform: translateY(-20px);
    opacity: 0;
  }

  .fade-enter-active, .fade-leave-active {
    transition: all .3s ease;
  }

  #float-button {
    right: 10%;
  }
</style>
