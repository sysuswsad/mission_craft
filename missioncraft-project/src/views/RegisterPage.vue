<template>
  <div id="register-container">
    <el-card class="register-card">
      <el-form v-bind:model="info" ref="info" v-bind:rules="rules">
        <transition name="info-form">
          <div v-show="state">
            <el-form-item prop="username">
              <el-input v-model="info.username" placeholder="用户名" prefix-icon="el-icon-user-solid"></el-input>
            </el-form-item>
            <el-form-item prop="studentId">
              <el-input v-model="info.studentId" placeholder="学号" prefix-icon="el-icon-user-solid"></el-input>
            </el-form-item>
            <el-form-item prop="email">
              <el-input v-model="info.email" placeholder="电子邮件" prefix-icon="el-icon-message"></el-input>
            </el-form-item>
            <el-form-item prop="code">
              <el-input v-model="info.code" placeholder="验证码" style="width: 60%"></el-input>
              <el-button type="primary" v-on:click="getCode" id="get-code-button" v-bind:disabled="!show" style="width: 39%">
                <span v-show="show">获取验证码</span>
                <span v-show="!show" class="count">{{count}} s</span>
              </el-button>
            </el-form-item>
            <el-form-item prop="password">
              <el-input type="password" v-model="info.password" placeholder="密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
            </el-form-item>
            <el-form-item prop="confirmPass">
              <el-input type="password" v-model="info.confirmPass" placeholder="确认密码" autocomplete="off" prefix-icon="el-icon-lock"></el-input>
            </el-form-item>
            <el-button type="primary" id="next-page-button" v-on:click="changeState">下一页</el-button>
            <div class="login-switch-container">
              <span>已有帐号？<el-button type="text" v-on:click="toLogin">登录</el-button></span>
            </div>
          </div>
        </transition>
        <transition name="contact-form">
          <div v-show="!state" class="contact-form">
            <p style="color: red; font-size: 12px; margin-bottom: 1rem">注：以下联系方式为选填内容，但建议填写</p>
            <el-form-item prop="phone">
              <el-input type="text" v-model="info.phone" placeholder="电话" auto-complete="off" prefix-icon="el-icon-phone"></el-input>
            </el-form-item>
            <el-form-item prop="weChat">
              <el-input type="text" v-model="info.weChat" placeholder="微信" auto-complete="off" prefix-icon="el-icon-chat-dot-round"></el-input>
            </el-form-item>
            <el-form-item prop="qq">
              <el-input type="text" v-model="info.qq" placeholder="QQ" auto-complete="off" prefix-icon="el-icon-position"></el-input>
            </el-form-item>
            <el-form-item prop="other">
              <el-input type="text" v-model="info.other" placeholder="其他联系方式" auto-complete="off" prefix-icon="el-icon-s-home"></el-input>
            </el-form-item>
            <el-button type="primary" id="last-page-button" v-on:click="changeState">上一页</el-button>
            <el-button type="primary" id="register-button" v-on:click="register('info')">注册</el-button>
          </div>
        </transition>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import backend from '../backend'
export default {
  name: 'RegisterPage',
  data () {
    let validatePass = (rule, value, callback) => {
      if (value !== this.info.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      info: {
        username: '',
        studentId: '',
        email: '',
        code: '',
        password: '',
        confirmPass: '',
        phone: '',
        weChat: '',
        qq: '',
        other: ''
      },
      count: '',
      show: true,
      timer: null,
      state: true,
      rules: {
        username: [
          {
            required: true,
            message: '用户名不能为空'
          },
          {
            pattern: /^[A-Za-z]+[A-Za-z0-9]{5,20}$/,
            message: '用户名必须是以字母开头由数字和字母组成的6-20个字符的串'
          }
        ],
        studentId: [
          {
            required: true,
            message: '学号不能为空'
          },
          {
            pattern: /^[0-9]{8}$/,
            message: '学号必须是8个数字组成的串'
          }
        ],
        email: [
          {
            required: true,
            message: '邮箱不能为空'
          },
          {
            pattern: /^[A-Za-z]+[A-Za-z]*[1-9]*@mail2.sysu.edu.cn$/,
            message: '请输入中大学生邮箱进行注册'
          }
        ],
        code: [
          {
            required: true,
            message: '验证码不能为空'
          },
          {
            pattern: /^[0-9]{6}$/,
            message: '验证码必须是4个数字组成的串'
          }
        ],
        password: [
          {
            required: true,
            message: '密码不能为空'
          },
          {
            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{8,16}$/,
            message: '密码至少包含1个大写字母，1个小写字母和1个数字的8位串'
          }
        ],
        confirmPass: [
          {
            required: true,
            message: '请再次输入密码',
            trigger: 'blur'
          },
          {
            validator: validatePass,
            trigger: 'change'
          }
        ],
        phone: [
          {
            pattern: /^(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[35678]\d{2}|4(?:0\d|1[0-2]|9\d))|9[189]\d{2}|66\d{2})\d{6}$/,
            message: '电话号码格式有误'
          }
        ],
        weChat: [
          {
            pattern: /^[a-zA-Z]{1}[-_a-zA-Z0-9]{5,19}$/,
            message: '微信号格式有误'
          }
        ],
        qq: [
          {
            pattern: /^[1-9]\d{4,9}$/,
            message: 'QQ号格式有误'
          }
        ],
        other: {
        }
      }
    }
  },
  methods: {
    getCode () {
      backend.postRequest('code/', { email: this.info.email })
        .then((response) => {
        }).catch(() => {
        })
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

    changeState () {
      this.state = !this.state
    },

    register (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          backend.postRequest('user/',
            { username: this.info.username,
              sid: this.info.studentId,
              email: this.info.email,
              password: this.info.password,
              code: this.info.code
            })
            .then((response) => {
              this.$router.push({ name: 'login' })
              this.$message.success('注册成功！')
            })
            .catch(() => {
            })
        } else {
          alert('表单错误')
          return false
        }
      })
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
    width: 25vw;
    margin: 10px auto;
    padding: 15px;
  }

  #register-button {
    margin-top: 10px;
    width: 100%;
    margin-left: 0px;
  }

  #get-code-button {
    position: absolute;
    right: 0;
  }

  .login-switch-container {
    margin-top: 1rem;
    text-align: center;
  }

  #next-page-button {
    margin-top: 10px;
    width: 100%;
  }

  #last-page-button {
    margin-top: 10px;
    width: 100%;
  }

  .contact-form-enter-active {
    transition: all .4s ease;
  }
  .contact-form-enter {
    transform: translateX(50px);
    opacity: 0;
  }

  .info-form-enter-active {
    transition: all .4s ease;
  }

  .info-form-enter {
    transform: translateX(50px);
    opacity: 0;
  }
</style>
