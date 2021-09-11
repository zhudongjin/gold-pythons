import Vue from 'vue'
import Antd from 'ant-design-vue';
import { Icon } from 'ant-design-vue';
import App from './App';
import 'ant-design-vue/dist/antd.css';
import router from './router'
import { axios } from './utils/http'

Vue.config.productionTip = false

Vue.use(Antd);

Vue.prototype.$http = axios

// 图标库
import iconFront from './assets/iconfonts/iconfont.js'
const myIcon = Icon.createFromIconfontCN({
  scriptUrl: iconFront
})
Vue.component('my-icon', myIcon)

new Vue({
  router,
  components: { App },
  render: h => h(App)
}).$mount('#app')
