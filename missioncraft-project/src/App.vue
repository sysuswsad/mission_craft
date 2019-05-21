<template>
  <div id="app">
    <el-container>
      <el-aside width="64px" v-show="isLogin"></el-aside>
      <el-container>
        <el-header id="top-menu">
          <TopMenu></TopMenu>
        </el-header>
        <el-main>
          <router-view/>
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

</style>
