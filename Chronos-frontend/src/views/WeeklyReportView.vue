<template>
    <div class="min-h-screen bg-gradient-to-br from-white via-gray-100 to-gray-200 p-6">
      <h1 class="text-3xl font-bold mb-6 text-gray-800">MonthlyReportView</h1>
  
      <!-- 系统级功能栏 -->
      <div class="w-full border border-gray-300 py-3 text-center font-medium mb-6 rounded-xl bg-white shadow">
        系统级功能栏
      </div>
  
      <!-- 周报模块（毛玻璃浮层）-->
      <div
        class="backdrop-blur-md bg-white/30 border border-gray-200 rounded-2xl p-10 shadow-lg ring-1 ring-gray-300"
      >
        <h2 class="text-xl font-semibold mb-6 text-gray-700">周报</h2>
  
        <div class="border border-gray-300 rounded-xl p-10 flex justify-center items-center bg-white/40">
          <button
            class="px-6 py-3 border border-gray-600 hover:bg-gray-200 rounded-xl text-gray-800 font-medium transition"
            @click="generateReport"
          >
            点此开始生成
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  function generateReport() {
    alert("周报生成中...");
  }
  </script>
  
  <style scoped>
  /* 可继续添加动画或响应式样式 */
  </style>
  