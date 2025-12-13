<template>
  <!-- 使用标题栏组件 -->
  <header_title />
  
  <!-- 路由视图 - 页面内容在这里显示 -->
  <router-view />
</template>

<script>
  // 从当前目录（即 src 目录）下的 components 文件夹中，导入名为 header_title.vue 的文件
  // 并将其默认导出（export default）的内容赋值给一个名为 header_title 的变量，建议同名
import header_title from './components/header_title.vue'

export default {
  name: 'App',
  components: {
    // 等价于 header_title : header_title，前一个header_title是template中，后一个header_title是import的
    header_title
  }
}
</script>

<style>
/* 全局样式，确保页面内容不被标题栏遮挡 */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 为所有页面内容添加顶部边距，避免被标题栏遮挡 */
.router-view-content {
  margin-top: 70px;
  padding: 20px;
}
</style>