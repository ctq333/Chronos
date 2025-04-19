<template>
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
        <div v-if="schedules.length === 0" class="text-gray-500 text-center mt-8">
          暂无日程
        </div>
        <div class="grid gap-4">
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
                <i class="pi pi-map-marker text-gray-500 mr-2"></i>{{ event.location || '未填写地点' }}
              </div>
              <div v-if="event.link" class="mb-2">
                <i class="pi pi-link text-gray-500 mr-2"></i>
                <a :href="event.link" target="_blank" class="text-blue-600 underline break-all">{{ event.link }}</a>
              </div>
              <div class="mb-2 text-gray-600">{{ event.description || '无描述' }}</div>
              <div class="flex gap-2 mt-2">
                <Button icon="pi pi-pencil" rounded text class="p-button-sm mr-2" @click="openEditDialog(event)" />
                <Button icon="pi pi-trash" rounded text severity="danger" class="p-button-sm" @click="confirmDelete(event)" />
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
            <div v-if="filteredEvents.length === 0" class="text-gray-500 text-center mt-8">
              当天暂无日程
            </div>
            <Timeline :value="timelineEvents" align="alternate" v-else>
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
                      <Button icon="pi pi-pencil" rounded text class="p-button-sm mr-2" @click="openEditDialog(slotProps.item)" />
                      <Button icon="pi pi-trash" rounded text severity="danger" class="p-button-sm" @click="confirmDelete(slotProps.item)" />
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
            <InputText v-model="form.title" maxlength="50" required class="w-full" />
          </div>
          <div class="mb-3 flex gap-2">
            <div class="flex-1">
              <label>开始日期 *</label>
              <Calendar v-model="form.startDate" dateFormat="yy-mm-dd" showIcon required class="w-full" />
            </div>
            <div class="flex-1">
              <label>开始时间 *</label>
              <InputText v-model="form.startTime" placeholder="HH:mm" required class="w-full" />
            </div>
          </div>
          <div class="mb-3 flex gap-2">
            <div class="flex-1">
              <label>结束日期 *</label>
              <Calendar v-model="form.endDate" dateFormat="yy-mm-dd" showIcon required class="w-full" />
            </div>
            <div class="flex-1">
              <label>结束时间 *</label>
              <InputText v-model="form.endTime" placeholder="HH:mm" required class="w-full" />
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
            <Button label="取消" icon="pi pi-times" severity="secondary" @click="showDialog=false" type="button" />
            <Button :label="dialogMode==='create'?'创建':'保存'" icon="pi pi-check" type="submit" />
          </div>
        </form>
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
  import { ref, computed } from 'vue';
  import Button from 'primevue/button';
  import SelectButton from 'primevue/selectbutton';
  import Dialog from 'primevue/dialog';
  import InputText from 'primevue/inputtext';
  import Calendar from 'primevue/calendar';
  import Textarea from 'primevue/textarea';
  import Card from 'primevue/card';
  import Timeline from 'primevue/timeline';
  
  const schedules = ref([
    {
      id: 1,
      title: '会议',
      start: '2025-04-19T09:00',
      end: '2025-04-19T10:00',
      location: '会议室A',
      description: '项目讨论',
      link: 'https://meeting.com/123'
    },
    {
      id: 2,
      title: '医生预约',
      start: '2025-04-19T14:30',
      end: '2025-04-19T15:00',
      location: '医院',
      description: '',
      link: ''
    }
  ]);
  
  const viewMode = ref('list');
  const viewModes = [
    { label: '列表', value: 'list', icon: 'pi pi-list' },
    { label: '日历', value: 'calendar', icon: 'pi pi-calendar' }
  ];
  
  const selectedDate = ref(new Date());
  
  const filteredEvents = computed(() => {
    const y = selectedDate.value.getFullYear();
    const m = (selectedDate.value.getMonth() + 1).toString().padStart(2, '0');
    const d = selectedDate.value.getDate().toString().padStart(2, '0');
    const dateStr = `${y}-${m}-${d}`;
    return schedules.value.filter(ev => (ev.start && ev.start.startsWith(dateStr)));
  });
  
  const timelineEvents = computed(() =>
    filteredEvents.value
      .slice()
      .sort((a, b) => a.start.localeCompare(b.start))
      .map(ev => ({
        ...ev,
        content: ev
      }))
  );
  
  function eventTimeRange(event) {
    if (event.end && event.end !== event.start) {
      return `${event.start.slice(11, 16)} - ${event.end.slice(11, 16)}`;
    } else {
      return event.start.slice(11,16);
    }
  }
  
  const showDialog = ref(false);
  const dialogMode = ref('create');
  const editId = ref(null);
  
  const emptyForm = {
    title: '', startDate: '', startTime: '', endDate: '', endTime: '', location: '', link: '', description: ''
  };
  const form = ref({ ...emptyForm });
  
  const showLLMDialog = ref(false);
  const llmInput = ref('');
  const llmResults = ref([]);
  
  function formatDateObjToStr(dateObj) {
    if (!dateObj) return '';
    const y = dateObj.getFullYear();
    const m = (dateObj.getMonth() + 1).toString().padStart(2, '0');
    const d = dateObj.getDate().toString().padStart(2, '0');
    return `${y}-${m}-${d}`;
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
  
  function onSubmit() {
    if (!form.value.title || !form.value.startDate || !form.value.startTime || !form.value.endDate || !form.value.endTime) {
      alert('请填写所有必填字段');
      return;
    }
    const startDateStr = formatDateObjToStr(form.value.startDate);
    const endDateStr = formatDateObjToStr(form.value.endDate);
    const start = `${startDateStr}T${form.value.startTime}`;
    const end = `${endDateStr}T${form.value.endTime}`;
    if (dialogMode.value === 'create') {
      schedules.value.push({
        id: Date.now(),
        title: form.value.title,
        start, end,
        location: form.value.location,
        link: form.value.link,
        description: form.value.description
      });
    } else if (dialogMode.value === 'edit') {
      const idx = schedules.value.findIndex(s => s.id === editId.value);
      if (idx !== -1) {
        schedules.value[idx] = {
          ...schedules.value[idx],
          ...form.value,
          start,
          end,
          link: form.value.link
        };
      }
    }
    showDialog.value = false;
  }
  
  function confirmDelete(row) {
    if (confirm(`确定要删除"${row.title}"?`)) {
      schedules.value = schedules.value.filter(s => s.id !== row.id);
    }
  }
  
  function openLLMDialog() {
    showLLMDialog.value = true;
    llmInput.value = '';
    llmResults.value = [];
  }
  
  // 模拟 LLM 返回多个日程，包含结束时间与链接
  function handleLLMCreate() {
    // 真实情况请替换为 LLM API 调用
    // 给每个日程加唯一 _uid（便于渲染 key）
    llmResults.value = [
      {
        _uid: Math.random().toString(36).slice(2),
        title: '看牙医',
        start_date: '2025-04-19',
        start_time: '15:00',
        end_date: '2025-04-19',
        end_time: '16:00',
        location: '医院',
        link: 'https://meet.example.com/dental',
        description: '牙科预约'
      },
      {
        _uid: Math.random().toString(36).slice(2),
        title: '和朋友吃饭',
        start_date: '2025-04-19',
        start_time: '19:00',
        end_date: '2025-04-19',
        end_time: '21:00',
        location: '餐厅',
        link: '',
        description: '聚餐'
      }
    ];
  }
  
  function removeLLMSchedule(idx) {
    llmResults.value.splice(idx, 1);
  }
  
  function confirmLLMSchedules() {
    for (const sch of llmResults.value) {
      if (!sch.title || !sch.start_date || !sch.start_time || !sch.end_date || !sch.end_time) continue;
      schedules.value.push({
        id: Date.now() + Math.random(),
        title: sch.title,
        start: `${sch.start_date}T${sch.start_time}`,
        end: `${sch.end_date}T${sch.end_time}`,
        location: sch.location || '',
        link: sch.link || '',
        description: sch.description || ''
      });
    }
    showLLMDialog.value = false;
  }
  
  function formatDate(date) {
    if (!date) return '';
    const y = date.getFullYear();
    const m = (date.getMonth() + 1).toString().padStart(2, '0');
    const d = date.getDate().toString().padStart(2, '0');
    return `${y}-${m}-${d}`;
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