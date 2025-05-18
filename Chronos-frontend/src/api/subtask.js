// src/api/subtask.js
import axios from 'axios'

const baseURL = 'http://localhost:5000/api/subtask'

// 创建带认证的实例
const api = axios.create({
  baseURL,
  headers: {
    Authorization: `Bearer ${localStorage.getItem('token')}`
  }
})

// 添加响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      // 跳转到登录页
      window.location.href = '/login'
    }
    return Promise.reject(error.response?.data || error.message)
  }
)

export default {
  /**
   * 获取子任务列表
   * @param {number} taskId - 主任务ID
   */
  getSubtasks(taskId) {
    return api.get(`/by_task/${taskId}`)
  },

  /**
   * 修改子任务
   * @param {number} subtaskId - 子任务ID 
   * @param {object} data - 更新数据
   */
  updateSubtask(subtaskId, data) {
    return api.put(`/${subtaskId}`, data)
  }
}