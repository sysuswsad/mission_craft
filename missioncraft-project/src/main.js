import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import './theme/element/index.css'
import * as VueCookies from 'vue-cookies'
import vueWaterfallEasy from 'vue-waterfall-easy'
import VueFab from 'vue-float-action-button'
import ECharts from 'vue-echarts'

import './filters'

Vue.use(ElementUI)
Vue.use(VueCookies)
Vue.use(vueWaterfallEasy)
Vue.use(VueFab)
Vue.component('v-chart', ECharts)

Vue.config.productionTip = false

let $vue = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
/*
router.beforeEach((to, from, next) => {
  let isLogin = $vue.$cookies.isKey('u-token')
  console.log('kkkk')
  if (!isLogin) {
    if (to.path !== '/login') {
      return next({ path: '/login' })
    } else {
      next()
    }
  } else {
    if (to.path === '/login') {
      return next({ path: '/square' })
    }
    next()
  }
})
*/
export default $vue
