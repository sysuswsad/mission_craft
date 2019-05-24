<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <el-menu
    id="top-nav-menu"
    mode="horizontal"
    text-color="#fff"
    active-text-color="#cff09e"
    background-color="#6AAFE6">
    <el-menu-item></el-menu-item>
    <el-menu-item index="2" class="nav-item">
      <i class="el-icon-question"></i>
      <template v-slot:title>
        <span>帮助</span>
      </template>
    </el-menu-item>
    <el-menu-item index="1" class="nav-item" v-if="isLogin">
      <i class="el-icon-guide"></i>
      <template v-slot:title>
        <span>广场</span>
      </template>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: 'TopMenu',
  data () {
    return {
      isLogin: false
    }
  }
}
</script>

<style scoped>
  #top-nav-menu {
    padding-right: 1rem;
  }

  .nav-item {
    float: right !important;
  }

  .el-icon-question, .el-icon-guide {
    color: white;
  }
</style>
