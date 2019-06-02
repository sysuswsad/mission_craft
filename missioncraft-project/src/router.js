import Vue from 'vue'
import Router from 'vue-router'
import Api from './views/Api.vue'
import LoginPage from './views/LoginPage.vue'
import RegisterPage from './views/RegisterPage.vue'
import UserInfoPage from './views/UserInfoPage.vue'
import MessagePage from './views/MessagePage.vue'
import SquarePage from './views/SquarePage'
import QuestionnairePage from './views/QuestionnairePage'
import AnswerQuestionnairePage from "./views/AnswerQuestionnairePage";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/api',
      name: 'api',
      component: Api
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage
    },
    {
      path: '/user',
      name: 'userInfo',
      component: UserInfoPage
    },
    {
      path: '/message',
      name: 'message',
      component: MessagePage
    },
    {
      path: '/square',
      name: 'square',
      component: SquarePage
    },
    {
      path: '/questionnaire',
      name: 'questionnaire',
      component: QuestionnairePage
    },
    {
      path: '/answerQuestionnaire',
      name: 'answerQuestionnaire',
      component: AnswerQuestionnairePage
    }
  ]
})
