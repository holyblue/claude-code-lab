import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    redirect: '/time-entries',
  },
  {
    path: '/time-entries',
    name: 'TimeEntries',
    component: () => import('../views/TimeEntries.vue'),
    meta: { title: '工時記錄' },
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: () => import('../views/Calendar.vue'),
    meta: { title: '日曆視圖' },
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/Projects.vue'),
    meta: { title: '專案管理' },
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('../views/Statistics.vue'),
    meta: { title: '統計報表' },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
    meta: { title: '系統設定' },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// 路由守衛
router.beforeEach((to, _from, next) => {
  // 設定頁面標題
  document.title = (to.meta.title as string) || '工時記錄系統'
  next()
})

export default router
