<template>
  <div class="user-info-container">
    <div class="head-container">
      <div class="image-name-container">
        <img class="head-image" alt="加载失败" v-bind:src=url>
        <div class="user-name">
          Hello
        </div>
      </div>
    </div>
    <el-card class="user-info-card">
      <el-tabs class="user-info-tabs">
        <el-tab-pane label="个人信息">
          <el-form label-width="100px">
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="专业">
                  <el-input v-model="privateInfo.subject" v-bind:disabled="!canEdit"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-button type="primary" icon="el-icon-edit" style="margin-left: 100px" v-if="!canEdit" v-on:click="editButtonClick">修改</el-button>
              <el-col>
                <el-button type="primary" style="margin-left: 100px" v-if="canEdit" v-on:click="cancelButtonClick">取消</el-button>
                <el-button type="primary" style="margin-left: 100px" v-if="canEdit">确认</el-button>
              </el-col>
            </el-row>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="修改密码">
          <el-form v-bind:model="passwordSet" label-width="100px" status-icon>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="旧密码"
                              prop="oldPassword"
                              v-bind:rules="{required: true, message: '请输入旧密码', trigger: 'blur'}">
                  <el-input v-model="passwordSet.oldPassword" placeholder="旧密码" type="password"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="新密码"
                              prop="newPassword"
                              v-bind:rules="{required: true, message: '请输入新密码', trigger: 'blur'}">
                  <el-input v-model="passwordSet.newPassword" placeholder="新密码" type="password"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col v-bind:span="12">
                <el-form-item label="确认密码"
                              prop="confirmPassword"
                              v-bind:rules="{required: true, message: '请再次确认密码', trigger: 'blur'}">
                  <el-input v-model="passwordSet.confirmPassword" placeholder="确认密码" type="password"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-button type="primary" icon="el-icon-edit" style="margin-left: 100px">修改</el-button>
            </el-row>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="更换头像">

        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'UserInfoPage',
  data () {
    return {
      url: 'https://oj.vmatrix.org.cn/img/default-avatar.b6541da3.png',
      canEdit: false,
      privateInfo: {
        subject: ''
      },
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
    },
    cancelButtonClick () {
      this.canEdit = !this.canEdit
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
</style>
