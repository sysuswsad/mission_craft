<template>
  <div class="main-container">
    <div class="add-button-container">
      <el-card class="add-button-card">
        <el-row type="flex" justify="center">
          <el-button type="primary" plain icon="el-icon-plus" v-on:click="addQuestion(0)" class="add-button">单选题</el-button>
        </el-row>
        <el-row type="flex" justify="center">
          <el-button type="primary" plain icon="el-icon-plus" v-on:click="addQuestion(1)" class="add-button">多选题</el-button>
        </el-row>
        <el-row type="flex" justify="center">
          <el-button type="primary" plain icon="el-icon-plus" v-on:click="addQuestion(2)" class="add-button">填空题</el-button>
        </el-row>
        <el-divider></el-divider>
      </el-card>
    </div>
    <div class="edit-column">
      <el-card>
        <el-form label-width="100px">
          <el-row>
            <el-col>
              <el-form-item label="问卷标题">
                <el-input v-model="interTitle"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <div>
          <div v-for="(q, index) in questions" v-bind:key="index" style="margin-top: 10px">
            <el-card shadow="hover">
              <div>
                <p>{{q.question}}</p>
                <div v-if="q.type === 2">
                  <el-input disabled></el-input>
                </div>
                <div v-else>
                  <el-radio v-for="(c, index) in q.choices" v-bind:key="index" style="margin-top: 10px">{{c}}</el-radio>
                </div>
                <el-button type="primary" plain v-on:click="editAble(index)" class="select-button" v-if="!edit[index]">修改</el-button>
                <el-button type="primary" plain v-on:click="editAble(index)" class="select-button" v-if="edit[index]">收起</el-button>
                <el-button type="primary" plain v-on:click="moveUp(index)" class="select-button">上移</el-button>
                <el-button type="primary" plain v-on:click="moveDown(index)" class="select-button">下移</el-button>
                <el-button type="primary" plain v-on:click="deleteQuestion(index)" class="select-button">删除题目</el-button>
              </div>
            </el-card>
            <el-card v-if="edit[index]">
              <el-form label-width="50px">
                <el-row>
                  <el-col>
                    <el-form-item label="题目">
                      <el-input v-model="questions[index].question" type="textarea">{{questions[index].question}}</el-input>
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
              <div v-if="questions[index].type !== 2">
                <div v-for="(c, indexChoice) in questions[index].choices" v-bind:key="indexChoice">
                  <el-form>
                    <el-row>
                      <el-col>
                        <el-form-item>
                          <el-input v-model="questions[index].choices[indexChoice]" style="width: 80%; height: 50px">{{c}}</el-input>
                          <el-button type="primary" plain icon="el-icon-plus" circle v-on:click="addChoice(index, indexChoice)" class="add-choice"></el-button>
                          <el-button type="primary" plain icon="el-icon-minus" circle v-on:click="deleteChoice(index, indexChoice)"></el-button>
                        </el-form-item>
                      </el-col>
                    </el-row>
                  </el-form>
                </div>
                <el-button class="confirm-button" v-on:click="hideCard(index)" type="primary">确定</el-button>
              </div>
            </el-card>
          </div>
        </div>
      </el-card>
      <el-button type="info" class="show-setting" v-on:click="showSetting">问卷信息设置</el-button>
      <el-card class="questionnaire-set-card" v-if="showMore">
        <el-form v-bind:model="questionnaireSetting" status-icon labelWidth="100px">
          <el-form-item
                  prop="recruitment"
                  label="招募人数"
                  v-bind:rules="{required: true, message: '招募人数（人）', trigger: 'blur'}"
          >
            <el-col :span="11">
              <el-input v-model="questionnaireSetting.money" placeholder="招募人数" prefix-icon="el-icon-s-custom"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item
                  prop="money"
                  label="悬赏金额"
                  v-bind:rules="{required: true, message: '悬赏金额（元/份）', trigger: 'blur'}"
          >
            <el-col :span="11">
              <el-input v-model="questionnaireSetting.money" placeholder="悬赏金额（元/份）" prefix-icon="el-icon-s-custom"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item
                  prop="endTime"
                  label="截止时间"
                  v-bind:rules="{required: true, message: '问卷截至时间', trigger: 'blur'}"
          >
            <el-col :span="11">
              <el-date-picker type="date" placeholder="问卷截至时间" v-model="questionnaireSetting.endTime" style="width: 100%;"></el-date-picker>
            </el-col>
          </el-form-item>
        </el-form>
        <el-button class="summit-button" type="primary" id="login-button">发布问卷</el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuestionnairePage',
  data () {
    return {
      questions: [],
      interTitle: '',
      currentIndex: -1,
      edit: [],
      show: [],
      showMore: false,
      questionnaireSetting: {
        recruitment: '',
        money: '',
        endTime: ''
      }
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
      this.edit.push(false)
      // console.log(this.questions)
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
      // this.currentIndex = index
      let temp = this.edit[index]
      this.edit.splice(index, 1)
      this.edit.splice(index, 0, !temp)
      // this.edit[index] = !this.edit[index]
    },
    addChoice (index, indexChoice) {
      this.questions[index].choices.splice(indexChoice + 1, 0, '选项')
    },
    deleteChoice (index, indexChoice) {
      this.questions[index].choices.splice(indexChoice, 1)
    },
    moveUp (index) {
      if (index === 0) {
        this.showTip('已经到顶啦！')
        return
      }
      let temp1 = this.questions[index - 1]
      let temp2 = this.questions[index]
      this.questions.splice(index - 1, 1, temp2)
      this.questions.splice(index, 1, temp1)
    },
    showTip (str) {
      this.$message.warning(str)
    },
    moveDown (index) {
      if (index === this.questions.length - 1) {
        this.showTip('已经到低啦！')
        return
      }
      let temp1 = this.questions[index + 1]
      let temp2 = this.questions[index]
      this.questions.splice(index + 1, 1, temp2)
      this.questions.splice(index, 1, temp1)
    },
    deleteQuestion (index) {
      this.questions.splice(index, 1)
    },
    showSetting () {
      this.showMore = !this.showMore
    },
    hideCard (index) {
      let temp = this.edit[index]
      this.edit.splice(index, 1)
      this.edit.splice(index, 0, !temp)
    }
  }
}
</script>

<style scoped>
  .main-container {
    overflow: hidden;
  }

  .add-button-container {
    width: 20%;
  }

  .add-button-container > .add-button-card {
    align-items: center;
    position: fixed;
    width: inherit;
  }

  .add-button-card .add-button {
    margin-top: 10px;
    /*padding: 0.618rem 1rem;*/
  }

  .edit-column {
    float: right;
    width: 70%;
  }

  .add-choice {
    margin-left: 10px;
  }

  .summit-button {
    margin-left: 100px;
  }

  .show-setting {
    width: 100%;
  }

  .select-button {
    float: right;
    margin: 10px;
  }

  .confirm-button {
    margin-bottom: 10px;
    width: 100%;
  }
</style>
