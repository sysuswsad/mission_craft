import Vue from 'vue'
import Router from 'vue-router'
import Api from './views/Api.vue'
import LoginPage from './views/LoginPage.vue'
import RegisterPage from './views/RegisterPage.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LoginPage',
      component: LoginPage
    },
    {
      path: '/api',
      name: 'api',
      component: Api
    },
    {
      path: '/Register',
      name: 'RegisterPage',
      component: RegisterPage
    }
  ]
})
