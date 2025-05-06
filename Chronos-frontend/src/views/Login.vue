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
  import InputText from 'primevue/inputtext'
  import Password from 'primevue/password'
  import Button from 'primevue/button'
  import axios from 'axios'
  
  const account = ref('')
  const password = ref('')
  const loading = ref(false)
  const loginError = ref('')
  const inputError = ref(false)
  
  const router = useRouter()
  const BACKEND_PATH = import.meta.env.VITE_BACKEND_PATH
  
  function onBtnLoginClick() {
    loginError.value = ''
    inputError.value = false
    if (!account.value || !password.value) {
        loginError.value = '请输入用户名和密码'
        inputError.value = true
        return
    }
    loading.value = true
    axios
        .get(`${BACKEND_PATH}/login?username=${encodeURIComponent(account.value)}&password=${encodeURIComponent(password.value)}`)
        .then(response => {
        if (response.data.length > 0) {
            const userInfo = response.data[0]
            // 判断账户状态
            if (userInfo.status && userInfo.status !== 'active') {
            // 你可以根据后端返回的禁用状态调整条件
            loginError.value = '账户已被管理员禁用，请联系管理员'
            return
            }
            sessionStorage.setItem('uuid', userInfo.uuid)
            sessionStorage.setItem('accessToken', userInfo.accessToken)
            sessionStorage.setItem('isLoggedIn', true)
            router.push({ path: '/' }).then(() => window.location.reload())
        } else {
            loginError.value = '登录失败：用户不存在或密码错误'
        }
        })
        .catch(() => {
        loginError.value = '登录失败：服务器连接异常'
        })
        .finally(() => {
        loading.value = false
        })
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