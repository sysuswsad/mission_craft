<template>
  <el-menu id="top-nav-menu" mode="horizontal">
    <el-menu-item index="2" class="nav-item">
      <i class="el-icon-question"></i>
      <template v-slot:title>
        <span>帮助</span>
      </template>
    </el-menu-item>
    <el-menu-item index="1" class="nav-item">
      <i class="el-icon-location"></i>
      <template v-slot:title>
        <span>广场</span>
      </template>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: 'TopMenu'
}
</script>

<style scoped>
.nav-item {
  float: right !important;
}
</style>
