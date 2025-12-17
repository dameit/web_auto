import { createRouter, createWebHistory } from 'vue-router'
// 导入登录页面组件
import login from '../pages/login.vue'
import register from '../pages/register.vue'
import left_layout from '@/components/left_layout.vue'
import home from '../pages/home.vue'

const routes = [
  // 其他路由...
  {
    path: '/login',  // 访问路径
    component: login // 对应的组件
  },

  {
    path: '/register',      // 注册页面路径
    component: register     // 对应的组件
  },

  {
    path: '/home',  // 默认子路由，当访问'/home'时，在left_layout的<router-view>中显示home
    component: home
  }
]

// 告诉Vue Router，当用户在浏览器地址栏输入某个URL（或点击某个链接）时，应该去加载和显示哪个Vue组件
const router = createRouter({
  // history (路由模式)，HTML5 History 模式 (createWebHistory())、Hash 模式 (createWebHashHistory())
  history: createWebHistory(),
  routes
})

export default router