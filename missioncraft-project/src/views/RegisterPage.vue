<template>
  <div class="register-container">
    <div class="table">
      <el-form :model="info" ref="info">
        <el-form-item prop="username">
          <el-input v-model="info.username" placeholder="昵称" prefix-icon="el-icon-s-custom"></el-input>
        </el-form-item>
        <el-form-item prop="studentNumber">
          <el-input v-model="info.studentNumber" placeholder="学号" prefix-icon="el-icon-s-custom"></el-input>
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="info.email" placeholder="电子邮件" prefix-icon="el-icon-s-promotion"></el-input>
        </el-form-item>
        <el-form-item prop="testCode">
          <el-input v-model="info.testCode" placeholder="验证码" style="width: 200px"></el-input>
          <el-button type="primary" v-on:click="toRegister" id="get-code-button">获取验证码</el-button>
        </el-form-item>

        <el-form-item prop="pass">
          <el-input type="password" v-model="info.pass" placeholder="密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item prop="confirmPass">
          <el-input type="password" v-model="info.confirmPass" placeholder="确认密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-button type="primary" id="register-button" v-on:click="toRegister">注册</el-button>
      </el-form>
    </div>

  </div>
</template>
<script>
export default {
  name: "RegisterPage",
  data() {
    return {
      info: {
        username: '',
        studentNumber: '',
        email: '',
        password: '',
        confirmPass: '',
        testCode: ''
      }
    }
  }
}
</script>

<style scoped>
  .register-container {
    width:400px;
    height: 450px;
    position: absolute;
    left:0; top:0; right:0; bottom: 0;
    margin: auto;
  }
  .table {
    width: 380px;
    margin: 10px auto 10px auto;
  }
  #register-button {
    width: 380px;
  }
  #get-code-button {
    position: absolute;
    right: 0;
  }
</style>
