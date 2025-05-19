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
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import { useStore } from 'vuex'
const store = useStore()

const BACKEND_PATH = import.meta.env.VITE_BACKEND_PATH

const step = ref('init') // 'init' | 'loading' | 'done'
const reportText = ref('')

const historyReports = ref([])
const showHistoryDialog = ref(false)
const selectedHistory = ref(null)

async function generateReport() {
  step.value = 'loading'
  try {
    const res = await axios.post(`${BACKEND_PATH}/llm/generateMonthlyReport`, {}, {
      headers: { Authorization: `Bearer ${store.state.token}` }
    })

    const data = res.data
    console.log("res.data:", data)

    const content = data?.content || '月报生成失败'
    reportText.value = content
    step.value = 'done'
    await loadHistoryReports()
  } catch (err) {
    step.value = 'init'
    reportText.value = '月报生成失败，请稍后重试'
  }
}

function reset() {
  step.value = 'init'
  reportText.value = ''
}

function openHistoryDialog() {
  showHistoryDialog.value = true
  selectedHistory.value = historyReports.value[0] || null
}

async function loadHistoryReports() {
  try {
    const res = await axios.get(`${BACKEND_PATH}/llm/monthly/history`, {
      headers: { Authorization: `Bearer ${store.state.token}` }
    })
    historyReports.value = res.data
  } catch (err) {
    historyReports.value = []
  }
}

onMounted(() => {
  loadHistoryReports()
})
</script>
