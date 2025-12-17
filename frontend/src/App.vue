<template>
  <!-- 使用标题栏组件 -->
  <header_title />
  <left_layout />
</template>

<script>
// 从当前目录（即 src 目录）下的 components 文件夹中，导入名为 header_title.vue 的文件
// 并将其默认导出（export default）的内容赋值给一个名为 header_title 的变量，建议同名
import header_title from './components/header_title.vue'
import left_layout from './components/left_layout.vue';
export default {
  components: {
    // 等价于 header_title : header_title，前一个header_title是template中，后一个header_title是import的
    header_title,
    left_layout
  }
}
</script>

<style>
</style>