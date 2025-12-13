<template>
  <!-- 标题栏容器 -->
  <header class="header">
    <h1 class="main-page-title">web自动化操作平台</h1>
  </header>
</template>


<style lang="scss">
/* 标题栏容器 - 固定在顶部 */
header {
  position: fixed;      /* 固定定位 */
  top: 0;               /* 紧贴顶部 */
  left: 0;              /* 紧贴左侧 */
  width: 100%;          /* 占满整个宽度 */
  height: 60px;         /* 设置高度 */
  background-color: #409EFF;  /* 背景色（蓝色） */
  color: white;         /* 文字颜色 */
  display: flex;        /* 弹性布局 */
  align-items: center;  /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); /* 阴影效果 */
  z-index: 1000;        /* 确保在最上层 */
}

/* 标题文字样式 */
.main-page-title {
  margin: 0;            /* 去除默认边距 */
  font-size: 20px;      /* 字体大小 */
  font-weight: bold;    /* 加粗 */
  letter-spacing: 1px;  /* 字间距 */
}
</style>