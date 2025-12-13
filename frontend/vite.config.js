import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue({
      // 禁用Vite的HMR客户端覆盖层
      hmr: false,
    })
  ],
  // 或者全局禁用所有客户端覆盖层
  server: {
    hmr: {
      overlay: false, // 禁用错误覆盖层
    }
  }
})