<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <el-container direction="vertical" style="height: 100%">
    <el-header style="padding: 0">
      <el-row class="logo-wrapper">
        <span>Mission Craft</span>
      </el-row>
    </el-header>
    <el-main style="padding: 0">
      <el-row class="user-info-container">
        <div class="avatar-wrapper" v-on:click="toUserInfo">
          <img
            alt="avatar"
            v-bind:src="avatarSrc"
            v-bind:class="{ 'avatar-expand': !isCollapsed, 'avatar-collapse': isCollapsed }">
        </div>
        <div class="user-meta">
          <span class="username" v-show="!isCollapsed">{{username}}</span>
        </div>
      </el-row>
      <el-divider direction="horizontal"></el-divider>
      <el-row style="overflow: hidden">
        <el-menu
          mode="vertical"
          class="sidebar-nav"
          ref="sidebar"
          v-bind:router="true"
          v-bind:collapse="isCollapsed"
          v-bind:collapse-transition="false"
          v-bind:default-active="activeIdx"
          v-on:select="checkIdx">
          <el-menu-item index="1" v-bind:route="{ name: 'published' }">
            <i class="el-icon-s-order"></i>
            <template v-slot:title>
              <span>我的发布</span>
            </template>
          </el-menu-item>
          <el-menu-item index="2" v-bind:route="{ name: 'received' }">
            <i class="el-icon-receiving"></i>
            <template v-slot:title>
              <span>我的领取</span>
            </template>
          </el-menu-item>
          <el-menu-item index="3" v-bind:route="{ name: 'message' }" style="overflow: hidden;">
            <el-badge v-bind:value="unread" v-bind:max="9" v-bind:hidden="!isCollapsed || hideUnread" class="message-icon-badge">
              <i class="el-icon-message-solid"></i>
            </el-badge>
            <template v-slot:title>
              <span>我的消息</span>
              <el-badge v-bind:value="unread" v-bind:max="9" v-bind:hidden="isCollapsed || hideUnread" class="message-badge"/>
            </template>
          </el-menu-item>
        </el-menu>
      </el-row>
    </el-main>
    <el-footer>
      <div class="logout-button-wrapper" v-show="!isCollapsed">
        <el-button type="danger" plain icon="el-icon-switch-button" class="logout-button" v-on:click="logout">退出登录</el-button>
      </div>
    </el-footer>
  </el-container>
</template>

<script>
export default {
  name: 'SideBar',

  data () {
    return {
      activeIdx: null
    }
  },

  props: {
    isCollapsed: {
      type: Boolean,
      default: true
    },

    unread: {
      type: Number,
      default: 0
    }
  },

  methods: {
    toUserInfo () {
      this.activeIdx = null
      this.$router.push({ name: 'userInfo' })
    },

    checkIdx (idx, idxPath) {
      this.activeIdx = idx
    },

    logout () {
      this.$store.commit('logout')
      this.$cookies.remove('u-token')
      this.$router.push({ name: 'login' })
      this.$store.commit('setLogin', false)
    }
  },

  computed: {
    hideUnread () {
      return this.unread <= 0
    },

    avatarSrc: {
      get () {
        if (this.$store.state.userInfo.avatar === '') {
          return 'default-avatar.png'
        } else {
          return 'http://172.18.34.59:5000' + this.$store.state.userInfo.avatar
        }
      }
    },

    ...mapState({
      username: state => state.userInfo.username
    })
  }
}
</script>

<style scoped>
  .logo-wrapper {
    text-align: center;
  }

  .avatar-wrapper {
    margin-top: 3rem;
    cursor: pointer;
  }

  .avatar-wrapper > img {
    display: block;
    margin: auto;
    transition: width .3s ease, height .3s ease;
  }

  .avatar-wrapper > .avatar-expand {
    width: 40%;
    height: auto;
  }

  .avatar-wrapper > .avatar-collapse {
    width: 70%;
    height: auto;
  }

  .user-meta {
    margin-top: 1.2rem;
    text-align: center;
  }

  .user-meta > .username {
    font-size: 1rem;
  }

  .sidebar-nav {
    width: calc(100% - 1px);
  }

  .message-icon-badge {
    display: inline-flex;
  }

  .message-badge {
    float: right;
  }

  .logout-button-wrapper {
    text-align: center;
    overflow: hidden;
  }

  .logout-button {
    color: #F56C6C;
  }
</style>
