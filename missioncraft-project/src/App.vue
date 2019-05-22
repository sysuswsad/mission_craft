<template>
  <div id="app">
    <el-container>
      <el-aside width="64px" v-if="isLogin"></el-aside>
      <el-container>
        <el-header id="top-menu">
          <TopMenu></TopMenu>
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
export default {
  components: { TopMenu },
  data () {
    return {
      isLogin: false // 根据登录情况判断是否展示侧栏
    }
  }
}
</script>

<style lang="scss" scoped>
  #top-menu {
    padding: 0;
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
