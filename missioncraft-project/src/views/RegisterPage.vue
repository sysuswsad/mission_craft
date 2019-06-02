<template>
  <div id="register-container">
    <el-card class="register-card">
      <el-form v-bind:model="info" ref="info">
        <el-form-item prop="username" required>
          <el-input v-model="info.username" placeholder="昵称" prefix-icon="el-icon-user-solid"></el-input>
        </el-form-item>
        <el-form-item prop="studentId" required>
          <el-input v-model="info.studentId" placeholder="学号" prefix-icon="el-icon-user-solid"></el-input>
        </el-form-item>
        <el-form-item prop="email" required>
          <el-input v-model="info.email" placeholder="电子邮件" prefix-icon="el-icon-message" v-on:change="handleEmailChange"></el-input>
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
        <el-button type="primary" id="register-button">注册</el-button>
        <div class="login-switch-container">
          <span>已有帐号？<el-button type="text" v-on:click="toLogin">登录</el-button></span>
        </div>
      </el-form>
    </el-card>
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
    getCode () {
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
    },

    toLogin () {
      this.$router.push({ name: 'login' })
    },

    handleEmailChange (value) {
      let regEmail = /^[A-Za-z]+[A-Za-z]*[1-9]*@mail2.sysu.edu.cn$/
      if (!regEmail.test(value)) {
        this.$message.error('请使用中山大学学生邮箱注册！')
      }
    }
  }
}
</script>

<style scoped>
  #register-container {
    height: 100%;
    display: flex;
    align-items: center;
  }

  .register-card {
    width: 20vw;
    margin: 10px auto;
    padding: 15px;
  }

  #register-button {
    margin-top: 10px;
    width: 100%;
  }

  #get-code-button {
    position: absolute;
    right: 0;
  }

  .login-switch-container {
    margin-top: 1rem;
    text-align: center;
  }
</style>
