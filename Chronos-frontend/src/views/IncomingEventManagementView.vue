<template>
<Toast position="top-center" />
<div class="min-h-screen bg-gradient-to-br from-white via-gray-100 to-gray-200 p-6 flex flex-col items-center">
  <div class="max-w-5xl w-full px-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">日程邀请</h2>
  </div>
    <div class="max-w-5xl w-full bg-white shadow-lg rounded-xl overflow-hidden pt-4" >
      <DataTable
        :value="invitations"
        dataKey="id"
        :paginator="true"
        :rows="10"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="显示 {first} 到 {last} 共 {totalRecords} 条日程"
      >
        <Column field="name" header="主题"></Column>
        <Column field="timeRange" header="时间" sortable>
          <template #body="{ data }">
            {{ formatTimeRange(data.startTime, data.endTime) }}
          </template>
        </Column>
        <Column field="location" header="地点"></Column>
        <Column field="sender" header="邀请人"></Column>
        <Column header="操作">
          <template #body="{ data }">
            <Button 
              icon="pi pi-check" 
              class="p-button-primary p-button-sm mr-2" 
              :disabled="loading_id"
              :loading="data.id === loading_id && loading_mode === 'accept'"
              @click="acceptSchedule(data.id)"
              label="接收"
            />
            <Button 
              icon="pi pi-times" 
              class="p-button-secondary p-button-sm" 
              :disabled="loading_id"
              :loading="data.id === loading_id && loading_mode === 'reject'"
              @click="rejectSchedule(data.id)"
              label="拒绝"
            />
          </template>
        </Column>
        <!-- 加载或无数据 -->
        <template #empty>
          <div class="text-center py-8">
            <template v-if="loading">
              <i class="pi pi-spinner pi-spin text-primary" style="font-size: 1.5rem"></i>
              <p class="mt-2 text-gray-500">加载中...</p>
            </template>
            <template v-else>
              <p class="text-gray-500">暂无日程邀请</p>
            </template>
          </div>
        </template>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import request from '@/utils/request';

const loading = ref(false);
const toast = useToast();
const invitations = ref([]);
const loading_id = ref();
const loading_mode = ref();

// 获取邀请数据
async function fetchInvitations() {
  loading.value = true;
  try {
    const res = await request.get('/invitation/fetch', null)
    invitations.value = res.data.data
  } catch (err) {
    console.error('获取邀请失败:', err)
  } finally {
    loading.value = false; 
  }
}

// 初始化
onMounted(() => {
  fetchInvitations();
})


// 格式化时间范围
const formatTimeRange = (start, end) => {
  return `${new Date(start).toLocaleString()} - ${new Date(end).toLocaleTimeString()}`;
};

// 接收日程
async function acceptSchedule(id) {
  loading_id.value = id;
  loading_mode.value = "accept";
  try {
    const res = await request.post('/invitation/accept', { id: id });
    if (res.data.code === 200) {
      toast.add({ severity: 'success', summary: '成功', detail: '已接收日程邀请', life: 3000 });
      invitations.value = invitations.value.filter(s => s.id !== id)
    } else {
      toast.add({ severity: 'error', summary: '错误', detail: res.data.message, life: 3000 });
    }
  } catch (err) {
    console.error('接受邀请失败:', err);
  } finally {
    loading_id.value = null;
    loading_mode.value = null;
  }
};

// 拒绝日程
async function rejectSchedule(id) {
  loading_id.value = id;
  loading_mode.value = "reject";
  try {
    const res = await request.post('/invitation/reject', { id: id });
    if (res.data.code === 200) {
      toast.add({ severity: 'success', summary: '成功', detail: '已拒绝日程邀请', life: 3000 });
      invitations.value = invitations.value.filter(s => s.id !== id)
    } else {
      toast.add({ severity: 'error', summary: '错误', detail: res.data.message, life: 3000 });
    }
  } catch (err) {
    console.error('接受邀请失败:', err);
  } finally {
    loading_id.value = null;
    loading_mode.value = null;
  }
};
</script>

<style scoped>
/* 按钮间距调整 */
.mr-2 {
  margin-right: 0.5rem;
}
</style>