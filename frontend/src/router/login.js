import { createRouter, createWebHistory } from 'vue-router'
// 导入登录页面组件
import login from '../pages/login.vue'

const routes = [
  // 其他路由...
  {
    path: '/login',  // 访问路径
    component: login // 对应的组件
  }
]

// 告诉Vue Router，当用户在浏览器地址栏输入某个URL（或点击某个链接）时，应该去加载和显示哪个Vue组件
const router = createRouter({
  // history (路由模式)，HTML5 History 模式 (createWebHistory())、Hash 模式 (createWebHashHistory())
  history: createWebHistory(),
  routes
})

export default router