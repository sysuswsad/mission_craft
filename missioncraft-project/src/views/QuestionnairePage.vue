<template>
  <div class="questionnaire-container">
    <EditQuestionnaire></EditQuestionnaire>
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
    height: 100%;
  }
</style>
