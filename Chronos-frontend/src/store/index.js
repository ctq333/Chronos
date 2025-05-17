import { createStore } from 'vuex'
import { useRouter } from "vue-router";

const router = useRouter();

export default createStore({
  state: {
    token: sessionStorage.getItem('token') || null,
    user: (() => {
      const userData = sessionStorage.getItem('user');
      if (!userData || userData === 'undefined' || userData === 'null') {
        return null;
      }
      try {
        return JSON.parse(userData);
      } catch (error) {
        sessionStorage.removeItem('user');
        return null;
      }
    })()
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
      sessionStorage.setItem('user', JSON.stringify(user))
    },
    SET_TOKEN(state,token){
      state.token = token
      sessionStorage.setItem('token', token)
    },
    CLEAR_USER(state) {
      state.user = null
      sessionStorage.removeItem('user')
    },
    CLEAR_TOKEN(state) {
      state.token = null
      sessionStorage.removeItem('token')
    }
  },
  actions: {
    logout({ commit }) {
      commit('CLEAR_USER')
      commit('CLEAR_TOKEN')
      router.push("/login")
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    isAdmin:  state => {
      return state.user?.is_admin || false;
    },
    isLogin(state) {
      // 1. 检查 token 是否存在
      if (!state.token) return false;
      
      // 2. 检查 token 过期时间
      const expiresAt = state.user?.token_expires_at;
      if (!expiresAt) return false; // 若过期时间不存在，视为无效
      
      // 3. 比较当前时间与过期时间
      const now = new Date();
      return new Date(expiresAt) > now;
    }
  }
})