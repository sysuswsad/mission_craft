<template>
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
            src="default-avatar.png"
            v-bind:class="{ 'avatar-expand': !isCollapsed, 'avatar-collapse': isCollapsed }">
        </div>
        <div class="user-meta">
          <span class="username" v-show="!isCollapsed">Apple</span>
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
          <el-menu-item index="1">
            <i class="el-icon-s-order"></i>
            <template v-slot:title>
              <span>我的发布</span>
            </template>
          </el-menu-item>
          <el-menu-item index="2">
            <i class="el-icon-receiving"></i>
            <template v-slot:title>
              <span>我的领取</span>
            </template>
          </el-menu-item>
          <el-menu-item index="3" v-bind:route="{ name: 'message' }">
            <i class="el-icon-message-solid"></i>
            <template v-slot:title>
              <span>我的消息</span>
            </template>
          </el-menu-item>
        </el-menu>
      </el-row>
    </el-main>
    <el-footer>
      <div class="logout-button-wrapper" v-show="!isCollapsed">
        <el-button type="danger" plain icon="el-icon-switch-button" class="logout-button">退出登录</el-button>
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
    }
  },

  methods: {
    toUserInfo () {
      this.activeIdx = null
      this.$router.push({ name: 'userInfo' })
    },

    checkIdx (idx, idxPath) {
      this.activeIdx = idx
    }
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

  .logout-button-wrapper {
    text-align: center;
    overflow: hidden;
  }

  .logout-button {
    color: #F56C6C;
    transition-delay: .3s;
  }
</style>