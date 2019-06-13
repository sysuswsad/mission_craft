<template>
  <div id="login-container">
    <el-card class="login-card">
      <template v-slot:header>
        <h1>LOGO</h1>
      </template>
      <div id="login-form">
        <el-form v-bind:model="info" v-bind:rules="rules" status-icon>
          <el-form-item prop="username">
            <el-input v-model="info.username" placeholder="用户名/邮箱" prefix-icon="el-icon-s-custom"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input type="password" v-model="info.password" placeholder="密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
          </el-form-item>
          <div id="func-container">
            <el-row>
              <el-button type="text" id="forget-password-button" class="text-button">忘记密码？</el-button>
              <el-button type="text" id="register-button" class="text-button" v-on:click="toRegister">注册</el-button>
            </el-row>
            <el-row>
              <el-button type="primary" id="login-button" v-on:click="login">登录</el-button>
            </el-row>
          </div>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import backend from '../backend'
export default {
  name: 'LoginPage',

  beforeCreate () {
    let isLogin = this.$cookies.isKey('u-token')
    backend.getRequest('user/')
      .then((response) => {
        this.$store.commit('setAll', response.data.data)
      })
      .catch((error) => {
        console.log(error)
      })
    if (isLogin) {
      this.$router.push({ name: 'square' })
    } else {
      console.log('ooo')
    }
  },

  data () {
    return {
      info: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          {
            required: true,
            message: '请输入用户名或邮箱',
            trigger: 'blur'
          },
          {
            pattern: /^[A-Za-z]+[A-Za-z0-9]{5,20}|^[A-Za-z]+[A-Za-z]*[1-9]*@mail2.sysu.edu.cn$/,
            message: '用户名非法'
          }
        ],
        password: [
          {
            required: true,
            message: '请输入密码',
            trigger: 'blur'
          },
          {
            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{8,16}$/,
            message: '至少8位且包含大写字母，小写字母和数字各一个'
          }
        ]
      }
    }
  },

  methods: {
    toRegister () {
      this.$router.push({ name: 'register' })
    },

    login () {
      backend.postRequest('token/',
        {
          username_or_email: this.info.username,
          password: this.info.password
        })
        .then((response) => {
          this.$emit('login')
          let pattern = /^[A-Za-z]+[A-Za-z0-9]{5,20}|^[A-Za-z]+[A-Za-z]*[1-9]*@mail2.sysu.edu.cn$/
          if (pattern.test(this.info.username)) {
            this.$store.commit('setEmail', this.info.username)
          } else {
            this.$store.commit('setUsername', this.info.username)
          }
          this.$cookies.set('u-token', response.data.data.token)
        })
        .catch(function (error) {
          console.log(error)
        })
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
    width: 25vw;
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
