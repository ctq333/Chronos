<template>
    <div class="min-h-screen bg-gradient-to-br from-white via-gray-100 to-gray-200 p-6 flex flex-col items-center">
        <div class="max-w-5xl w-full px-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">日程邀请</h2>
        </div>
        <div class="max-w-5xl w-full bg-white shadow-lg rounded-xl overflow-hidden pt-4" >
        <DataTable
            :value="schedules"
            dataKey="id"
            :paginator="true"
            :rows="10"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            currentPageReportTemplate="显示 {first} 到 {last} 共 {totalRecords} 条日程"
        >
            <!-- 多选框列 -->
            <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
    
            <!-- 日程名称 -->
            <Column field="name" header="日程名称" sortable></Column>
    
            <!-- 时间范围 -->
            <Column field="timeRange" header="时间范围" sortable>
            <template #body="{ data }">
                {{ formatTimeRange(data.startTime, data.endTime) }}
            </template>
            </Column>
    
            <!-- 地点 -->
            <Column field="location" header="地点" sortable></Column>
    
            <!-- 操作栏（接收/拒绝按钮） -->
            <Column header="操作">
            <template #body="{ data }">
                <Button 
                icon="pi pi-check" 
                class="p-button-primary p-button-sm mr-2" 
                @click="acceptSchedule(data.id)"
                label="接收"
                />
                <Button 
                icon="pi pi-times" 
                class="p-button-secondary p-button-sm" 
                @click="rejectSchedule(data.id)"
                label="拒绝"
                />
            </template>
            </Column>
        </DataTable>
        </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Button from 'primevue/button';
  
  const BACKEND_PATH = import.meta.env.VITE_BACKEND_PATH;
  
  // 模拟数据
  const schedules = ref([
    { id: 1, name: '团队周会', startTime: '2023-10-01T09:00:00', endTime: '2023-10-01T10:00:00', location: '会议室A' },
    { id: 2, name: '客户演示', startTime: '2023-10-02T14:00:00', endTime: '2023-10-02T15:30:00', location: '线上会议' },
    { id: 3, name: '项目评审', startTime: '2023-10-03T10:00:00', endTime: '2023-10-03T12:00:00', location: '会议室B' },
  ]);
  
  const selectedSchedules = ref([]); // 多选存储
  
  // 格式化时间范围
  const formatTimeRange = (start, end) => {
    return `${new Date(start).toLocaleString()} - ${new Date(end).toLocaleTimeString()}`;
  };
  
  // 接收日程
  const acceptSchedule = (id) => {
    alert(`已接收日程 ID: ${id}`);
    // 实际调用 API 更新状态
  };
  
  // 拒绝日程
  const rejectSchedule = (id) => {
    alert(`已拒绝日程 ID: ${id}`);
    // 实际调用 API 更新状态
  };
  </script>
  
  <style scoped>
  /* 按钮间距调整 */
  .mr-2 {
    margin-right: 0.5rem;
  }
  </style>