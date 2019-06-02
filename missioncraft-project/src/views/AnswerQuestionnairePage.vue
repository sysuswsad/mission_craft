<template>
  <div class="question-container">
    <el-card class="question-card">
      <h2>{{questionnaire.title}}</h2>
      <el-divider></el-divider>
      <div v-for="(q, index) in questionnaire.questions" v-bind:key="index">
        <div v-if="q.type === 0">
          <h1>（单选）{{q.question}}</h1>
          <el-radio v-for="(c, indexC) in q.choices" v-bind:key="indexC" v-model="answer[index]" v-bind:label="indexC">{{c}}</el-radio>
        </div>
        <div v-else-if="q.type === 1">
          <h1>（多选）{{q.question}}</h1>
          <el-checkbox-group v-model="answer[index]">
            <el-checkbox v-for="(c, indexC) in q.choices" v-bind:key="indexC" v-bind:label="indexC">{{c}}</el-checkbox>
          </el-checkbox-group>
        </div>
        <div v-else>
          <h1>（填空）{{q.question}}</h1>
          <el-input type="textarea" v-model="answer[index]"></el-input>
        </div>
        <el-divider></el-divider>
      </div>
      <el-button class="summit-button" type="primary" v-on:click="summit">提交</el-button>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AnswerQuestionnairePage',
  data () {
    return {
      questionnaire: {
        title: '我的问卷',
        questions: [
          { 'type': 0, 'question': '这是单选题', 'choices': ['我是a', '我是b'] },
          { 'type': 1, 'question': '这是多选题', 'choices': ['选项1', '选项2'] },
          { 'type': 2, 'question': '这是填空题', 'choices': ['选项1', '选项2'] }
        ]
      },
      answer: []
    }
  },
  created: function () {
    for (let i = 0; i < this.questionnaire.questions.length; i++) {
      if (this.questionnaire.questions[i].type === 1) {
        this.answer.push([])
      } else {
        this.answer.push('')
      }
    }
  },
  methods: {
    summit () {
      console.log(this.answer)
    }
  }
}
</script>

<style scoped>
  .question-container {
    height: 100%;
  }

  .question-card {
    width: 70vw;
    margin: auto;
  }

  .summit-button {
    width: 100%;
  }
</style>
