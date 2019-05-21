<template>
  <div id="register-container">
    <div id="register-form">
      <el-form v-bind:model="info" ref="info">
        <el-form-item prop="username" required>
          <el-input v-model="info.username" placeholder="昵称" prefix-icon="el-icon-s-custom"></el-input>
        </el-form-item>
        <el-form-item prop="studentId" required>
          <el-input v-model="info.studentId" placeholder="学号" prefix-icon="el-icon-s-custom"></el-input>
        </el-form-item>
        <el-form-item prop="email" required>
          <el-input v-model="info.email" placeholder="电子邮件" prefix-icon="el-icon-s-promotion"></el-input>
        </el-form-item>
        <el-form-item prop="testCode">
          <el-input v-model="info.code" placeholder="验证码" style="width: 200px"></el-input>
          <el-button type="primary" v-on:click="getCode" id="get-code-button" v-bind:disabled="!show">
            <span v-show="show">获取验证码</span>
            <span v-show="!show" class="count">{{count}} s</span>
          </el-button>
        </el-form-item>

        <el-form-item prop="pass" required>
          <el-input type="password" v-model="info.password" placeholder="密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item prop="confirmPass" required>
          <el-input type="password" v-model="info.confirmPass" placeholder="确认密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-button type="primary" id="register-button" v-on:click="toRegister">注册</el-button>
      </el-form>
    </div>

  </div>
</template>
<script>
export default {
  name: 'RegisterPage',
  data () {
    return {
      info: {
        username: '',
        studentId: '',
        email: '',
        password: '',
        confirmPass: ''
      },
      count: '',
      show: true,
      timer: null,
      code: ''
    }
  },
  methods: {
    getCode: function () {
      if (!this.timer) {
        this.count = 60
        this.show = false
        this.timer = setInterval(() => {
          if (this.count > 0 && this.count <= 60) {
            this.count--
          } else {
            this.show = true
            clearInterval(this.timer)
            this.timer = null
          }
        }, 1000)
      }
    }
  }
}
</script>

<style scoped>
  #register-container {
    width:400px;
    height: 450px;
    position: absolute;
    left:0; top:0; right:0; bottom: 0;
    margin: auto;
  }

  #register-form {
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
