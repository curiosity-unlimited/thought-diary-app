import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import i18n from '@/i18n';

/**
 * Route definitions with lazy loading
 * All components are loaded on-demand to improve initial load time
 */
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      titleKey: 'router.home',
      requiresAuth: false,
      guestOnly: false,
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      titleKey: 'router.login',
      requiresAuth: false,
      guestOnly: true,
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: {
      titleKey: 'router.register',
      requiresAuth: false,
      guestOnly: true,
    },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      titleKey: 'router.dashboard',
      requiresAuth: true,
      guestOnly: false,
    },
  },
  {
    path: '/diaries',
    name: 'Diaries',
    component: () => import('@/views/Diaries.vue'),
    meta: {
      titleKey: 'router.diaries',
      requiresAuth: true,
      guestOnly: false,
    },
  },
  {
    path: '/diaries/:id',
    name: 'DiaryDetail',
    component: () => import('@/views/DiaryDetail.vue'),
    meta: {
      titleKey: 'router.diaryEntry',
      requiresAuth: true,
      guestOnly: false,
    },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: {
      titleKey: 'router.profile',
      requiresAuth: true,
      guestOnly: false,
    },
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue'),
    meta: {
      titleKey: 'router.about',
      requiresAuth: false,
      guestOnly: false,
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      titleKey: 'router.notFound',
      requiresAuth: false,
      guestOnly: false,
    },
  },
];

/**
 * Create router instance with web history mode
 */
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    // Scroll to saved position on back/forward navigation
    if (savedPosition) {
      return savedPosition;
    }
    // Scroll to top on new navigation
    return { top: 0 };
  },
});

/**
 * Navigation guard: Authentication check
 * Redirects unauthenticated users from protected routes to login
 * Redirects authenticated users from guest-only routes to dashboard
 */
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;

  // Update page title using i18n
  const appName = import.meta.env.VITE_APP_NAME || 'Thought Diary App';
  const titleKey = to.meta.titleKey as string | undefined;
  const { t } = i18n.global;
  document.title = titleKey ? `${t(titleKey)} - ${appName}` : appName;

  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Save intended destination for redirect after login
    const intendedRoute = to.fullPath;
    next({
      name: 'Login',
      query: { redirect: intendedRoute },
    });
    return;
  }

  // Check if route is guest-only (login/register pages)
  if (to.meta.guestOnly && isAuthenticated) {
    // Redirect authenticated users to dashboard
    next({ name: 'Dashboard' });
    return;
  }

  // Allow navigation
  next();
});

export default router;
