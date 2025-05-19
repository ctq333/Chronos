<template>
  <div class="min-h-screen flex flex-col items-center justify-start bg-gradient-to-br p-6">
    <!-- 周报标题，左对齐 -->
    <div class="max-w-6xl w-full px-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <i class="pi pi-file-edit text-gray-500"></i>
        周报
      </h2>
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
          <div class="text-lg text-gray-700">正在生成周报，请稍候...</div>
        </div>
      </template>
      <template v-else-if="step === 'done'">
        <div class="w-full">
          <div class="flex items-center mb-4 gap-2">
            <i class="pi pi-check-circle text-green-500"></i>
            <span class="text-lg font-semibold text-gray-700">周报生成成功</span>
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
    <div class="max-w-6xl w-full px-6 mb-6">
      <div class="flex items-center gap-3 mb-2">
        <i class="pi pi-clock text-gray-400"></i>
        <span class="text-lg font-semibold text-gray-700">历史周报</span>
      </div>
      <div class="flex flex-wrap gap-2 mb-2">
        <Button
          v-for="r in historyReports"
          :key="r.id"
          :label="r.week"
          size="small"
          :outlined="selectedHistory?.id !== r.id"
          :severity="selectedHistory?.id === r.id ? 'primary' : 'secondary'"
          @click="selectedHistory = r"
        />
      </div>
      <div
        v-if="selectedHistory"
        class="bg-white/70 rounded-lg p-4 shadow-inner border border-gray-200 text-gray-800 whitespace-pre-line"
        style="min-height:120px"
      >
        {{ selectedHistory.content }}
      </div>
      <div v-else class="text-gray-400">暂无历史周报</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Button from 'primevue/button'
import axios from 'axios';
import store from '@/store'

const BACKEND_PATH = import.meta.env.VITE_BACKEND_PATH;

const step = ref('init') // 'init' | 'loading' | 'done'
const reportText = ref('')

async function generateReport() {
  step.value = 'loading'
  try {
    const res = await axios.post('/api/llm/weeklyReportGenerate', {}, {
      headers: { Authorization: 'Bearer ' + store.state.token }
    })
    if (res.data.code === 200) {
      reportText.value = res.data.data.content
      step.value = 'done'
      await fetchHistoryReports() // 自动刷新历史
    } else {
      step.value = 'init'
      alert(res.data.message || '生成失败')
    }
  } catch (err) {
    step.value = 'init'
    alert('生成失败: ' + (err.response?.data?.message || err.message))
  }
}

function reset() {
  step.value = 'init'
  reportText.value = ''
}

const historyReports = ref([])

async function fetchHistoryReports() {
  const res = await axios.get('/api/llm/weeklyReportHistory', {
    headers: { Authorization: 'Bearer ' + store.state.token }
  })
  if (res.data.code === 200) {
    historyReports.value = res.data.data
    selectedHistory.value = historyReports.value[0] || null
  }
}
onMounted(fetchHistoryReports)

const selectedHistory = ref(historyReports.value[0] || null)

// 生成后自动保存到历史（可选）
function saveCurrentToHistory() {
  // 假设使用“今年第N周”作为周报标题
  const now = new Date()
  const firstDay = new Date(now.getFullYear(), 0, 1)
  const dayOfYear = Math.floor((now - firstDay) / (24*60*60*1000)) + 1
  const weekNum = Math.ceil(dayOfYear / 7)
  const weekStr = `${now.getFullYear()}年第${weekNum}周`
  historyReports.value.unshift({
    id: Date.now(),
    week: weekStr,
    content: reportText.value
  })
  selectedHistory.value = historyReports.value[0]
}
</script>

<style scoped>
/* 让pi-spin动起来（PrimeIcons自带动画） */
</style>