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
            <el-input type="password" v-model="info.password" placeholder="密码" autocomplete="off" prefix-icon="el-icon-lock" v-on:keyup.enter="login"></el-input>
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
          this.$cookies.set('u-token', response.data.data.token)
          setTimeout(() => {
            backend.getRequest('user/')
              .then((response) => {
                this.isLogin = true
                this.$store.commit('setAll', response.data.data)
                if (this.$route.path === '/login' || this.$route.path === '/') {
                  this.$router.push({ name: 'square' })
                }
                this.$store.commit('setLogin', true)
                this.$router.push({ name: 'square' })
              })
              .catch(() => {
                // console.log('ooooo')
                // console.log(error.response)
                this.$router.push({ name: 'login' })
              })
          })
        })
        .catch((error) => {
          let msg = Object.values(error.response.data)[1]
          msg = parseInt(msg.split(' '))
          switch (msg) {
            case 105:
              this.$message.error('用户名错误')
              break
            case 106:
              this.$message.error('密码错误')
              break
            default:
              this.$message.error('未知错误')
              break
          }
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
