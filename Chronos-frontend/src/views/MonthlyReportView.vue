<template>
  <div class="min-h-screen flex flex-col items-center justify-start bg-gradient-to-br p-6">
    <!-- 月报标题，左对齐 -->
    <div class="max-w-6xl w-full px-6 flex items-center justify-between">
      <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <i class="pi pi-file-edit text-gray-500"></i>
        月报
      </h2>
      <Button
        label="历史月报"
        icon="pi pi-clock"
        size="small"
        class="mb-2"
        severity="secondary"
        outlined
        @click="openHistoryDialog"
      />
    </div>
    <!-- 毛玻璃大框 -->
    <div
      class="max-w-6xl w-full px-6 py-10 rounded-2xl shadow-lg backdrop-blur-lg bg-white/50 border border-black/30 flex flex-col items-center min-h-[70vh] transition"
      style="margin-bottom: 5vh;"
    >
      <template v-if="step === 'init'">
        <Button
          label="点此开始生成"
          icon="pi pi-play"
          size="large"
          class="px-8 py-3 text-lg"
          @click="generateReport"
        />
      </template>
      <template v-else-if="step === 'loading'">
        <div class="flex flex-col items-center">
          <i class="pi pi-spin pi-spinner text-4xl text-gray-500 mb-6"></i>
          <div class="text-lg text-gray-700">正在生成月报，请稍候...</div>
        </div>
      </template>
      <template v-else-if="step === 'done'">
        <div class="w-full">
          <div class="flex items-center mb-4 gap-2">
            <i class="pi pi-check-circle text-green-500"></i>
            <span class="text-lg font-semibold text-gray-700">月报生成成功</span>
          </div>
          <div class="bg-white/80 rounded-lg p-6 shadow-inner border border-gray-200 text-gray-800 whitespace-pre-line">
            {{ reportText }}
          </div>
          <div class="mt-8 flex justify-center">
            <Button label="重新生成" icon="pi pi-refresh" outlined @click="reset" />
          </div>
        </div>
      </template>
    </div>
    <Dialog v-model:visible="showHistoryDialog" header="历史月报" modal :style="{width: '520px'}">
      <div v-if="historyReports.length">
        <div class="flex gap-2 mb-4 flex-wrap">
          <Button
            v-for="r in historyReports"
            :key="r.id"
            :label="r.month"
            size="small"
            :outlined="selectedHistory?.id !== r.id"
            :severity="selectedHistory?.id === r.id ? 'primary' : 'secondary'"
            @click="selectedHistory = r"
          />
        </div>
        <div class="bg-white/80 rounded-lg p-4 shadow-inner border border-gray-200 text-gray-800 whitespace-pre-line min-h-[200px]">
          {{ selectedHistory?.content || '无内容' }}
        </div>
      </div>
      <div v-else class="text-gray-500 py-6 text-center">暂无历史月报</div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Button from 'primevue/button'

const BACKEND_PATH = import.meta.env.VITE_BACKEND_PATH;

const step = ref('init') // 'init' | 'loading' | 'done'
const reportText = ref('')

function generateReport() {
  step.value = 'loading'
  // 模拟异步生成
  setTimeout(() => {
    // 你可以把这里替换成真实后端接口请求
    reportText.value =
      `【本月工作总结】
- 完成A项目的核心开发与测试工作，按期上线并获好评。
- 推进B系统需求调研，输出需求文档并组织评审。
- 优化了团队周报自动化流程，提升效率20%。
- 参与技术分享2场，推动团队知识交流。

【下月工作计划】
- 启动C平台数据库迁移方案设计与实施。
- 跟进D项目需求变更，确保按时交付。
- 继续参与团队协作与技术提升。

【问题与建议】
- 希望加强跨部门沟通，提前介入项目需求讨论。`
    step.value = 'done'
    saveCurrentToHistory()
  }, 1800)
  
}

function reset() {
  step.value = 'init'
  reportText.value = ''
}

import Dialog from 'primevue/dialog'

const historyReports = ref([
  {
    id: 1,
    month: '2024-04',
    content: `【本月工作总结】
- 参与X项目，与团队协作完成阶段目标。
- 学习新技术栈，输出内部分享文档。

【下月工作计划】
- 深入推进Y业务线开发。
- 组织团队技术交流。

【问题与建议】
- 资源协调有待优化。`
  },
  {
    id: 2,
    month: '2024-03',
    content: `【本月工作总结】
- 完成产品迭代发布。
- 优化线上流程，提升用户满意度。

【下月工作计划】
- 启动新项目需求讨论。
- 加强同其他部门沟通。`
  }
])

const showHistoryDialog = ref(false)
const selectedHistory = ref(null)

function openHistoryDialog() {
  showHistoryDialog.value = true
  selectedHistory.value = historyReports.value[0] || null
}

// 可选：生成后自动保存到历史
function saveCurrentToHistory() {
  const now = new Date()
  const monthStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  historyReports.value.unshift({
    id: Date.now(),
    month: monthStr,
    content: reportText.value
  })
}
</script>

<style scoped>
/* 让pi-spin动起来（PrimeIcons自带动画） */
</style>