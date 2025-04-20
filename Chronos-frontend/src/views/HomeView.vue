<template>
  <div class="p-4 max-w-5xl mx-auto flex flex-col">
    <!-- 标题 -->
    <h2 class="text-3xl font-medium text-gray-800 mb-6">欢迎 👏</h2>

    <!-- 双列容器 -->
    <div class="flex-1 grid md:grid-cols-2 gap-4">
      <!-- 今日事项 -->
      <div class="bg-white rounded-lg shadow-sm p-4 flex flex-col">
        <h3 class="text-lg font-semibold text-gray-800 text-center mb-4">今日事项</h3>
        <OrderList 
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
                    截止: {{ formatRelativeDate(slotProps.item.deadline) }}
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
        <OrderList 
          v-model="sortedSchedules" 
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
import { ref, computed } from 'vue';
import OrderList from 'primevue/orderlist';

// 示例数据
const tasks = ref([
  { 
    id: 1, 
    title: '项目需求文档提交', 
    deadline: '2025-04-18'
  },
  { 
    id: 2, 
    title: '季度汇报终稿', 
    deadline: '2025-04-20'
  },
  { 
    id: 3, 
    title: '网络学习文档整理', 
    deadline: '2025-05-08'
  },
  // 新增任务样例
  { 
    id: 4,
    title: '系统测试计划审核',
    deadline: '2025-04-25'
  },
  { 
    id: 5,
    title: 'UI界面优化方案确认',
    deadline: '2025-05-02'
  },
  { 
    id: 6,
    title: '后端代码审查会议',
    deadline: '2025-04-22'
  },
  { 
    id: 7,
    title: '生产环境部署计划',
    deadline: '2025-04-28'
  }
]);

const schedules = ref([
  { 
    id: 1, 
    title: '产品设计评审', 
    start: '2025-04-19T21:30',
    end: '2025-04-19T22:00'
  },
  { 
    id: 2, 
    title: '客户演示会议', 
    start: '2025-04-19T14:00',
    end: '2025-04-19T15:30'
  },
  { 
    id: 3, 
    title: '晨间例会', 
    start: '2025-04-19T08:30',
    end: '2025-04-19T09:00'
  },
  // 新增日程样例
  { 
    id: 4,
    title: '团队头脑风暴',
    start: '2025-04-19T10:00',
    end: '2025-04-19T11:30'
  },
  { 
    id: 5,
    title: '新需求评审会',
    start: '2025-04-19T16:00',
    end: '2025-04-19T17:00'
  },
  { 
    id: 6,
    title: '技术培训分享',
    start: '2025-04-19T19:00',
    end: '2025-04-19T20:30'
  },
  { 
    id: 7,
    title: '周工作总结会',
    start: '2025-04-19T22:30',
    end: '2025-04-19T23:00'
  }
]);

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

// 排序后的日程（进行中的排前）
const sortedSchedules = computed(() => {
  return [...schedules.value].sort((a, b) => {
    const aPast = isPastEvent(a);
    const bPast = isPastEvent(b);
    if (aPast === bPast) return 0;
    return aPast ? 1 : -1;
  });
});
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