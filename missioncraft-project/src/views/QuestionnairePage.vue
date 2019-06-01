<template>
  <div class="main-container">
    <div class="questionnaire-container">
      <EditQuestionnaire></EditQuestionnaire>
      <el-card style="float: right; width: 70%; border: green 1px dashed">
        <el-form label-width="100px">
          <el-row>
            <el-col v-bind:span="12">
              <el-form-item label="专业">
                <el-input></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import EditQuestionnaire from '../components/EditQuestionnaire.vue'
export default {
  name: 'QuestionnairePage',
  components: {
    EditQuestionnaire
  }
}
</script>

<style scoped>
  .questionnaire-container {
  }

  .main-container {
    height: 100%;
   }
</style>
