<template>
  <div id="login-container">
    <div id="logo-container">
      LOGO
    </div>
    <div id="login-form">
      <el-form v-bind:model="info" status-icon>
        <el-form-item
          prop="username"
          v-bind:rules="{required: true, message: '请输入用户名或邮箱', trigger: 'blur'}"
        >
          <el-input v-model="info.username" label="用户名/邮箱" prefix-icon="el-icon-s-custom"></el-input>
        </el-form-item>
        <el-form-item
          prop="password"
          v-bind:rules="{required: true, message: '请输入密码', trigger: 'blur'}"
        >
          <el-input type="password" v-model="info.password" label="密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <div id="func-container">
          <el-button type="text" id="forget-password-button" class="text-button">忘记密码？</el-button>
          <el-button type="text" id="register-button" class="text-button" v-on:click="toRegister">注册</el-button>
          <el-button type="primary" id="login-button">登录</el-button>
        </div>
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
        password: ''
      }
    }
  },
  methods: {
    toRegister: function () {
      this.$router.push({ path: '/Register' })
    }
  }
}
</script>

<style scoped>
  #login-container {
    width: 400px;
    height: 380px;
    position: absolute;
    left:0; top:0; right:0; bottom: 0;
    margin: auto;
    padding: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
  }

  #logo-container {
    width: fit-content;
    font-size: 40px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 30px;
  }

  #login-button {
    margin-top: 10px;
    width: 100%;
    margin-left: 0;
  }

  #login-form {
    margin: 30px 10px 0 10px;
  }

  #func-container {
    margin-top: 30px;
  }

  #register-button {
    /*display: inline-block;*/
    float: right;
  }
</style>
