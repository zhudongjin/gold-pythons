import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    children:[,
      {
				path: '/',
				name: '蜜蜂帐号',
				component: () => import('@/views/mf/AccountList')
			},
			{
				path: '/mf/accountList',
				name: '蜜蜂帐号',
				component: () => import('@/views/mf/AccountList')
			}
		]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
