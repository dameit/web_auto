import { createRouter, createWebHistory } from 'vue-router'
// 导入登录页面组件
import login from '../pages/login.vue'

const routes = [
  // 其他路由...
  {
    path: '/login',  // 访问路径
    name: 'login',   // 路由名称
    component: login // 对应的组件
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router