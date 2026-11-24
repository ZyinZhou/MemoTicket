import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 落地页
  { path: '/', name: 'Home', component: () => import('../views/Home.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/register.vue') },

  // ---------------- 兴趣社区 ----------------
  // 兴趣社区首页
  {
    path: '/community',
    name: 'CommunityHome',
    component: () => import('../views/CommunityHome.vue'),
    meta: { title: '兴趣社区' }
  },
  // 社区动态列表
  {
    path: '/community/feed',
    name: 'CommunityFeed',
    component: () => import('../views/CommunityFeed.vue'),
    meta: { title: '社区动态' }
  },
  // 体验分享发布（需登录）
  {
    path: '/share/create',
    name: 'ShareCreate',
    component: () => import('../views/ShareCreate.vue'),
    meta: { requiresAuth: true, title: '发布体验分享' }
  },
  // 体验分享详情
  {
    path: '/share/:id',
    name: 'ShareDetail',
    component: () => import('../views/ShareDetail.vue'),
    meta: { title: '分享详情' }
  },

  // ---------------- 票夹 ----------------
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/profile.vue'),
    meta: { requiresAuth: true, title: '个人主页' }
  },
  // 票夹列表页
  {
    path: '/tickets',
    name: 'TicketList',
    component: () => import('../views/TicketList.vue'),
    meta: { requiresAuth: true, title: '我的票夹' }
  },
  // 票根详情页
  {
    path: '/ticket/:id',
    name: 'TicketDetail',
    component: () => import('../views/TicketDetail.vue'),
    meta: { requiresAuth: true, title: '票根详情' }
  },
  // 票根编辑/新增页
  {
    path: '/ticket/edit/:id?',
    name: 'TicketEdit',
    component: () => import('../views/TicketEdit.vue'),
    meta: { requiresAuth: true, title: '编辑票根' }
  },

  // 旧入口兼容：兴趣广场已并入社区
  { path: '/interests', redirect: '/community' },
  // 兜底 404
  { path: '/:pathMatch(.*)*', redirect: '/community' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    // 记录来源页，登录后可回跳
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

router.afterEach((to) => {
  const title = to.meta?.title
  document.title = title ? `${title} · MemoTicket` : 'MemoTicket · 兴趣社区'
})

export default router
