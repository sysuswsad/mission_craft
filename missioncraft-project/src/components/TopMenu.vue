<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <el-menu
    id="top-nav-menu"
    mode="horizontal"
    text-color="#fff"
    active-text-color="#cff09e"
    background-color="#2FA9F5">
    <div class="toggle-wrapper" v-on:click="collapseSideBar">
      <i v-bind:class="collapseIcon" id="collapse-toggle"></i>
    </div>
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
      isLogin: true,
      collapseIcon: 'el-icon-s-unfold'
    }
  },

  methods: {
    collapseSideBar () {
      this.$emit('barCollapse')
      if (this.collapseIcon.localeCompare('el-icon-s-unfold') === 0) {
        this.collapseIcon = 'el-icon-s-fold'
      } else {
        this.collapseIcon = 'el-icon-s-unfold'
      }
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

  .toggle-wrapper {
    position: absolute;
    display: flex;
    align-items: center;
    height: 100%;
    padding: 0 1rem;
    color: white;
    cursor: pointer;
    font-size: 1.3rem;
    transition: all .3s ease;
  }

  .toggle-wrapper:hover {
    background-color: #2687C4;
  }

  .toggle-wrapper:focus {
    outline: none;
  }

  .el-icon-question, .el-icon-guide {
    color: white;
  }
</style>
