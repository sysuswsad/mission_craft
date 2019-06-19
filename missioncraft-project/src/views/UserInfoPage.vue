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
                  <el-input v-model="username" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="年级">
                  <el-input v-model="grade" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="学院">
                  <el-input v-model="school" v-bind:disabled="!canEdit"></el-input>
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
          <el-form v-bind:model="passwordSet" label-width="100px" status-icon>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item
                  label="旧密码"
                  prop="oldPassword"
                  v-bind:rules="{required: true, message: '请输入旧密码', trigger: 'blur'}">
                  <el-input v-model="passwordSet.oldPassword" placeholder="旧密码" type="password"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item
                  label="新密码"
                  prop="newPassword"
                  v-bind:rules="{required: true, message: '请输入新密码', trigger: 'blur'}">
                  <el-input v-model="passwordSet.newPassword" placeholder="新密码" type="password"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item
                  label="确认密码"
                  prop="confirmPassword"
                  v-bind:rules="{required: true, message: '请再次确认密码', trigger: 'blur'}">
                  <el-input v-model="passwordSet.confirmPassword" placeholder="确认密码" type="password"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-button type="primary" icon="el-icon-edit" style="margin-left: 100px" v-on:click="changePassword">修改</el-button>
            </el-row>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="更换头像">
          <el-upload
            class="avatar-uploader"
            :http-request="uploadImage"
            action="http://172.18.34.59:5000/api/avatar/"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar" alt="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
          <el-button type="primary" style="margin-top: 10px">确认修改</el-button>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import backend from '../backend'
export default {
  name: 'UserInfoPage',
  data () {
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
      }
    }
  },
  methods: {
    editButtonClick () {
      this.canEdit = !this.canEdit
      this.interUsername = this.username
      this.interGrade = this.grade
      this.interSchool = this.school
    },
    cancelButtonClick () {
      this.canEdit = !this.canEdit
      this.username = this.interUsername
      this.grade = this.interGrade
      this.school = this.interSchool
    },
    handleAvatarSuccess (res, file) {
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeAvatarUpload (file) {
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isJPG && isLt2M
    },
    uploadImage (p) {
      backend.postRequest('avatar/',
        {
          image: p.file
        })
        .then((response) => {
          console.log(response)
        })
        .catch(function (error) {
          console.log(p.file)
          console.log(error)
        })
    },
    submitInfo () {
      backend.putRequest('user/',
        {
          username: this.username,
          grade: this.grade,
          school: this.school
        })
        .then((response) => {
          this.$message.success('用户信息修改成功！')
        })
        .catch(function (error) {
          console.log(error)
          this.username = this.interUsername
          this.grade = this.interGrade
          this.school = this.interSchool
          this.$message.error('用户信息修改失败！')
        })
    },
    changePassword () {
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
    school: {
      get () {
        return this.$store.state.userInfo.school
      },
      set (val) {
        this.$store.state.userInfo.school = val
      }
    },
    grade: {
      get () {
        return this.$store.state.userInfo.grade
      },
      set (val) {
        this.$store.state.userInfo.grade = val
      }
    },
    username: {
      get () {
        return this.$store.state.userInfo.username
      },
      set (val) {
        this.$store.state.userInfo.username = val
      }
    },
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
        return this.url
      } else {
        return this.defaultUrl
      }
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
