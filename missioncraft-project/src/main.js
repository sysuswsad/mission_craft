import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import './theme/element/index.css'
import * as VueCookies from 'vue-cookies'
import vueWaterfallEasy from 'vue-waterfall-easy'

import './filters'

Vue.use(ElementUI)
Vue.use(VueCookies)
Vue.use(vueWaterfallEasy)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
