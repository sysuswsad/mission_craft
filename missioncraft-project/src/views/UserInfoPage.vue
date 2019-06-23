<template>
  <div class="user-info-container">
    <div class="head-container">
      <div class="image-name-container">
        <img class="head-image" alt="加载失败" v-bind:src=selectUrl>
        <div class="user-name">
          {{interUsername}}
        </div>
      </div>
    </div>
    <el-card class="user-info-card">
      <el-tabs class="user-info-tabs">
        <el-tab-pane label="个人信息">
          <el-form label-width="100px">
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="用户名">
                  <el-input v-model="interUsername" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="年级">
                  <el-input v-model="interGrade" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="学院">
                  <el-input v-model="interSchool" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-button type="primary" icon="el-icon-edit" style="margin-left: 100px" v-if="!canEdit" v-on:click="editButtonClick">修改</el-button>
              <el-col>
                <el-button type="primary" style="margin-left: 100px" v-if="canEdit" v-on:click="cancelButtonClick">取消</el-button>
                <el-button type="primary" style="margin-left: 100px" v-if="canEdit" v-on:click="submitInfo">确认</el-button>
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
            action="http://172.18.34.59:5000/api/avatar/"
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
          this.interUsername = response.data.data['username']
          this.interSchool = response.data.data['school']
          this.interGrade = response.data.data['grade']
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
      interUsername: '',
      interSchool: '',
      interGrade: '',
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
      this.interUsername = this.$store.state.userInfo.username
      this.interGrade = this.$store.state.userInfo.grade
      this.interSchool = this.$store.state.userInfo.school
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
    submitInfo () {
      backend.putRequest('user/',
        {
          username: this.interUsername,
          grade: this.interGrade,
          school: this.interSchool
        })
        .then((response) => {
          this.$message.success('用户信息修改成功！')
          this.$store.commit('changeInfo', { 'username': this.interUsername, 'school': this.interSchool, 'grade': this.interGrade })
          this.canEdit = !this.canEdit
        })
        .catch(function (error) {
          console.log(error)
          this.$message.error('用户信息修改失败！')
        })
    },
    changePassword (formName) {
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
      backend.postRequest('password/',
        {
          username: this.username,
          old_password: this.passwordSet.oldPassword,
          new_password: this.passwordSet.newPassword
        })
        .then((response) => {
          this.$message.success('密码修改成功！')
        })
        .catch(() => {
          this.$message.error('密码修改失败！')
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
        return 'http://172.18.34.59:5000' + this.url
      } else {
        return this.defaultUrl
      }
    },
    getToken () {
      return { 'Authorization': `Bearer ${this.$cookies.get('u-token')}`,
        'Accept': 'application/json, text/plain, */*' }
    }
  }
}
</script>

<style scoped>
  .head-container {
    height: 300px;
    background-color: aquamarine;
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
