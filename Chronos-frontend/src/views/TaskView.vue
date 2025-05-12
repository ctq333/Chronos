<template>
	<div class="p-4 pt-10 max-w-5xl mx-auto">
		<!-- Toolbar & Filter -->
		<div class="flex flex-col gap-2 mb-4">
			<div class="flex justify-between items-center">
				<div class="flex-wrap">
					<Button label="创建事项" icon="pi pi-plus" @click="openCreateDialog" class="mr-2 mb-2" />
					<Button label="事项智能创建" icon="pi pi-comments" severity="info" @click="openLLMDialog" />
				</div>
				<SelectButton
					v-model="filterType"
					:options="filterTypeOptions"
					optionLabel="label"
					optionValue="value"
					class="mr-1"
				>
					<template #option="slotProps">
						<span>
							<i :class="slotProps.option.icon" v-if="slotProps.option.icon" style="margin-right:4px"></i>
							{{ slotProps.option.label }}
						</span>
					</template>
				</SelectButton>
			</div>
			<div class="flex flex-wrap items-center gap-2 pt-2">
				<div v-if="allUserTags.length" class="flex flex-wrap gap-1 ml-2 items-center">
					<span class="text-gray-500 text-sm mr-1">标签：</span>
					<Tag
						v-for="tag in allUserTags"
						:key="tag"
						:value="tag"
						:class="[
							'cursor-pointer',
							selectedTags.includes(tag) ? 'bg-blue-600 text-white border-blue-800' : 'bg-gray-200 text-gray-800 border-gray-300',
							'rounded-full px-3 py-1 text-sm border hover:bg-blue-100 transition duration-150'
						]"
						@click="toggleTag(tag)"
					/>
					<Tag
						v-if="selectedTags.length"
						value="清除标签筛选"
						class="cursor-pointer bg-yellow-500 text-white rounded-full px-3 py-1 text-sm border border-yellow-700"
						icon="pi pi-times"
						@click="selectedTags = []"
					/>
				</div>
			</div>
		</div>

		<!-- List View -->
		<div>
			<div v-if="filteredTasks.length === 0" class="text-gray-500 text-center mt-8">
				暂无事项
			</div>
			<div class="grid gap-4">
				<Card
                    v-for="event in filteredTasks"
                    :key="event.id"
                    class="w-full"
                    :style="event.status === 'completed' ? {'--p-card-background':bg-gray-300} : {}"
                >
                    <template #title>
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                            <!-- 标题加删除线和变灰 -->
                            <span
                                :class="event.status === 'completed' ? 'line-through text-gray-400' : ''"
                            >
                                {{ event.title }}
                            </span>
                            <span class="text-sm text-gray-500">计划：{{ event.planDate }}</span>
                            <span class="text-sm text-gray-500">截止：{{ event.dueDate }}</span>
                            <span class="text-sm text-gray-500">剩余时间：{{ getRemainingDays(event.dueDate) }}</span>
                            <!-- knob进度：完成100，否则原值 -->
                            <Knob
                                class="text-sm text-gray-500"
                                size="70"
                                :model-value="event.status === 'completed' ? 100 : event.progress"
								valueTemplate="{value}%"
                            />
                        </div>
                    </template>
                    <template #content>

                        <div class="mb-2">
                            <span>优先级：{{ getPriorityText(event.priority) || '未设置' }}</span>
                        </div>
                        <div class="mb-2">
                            <span>标签：</span>
                            <span v-if="event.tags && event.tags.length">
                                <Tag v-for="tag in event.tags" :key="tag" :value="tag" class="mr-1 mb-1" />
                            </span>
                            <span v-else>未设置</span>
                        </div>
                        <div v-if="event.postponeCount" class="mb-2">
                            <span>推迟计数：{{ event.postponeCount }}</span>
                        </div>
                        <div class="mb-2">
                            <span>备注：{{ event.notes || '无' }}</span>
                        </div>
                        <div v-if="event.subtasks && event.subtasks.length" class="mb-4">
                            <div class="mb-2">子任务</div>
                            <div class="space-y-2">
                                <div 
                                    v-for="subtask in event.subtasks" 
                                    :key="subtask.id" 
                                    class="flex items-center"
                                >
                                    <Checkbox
                                        v-model="subtask.completed"
                                        :binary="true"
                                        class="h-4 w-4"
                                    />
                                    <label 
                                        class="ml-2 text-sm cursor-pointer"
                                        @click="subtask.completed = !subtask.completed"
                                    >
                                        {{ subtask.title }}
                                    </label>
                                </div>
                            </div>
                        </div>
                        <div class="flex sm:flex-row sm:items-center justify-between">
                            <div class="flex items-center gap-1">
                                <Button icon="pi pi-calendar-plus" rounded text class="p-button-sm" title="推迟日程" @click.stop="openPostponeDialog(event)" />
                                <Button icon="pi pi-plus-circle" rounded text class="p-button-sm" title="创建子任务" @click.stop="openAddSubTaskDialog(event)" />
                                <Button icon="pi pi-sparkles" rounded text class="p-button-sm" title="智能创建子任务" @click.stop="openSmartSubTaskDialog(event)" />
								<Button
									icon="pi pi-calendar"
									rounded
									text
									class="p-button-sm"
									title="由事项创建日程"
									@click.stop="openScheduleDialog(event)"
								/>
                            </div>
                            <div class="flex items-center gap-1">
                                <Button icon="pi pi-pencil" rounded text class="p-button-sm" @click="openEditDialog(event)" />
                                <Button icon="pi pi-trash" rounded text severity="danger" class="p-button-sm" @click="confirmDelete(event)" />
                                <!-- 状态切换按钮 -->
                                <Button
                                    :icon="event.status === 'completed' ? 'pi pi-undo' : 'pi pi-check'"
                                    rounded text
                                    :severity="event.status === 'completed' ? 'warning' : 'success'"
                                    class="p-button-sm"
                                    @click="toggleCompleted(event.id)"
                                    :title="event.status === 'completed' ? '标记为未完成' : '标记为已完成'"
                                />
                            </div>
                        </div>
                    </template>
                </Card>
			</div>
		</div>

		<!-- 创建/编辑事项对话框（全功能: 子任务增删改） -->
		<Dialog v-model:visible="showDialog" :header="dialogMode==='create'?'新建事项':'编辑事项'" :modal="true" :closable="false" :style="{width:'480px'}">
			<form @submit.prevent="onSubmit">
				<div class="mb-3">
					<label>标题 *</label>
					<InputText v-model="form.title" maxlength="50" required class="w-full" />
				</div>
				<div class="mb-3 flex gap-2">
					<div class="flex-1">
						<label>计划处理日期 *</label>
						<Calendar v-model="form.planDate" dateFormat="yy-mm-dd" showIcon required class="w-full" />
					</div>
					<div class="flex-1">
						<label>截止日期 *</label>
						<Calendar v-model="form.dueDate" dateFormat="yy-mm-dd" showIcon required class="w-full" />
					</div>
				</div>
				<div class="mb-3">
					<label>优先级</label>
					<SelectButton 
						v-model="form.priority"
						:options="priorityOptions"
						optionLabel="label"
						optionValue="value"
						class="w-full"
					/>
				</div>
				<div class="mb-3">
					<label>标签（逗号分隔）</label>
					<InputText v-model="form.tagsInput" placeholder="如：设计,前端,项目" class="w-full" />
				</div>
				<div class="mb-3">
					<label>备注</label>
					<Textarea v-model="form.notes" maxlength="200" rows="3" class="w-full" />
				</div>
				<!-- 子任务编辑区 -->
				<div class="mb-3">
					<label class="block mb-1">子任务</label>
					<div v-for="(sub, idx) in form.subtasks" :key="sub.id" class="flex items-center gap-2 mb-2">
						<Checkbox v-model="sub.completed" :binary="true" />
						<InputText v-model="sub.title" placeholder="子任务标题" class="flex-1" />
						<Button icon="pi pi-trash" text severity="danger" @click="removeEditSubTask(idx)" />
					</div>
					<div class="flex gap-2 mt-1">
						<InputText v-model="newSubTaskTitle" placeholder="新增子任务标题" class="flex-1" @keyup.enter="addEditSubTask" />
						<Button icon="pi pi-plus" label="添加" class="p-button-sm" @click="addEditSubTask" :disabled="!newSubTaskTitle.trim()" />
					</div>
				</div>
				<div class="flex justify-end gap-2">
					<Button label="取消" icon="pi pi-times" severity="secondary" @click="showDialog=false" type="button" />
					<Button :label="dialogMode==='create'?'创建':'保存'" icon="pi pi-check" type="submit" />
				</div>
			</form>
		</Dialog>

		<!-- 智能事项批量创建对话框 -->
		<Dialog v-model:visible="showLLMDialog" header="LLM智能创建事项" modal style="width: 700px">
			<div>
				<Textarea
					v-model="llmInput"
					:autoResize="false"
					rows="5"
					style="max-height:120px;overflow-y:auto"
					placeholder="请输入自然语言描述，例如：5月10日处理发票，下周三前提交设计文档"
					class="w-full"
				/>
				<Button label="生成事项" class="mt-2" icon="pi pi-send" @click="handleLLMCreate" />
			</div>
			<div v-if="llmResults.length" class="mt-4 space-y-4">
				<div
					v-for="(task, idx) in llmResults"
					:key="task._uid"
					class="p-2 bg-gray-100 rounded relative"
				>
					<div class="flex justify-between">
						<b>事项{{ idx + 1 }}</b>
						<Button
							icon="pi pi-trash"
							class="p-button-sm absolute top-2 right-2"
							severity="danger"
							text
							@click="removeLLMSchedule(idx)"
							title="删除该事项"
						/>
					</div>
					<div class="grid grid-cols-2 gap-2 mt-2">
						<div>
							<label class="block text-xs text-gray-500 mb-1">标题</label>
							<InputText v-model="task.title" class="w-full" />
						</div>
						<div>
							<label class="block text-xs text-gray-500 mb-1">计划处理日期</label>
							<InputText v-model="task.plan_date" class="w-full" />
						</div>
						<div>
							<label class="block text-xs text-gray-500 mb-1">截止日期</label>
							<InputText v-model="task.due_date" class="w-full" />
						</div>
						<div>
							<label class="block text-xs text-gray-500 mb-1">优先级</label>
							<SelectButton 
								v-model="task.priority"
								:options="priorityOptions"
								optionLabel="label"
								optionValue="value"
								class="w-full"
							/>
						</div>
						<div class="col-span-2">
							<label class="block text-xs text-gray-500 mb-1">标签（逗号分隔）</label>
							<InputText v-model="task.tagsInput" class="w-full" />
						</div>
						<div class="col-span-2">
							<label class="block text-xs text-gray-500 mb-1">备注</label>
							<InputText v-model="task.notes" class="w-full" />
						</div>
					</div>
				</div>
				<Button label="确认创建全部" icon="pi pi-check" class="mt-2" @click="confirmLLMSchedules" :disabled="llmResults.length===0" />
			</div>
		</Dialog>

		<!-- 推迟日程对话框 -->
		<Dialog v-model:visible="showPostponeDialog" header="推迟日程" :modal="true" :closable="false" :style="{width:'340px'}">
			<form @submit.prevent="onPostponeSubmit">
				<div class="mb-3">
					<label>新的计划处理日期 *</label>
					<Calendar v-model="postponeDate" dateFormat="yy-mm-dd" showIcon required class="w-full" />
				</div>
				<div class="flex justify-end gap-2">
					<Button label="取消" icon="pi pi-times" severity="secondary" @click="showPostponeDialog=false" type="button" />
					<Button label="确定" icon="pi pi-check" type="submit" />
				</div>
			</form>
		</Dialog>

		<!-- 创建子任务对话框 -->
		<Dialog v-model:visible="showAddSubTaskDialog" header="创建子任务" :modal="true" :closable="false" :style="{width:'340px'}">
			<form @submit.prevent="onAddSubTaskSubmit">
				<div class="mb-3">
					<label>子任务标题 *</label>
					<InputText v-model="subTaskTitle" maxlength="50" required class="w-full" />
				</div>
				<div class="flex justify-end gap-2">
					<Button label="取消" icon="pi pi-times" severity="secondary" @click="showAddSubTaskDialog=false" type="button" />
					<Button label="创建" icon="pi pi-check" type="submit" />
				</div>
			</form>
		</Dialog>

		<!-- 智能创建子任务对话框 -->
		<Dialog v-model:visible="showSmartSubTaskDialog" header="智能创建子任务" :modal="true" :closable="false" :style="{width:'520px'}">
			<div v-if="smartSubTaskLoading" class="flex flex-col items-center py-10">
				<i class="pi pi-spin pi-spinner text-3xl mb-3 text-blue-500"></i>
				<div class="text-gray-700">正在智能生成子任务，请稍候……</div>
			</div>
			<div v-else>
				<div v-if="smartSubTaskList.length" class="space-y-2">
					<div v-for="(sub, idx) in smartSubTaskList" :key="sub._uid" class="flex items-center gap-2">
						<InputText v-model="sub.title" class="flex-1" />
						<Button icon="pi pi-trash" text severity="danger" @click="removeSmartSubTask(idx)" />
					</div>
					<div class="flex justify-end gap-2 mt-4">
						<Button label="取消" icon="pi pi-times" severity="secondary" @click="showSmartSubTaskDialog=false" />
						<Button label="全部添加" icon="pi pi-check" @click="confirmSmartSubTasks" :disabled="!smartSubTaskList.length" />
					</div>
				</div>
				<div v-else class="text-gray-500 text-center py-6">未获取到可用子任务</div>
			</div>
		</Dialog>

		<!-- 创建日程对话框 -->
		<Dialog v-model:visible="showScheduleDialog" header="由事项创建日程" :modal="true" :closable="false" :style="{width:'400px'}">
		<form @submit.prevent="onScheduleSubmit">
			<div class="mb-3">
			<label>主题 *</label>
			<InputText v-model="scheduleForm.title" maxlength="50" required class="w-full" />
			</div>
			<div class="mb-3 flex gap-2">
			<div class="flex-1">
				<label>开始日期 *</label>
				<Calendar v-model="scheduleForm.startDate" dateFormat="yy-mm-dd" showIcon required class="w-full" />
			</div>
			<div class="flex-1">
				<label>开始时间 *</label>
				<InputText v-model="scheduleForm.startTime" placeholder="HH:mm" required class="w-full" />
			</div>
			</div>
			<div class="mb-3 flex gap-2">
			<div class="flex-1">
				<label>结束日期 *</label>
				<Calendar v-model="scheduleForm.endDate" dateFormat="yy-mm-dd" showIcon required class="w-full" />
			</div>
			<div class="flex-1">
				<label>结束时间 *</label>
				<InputText v-model="scheduleForm.endTime" placeholder="HH:mm" required class="w-full" />
			</div>
			</div>
			<div class="mb-3">
			<label>地点</label>
			<InputText v-model="scheduleForm.location" maxlength="100" class="w-full" />
			</div>
			<div class="mb-3">
			<label>链接</label>
			<InputText v-model="scheduleForm.link" maxlength="200" class="w-full" placeholder="如 https://..."/>
			</div>
			<div class="mb-3">
			<label>描述</label>
			<Textarea v-model="scheduleForm.description" maxlength="500" rows="3" class="w-full" />
			</div>
			<div class="flex justify-end gap-2">
			<Button label="取消" icon="pi pi-times" severity="secondary" @click="showScheduleDialog=false" type="button" />
			<Button label="创建" icon="pi pi-check" type="submit" />
			</div>
		</form>
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
import Knob from 'primevue/knob';
import Tag from 'primevue/tag';
import Checkbox from 'primevue/checkbox';

function getPriorityText(priority) {
	const texts = { 1: '低', 2: '中', 3: '高', 4: '紧急' };
	return texts[priority] || priority;
}
const priorityOptions = [
	{ label: '低', value: 1 },
	{ label: '中', value: 2 },
	{ label: '高', value: 3 },
	{ label: '紧急', value: 4 }
];

const tasks = ref([
  {
    id: 1,
    title: '完成项目原型设计',
    planDate: '2025-05-10',
    dueDate: '2025-05-15',
    priority: 3,
    tags: ['设计', '前端', '项目'],
    postponeCount: 0,
    notes: '需要与UI团队确认设计规范后再开始',
    subtasks: [
      { id: 101, title: '收集设计需求', completed: true },
      { id: 102, title: '创建线框图', completed: false },
      { id: 103, title: '制作交互原型', completed: false }
    ],
    progress: 33,
    status: 'in-progress'
  },
  {
    id: 2,
    title: '准备季度汇报',
    planDate: '2025-04-25',
    dueDate: '2025-04-30',
    priority: 2,
    tags: ['汇报', '管理'],
    postponeCount: 2,
    notes: '需要包含Q1成果和Q2计划',
    subtasks: [
      { id: 201, title: '收集各部门数据', completed: true },
      { id: 202, title: '制作PPT', completed: false }
    ],
    progress: 50,
    status: 'in-progress'
  },
  {
    id: 3,
    title: '团队建设活动',
    planDate: '2025-05-15',
    dueDate: '2025-05-20',
    priority: 1,
    tags: ['团建', '休闲'],
    postponeCount: 0,
    notes: '地点待定，预算5000元',
    subtasks: [],
    progress: 0,
    status: 'not-started'
  }
]);

function getRemainingDays(dueDate) {
	const now = new Date();
	const due = new Date(dueDate);
	const diffTime = due - now;
	const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
	if (diffDays < 0) {
		return `已过期${Math.abs(diffDays)}天`;
	} else if (diffDays === 0) {
		return '今天到期';
	} else {
		return `${diffDays}天`;
	}
}

// ========== 筛选相关 ==========
const filterTypeOptions = [
	{ label: '全部', value: 'all', icon: 'pi pi-list' },
	{ label: '未完成', value: 'not-completed', icon: 'pi pi-clock' },
	{ label: '已完成', value: 'completed', icon: 'pi pi-check' }
];
const filterType = ref('all');
const selectedTags = ref([]);

function toggleTag(tag) {
	const idx = selectedTags.value.indexOf(tag);
	if (idx === -1) {
		selectedTags.value.push(tag);
	} else {
		selectedTags.value.splice(idx, 1);
	}
}

const allUserTags = computed(() => {
	const tagSet = new Set();
	tasks.value.forEach(item => {
		(item.tags || []).forEach(tag => tagSet.add(tag));
	});
	return Array.from(tagSet);
});

const filteredTasks = computed(() => {
	let arr = tasks.value;

	// 标签筛选
	if (selectedTags.value.length) {
		arr = arr.filter(t =>
			t.tags && t.tags.some(tag => selectedTags.value.includes(tag))
		);
	}

	// 筛选类型
	if (filterType.value === 'completed') {
		arr = arr.filter(t => t.status === 'completed');
	} else if (filterType.value === 'not-completed') {
		arr = arr.filter(t => t.status !== 'completed');
	}

	// 分两组：未完成和已完成
	const uncompleted = arr.filter(t => t.status !== 'completed');
	const completed = arr.filter(t => t.status === 'completed');

	// 未完成：截止日期升序，截止一样则计划日期升序
	uncompleted.sort((a, b) => {
		const dueA = a.dueDate ? new Date(a.dueDate) : new Date(0);
		const dueB = b.dueDate ? new Date(b.dueDate) : new Date(0);
		if (dueA.getTime() !== dueB.getTime()) {
			return dueA - dueB;
		}
		const planA = a.planDate ? new Date(a.planDate) : new Date(0);
		const planB = b.planDate ? new Date(b.planDate) : new Date(0);
		return planA - planB;
	});

	// 已完成：截止日期降序，截止一样则计划日期降序
	completed.sort((a, b) => {
		const dueA = a.dueDate ? new Date(a.dueDate) : new Date(0);
		const dueB = b.dueDate ? new Date(b.dueDate) : new Date(0);
		if (dueA.getTime() !== dueB.getTime()) {
			return dueB - dueA;
		}
		const planA = a.planDate ? new Date(a.planDate) : new Date(0);
		const planB = b.planDate ? new Date(b.planDate) : new Date(0);
		return planB - planA;
	});

	return [...uncompleted, ...completed];
});

// ========== 新增/编辑/删除等逻辑 ==========
const showDialog = ref(false);
const dialogMode = ref('create');
const editId = ref(null);

const emptyForm = {
	title: '', planDate: '', dueDate: '', priority: 2, tagsInput: '', notes: '', subtasks: []
};
const form = ref({ ...emptyForm });

const newSubTaskTitle = ref('');

function openCreateDialog() {
	dialogMode.value = 'create';
	Object.assign(form.value, emptyForm);
	form.value.priority = 2;
	form.value.subtasks = [];
	newSubTaskTitle.value = '';
	showDialog.value = true;
}
function openEditDialog(row) {
	dialogMode.value = 'edit';
	editId.value = row.id;
	form.value = {
		title: row.title,
		planDate: new Date(row.planDate),
		dueDate: new Date(row.dueDate),
		priority: row.priority,
		tagsInput: row.tags ? row.tags.join(',') : '',
		notes: row.notes || '',
		subtasks: row.subtasks ? row.subtasks.map(sub => ({ ...sub })) : []
	};
	newSubTaskTitle.value = '';
	showDialog.value = true;
}

function formatDateObjToStr(dateObj) {
	if (!dateObj) return '';
	const y = dateObj.getFullYear();
	const m = (dateObj.getMonth() + 1).toString().padStart(2, '0');
	const d = dateObj.getDate().toString().padStart(2, '0');
	return `${y}-${m}-${d}`;
}

function addEditSubTask() {
	const title = newSubTaskTitle.value.trim();
	if (!title) return;
	form.value.subtasks.push({
		id: Date.now() + Math.random(),
		title,
		completed: false
	});
	newSubTaskTitle.value = '';
}
function removeEditSubTask(idx) {
	form.value.subtasks.splice(idx, 1);
}

function onSubmit() {
	if (!form.value.title || !form.value.planDate || !form.value.dueDate) {
		alert('请填写所有必填字段');
		return;
	}
	const planDateStr = formatDateObjToStr(form.value.planDate);
	const dueDateStr = formatDateObjToStr(form.value.dueDate);
	const tags = form.value.tagsInput
		? form.value.tagsInput.split(',').map(t => t.trim()).filter(Boolean)
		: [];
	if (dialogMode.value === 'create') {
		tasks.value.push({
			id: Date.now(),
			title: form.value.title,
			planDate: planDateStr,
			dueDate: dueDateStr,
			priority: form.value.priority,
			tags,
			postponeCount: 0,
			notes: form.value.notes,
			subtasks: form.value.subtasks.map(sub => ({ ...sub })),
			progress: 0,
			status: 'not-started'
		});
	} else if (dialogMode.value === 'edit') {
		const idx = tasks.value.findIndex(t => t.id === editId.value);
		if (idx !== -1) {
			tasks.value[idx] = {
				...tasks.value[idx],
				title: form.value.title,
				planDate: planDateStr,
				dueDate: dueDateStr,
				priority: form.value.priority,
				tags,
				notes: form.value.notes,
				subtasks: form.value.subtasks.map(sub => ({ ...sub }))
			};
		}
	}
	showDialog.value = false;
}

// 修复标记完成问题（务必用id查找原tasks对象）
function markCompleted(id) {
	const idx = tasks.value.findIndex(t => t.id === id);
	if (idx !== -1) {
		tasks.value[idx].status = 'completed';
	}
}

const showPostponeDialog = ref(false);
const currentPostponeTaskId = ref(null);
const postponeDate = ref(null);

function openPostponeDialog(task) {
	currentPostponeTaskId.value = task.id;
	postponeDate.value = new Date(task.planDate);
	showPostponeDialog.value = true;
}
function onPostponeSubmit() {
	if (!postponeDate.value) return;
	const idx = tasks.value.findIndex(t => t.id === currentPostponeTaskId.value);
	if (idx !== -1) {
		const dateStr = formatDateObjToStr(postponeDate.value);
		tasks.value[idx].planDate = dateStr;
		tasks.value[idx].postponeCount = (tasks.value[idx].postponeCount || 0) + 1;
	}
	showPostponeDialog.value = false;
}

const showAddSubTaskDialog = ref(false);
const currentSubTaskParentId = ref(null);
const subTaskTitle = ref('');

function openAddSubTaskDialog(task) {
	currentSubTaskParentId.value = task.id;
	subTaskTitle.value = '';
	showAddSubTaskDialog.value = true;
}
function onAddSubTaskSubmit() {
	if (!subTaskTitle.value) return;
	const idx = tasks.value.findIndex(t => t.id === currentSubTaskParentId.value);
	if (idx !== -1) {
		tasks.value[idx].subtasks = tasks.value[idx].subtasks || [];
		const newId = Date.now() + Math.random();
		tasks.value[idx].subtasks.push({ id: newId, title: subTaskTitle.value, completed: false });
	}
	showAddSubTaskDialog.value = false;
}

const showSmartSubTaskDialog = ref(false);
const currentSmartSubTaskParentId = ref(null);
const smartSubTaskList = ref([]);
const smartSubTaskLoading = ref(false);

function openSmartSubTaskDialog(task) {
	currentSmartSubTaskParentId.value = task.id;
	smartSubTaskList.value = [];
	showSmartSubTaskDialog.value = true;
	smartSubTaskLoading.value = true;
	setTimeout(() => {
		smartSubTaskList.value = [
			{ _uid: Math.random().toString(36).slice(2), title: 'AI子任务1' },
			{ _uid: Math.random().toString(36).slice(2), title: 'AI子任务2' },
			{ _uid: Math.random().toString(36).slice(2), title: 'AI子任务3' }
		];
		smartSubTaskLoading.value = false;
	}, 1200);
}
function removeSmartSubTask(idx) {
	smartSubTaskList.value.splice(idx, 1);
}
function confirmSmartSubTasks() {
	const idx = tasks.value.findIndex(t => t.id === currentSmartSubTaskParentId.value);
	if (idx !== -1) {
		const nextId = () => Date.now() + Math.random();
		const newSubs = smartSubTaskList.value.map(sub => ({
			id: nextId(),
			title: sub.title,
			completed: false
		}));
		tasks.value[idx].subtasks = (tasks.value[idx].subtasks || []).concat(newSubs);
	}
	showSmartSubTaskDialog.value = false;
}

const showLLMDialog = ref(false);
const llmInput = ref('');
const llmResults = ref([]);

function openLLMDialog() {
	showLLMDialog.value = true;
	llmInput.value = '';
	llmResults.value = [];
}

function handleLLMCreate() {
	llmResults.value = [
		{
			_uid: Math.random().toString(36).slice(2),
			title: '写周报',
			plan_date: '2025-04-22',
			due_date: '2025-04-25',
			priority: 2,
			tagsInput: '文档,总结',
			notes: '需包括本周工作重点'
		},
		{
			_uid: Math.random().toString(36).slice(2),
			title: '提交发票',
			plan_date: '2025-04-27',
			due_date: '2025-04-30',
			priority: 1,
			tagsInput: '财务',
			notes: ''
		}
	];
}
function removeLLMSchedule(idx) {
	llmResults.value.splice(idx, 1);
}
function confirmLLMSchedules() {
	for (const task of llmResults.value) {
		if (!task.title || !task.plan_date || !task.due_date) continue;
		const tags = task.tagsInput
			? task.tagsInput.split(',').map(t => t.trim()).filter(Boolean)
			: [];
		tasks.value.push({
			id: Date.now() + Math.random(),
			title: task.title,
			planDate: task.plan_date,
			dueDate: task.due_date,
			priority: task.priority,
			tags,
			postponeCount: 0,
			notes: task.notes,
			subtasks: [],
			progress: 0,
			status: 'not-started'
		});
	}
	showLLMDialog.value = false;
}
function confirmDelete(row) {
	if (confirm(`确定要删除"${row.title}"?`)) {
		tasks.value = tasks.value.filter(t => t.id !== row.id);
	}
}

function toggleCompleted(id) {
	const idx = tasks.value.findIndex(t => t.id === id);
	if (idx !== -1) {
		if (tasks.value[idx].status === 'completed') {
			tasks.value[idx].status = 'in-progress';
			// 可自定义设置：tasks.value[idx].progress = 0;
		} else {
			tasks.value[idx].status = 'completed';
			tasks.value[idx].progress = 100;
		}
	}
}

// 日程对话框相关
const showScheduleDialog = ref(false)
const scheduleForm = ref({
  title: '',
  startDate: '',
  startTime: '',
  endDate: '',
  endTime: '',
  location: '',
  link: '',
  description: ''
})

// 打开日程对话框并填充事项信息
function openScheduleDialog(task) {
  // 计划日期为起始，截止日期为结束
  scheduleForm.value = {
    title: task.title,
    startDate: task.planDate ? new Date(task.planDate) : '',
    startTime: '09:00',
    endDate: task.dueDate ? new Date(task.dueDate) : (task.planDate ? new Date(task.planDate) : ''),
    endTime: '10:00',
    location: '',
    link: '',
    description: task.notes || ''
  }
  showScheduleDialog.value = true;
}
function onScheduleSubmit() {
  const f = scheduleForm.value;
  if (!f.title || !f.startDate || !f.startTime || !f.endDate || !f.endTime) {
    alert('请填写所有必填字段');
    return;
  }
  const startDateStr = formatDateObjToStr(f.startDate);
  const endDateStr = formatDateObjToStr(f.endDate);
  schedules.value.push({
    id: Date.now() + Math.random(),
    title: f.title,
    start: `${startDateStr}T${f.startTime}`,
    end: `${endDateStr}T${f.endTime}`,
    location: f.location,
    link: f.link,
    description: f.description
  });
  showScheduleDialog.value = false;
}
</script>
<style scoped>
.completed-card-text,
.completed-card-text :where(span, label, div, p, .p-tag) {
    text-decoration: line-through !important;
    color: #a3a3a3 !important; /* Tailwind text-gray-400 */
}
</style>