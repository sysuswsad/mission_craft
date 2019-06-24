<template>
  <div class="question-container">
    <el-card class="question-card">
      <template v-slot:header>
        <h2>{{questionnaire.title}}</h2>
      </template>
      <div v-for="(q, index) in questionnaire.questions" v-bind:key="index">
        <div v-if="q.type === 0">
          <h1>（单选）{{q.question}}</h1>
          <el-radio v-for="(c, indexC) in q.choices" v-bind:key="indexC" v-model="answers[index]" v-bind:label="indexC">{{c}}</el-radio>
        </div>
        <div v-else-if="q.type === 1">
          <h1>（多选）{{q.question}}</h1>
          <el-checkbox-group v-model="answers[index]">
            <el-checkbox v-for="(c, indexC) in q.choices" v-bind:key="indexC" v-bind:label="indexC">{{c}}</el-checkbox>
          </el-checkbox-group>
        </div>
        <div v-else>
          <h1>（填空）{{q.question}}</h1>
          <el-input type="textarea" v-model="answers[index]"></el-input>
        </div>
        <el-divider v-if="index !== questionnaire.questions.length - 1"></el-divider>
      </div>
      <el-button class="summit-button" type="primary" v-on:click="summit">提交</el-button>
    </el-card>
  </div>
</template>

<script>
import backend from '../backend'
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
      answers: []
    }
  },
  created: function () {
    console.log(this.$route.params.missionId)
    console.log(this.$route.params.orderId)
    backend.getRequest('mission/', {
      mission_id: this.$route.params.missionId
    }).then((response) => {
      this.questionnaire.questions = response.data.data['mission']['problems']
      this.questionnaire.title = response.data.data['mission']['title']
      for (let i = 0; i < this.questionnaire.questions.length; i++) {
        if (this.questionnaire.questions[i].type === 1) {
          this.answers.push([])
        } else {
          this.answers.push('')
        }
      }
    }).catch(() => {
    })
  },
  methods: {
    summit () {
      console.log(this.answers)
      backend.putRequest('order/', {
        order_id: this.$route.params.orderId,
        answers: this.answers
      }).then((response) => {
        console.log(response)
      }).catch(() => {
      })
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
    margin-top: 20px;
  }
</style>
