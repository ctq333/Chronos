<template>
  <Toast position="top-center" />
  <div class="p-4 max-w-5xl mx-auto">
    
    <!-- Toolbar -->
    <div class="flex justify-between items-center mb-4">
      <div>
        <Button label="创建日程" icon="pi pi-plus" @click="openCreateDialog" class="mr-2" />
        <Button label="日程智能创建" icon="pi pi-comments" severity="info" @click="openLLMDialog" />
      </div>
      <div>
        <SelectButton
          v-model="viewMode"
          :options="viewModes"
          optionLabel="label"
          optionValue="value"
        >
          <template #option="slotProps">
            <i :class="slotProps.option.icon" style="margin-right:6px"></i>
            {{ slotProps.option.label }}
          </template>
        </SelectButton>
      </div>
    </div>

    <!-- List View -->
    <div v-if="viewMode==='list'">
      <Calendar
        v-model="dateRange"
        selectionMode="range"
        dateFormat="yy-mm-dd"
        :showIcon="true"
        placeholder="开始日期 - 结束日期"
        :manualInput="false"
        class="w-70 mb-4"
      />
      <div v-if="loading" class="text-center py-8">
        <i class="pi pi-spinner pi-spin text-primary" style="font-size: 1.5rem"></i>
        <p class="mt-2 text-gray-500">加载中...</p>
      </div>
      <div v-else-if="schedules.length === 0" class="text-gray-500 text-center mt-8">
        暂无日程
      </div>
      <div v-else class="grid gap-4">
        <Card v-for="event in schedules" :key="event.id" class="w-full">
          <template #title>
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <span>{{ event.title }}</span>
              <span class="text-sm text-gray-500">
                {{ eventTimeRange(event) }} ({{ event.start.split('T')[0] }})
              </span>
            </div>
          </template>
          <template #content>
            <div class="mb-2">
              <i class="pi pi-map-marker text-gray-500 mr-2"></i>{{ event.location || '暂未记录地点' }}
            </div>
            <div v-if="event.link" class="mb-2">
              <i class="pi pi-link text-gray-500 mr-2"></i>
              <a :href="event.link" target="_blank" class="text-blue-600 underline break-all">{{ event.link }}</a>
            </div>
            <div class="mb-2 text-gray-600">{{ event.description || '暂无描述' }}</div>
            <div class="flex gap-2 mt-2">
              <Button icon="pi pi-pencil" rounded text class="p-button-sm" @click="openEditDialog(event)" />
              <Button icon="pi pi-trash" rounded text severity="danger" class="p-button-sm" @click="openDeleteDialog(event)" />
              <Button
                icon="pi pi-user-plus"
                rounded
                text
                severity="info"
                class="p-button-sm"
                @click="openInviteDialog(event)"
                title="邀请成员"
              />
            </div>
          </template>
        </Card>
      </div>
    </div>

    <!-- Calendar View with Timeline -->
    <div v-else>
      <div class="flex flex-col md:flex-row gap-4 mb-4">
        <!-- 日历选择器区域 -->
        <div class="md:w-[22rem] w-full flex-shrink-0">
          <Calendar v-model="selectedDate" dateFormat="yy-mm-dd" inline class="w-full" />
        </div>
        <!-- Timeline 区域 -->
        <div class="flex-1 min-w-0">
          <div v-if="loading" class="text-center py-8">
            <i class="pi pi-spinner pi-spin text-primary" style="font-size: 1.5rem"></i>
            <p class="mt-2 text-gray-500">加载中...</p>
          </div>
          <div v-else-if="events.length === 0" class="text-gray-500 text-center mt-8">
            当天暂无日程
          </div>
          <Timeline :value="events" align="alternate" v-else>
            <template #content="slotProps">
              <Card class="w-full">
                <template #title>
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <span>{{ slotProps.item.title }}</span>
                    <span class="text-sm text-gray-500">{{ eventTimeRange(slotProps.item) }}</span>
                  </div>
                </template>
                <template #content>
                  <div class="mb-2">
                    <i class="pi pi-map-marker text-gray-500 mr-2"></i>{{ slotProps.item.location || '未填写地点' }}
                  </div>
                  <div v-if="slotProps.item.link" class="mb-2">
                    <i class="pi pi-link text-gray-500 mr-2"></i>
                    <a :href="slotProps.item.link" target="_blank" class="text-blue-600 underline break-all">{{ slotProps.item.link }}</a>
                  </div>
                  <div class="mb-2 text-gray-600">{{ slotProps.item.description || '无描述' }}</div>
                  <div class="flex gap-2 mt-2">
                    <Button icon="pi pi-pencil" rounded text class="p-button-sm" @click="openEditDialog(slotProps.item)" />
                    <Button icon="pi pi-trash" rounded text severity="danger" class="p-button-sm" @click="openDeleteDialog(slotProps.item)" />
                    <Button
                      icon="pi pi-user-plus"
                      rounded
                      text
                      severity="info"
                      class="p-button-sm"
                      @click="openInviteDialog(event)"
                      title="邀请成员"
                    />
                  </div>
                </template>
              </Card>
            </template>
          </Timeline>
        </div>
      </div>
    </div>

    <!-- Create/Edit Schedule Dialog -->
    <Dialog v-model:visible="showDialog" :header="dialogMode==='create'?'新建日程':'编辑日程'" :modal="true" :closable="false" :style="{width:'400px'}">
      <form @submit.prevent="onSubmit">
        <div class="mb-3">
          <label>主题 *</label>
          <InputText v-model="form.title" maxlength="50" class="w-full" />
        </div>
        <div class="mb-3 flex gap-2">
          <div class="flex-1">
            <label>开始日期 *</label>
            <Calendar v-model="form.startDate" dateFormat="yy-mm-dd" showIcon class="w-full" />
          </div>
          <div class="flex-1">
            <label>开始时间 *</label>
            <InputText v-model="form.startTime" placeholder="HH:mm" class="w-full" />
          </div>
        </div>
        <div class="mb-3 flex gap-2">
          <div class="flex-1">
            <label>结束日期 *</label>
            <Calendar v-model="form.endDate" dateFormat="yy-mm-dd" showIcon class="w-full" />
          </div>
          <div class="flex-1">
            <label>结束时间 *</label>
            <InputText v-model="form.endTime" placeholder="HH:mm" class="w-full" />
          </div>
        </div>
        <div class="mb-3">
          <label>地点</label>
          <InputText v-model="form.location" maxlength="100" class="w-full" />
        </div>
        <div class="mb-3">
          <label>链接</label>
          <InputText v-model="form.link" maxlength="200" class="w-full" placeholder="如 https://..."/>
        </div>
        <div class="mb-3">
          <label>描述</label>
          <Textarea v-model="form.description" maxlength="500" rows="3" class="w-full" />
        </div>
        <div class="flex justify-end gap-2">
          <Button label="取消" icon="pi pi-times" severity="secondary" @click="showDialog=false; submitLoading = false" type="button" :disabled="submitLoading"/>
          <Button :label="dialogMode==='create'?'创建':'保存'" icon="pi pi-check" :loading="submitLoading" type="submit" />
        </div>
      </form>
    </Dialog>

    <!-- Delete Schedule Dialog -->
    <Dialog 
      v-model:visible="showDeleteDialog" 
      header="确认删除" 
      :modal="true" 
      :style="{ width: '350px' }"
    >
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>确定要删除日程 "{{ scheduleToDelete?.title }}" 吗？</span>
      </div>
      <template #footer>
        <Button 
          label="取消" 
          icon="pi pi-times" 
          @click="showDeleteDialog = false; submitLoading = false" 
          :disabled="submitLoading"
          text 
        />
        <Button 
          label="删除" 
          icon="pi pi-check"
          :loading="submitLoading"
          @click="confirmDelete" 
          severity="danger" 
          autofocus
        />
      </template>
    </Dialog>

    <!-- Invite Dialog -->
    <Dialog v-model:visible="showInviteDialog" header="邀请成员" modal :style="{width:'350px'}">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">用户名</label>
          <InputText v-model="inviteUser" placeholder="输入用户名" class="w-full" />
        </div>
        <div class="flex justify-end gap-2">
          <Button label="取消" icon="pi pi-times" severity="secondary" @click="showInviteDialog=false; submitLoading=false" :disabled="submitLoading"/>
          <Button
            label="邀请"
            icon="pi pi-user-plus"
            :loading="submitLoading"
            :disabled="!inviteUser"
            @click="sendInvite"
          />
        </div>
        <div v-if="inviteResult" :class="inviteResult.success ? 'text-green-600' : 'text-red-500'">
          {{ inviteResult.message }}
        </div>
      </div>
    </Dialog>

    <!-- LLM Dialog with Editable Multiple Schedules & Delete -->
    <Dialog v-model:visible="showLLMDialog" header="LLM智能创建日程" modal style="width: 700px">
      <div>
        <Textarea
          v-model="llmInput"
          :autoResize="false"
          rows="5"
          style="max-height:120px;overflow-y:auto"
          placeholder="请输入自然语言描述，例如：明天下午3点去医院看牙医，晚上7点吃饭"
          class="w-full"
        />
        <Button label="生成日程" class="mt-2" icon="pi pi-send" @click="handleLLMCreate" />
      </div>
      <div v-if="llmResults.length" class="mt-4 space-y-4">
        <div
          v-for="(sch, idx) in llmResults"
          :key="sch._uid"
          class="p-2 bg-gray-100 rounded relative"
        >
          <div class="flex justify-between">
            <b>日程{{ idx + 1 }}</b>
            <Button
              icon="pi pi-trash"
              class="p-button-sm absolute top-2 right-2"
              severity="danger"
              text
              @click="removeLLMSchedule(idx)"
              title="删除该日程"
            />
          </div>
          <div class="grid grid-cols-2 gap-2 mt-2">
            <div>
              <label class="block text-xs text-gray-500 mb-1">主题</label>
              <InputText v-model="sch.title" class="w-full" />
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">地点</label>
              <InputText v-model="sch.location" class="w-full" />
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">开始日期</label>
              <InputText v-model="sch.start_date" class="w-full" />
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">开始时间</label>
              <InputText v-model="sch.start_time" class="w-full" />
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">结束日期</label>
              <InputText v-model="sch.end_date" class="w-full" />
            </div>
            <div>
              <label class="block text-xs text-gray-500 mb-1">结束时间</label>
              <InputText v-model="sch.end_time" class="w-full" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs text-gray-500 mb-1">链接</label>
              <InputText v-model="sch.link" class="w-full" placeholder="如 https://..." />
            </div>
            <div class="col-span-2">
              <label class="block text-xs text-gray-500 mb-1">描述</label>
              <InputText v-model="sch.description" class="w-full" />
            </div>
          </div>
        </div>
        <Button label="确认创建全部" icon="pi pi-check" class="mt-2" @click="confirmLLMSchedules" :disabled="llmResults.length===0" />
      </div>
    </Dialog>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import Button from 'primevue/button';
import SelectButton from 'primevue/selectbutton';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Calendar from 'primevue/calendar';
import Textarea from 'primevue/textarea';
import Card from 'primevue/card';
import Timeline from 'primevue/timeline';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import request from '@/utils/request';

const loading = ref(false);
const submitLoading = ref(false);
const toast = useToast();

const viewMode = ref('list');
const viewModes = [
  { label: '列表', value: 'list', icon: 'pi pi-list' },
  { label: '日历', value: 'calendar', icon: 'pi pi-calendar' }
];
const schedules = ref([]);
const dateRange = ref([]);
const events = ref([]);
const selectedDate = ref(new Date());

const showDialog = ref(false);     // 开启创建/编辑框
const dialogMode = ref('create');
const editId = ref(null);
const emptyForm = {
  title: '', startDate: '', startTime: '', endDate: '', endTime: '', location: '', link: '', description: ''
};
const form = ref({ ...emptyForm });   // 编辑框中的内容

const showDeleteDialog = ref(false);
const scheduleToDelete = ref(null);

const showInviteDialog = ref(false);
const inviteUser = ref('');
const inviteEventId = ref(null);
const inviteResult = ref(null);

const showLLMDialog = ref(false);
const llmInput = ref('');
const llmResults = ref([]);

// 设置默认日期范围
function getDefaultDateRange() {
  const now = new Date();
  const beijingOffset = 8 * 60 * 60 * 1000; // 8小时的毫秒数
  const today = new Date(now.getTime() + beijingOffset);
  today.setUTCHours(0, 0, 0, 0); // 使用UTC方法
  const endDate = new Date(today);
  endDate.setUTCDate(today.getUTCDate() + 6); // 6天后
  endDate.setUTCHours(23, 59, 59, 999);
  return [
    new Date(today.getTime() - beijingOffset),
    new Date(endDate.getTime() - beijingOffset)
  ];
}

// 获取列表页日程数据
async function fetchSchedules(start, end) {
  loading.value = true;
  try {
    const params = {
      start: formatDateObjToStr(start),
      end: formatDateObjToStr(end)
    }
    
    const res = await request.get('/schedule/fetch', { params })
    if(res.data.code === 200){
      schedules.value = res.data.data
    }else{
      toast.add({
        severity: 'error',
        summary: '错误',
        detail: res.data.message,
        life: 3000
      });
    }
  } catch (err) {
    console.error('获取日程失败:', err)
  } finally {
    loading.value = false; 
  }
}

// 获取日历页日程数据
async function fetchEvents(date) {
  loading.value = true;
  try {
    const params = {
      start: formatDateObjToStr(date),
      end: formatDateObjToStr(date)
    }
    const res = await request.get('/schedule/fetch', { params })
    if(res.data.code === 200){
      events.value = res.data.data
    }else{
      toast.add({
        severity: 'error',
        summary: '错误',
        detail: res.data.message,
        life: 3000
      });
    }
  } catch (err) {
    console.error('获取日程失败:', err)
  } finally {
    loading.value = false; 
  }
}

// 初始化
onMounted(() => {
  dateRange.value = getDefaultDateRange()
})

// 监听日期范围变化
watch(dateRange, (newVal) => {
  if (newVal && newVal[0] && newVal[1]) {
    fetchSchedules(newVal[0], newVal[1])
  }
})
watch(selectedDate, (newVal) => {
  if (newVal) {
    fetchEvents(newVal)
  }
})

function eventTimeRange(event) {
  if (event.end && event.end !== event.start) {
    return `${event.start.slice(11, 16)} - ${event.end.slice(11, 16)}`;
  } else {
    return event.start.slice(11,16);
  }
}

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

function openCreateDialog() {
  dialogMode.value = 'create';
  Object.assign(form.value, emptyForm);
  showDialog.value = true;
}

function openEditDialog(row) {
  dialogMode.value = 'edit';
  editId.value = row.id;
  form.value = {
    title: row.title,
    startDate: new Date(row.start.split('T')[0]), // 字符串转 Date
    startTime: row.start.split('T')[1].slice(0,5),
    endDate: row.end ? new Date(row.end.split('T')[0]) : new Date(row.start.split('T')[0]),
    endTime: row.end ? row.end.split('T')[1].slice(0,5) : row.start.split('T')[1].slice(0,5),
    location: row.location,
    link: row.link || '',
    description: row.description
  };
  showDialog.value = true;
}

function openDeleteDialog(row) {
  scheduleToDelete.value = row;
  showDeleteDialog.value = true;
}

function openInviteDialog(event) {
  showInviteDialog.value = true;
  inviteUser.value = '';
  inviteResult.value = null;
  inviteEventId.value = event.id;
}

// 提交表单
async function onSubmit() {
  if (!form.value.title || !form.value.startDate || !form.value.startTime || !form.value.endDate || !form.value.endTime) {
    toast.add({
      severity: 'warn',
      summary: '警告',
      detail: '请填写所有必填（*标）字段',
      life: 3000
    });
    return;
  }

  const startDateStr = formatDateObjToStr(form.value.startDate);
  const endDateStr = formatDateObjToStr(form.value.endDate);
  const start = `${startDateStr}T${form.value.startTime}:00`;
  const end = `${endDateStr}T${form.value.endTime}:00`;

  const timeFormatRegex = /^([01][0-9]|2[0-3])(:[0-5][0-9])?$/;  // 验证时间格式
  if (!timeFormatRegex.test(form.value.startTime)) {
    toast.add({
      severity: 'warn',
      summary: '警告',
      detail: '开始时间格式不正确，请使用 HH 或 HH:mm 格式，如 09 或 14:30',
      life: 3000
    });
    return;
  }else if (!timeFormatRegex.test(form.value.endTime)) {
    toast.add({
      severity: 'warn',
      summary: '警告',
      detail: '结束时间格式不正确，请使用 HH 或 HH:mm 格式，如 09 或 14:30',
      life: 3000
    });
    return;
  }

  if (new Date(start) > new Date(end)) {
    toast.add({
      severity: 'warn',
      summary: '警告',
      detail: '结束时间必须晚于开始时间',
      life: 3000
    });
    return;
  }

  const payload = {
    title: form.value.title,
    start,
    end,
    location: form.value.location || null,
    link: form.value.link || null,
    description: form.value.description || null
  };

  try{
    submitLoading.value = true;
    if (dialogMode.value === 'create') {
      const res = await request.post('/schedule/create', payload);
      if(res.data.code === 200){
        toast.add({
          severity: 'success',
          summary: '成功',
          detail: '日程创建成功',
          life: 3000
        });
      }else{
        toast.add({
          severity: 'error',
          summary: '错误',
          detail: res.data.message,
          life: 3000
        });
      }
    } else if (dialogMode.value === 'edit') {
      const res = await request.post(`/schedule/update/${editId.value}`, payload);
      if(res.data.code === 200){
        toast.add({
          severity: 'success',
          summary: '成功',
          detail: '日程修改成功',
          life: 3000
        });
      }else{
        toast.add({
          severity: 'error',
          summary: '错误',
          detail: res.data.message,
          life: 3000
        });
      }
    }
  }catch (err) {
    console.error('日程创建/更新失败:', err)
  }finally {
    submitLoading.value = false; 
    showDialog.value = false;
    fetchSchedules(dateRange.value[0], dateRange.value[1]);
    fetchEvents(selectedDate.value);
  }
}

// 确认删除
async function confirmDelete() {
  if (!scheduleToDelete.value) return

  submitLoading.value = true;
  try {
    const res = await request.delete(`/schedule/delete/${scheduleToDelete.value.id}`)
    if(res.data.code === 200){
      schedules.value = schedules.value.filter(s => s.id !== scheduleToDelete.value.id)
      toast.add({
        severity: 'success',
        summary: '删除成功',
        detail: `日程 "${scheduleToDelete.value.title}" 已删除`,
        life: 3000
      })
    }else{
      toast.add({
        severity: 'error',
        summary: '错误',
        detail: res.data.message,
        life: 3000
      });
    }
  } catch (err) {
    console.error('删除失败:', err)
  } finally {
    showDeleteDialog.value = false;
    scheduleToDelete.value = null;
    submitLoading.value = false;
  }
}

// 发送邀请
async function sendInvite() {
  submitLoading.value = true;

  try {
    const payload = {
      scheduleId : inviteEventId.value,
      receiver : inviteUser.value
    };
    const res = await request.post(`/schedule/invite`, payload);
    if(res.data.code === 200){
      inviteResult.value = { success: true, message: `已向 ${inviteUser.value} 发送邀请` };
      inviteUser.value = '';
    }else{
      inviteResult.value = { success: false, message: '未找到该用户' };
    }
  } catch (e) {
    inviteResult.value = { success: false, message: '未找到该用户' };
  } finally {
    submitLoading.value = false;
  }
}

function openLLMDialog() {
  showLLMDialog.value = true;
  llmInput.value = '';
  llmResults.value = [];
}

async function handleLLMCreate() {
  if (!llmInput.value.trim()) {
    toast.add({
      severity: 'warn',
      summary: '警告',
      detail: '请输入自然语言描述',
      life: 3000
    });
    return;
  }
  try {
    llmResults.value = [];
    const res = await request.post('/llm/createSchedule', {
      paragraph: llmInput.value
    });
    if (Array.isArray(res.data)) {
      llmResults.value = res.data.map(item => ({
        _uid: Math.random().toString(36).slice(2),
        title: item.topic || '',
        location: item.location || '',
        link: (item.links && item.links.length) ? item.links[0] : '',
        description: item.notes || '',
        start_date: item.startTime ? item.startTime.split(' ')[0] : '',
        start_time: item.startTime ? item.startTime.split(' ')[1].slice(0,5) : '',
        end_date: item.endTime ? item.endTime.split(' ')[0] : '',
        end_time: item.endTime ? item.endTime.split(' ')[1].slice(0,5) : ''
      }));
    } else {
      toast.add({
        severity: 'error',
        summary: '生成失败',
        detail: 'AI未解析到日程，请重试',
        life: 3000
      });
    }
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: '生成失败',
      detail: err.response?.data?.message || err.message,
      life: 4000
    });
  }
}

function removeLLMSchedule(idx) {
  llmResults.value.splice(idx, 1);
}

async function confirmLLMSchedules() {
  // 校验
  const validSchedules = llmResults.value.filter(
    sch => sch.title && sch.start_date && sch.start_time && sch.end_date && sch.end_time
  );
  if (!validSchedules.length) {
    toast.add({
      severity: 'warn',
      summary: '警告',
      detail: '没有可用日程',
      life: 3000
    });
    return;
  }

  const payload = {
    schedules: validSchedules.map(sch => ({
      title: sch.title,
      start: `${sch.start_date}T${sch.start_time}`,
      end: `${sch.end_date}T${sch.end_time}`,
      location: sch.location,
      link: sch.link,
      description: sch.description
    }))
  };

  try {
    const res = await request.post('/schedule/batch_create', payload);
    if (res.data.code === 201) {
      // 直接刷新日程数据
      showLLMDialog.value = false;
      await fetchSchedules(dateRange.value[0], dateRange.value[1]);
      await fetchEvents(selectedDate.value);
      toast.add({
        severity: 'success',
        summary: '成功',
        detail: '批量创建成功',
        life: 3000
      });
    } else {
      toast.add({
        severity: 'error',
        summary: '错误',
        detail: res.data.message || '批量创建失败',
        life: 4000
      });
    }
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: '错误',
      detail: err.response?.data?.message || err.message,
      life: 4000
    });
  }
}

</script>

<style scoped>
.p-button-sm {
  font-size: 0.8rem;
  padding: 0.3rem 0.6rem;
}
.break-all { word-break: break-all; }
.relative { position: relative; }
.absolute { position: absolute; }
.top-2 { top: .5rem; }
.right-2 { right: .5rem; }
</style>