<template>
  <el-container direction="vertical" style="height: 100%">
    <el-header style="padding: 0">
      <el-row class="logo-wrapper">
        <span>Mission Craft</span>
      </el-row>
    </el-header>
    <el-main style="padding: 0">
      <el-row class="user-info-container">
        <div class="avatar-wrapper">
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
      <el-row>
        <el-menu
          mode="vertical"
          class="sidebar-nav"
          v-bind:collapse="isCollapsed"
          v-bind:collapse-transition="false">
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
          <el-menu-item index="3">
            <i class="el-icon-message-solid"></i>
            <template v-slot:title>
              <span v-on:click="toMessage">我的消息</span>
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

  props: {
    isCollapsed: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    toMessage () {
      this.$router.push({ name: 'message' })
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
  }

  .logout-button {
    color: #F56C6C;
  }
</style>
