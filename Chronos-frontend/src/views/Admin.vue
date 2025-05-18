<template>
  <div class="bg-gray-50">
    <Toast />

    <div class="p-6 max-w-7xl mx-auto">
      <div class="mb-6">
        <h2 class="text-3xl font-medium text-gray-800 mb-6">用户列表</h2>
        <div class="flex gap-2 mb-4">
          <Button label="添加用户" icon="pi pi-plus" severity="primary" size="small" @click="showAddDialog = true"/>
          <Button label="删除用户" icon="pi pi-trash" severity="danger" 
                  :disabled="selectedUsers.length === 0"  size="small" @click="confirmDelete"/>
        </div>
      </div>
      
      <DataTable :value="users" v-model:selection="selectedUsers" selectionMode="multiple" :key-field="id"
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
import { ref, watch } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Tag from 'primevue/tag';
import request from '@/utils/request'
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast'

const toast = useToast();

// 用户数据
const users = ref([]);

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

// 初始化获取用户列表
watch(() => {
  fetchUsers();
}, [], { immediate: true });

async function fetchUsers() {
  try {
    const response = await request.get('/admin/users');
    if (response.data.code === 200){
      users.value = response.data.users;
    } else {
      toast.add({
        severity: 'error',
        summary: '失败',
        detail: response.data.message || '获取用户失败',
        life: 3000
      });
    }
  } catch (error) {
    console.error('获取用户失败:', error);
    toast.add({
        severity: 'error',
        summary: '失败',
        detail: error.response?.data?.message || '获取用户失败',
        life: 3000
      });
  }
}

// 用户操作
async function toggleStatus(user){
  try {
    const response = await request.put(`/admin/users/${user.id}/status`);
    if (response.data.code === 200){
      fetchUsers()
      toast.add({
          severity: 'success',
          summary: '成功',
          detail: "修改用户状态成功",
          life: 3000
        });
    } else {
      toast.add({
          severity: 'error',
          summary: '失败',
          detail: "修改用户状态失败：" + response.data.message,
          life: 3000
        });
    }
  } catch (error) {
    console.error('切换状态失败:', error.response?.data?.message || '未知错误');
    toast.add({
        severity: 'error',
        summary: '失败',
        detail: error.response?.data?.message || '切换状态失败',
        life: 3000
      });
  }
};

const openResetDialog = (user) => {
  currentUser.value = user;
  showResetDialog.value = true;
};

async function createUser() {
  if (newUser.value.username && newUser.value.password) {
    try {
      const response = await request.post('/admin/users', newUser.value);
      if (response.data.code === 200) {
        toast.add({
          severity: 'success',
          summary: '成功',
          detail: "添加用户成功",
          life: 3000
        });
        fetchUsers();
        showAddDialog.value = false;
        newUser.value = { username: '', password: '' };
      } else {
        toast.add({
          severity: 'error',
          summary: '失败',
          detail: "添加用户失败：" + response.data.message,
          life: 3000
        });
      }
    } catch (error) {
      console.error('创建用户失败:', error.response?.data?.message || '未知错误');
      toast.add({
          severity: 'error',
          summary: '失败',
          detail: "添加用户失败：" + error.response?.data?.message || "未知错误",
          life: 3000
        });
    }
  } else {
    toast.add({
      severity: 'error',
      summary: '失败',
      detail: '请输入用户名和密码',
      life: 3000
    });
  }
};

const confirmDelete = () => {
  showDeleteConfirm.value = true;
};

async function deleteUsers(){
  if (selectedUsers.value.length === 0) return;

  try {
    const response = await request.delete('/admin/users/batch', {
      data: { user_ids: selectedUsers.value.map(u => u.id) }
    });
    if (response.data.code === 200){
      fetchUsers();
      toast.add({
          severity: 'success',
          summary: '成功',
          detail: "删除用户成功",
          life: 3000
        });
    } else {
      toast.add({
          severity: 'error',
          summary: '失败',
          detail: "删除用户失败：" + response.data.message,
          life: 3000
        });
    }
    selectedUsers.value = [];
    showDeleteConfirm.value = false;
  } catch (error) {
    console.error('删除用户失败:', error.response?.data?.message || '未知错误');
    toast.add({
          severity: 'error',
          summary: '失败',
          detail: '删除用户失败:' + error.response?.data?.message || '未知错误',
          life: 3000
        });
  }
};

async function confirmReset() {
  if (resetData.value.newPassword === "" ||  resetData.value.confirmPassword === "") {
    toast.add({
          severity: 'error',
          summary: '失败',
          detail: "密码不能为空",
          life: 3000
        });
    return;
  }
  
  if (resetData.value.newPassword !== resetData.value.confirmPassword) {
    toast.add({
          severity: 'error',
          summary: '失败',
          detail: "两次密码不一致",
          life: 3000
        });
    return;
  }

  try {
    const response = await request.put(`/admin/users/${currentUser.value.id}/password`, {
      new_password: resetData.value.newPassword
    });
    if (response.data.code === 200){
      toast.add({
          severity: 'success',
          summary: '成功',
          detail: "重置密码成功",
          life: 3000
        });
        showResetDialog.value = false;
        resetData.value = { newPassword: '', confirmPassword: '' };
    } else {
      toast.add({
          severity: 'error',
          summary: '失败',
          detail: "重置密码失败：" + response.data.message,
          life: 3000
        });
    }
    
  } catch (error) {
    console.error('重置密码失败:', error.response?.data?.message || '未知错误');
    toast.add({
          severity: 'error',
          summary: '失败',
          detail: '重置密码失败:' + error.response?.data?.message || '未知错误',
          life: 3000
        });
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