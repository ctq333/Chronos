<template>
    <div class="min-h-screen bg-gradient-to-br from-white via-gray-100 to-gray-200 p-6 flex flex-col items-center">
      
      <!-- 周报标题，和大框左对齐 -->
      <div class="max-w-5xl w-full px-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">周报</h2>
      </div>
  
      <!-- 毛玻璃大框 -->
      <div
        class="max-w-5xl w-full px-6 py-8 rounded-lg shadow-xl backdrop-blur-lg bg-white/30 border border-black/40 flex justify-center items-center"
        style="min-height: 75vh; margin-bottom: 5vh;"
      >
        <button
          class="px-6 py-3 border border-gray-700 rounded-lg bg-white/60 hover:bg-white text-gray-800 font-semibold text-lg shadow transition"
          @click="generateReport"
        >
          点此开始生成
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  function generateReport() {
    alert("开始生成周报...");
  }
  </script>
  