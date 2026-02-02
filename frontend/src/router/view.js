import { createRouter, createWebHistory } from 'vue-router'
// 导入登录页面组件
import login from '../pages/login.vue'
import register from '../pages/register.vue'
import home from '../pages/home.vue'
import test_cases_save from '@/pages/test_cases_save.vue'
import monitor from '@/pages/monitor.vue'

const routes = [
  {
    path: '/',
    redirect: '/home', // 将根路径重定向到/home，默认访问首页
  },

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
    path: '/home',
    component: home
  },

  {
    path: '/test-cases/save',
    component: test_cases_save
  },

  {
    path: '/monitor',
    component: monitor
  }
]

// 告诉Vue Router，当用户在浏览器地址栏输入某个URL（或点击某个链接）时，应该去加载和显示哪个Vue组件
const router = createRouter({
  // history (路由模式)，HTML5 History 模式 (createWebHistory())、Hash 模式 (createWebHashHistory())
  history: createWebHistory(),
  routes
})

export default router