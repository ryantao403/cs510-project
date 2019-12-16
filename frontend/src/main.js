import Vue from 'vue'
import App from './App.vue'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import store from './store'
import router from './router'
 
Vue.use(Element)
Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App),
  components: { App }
}).$mount('#app')