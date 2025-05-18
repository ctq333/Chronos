import axios from 'axios'
import store from '@/store'
import { useRouter } from 'vue-router'

const router = useRouter()

// create an axios instance
const http = axios.create({
  baseURL: '/api',
  timeout: 120000
})

// 定义不需要Token验证的API路径白名单
const NO_AUTH_URLS = ['/auth/login', '/auth/register']

// request interceptor
http.interceptors.request.use(config => {
  if (NO_AUTH_URLS.some(url => config.url.includes(url))) {
    return config
  } 

  if (!store.getters.isLogin) {
    store.dispatch('logout')
    router.push("/login")
    return Promise.reject(new Error('Token expired'))
  }

  const token = store.state.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default http