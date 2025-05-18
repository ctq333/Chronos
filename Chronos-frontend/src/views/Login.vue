<template>
    <div class="fixed inset-0 flex items-center justify-center bg-gradient-to-br overflow-hidden">
      <div class="w-full max-w-md mx-auto bg-white rounded-2xl shadow-lg px-8 py-10">
        <form @submit.prevent="onBtnLoginClick" class="space-y-6" autocomplete="off">
          <h2 class="text-3xl font-bold text-center mb-8 flex items-center justify-center gap-2">
            登录
          </h2>
          <div>
            <span class="p-input-icon-left w-full">
              <i class="pi pi-user text-gray-500" />
              <InputText
                v-model="account"
                type="text"
                class="w-full"
                size="large"
                placeholder="用户名或邮箱"
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
                :feedback="false"
                placeholder="密码"
                class="w-full"
                inputClass="w-full"
                size="large"
                autocomplete="current-password"
                :class="inputError && !password ? 'border-red-500' : ''"
              />
            </span>
          </div>
          <div class="flex justify-between items-center">
            <router-link to="/signup" class="text-blue-500 hover:underline text-sm flex items-center">
              <i class="pi pi-user-plus mr-1"></i> 注册账号
            </router-link>
          </div>
          <Button
            label="登录"
            icon="pi pi-sign-in"
            class="w-full"
            size="large"
            :loading="loading"
            @click="onBtnLoginClick"
          />
          <div v-if="loginError" class="text-red-500 text-sm mt-4 text-center">
            {{ loginError }}
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import store from '@/store'
  import InputText from 'primevue/inputtext'
  import Password from 'primevue/password'
  import Button from 'primevue/button'
  import request from '@/utils/request'
  
  const account = ref('')
  const password = ref('')
  const loading = ref(false)
  const loginError = ref('')
  const inputError = ref(false)
  
  const router = useRouter()
  
  async function onBtnLoginClick() {
    loginError.value = ''
    inputError.value = false

    if (!account.value || !password.value) {
        loginError.value = '请输入用户名和密码'
        inputError.value = true
        return
    }

    loading.value = true
    try {
      const response = await request.post('/auth/login', {
        username: account.value,
        password: password.value
      })
      if (response.data.code === 200) {
        store.commit('SET_USER',response.data.data.user)
        store.commit('SET_TOKEN',response.data.data.token)
        router.push('/')
      } else {
        loginError.value = `登录失败: ${response.data.message}`
      }
    } catch (error) {
      if (error.response) {
        loginError.value = error.response.data.message || '服务器错误'
      } else {
        loginError.value = error.message
      }
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  /* PrimeVue左侧图标美化 */
  .p-input-icon-left > .pi {
    left: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    
  }
  </style>