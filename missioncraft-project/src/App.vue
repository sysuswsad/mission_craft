<template>
  <div id="app">
    <el-container>
      <el-aside v-bind:width="sideWidth" v-if="isLogin" class="sidebar-container">
        <side-bar v-bind:is-collapsed="sidebarCollapsed"></side-bar>
      </el-aside>
      <el-container>
        <el-header id="top-menu">
          <top-menu v-on:barCollapse="changeBarWidth"></top-menu>
        </el-header>
        <el-main class="inner-container">
          <transition name="fade" mode="out-in">
            <router-view/>
          </transition>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import TopMenu from './components/TopMenu'
import SideBar from './components/SideBar'

export default {
  components: { SideBar, TopMenu },
  data () {
    return {
      sideWidth: '64px',
      isLogin: true, // 根据登录情况判断是否展示侧栏
      sidebarCollapsed: true
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
  }

  .inner-container {
    height: calc(100vh - 60px)
  }

  .fade-enter, .fade-leave-to {
    transform: translateY(-20px);
    opacity: 0;
  }

  .fade-enter-active, .fade-leave-active {
    transition: all .3s ease;
  }
</style>
