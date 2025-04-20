<template>
	<div class="p-4 max-w-5xl mx-auto">
		<!-- Toolbar -->
		<div class="flex justify-between items-center mb-4">
			<div>
				<Button label="创建事项" icon="pi pi-plus" @click="openCreateDialog" class="mr-2" />
				<Button label="事项智能创建" icon="pi pi-comments" severity="info" @click="openLLMDialog" />
			</div>
		</div>

		<!-- List View -->
		<div>
			<div v-if="tasks.length === 0" class="text-gray-500 text-center mt-8">
				暂无日程
			</div>
			<div class="grid gap-4">
				<Card v-for="event in tasks" :key="event.id" class="w-full">
					<template #title>
						<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
							<span>{{ event.title }}</span>
							<span class="text-sm text-gray-500">
								计划：{{ event.dueDate.split('T')[0] }}
							</span >
							<span class="text-sm text-gray-500">
								剩余时间：{{ getRemainingDays(event.dueDate) }}
							</span>
							<Knob class="text-sm text-gray-500" size="70" v-model="event.progress" />
						</div>
					</template>
					<template #content>
						<div class="mb-2">
							<span>优先级：{{ getPriorityText(event.priority) || '未设置' }}
							</span>
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
						<div class="flex gap-2 mt-2">
							<Button icon="pi pi-pencil" rounded text class="p-button-sm mr-2" @click="openEditDialog(event)" />
							<Button icon="pi pi-trash" rounded text severity="danger" class="p-button-sm" @click="confirmDelete(event)" />
						</div>
					</template>
				</Card>
			</div>
		</div>

	</div>


</template>

<script setup>

	import { ref, computed, onMounted } from 'vue';
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
		const texts = {
			1: '低',
			2: '中',
			3: '高',
			4: '紧急'
		};
		return texts[priority] || priority;
	}

	const tasks = ref([
  {
    id: 1,
    title: '完成项目原型设计',
    dueDate: '2025-05-15T18:00', // 计划/截止日期
    priority: 3, // 优先级：low/medium/high/urgent
    tags: ['设计', '前端', '项目'], // 标签数组
    postponeCount: 0, // 推迟计数
    notes: '需要与UI团队确认设计规范后再开始', // 备注
    subtasks: [ // 子任务数组
      {
        id: 101,
        title: '收集设计需求',
        completed: true
      },
      {
        id: 102,
        title: '创建线框图',
        completed: false
      },
      {
        id: 103,
        title: '制作交互原型',
        completed: false
      }
    ],
    progress: 33, // 完成进度百分比
    status: 'in-progress' // 可选状态：not-started/in-progress/completed
  },
  {
    id: 2,
    title: '准备季度汇报',
    dueDate: '2025-04-30T12:00',
    priority: 2,
    tags: ['汇报', '管理'],
    postponeCount: 2,
    notes: '需要包含Q1成果和Q2计划',
    subtasks: [
      {
        id: 201,
        title: '收集各部门数据',
        completed: true
      },
      {
        id: 202,
        title: '制作PPT',
        completed: false
      }
    ],
    progress: 50,
    status: 'in-progress'
  },
  {
    id: 3,
    title: '团队建设活动',
    dueDate: '2025-05-20T15:00',
    priority: 1,
    tags: ['团建', '休闲'],
    postponeCount: 0,
    notes: '地点待定，预算5000元',
    subtasks: [],
    progress: 0,
    status: 'not-started'
  }]);

	// 计算剩余时间
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

</script>
