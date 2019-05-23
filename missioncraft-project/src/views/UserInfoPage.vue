<template>
  <div class="user-info-container">
    <div class="head-container">
      <div class="image-name-container">
        <el-image
                class="head-image"
                :src=url>
        </el-image>
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
                  <el-input v-model="privateInfo.subject"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-button type="primary" icon="el-icon-edit" style="margin-left: 100px">修改</el-button>
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
              <el-button type="primary" icon="el-icon-edit" style="margin-left: 100px">确认修改</el-button>
            </el-row>
          </el-form>
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
      url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      privateInfo: {
        subject: ''
      },
      passwordSet: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
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
    margin: 10px auto;
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
