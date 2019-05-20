<template>
  <div class="login-container">
    <div class="logo-container">
      LOGO
    </div>
    <div  class="table">
      <el-form :model="info" ref="info">
        <el-form-item prop="pass">
          <el-input v-model="info.username" placeholder="用户名/邮箱" prefix-icon="el-icon-s-custom"></el-input>
        </el-form-item>
        <el-form-item prop="pass">
          <el-input type="password" v-model="info.pass" placeholder="密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-button type="text" id="forget-password" class="text-button">忘记密码？</el-button>
        <el-button type="text" id="register-button" class="text-button" v-on:click="toRegister">注册</el-button>
        <el-button type="primary" id="login-button">登录</el-button>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data () {
    return {
      info: {
        username: '',
        pass: ''
      }
    }
  },
  methods: {
    toRegister: function () {
      this.$router.push({ path: '/RegisterPage' })
    }
  }
}
</script>

<style scoped>
  .login-container {
    width: 400px;
    height: 400px;
    position: absolute;
    left:0; top:0; right:0; bottom: 0;
    margin: auto;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
  }
  #login-button {
    position: relative;
    top: 10px;
    width: 100%;
    margin-left: 0;
  }
  #register-button {
    display: inline-block;
    position: absolute;
    right: 0;
  }
  .table {
    width: 380px;
    position: relative;
    height: 250px;
    left: 10px;
    right: 10px;
    top: 30px;
  }
  .logo-container {
    width: fit-content;
    font-size: 40px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 30px;
  }
  body {
    width: 100%;height: 100%;position: relative;background-color: #ccc
  }
</style>
