<template>
  <div class="user-info-container">
    <div class="head-container">
      <div class="image-name-container">
        <img class="head-image" alt="加载失败" v-bind:src=selectUrl>
        <div class="user-name">
          余额：{{info.interBalance}}
        </div>
      </div>
    </div>
    <el-card class="user-info-card">
      <el-tabs class="user-info-tabs">
        <el-tab-pane label="个人信息">
          <el-form label-width="100px" ref="info" v-bind:rules="rules" v-bind:model="info">
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="用户名" prop="interUsername">
                  <el-input v-model="info.interUsername" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="年级" prop="interGrade">
                  <el-input v-model="info.interGrade" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="学院" prop="interSchool">
                  <el-input v-model="info.interSchool" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="电话" prop="interPhone">
                  <el-input v-model="info.interPhone" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="微信" prop="interWeChat">
                  <el-input v-model="info.interWeChat" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="qq" prop="interQQ">
                  <el-input v-model="info.interQQ" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-button type="primary" icon="el-icon-edit" style="margin-left: 100px" v-if="!canEdit" v-on:click="editButtonClick">修改</el-button>
              <el-col>
                <el-button type="primary" style="margin-left: 100px" v-if="canEdit" v-on:click="cancelButtonClick">取消</el-button>
                <el-button type="primary" style="margin-left: 100px" v-if="canEdit" v-on:click="submitInfo('info')">确认</el-button>
              </el-col>
            </el-row>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="修改密码">
          <el-form v-bind:model="passwordSet" label-width="100px" status-icon ref="passwordSet" v-bind:rules="rules">
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item
                  label="旧密码"
                  prop="oldPassword">
                  <el-input v-model="passwordSet.oldPassword" placeholder="旧密码" type="password"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item
                  label="新密码"
                  prop="newPassword">
                  <el-input v-model="passwordSet.newPassword" placeholder="新密码" type="password"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item
                  label="确认密码"
                  prop="confirmPassword">
                  <el-input v-model="passwordSet.confirmPassword" placeholder="确认密码" type="password"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-button type="primary" icon="el-icon-edit" style="margin-left: 100px" v-on:click="changePassword('passwordSet')">修改</el-button>
            </el-row>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="更换头像">
          <el-upload
            class="avatar-uploader"
            :action="getBaseURL"
            name="image"
            :headers="getToken"
            :show-file-list="false"
            ref="upload"
            :auto-upload="true"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar" alt="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import backend from '../backend'
export default {
  name: 'UserInfoPage',
  created () {
    if (this.$cookies.isKey('u-token')) {
      backend.getRequest('user/')
        .then((response) => {
          this.info.interUsername = response.data.data['username']
          this.info.interSchool = response.data.data['school']
          this.info.interGrade = response.data.data['grade']
          this.info.interPhone = response.data.data['phone']
          this.info.interWeChat = response.data.data['wechat']
          this.info.interQQ = response.data.data['qq']
          this.info.interBalance = response.data.data['balance']
        })
        .catch(() => {
        })
    } else {
      this.$router.push({ name: 'login' })
    }
  },

  data () {
    let validatePass = (rule, value, callback) => {
      if (value !== this.passwordSet.newPassword) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      defaultUrl: 'https://oj.vmatrix.org.cn/img/default-avatar.b6541da3.png',
      canEdit: false,
      imageUrl: '',
      info: {
        interUsername: '',
        interSchool: '',
        interGrade: '',
        interPhone: '',
        interWeChat: '',
        interQQ: '',
        interBalance: ''
      },
      passwordSet: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      rules: {
        newPassword: [
          {
            required: true,
            message: '密码不能为空'
          },
          {
            pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\s\S]{8,16}$/,
            message: '密码至少包含1个大写字母，1个小写字母和1个数字的8位串'
          }
        ],
        confirmPassword: [
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
        interPhone: [
          {
            pattern: /^(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[35678]\d{2}|4(?:0\d|1[0-2]|9\d))|9[189]\d{2}|66\d{2})\d{6}$/,
            message: '电话号码格式有误'
          }
        ],
        interWeChat: [
          {
            pattern: /^[a-zA-Z]{1}[-_a-zA-Z0-9]{5,19}$/,
            message: '微信号格式有误'
          }
        ],
        interQQ: [
          {
            pattern: /^[1-9]\d{4,9}$/,
            message: 'QQ号格式有误'
          }
        ]
      }
    }
  },
  methods: {
    editButtonClick () {
      this.canEdit = !this.canEdit
    },
    cancelButtonClick () {
      this.canEdit = !this.canEdit
      this.info.interUsername = this.$store.state.userInfo.username
      this.info.interGrade = this.$store.state.userInfo.grade
      this.info.interSchool = this.$store.state.userInfo.school
      this.info.interPhone = this.$store.state.userInfo.phone
      this.info.interWeChat = this.$store.state.userInfo.wechat
      this.info.interqq = this.$store.state.userInfo.qq
    },
    handleAvatarSuccess (res, file) {
      this.url = res.data.avatar
      this.$message.success('头像上传成功')
    },
    beforeAvatarUpload (file) {
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isLt2M
    },
    submitInfo (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          backend.putRequest('user/',
            {
              username: this.info.interUsername,
              grade: this.info.interGrade,
              school: this.info.interSchool,
              phone: this.info.interPhone,
              qq: this.info.interQQ,
              wechat: this.info.interWeChat
            })
            .then((response) => {
              this.$message.success('用户信息修改成功！')
              this.$store.commit('changeInfo', {
                'username': this.info.interUsername,
                'school': this.info.interSchool,
                'grade': this.info.interGrade,
                'phone': this.info.interPhone,
                'qq': this.info.interQQ,
                'wechat': this.info.interWeChat
              })
              this.canEdit = !this.canEdit
            })
            .catch(() => {
              this.$message.error('用户信息修改失败！')
            })
        }
      })
    },
    changePassword (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          backend.postRequest('password/',
            {
              username: this.username,
              old_password: this.passwordSet.oldPassword,
              new_password: this.passwordSet.newPassword
            })
            .then((response) => {
              this.$message.success('密码修改成功')
            })
            .catch((error) => {
              let msg = Object.values(error.response.data)[1]
              msg = parseInt(msg.split(' '))
              switch (msg) {
                case 112:
                  this.$message.error('旧密码错误')
                  break
                default:
                  this.$message.error('未知错误')
                  break
              }
            })
        }
      })
    }
  },

  computed: {
    url: {
      get () {
        return this.$store.state.userInfo.avatar
      },
      set (val) {
        this.$store.state.userInfo.avatar = val
      }
    },
    selectUrl () {
      if (this.url !== '') {
        return backend.baseURL + this.url
      } else {
        return this.defaultUrl
      }
    },
    getToken () {
      return { 'Authorization': `Bearer ${this.$cookies.get('u-token')}`,
        'Accept': 'application/json, text/plain, */*' }
    },
    getBaseURL () {
      return backend.baseURL + '/api/avatar/'
    }
  }
}
</script>

<style scoped>
  .head-container {
    height: 300px;
    background-color: rgb(244, 244, 245);
    width: 100%;
    display: flex;
    align-items: center;
  }

  .image-name-container {
    width: fit-content;
    height: fit-content;
    margin: 10px auto;
  }

  .head-image {
    width: 100px;
    height: 100px;
    border-radius: 50%;
  }

  .user-name {
    text-align: center;
  }

  .user-info-container {
    height: 100%;
  }

  .user-info-card {
    width: 60vw;
    margin: 10px auto;
    padding: 15px;
  }

  .avatar-uploader {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    width: 100px;
    height: 100px;
  }
  .avatar-uploader:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 100px;
    height: 100px;
    line-height: 100px;
    text-align: center;
  }
  .avatar {
    width: 100px;
    height: 100px;
    display: block;
  }
</style>
