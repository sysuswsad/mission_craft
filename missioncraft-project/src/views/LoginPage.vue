<template>
  <div id="login-container">
    <el-card class="login-card">
      <template v-slot:header>
        <h1>LOGO</h1>
      </template>
      <div id="login-form">
        <el-form v-bind:model="info" status-icon>
          <el-form-item
            prop="username"
            v-bind:rules="{required: true, message: '请输入用户名或邮箱', trigger: 'blur'}"
          >
            <el-input v-model="info.username" placeholder="用户名/邮箱" prefix-icon="el-icon-s-custom"></el-input>
          </el-form-item>
          <el-form-item
            prop="password"
            v-bind:rules="{required: true, message: '请输入密码', trigger: 'blur'}"
          >
            <el-input type="password" v-model="info.password" placeholder="密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
          </el-form-item>
          <div id="func-container">
            <el-row>
              <el-button type="text" id="forget-password-button" class="text-button">忘记密码？</el-button>
              <el-button type="text" id="register-button" class="text-button" v-on:click="toRegister">注册</el-button>
            </el-row>
            <el-row>
              <el-button type="primary" id="login-button" v-on:click="toUserInfo">登录</el-button>
            </el-row>
          </div>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data () {
    return {
      info: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    toRegister () {
      this.$router.push({ name: 'register' })
    },
    toUserInfo () {
      this.$router.push({ name: 'userInfo' })
    }
  }
}
</script>

<style scoped>
  #login-container {
    height: 100%;
    display: flex;
    align-items: center;
  }

  .login-card {
    width: 20vw;
    margin: 10px auto;
    padding: 15px;
  }

  #login-button {
    margin-top: 10px;
    width: 100%;
  }

  #func-container {
    margin-top: 20px;
  }

  #register-button {
    /*display: inline-block;*/
    float: right;
  }
</style>
