<template>
  <div class="p-4 max-w-5xl mx-auto flex flex-col">
    <!-- 标题 -->
    <h2 class="text-3xl font-medium text-gray-800 mb-6">欢迎 👏</h2>

    <!-- 双列容器 -->
    <div class="flex-1 grid md:grid-cols-2 gap-4">
      <!-- 今日事项 -->
      <div class="bg-white rounded-lg shadow-sm p-4 flex flex-col">
        <h3 class="text-lg font-semibold text-gray-800 text-center mb-4">今日事项</h3>
        <div v-if="taskLoading" class="flex-1 flex items-center justify-center">
          <div class="text-center py-8">
            <i class="pi pi-spinner pi-spin text-primary" style="font-size: 1.5rem"></i>
            <p class="mt-2 text-gray-500">加载中...</p>
          </div>
        </div>
        <div v-else-if="!taskLoading && tasks.length === 0" class="flex-1 flex items-center justify-center">
          <div class="text-center py-8 text-gray-500">
            <i class="pi pi-inbox" style="font-size: 2rem"></i>
            <p class="mt-2">暂无安排</p>
          </div>
        </div>
        <OrderList 
          v-else
          v-model="tasks" 
          dataKey="id"
          :listStyle="{ 'height': '60vh', 'max-height': '60vh'}"
          class="border-t border-gray-100 flex-1" 
        >
          <template #item="slotProps">
            <div class="p-3 hover:bg-gray-50 transition-colors">
              <div class="flex items-center gap-3">
                <i class="pi pi-calendar text-gray-500"></i>
                <div class="flex-1">
                  <div class="font-medium text-gray-800">{{ slotProps.item.title }}</div>
                  <div class="text-sm text-gray-500 mt-1">
                    截止: {{ formatRelativeDate(slotProps.item.dueDate) }}
                  </div>
                </div>
              </div>
            </div>
          </template>
        </OrderList>
      </div>

      <!-- 今日日程 -->
      <div class="bg-white rounded-lg shadow-sm p-4 flex flex-col">
        <h3 class="text-lg font-semibold text-gray-800 text-center mb-4">今日日程</h3>
        <div v-if="scheduleLoading" class="flex-1 flex items-center justify-center">
          <div class="text-center py-8">
            <i class="pi pi-spinner pi-spin text-primary" style="font-size: 1.5rem"></i>
            <p class="mt-2 text-gray-500">加载中...</p>
          </div>
        </div>
        <div v-else-if="!scheduleLoading && schedules.length === 0" class="flex-1 flex items-center justify-center">
          <div class="text-center py-8 text-gray-500">
            <i class="pi pi-inbox" style="font-size: 2rem"></i>
            <p class="mt-2">暂无安排</p>
          </div>
        </div>
        <OrderList 
          v-else
          v-model="schedules" 
          dataKey="id"
          :listStyle="{ 'height': '60vh', 'max-height': '60vh' }"
          class="border-t border-gray-100 flex-1"
        >
          <template #item="slotProps">
            <div 
              :class="['p-3 transition-colors', 
                isPastEvent(slotProps.item) ? 'bg-gray-50 text-gray-400' : 'hover:bg-gray-50']"
            >
              <div class="flex items-center gap-3">
                <i class="pi pi-clock text-gray-500"></i>
                <div class="flex-1">
                  <div class="font-medium">{{ slotProps.item.title }}</div>
                  <div class="text-sm mt-1">
                    {{ formatTimeRange(slotProps.item) }}
                  </div>
                </div>
              </div>
            </div>
          </template>
        </OrderList>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import OrderList from 'primevue/orderlist';
import request from '@/utils/request';
import axios from 'axios';
import { useStore } from 'vuex'

const scheduleLoading = ref(false);
const schedules = ref([]);
const taskLoading = ref(false);
const tasks = ref([]);
const store = useStore();

async function fetchTasks() {
  taskLoading.value = true;
  try {
    const res = await axios.get('/api/task/home', {
      headers: {
        'Authorization': 'Bearer ' + store.state.token
      }
    })
    if (res.data.code === 200) {
      tasks.value = res.data.data.tasks
    } else {
      alert(res.data.message || '获取事项失败')
    }
  } catch (err) {
    alert('获取事项错误: ' + (err.response?.data?.message || err.message))
  } finally {
    taskLoading.value = false; 
  }
}

async function fetchSchedules() {
  scheduleLoading.value = true;
  try {
    const params = {
      start: formatDateObjToStr(new Date()),
      end: formatDateObjToStr(new Date())
    }
    const res = await request.get('/schedule/fetch', { params })
    schedules.value = res.data.data
  } catch (err) {
    console.error('获取日程失败:', err)
  } finally {
    scheduleLoading.value = false; 
  }
}

onMounted(() => {
  fetchTasks();
  fetchSchedules();
})

// function formatDateObjToStr(dateObj) {
//   if (!dateObj) return '';
//   const y = dateObj.getFullYear();
//   const m = (dateObj.getMonth() + 1).toString().padStart(2, '0');
//   const d = dateObj.getDate().toString().padStart(2, '0');
//   return `${y}-${m}-${d}`;
// }

function formatDateObjToStr(dateObj) {
  if (!dateObj) return '';
  // 转换为北京时间 (UTC+8)
  const beijingTime = new Date(dateObj.getTime() + 8 * 60 * 60 * 1000);
  return beijingTime.toISOString().slice(0, 10); // YYYY-MM-DD
}

// 格式化相对日期
const formatRelativeDate = (dateStr) => {
  const date = new Date(dateStr);
  const today = new Date();
  today.setHours(0,0,0,0);
  
  const diffDays = Math.floor((date - today) / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return '今天';
  if (diffDays === 1) return '明天';
  if (diffDays === -1) return '昨天';
  if (diffDays < 0) return `${Math.abs(diffDays)}天前`;
  
  return `${date.getMonth() + 1}月${date.getDate()}日`;
};

// 时间范围格式化
const formatTimeRange = (item) => {
  const start = new Date(item.start).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
  const end = new Date(item.end).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
  return `${start} - ${end}`;
};

// 判断是否过去事件
const isPastEvent = (event) => {
  return new Date(event.end) < new Date();
};
</script>

<style scoped>
/* 容器高度控制 */
.flex-1 { flex: 1 1 0%; }

/* 文本颜色覆盖 */
.text-gray-400 { color: #9ca3af; }
.bg-gray-50 { background-color: #f9fafb; }

/* 基础样式保持 */
.rounded-lg { border-radius: 0.5rem; }
.shadow-sm { box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.border-gray-100 { border-color: #f3f4f6; }

:deep(.p-listbox.p-component){
  width: 100% !important;
}
:deep(.p-3.transition-colors.bg-gray-50.text-gray-400){
  width: 100% !important;
}
</style>