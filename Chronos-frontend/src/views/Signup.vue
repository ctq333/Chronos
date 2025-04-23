<template>
    <div class="fixed inset-0 flex items-center justify-center bg-gradient-to-br overflow-hidden">
      <div class="w-full max-w-md mx-auto bg-white rounded-2xl shadow-lg px-8 py-10">
        <form @submit.prevent="onRegisterClick" class="space-y-6" autocomplete="off">
          <h2 class="text-3xl font-bold text-center mb-8 flex items-center justify-center gap-2">
            注册
          </h2>
          <div>
            <span class="p-input-icon-left w-full">
              <i class="pi pi-user text-gray-500" />
              <InputText
                v-model="account"
                type="text"
                class="w-full"
                size="large"
                placeholder="用户名"
                autocomplete="username"
                :class="inputError && !account ? 'border-red-500' : ''"
              />
            </span>
          </div>
          <div>
            <span class="p-input-icon-left w-full">
              <i class="pi pi-lock text-gray-500" />
              <Password
                v-model="password"
                toggleMask
                :feedback="true"
                placeholder="密码"
                class="w-full"
                inputClass="w-full"
                size="large"
                autocomplete="new-password"
                :class="inputError && !password ? 'border-red-500' : ''"
              />
            </span>
          </div>
          <div class="flex justify-between items-center">
            <router-link to="/login" class="text-blue-500 hover:underline text-sm flex items-center">
              <i class="pi pi-arrow-left text-gray-500 mr-1"></i> 返回登录
            </router-link>
          </div>
          <Button
            label="注册"
            icon="pi pi-user-plus"
            class="w-full"
            size="large"
            :loading="loading"
            @click="onRegisterClick"
          />
          <div v-if="regError" class="text-red-500 text-sm mt-4 text-center">
            {{ regError }}
          </div>
          <div v-if="regSuccess" class="text-green-600 text-sm mt-4 text-center">
            {{ regSuccess }}
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import InputText from 'primevue/inputtext'
  import Password from 'primevue/password'
  import Button from 'primevue/button'
  import axios from 'axios'
  
  const account = ref('')
  const password = ref('')
  const loading = ref(false)
  const regError = ref('')
  const regSuccess = ref('')
  const inputError = ref(false)
  
  const router = useRouter()
  const BACKEND_PATH = import.meta.env.VITE_BACKEND_PATH
  
  async function onRegisterClick() {
    regError.value = ''
    regSuccess.value = ''
    inputError.value = false
    if (!account.value || !password.value) {
      regError.value = '请输入用户名和密码'
      inputError.value = true
      return
    }
    loading.value = true
    try {
      const response = await axios.post(`${BACKEND_PATH}/register`, {
        username: account.value,
        password: password.value
      })
      if (response.data.error) {
        regError.value = '注册失败: ' + response.data.error
      } else {
        regSuccess.value = '注册成功，正在跳转登录...'
        setTimeout(() => {
          router.push({ name: 'login' })
        }, 1000)
      }
    } catch (error) {
      if (error.response && error.response.data.error) {
        regError.value = '注册失败: ' + error.response.data.error
      } else {
        regError.value = '注册失败: 发生未知错误'
      }
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .p-input-icon-left > .pi {
    left: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
  }
  </style>