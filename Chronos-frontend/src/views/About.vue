<template>
  <div class="p-4 max-w-5xl mx-auto flex flex-col space-y-8">
    <!-- 页面标题 -->
    <h2 class="text-3xl font-medium text-gray-800">关于我们 🌟</h2>

    <!-- 系统简介 -->
    <div class="bg-white rounded-xl shadow-sm p-6 space-y-4">
      <div class="flex items-center gap-4">
        <i class="pi pi-globe text-2xl text-blue-500"></i>
        <h3 class="text-xl font-semibold">Chronos</h3>
      </div>
      <p class="text-gray-600 leading-relaxed">
        本系统专注于个人的事项管理与日程规划，通过智能化的任务管理和日程规划功能，能够根据待办事项的优先级和截止日期，自动生成合理的日程规划，帮助用户更清晰地规划每日/每周事务，实现工作与生活的有序平衡。
      </p>
    </div>

    <!-- 开发团队 -->
    <div class="bg-white rounded-xl shadow-sm p-6 space-y-4">
      <div class="flex items-center gap-4">
        <i class="pi pi-code text-2xl text-green-500"></i>
        <h3 class="text-xl font-semibold">开发团队</h3>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="p-3 text-center font-medium bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
          陈天琦
        </div>
        <div class="p-3 text-center font-medium bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
          舒豪
        </div>
        <div class="p-3 text-center font-medium bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
          路晓莹
        </div>
        <div class="p-3 text-center font-medium bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
          谭婕
        </div>
      </div>
    </div>

    <!-- 提供反馈 -->
    <div class="bg-white rounded-xl shadow-sm p-6 space-y-4">
      <div class="flex items-center gap-4">
        <i class="pi pi-comments text-2xl text-purple-500"></i>
        <h3 class="text-xl font-semibold">提供反馈</h3>
      </div>
      <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
        <i class="pi pi-send text-purple-500"></i>
        <span class="font-medium">feedback@smartwork.com</span>
      </div>
      <p class="text-sm text-gray-400">
        我们重视每一条用户建议，工作日24小时内必定回复
      </p>
    </div>
  </div>
</template>

<style scoped>
/* 优化视觉层次 */
.rounded-xl { border-radius: 1rem; }
.shadow-sm { box-shadow: 0 2px 12px rgba(0,0,0,0.05); }

/* 响应式调整 */
@media (min-width: 768px) {
  .grid-cols-4 {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}
</style>