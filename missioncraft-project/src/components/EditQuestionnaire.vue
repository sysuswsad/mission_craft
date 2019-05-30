<template>
  <div class="main-container">
    <div class="add-button-container">
      <el-card style="align-items: center;">
        <el-row>
          <el-button icon="el-icon-plus" v-on:click="addQuestion(0)" style="width: 80%; margin-top: 10px;margin-left: 10%">单选题</el-button>
        </el-row>
        <el-row>
          <el-button icon="el-icon-plus" v-on:click="addQuestion(1)" style="width: 80%; margin-top: 10px;margin-left: 10%">多选题</el-button>
        </el-row>
        <el-row>
          <el-button icon="el-icon-plus" v-on:click="addQuestion(2)" style="width: 80%; margin-top: 10px;margin-left: 10%">填空题</el-button>
        </el-row>
        <el-divider></el-divider>
        <div v-if="questions[currentIndex]">
          <p style="margin-left: 10px">{{modeToStr(questions[this.currentIndex].type)}}</p>
          <el-form label-width="50px">
            <el-row>
              <el-col>
                <el-form-item label="题目">
                  <el-input v-model="questions[currentIndex].question" type="textarea">{{questions[currentIndex].question}</el-input>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <div v-if="questions[currentIndex].type !== 2">
            <div v-for="(c, index) in questions[currentIndex].choices" v-bind:key="index">
              <el-form>
                <el-row>
                  <el-col>
                    <el-form-item>
                      <el-input v-model="questions[currentIndex].choices[index]" style="width: 50%">{{c}}</el-input>
                      <el-button icon="el-icon-plus" circle v-on:click="addChoice(index)"></el-button>
                      <el-button icon="el-icon-minus" circle v-on:click="deleteChoice(index)"></el-button>
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </div>
          </div>
          <el-row style="margin-top: 10px" v-on:click.native="moveUp">
            <el-button>上移</el-button>
          </el-row>
          <el-row style="margin-top: 10px" v-on:click.native="moveDown">
            <el-button>下移</el-button>
          </el-row>
          <el-row style="margin-top: 10px" v-on:click.native="deleteQuestion">
            <el-button>删除题目</el-button>
          </el-row>
        </div>
      </el-card>
    </div>
    <div class="edit-column">
      <el-card>
        <el-form label-width="100px">
          <el-row>
            <el-col>
              <el-form-item label="问卷标题">
                <el-input></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <div>
          <el-card v-for="(q, index) in questions" v-bind:key="index">
            <div>
              <span>{{q.question}}</span>
              <div v-if="q.type === 2">
                <el-input disabled></el-input>
              </div>
              <div v-else>
                <el-radio v-for="(c, index) in q.choices" v-bind:key="index" style="margin-top: 10px">{{c}}</el-radio>
              </div>
              <el-button v-on:click="editAble(index)" style="float: right; margin-bottom: 10px">修改</el-button>
            </div>
          </el-card>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditQuestionnaire',
  data () {
    return {
      questions: [],
      currentIndex: -1,
      show: []
    }
  },
  methods: {
    addQuestion (mode) {
      let temp
      if (mode === 0) {
        temp = { 'type': 0, 'question': '题目描述', 'choices': ['选项1', '选项2'] }
      } else if (mode === 1) {
        temp = { 'type': 1, 'question': '题目描述', 'choices': ['选项1', '选项2'] }
      } else {
        temp = { 'type': 2, 'question': '题目描述' }
      }
      this.questions.push(temp)
      this.show.push(false)
      console.log(this.questions)
    },
    modeToStr (mode) {
      if (mode === 0) {
        return '单选题'
      } else if (mode === 1) {
        return '多选题'
      } else {
        return '填空题'
      }
    },
    editAble (index) {
      this.currentIndex = index
    },
    addChoice (index) {
      this.questions[this.currentIndex].choices.splice(index + 1, 0, '选项')
    },
    deleteChoice (index) {
      this.questions[this.currentIndex].choices.splice(index, 1)
    },
    moveUp () {
      if (this.currentIndex === 0) {
        this.showTip('已经到顶啦！')
        return
      }
      let temp1 = this.questions[this.currentIndex - 1]
      let temp2 = this.questions[this.currentIndex]
      this.questions.splice(this.currentIndex - 1, 1, temp2)
      this.questions.splice(this.currentIndex, 1, temp1)
      this.currentIndex -= 1
    },
    showTip (str) {
      this.$message.error(str)
    },
    moveDown () {
      if (this.currentIndex === this.questions.length - 1) {
        this.showTip('已经到顶啦！')
        return
      }
      let temp1 = this.questions[this.currentIndex + 1]
      let temp2 = this.questions[this.currentIndex]
      this.questions.splice(this.currentIndex + 1, 1, temp2)
      this.questions.splice(this.currentIndex, 1, temp1)
      this.currentIndex += 1
    },
    deleteQuestion () {
      this.questions.splice(this.currentIndex, 1)
    }
  }
}
</script>

<style scoped>
  .main-container {
    transform: translate(0,0);
    width: 100%;
  }
  .add-button-container {
    width: 30%;
    position: fixed;
  }
  .edit-column {
    float: right;
    width: 70%;
  }
</style>
