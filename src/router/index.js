import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: () => import('../views/Login.vue') },
  { path: '/register', component: () => import('../views/Register.vue') },
  { 
    path: '/profile', 
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true } // 需要登录才能访问
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局路由守卫：未登录跳回登录页
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router