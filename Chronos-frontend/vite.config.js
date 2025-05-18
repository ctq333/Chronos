import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import tailwindcss from '@tailwindcss/vite';

const env = loadEnv('', process.cwd());
const BACKEND_PATH = env.VITE_BACKEND_PATH;

export default defineConfig({
  plugins: [vue(),
    tailwindcss()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: BACKEND_PATH,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      }
    }    
  }
});