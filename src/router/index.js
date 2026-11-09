import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: () => import('../views/Login.vue') },
  { path: '/register', component: () => import('../views/Register.vue') },
  { 
    path: '/profile', 
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true } 
  },
  // 票夹列表页
  {
    path: '/tickets',
    component: () => import('../views/TicketList.vue'),
    meta: { requiresAuth: true }
  },
  // 票根详情页
  {
    path: '/ticket/:id',
    component: () => import('../views/TicketDetail.vue'),
    meta: { requiresAuth: true }
  },
  // 票根编辑/新增页
  {
    path: '/ticket/edit/:id?',
    component: () => import('../views/TicketEdit.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router