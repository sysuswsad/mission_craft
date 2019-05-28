<template>
  <div class="main-container">
    <el-card class="add-button-container">
      <el-row>
        <el-col>
          <el-button icon="el-icon-plus">单选题</el-button>
          <el-button icon="el-icon-plus">多选题</el-button>
          <el-button icon="el-icon-plus">文本题</el-button>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'EditQuestionnaire'
}
</script>

<style scoped>
  .main-container {
    width: 100%;
  }
</style>
