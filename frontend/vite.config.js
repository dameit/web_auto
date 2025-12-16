import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [
    vue({
      // 禁用Vite的HMR客户端覆盖层
      hmr: false,
    })
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src') // 确保这行存在
    }
  },
  // 或者全局禁用所有客户端覆盖层
  server: {
    hmr: {
      overlay: false, // 禁用错误覆盖层
    }
  }
})