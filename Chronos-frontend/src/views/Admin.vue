<template>
  <div class="bg-gray-50">
    <div class="p-6 max-w-7xl mx-auto">
      <div class="mb-6">
        <h2 class="text-3xl font-medium text-gray-800 mb-6">用户列表</h2>
        <div class="flex gap-2 mb-4">
          <Button label="添加用户" icon="pi pi-plus" severity="primary" size="small" @click="showAddDialog = true"/>
          <Button label="删除用户" icon="pi pi-trash" severity="danger" 
                  :disabled="selectedUsers.length === 0"  size="small" @click="confirmDelete"/>
        </div>
      </div>
      
      <DataTable :value="users" v-model:selection="selectedUsers" selectionMode="multiple"
                class="p-datatable-sm" scrollable scrollHeight="65vh" tableStyle="min-width: 50rem">
        <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
        <Column field="username" header="用户名" headerStyle="width: 50%"></Column>
        <Column header="状态">
        <template #body="{data}">
            <Tag :value="data.status ? '允许登录' : '禁止登录'" 
                :severity="data.status ? 'success' : 'danger'"/>
        </template>
        </Column>
        <Column header="操作">
        <template #body="{data}">
            <div class="flex gap-2">
            <Button v-if="data.status" label="禁用" severity="danger" outlined size="small"
                    @click="toggleStatus(data)"/>
            <Button v-else label="启用" severity="success" outlined size="small"
                    @click="toggleStatus(data)"/>
            <Button label="重设密码" severity="info" outlined size="small"
                    @click="openResetDialog(data)"/>
            </div>
        </template>
        </Column>
      </DataTable>
    </div>

    <!-- 添加用户弹窗 -->
    <Dialog v-model:visible="showAddDialog" header="新建用户" :style="{width: '400px'}">
      <div class="space-y-4">
        <InputText v-model="newUser.username" placeholder="用户名" class="w-full"/>
        <Password v-model="newUser.password" placeholder="初始密码" toggleMask class="w-full"/>
        <div class="flex justify-end gap-3">
          <Button label="取消" severity="secondary" @click="showAddDialog = false"/>
          <Button label="确认" @click="createUser"/>
        </div>
      </div>
    </Dialog>

    <!-- 删除确认弹窗 -->
    <Dialog v-model:visible="showDeleteConfirm" header="确认删除" :style="{width: '500px'}">
      <p>确定要删除选中的 {{ selectedUsers.length }} 个用户吗？</p>
      <template #footer>
        <Button label="取消" severity="secondary" @click="showDeleteConfirm = false"/>
        <Button label="确认删除" severity="danger" @click="deleteUsers"/>
      </template>
    </Dialog>

    <!-- 重设密码弹窗 -->
    <Dialog v-model:visible="showResetDialog" header="重设密码" :style="{width: '400px'}">
      <div class="space-y-4">
        <Password v-model="resetData.newPassword" placeholder="新密码" toggleMask class="w-full"/>
        <Password v-model="resetData.confirmPassword" placeholder="确认密码" toggleMask class="w-full"/>
        <div class="flex justify-end gap-3">
          <Button label="取消" severity="secondary" @click="cancelReset"/>
          <Button label="确认修改" @click="confirmReset"/>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Tag from 'primevue/tag';

// 用户数据
const users = ref([
{ id: 1, username: 'admin', status: true, password: '******' },
{ id: 2, username: 'user1', status: false, password: '123456' },
{ id: 3, username: 'tester', status: true, password: 'test@2023' }
]);

// 状态管理
const selectedUsers = ref([]);
const showAddDialog = ref(false);
const showDeleteConfirm = ref(false);
const showResetDialog = ref(false);
const currentUser = ref(null);

// 表单数据
const newUser = ref({
username: '',
password: ''
});

const resetData = ref({
newPassword: '',
confirmPassword: ''
});

// 用户操作
const toggleStatus = (user) => {
user.status = !user.status;
};

const openResetDialog = (user) => {
currentUser.value = user;
showResetDialog.value = true;
};

const createUser = () => {
if (newUser.value.username && newUser.value.password) {
    users.value.push({
    id: Date.now(),
    ...newUser.value,
    status: true
    });
    showAddDialog.value = false;
    newUser.value = { username: '', password: '' };
}
};

const confirmDelete = () => {
showDeleteConfirm.value = true;
};

const deleteUsers = () => {
users.value = users.value.filter(user => 
    !selectedUsers.value.some(selected => selected.id === user.id)
);
selectedUsers.value = [];
showDeleteConfirm.value = false;
};

const confirmReset = () => {
if (resetData.value.newPassword === resetData.value.confirmPassword) {
    currentUser.value.password = resetData.value.newPassword;
    showResetDialog.value = false;
    resetData.value = { newPassword: '', confirmPassword: '' };
}
};

const cancelReset = () => {
showResetDialog.value = false;
resetData.value = { newPassword: '', confirmPassword: '' };
};
</script>

<style scoped>
/* 自定义表格样式 */
.p-datatable {
background: white;
border-radius: 0.5rem;
border: 1px solid #e5e7eb;
}

/* 按钮间距调整 */
.p-button {
margin: 0.1rem;
}

</style>