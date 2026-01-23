# Frontend Architecture

This document describes the architectural patterns, design decisions, and technical structure of the Thought Diary App frontend.

## Table of Contents
- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Architecture Patterns](#architecture-patterns)
- [State Management](#state-management)
- [Routing Architecture](#routing-architecture)
- [Component Architecture](#component-architecture)
- [Styling System](#styling-system)
- [API Integration](#api-integration)
- [Authentication Flow](#authentication-flow)
- [Error Handling](#error-handling)
- [Performance Considerations](#performance-considerations)

## Overview

The frontend follows a modern, component-based architecture using Vue 3 with TypeScript. The application is built with:

- **Framework**: Vue 3 Composition API
- **Language**: TypeScript (strict mode)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Routing**: Vue Router 4
- **Styling**: Tailwind CSS + Scoped CSS
- **Testing**: Vitest + Vue Test Utils

### Architecture Principles

1. **Separation of Concerns**: Clear boundaries between UI, logic, and data
2. **Type Safety**: TypeScript strict mode throughout
3. **Composition Over Inheritance**: Vue 3 Composition API patterns
4. **Single Responsibility**: Components and functions do one thing well
5. **DRY (Don't Repeat Yourself)**: Reusable composables and utilities
6. **Progressive Enhancement**: Works without JavaScript where possible
7. **Mobile-First**: Responsive design from smallest screens up

## Technology Stack

### Core Dependencies

```json
{
  "vue": "^3.5.13",
  "vue-router": "^4.5.0",
  "pinia": "^2.3.0",
  "axios": "^1.7.9",
  "typescript": "~5.7.2",
  "vite": "^6.0.5"
}
```

### UI Framework

```json
{
  "tailwindcss": "^4.0.0",
  "@headlessui/vue": "^1.7.25",
  "vue-toastification": "^2.0.0-rc.5"
}
```

### Form Validation

```json
{
  "vee-validate": "^4.15.1",
  "yup": "^1.6.1"
}
```

### Development Tools

```json
{
  "vitest": "^2.1.8",
  "@vue/test-utils": "^2.4.6",
  "eslint": "^9.18.0",
  "prettier": "^3.4.2"
}
```

## Architecture Patterns

### Application Factory Pattern

The application is initialized in `main.ts` with a clear plugin registration order:

```typescript
// src/main.ts
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import Toast from 'vue-toastification';
import App from './App.vue';

const app = createApp(App);

// Plugin order matters:
// 1. Pinia (state management)
app.use(createPinia());

// 2. Router (depends on Pinia for auth guards)
app.use(router);

// 3. Toast (UI notifications)
app.use(Toast, {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
});

app.mount('#app');
```

**Why This Order:**
1. Pinia first: Stores needed by router guards
2. Router second: Navigation setup before rendering
3. Toast last: UI enhancement, non-critical

### Module Organization

```
src/
├── main.ts              # App entry point
├── App.vue              # Root component
├── components/          # Reusable UI components
├── composables/         # Reusable composition functions
├── layouts/             # Layout wrappers
├── router/              # Routing configuration
├── services/            # External service integrations
├── stores/              # Pinia state management
├── types/               # TypeScript definitions
├── utils/               # Pure utility functions
└── views/               # Page-level components
```

**Directory Rules:**
- **components/**: No business logic, accept props, emit events
- **views/**: Page components, use stores, handle route params
- **composables/**: Reusable logic, return reactive values
- **utils/**: Pure functions, no Vue dependencies
- **stores/**: State management, API calls, business logic
- **services/**: External integrations (API, third-party)

## State Management

### Pinia Store Architecture

We use Pinia with Composition API syntax for type safety and clarity:

```typescript
// Example store structure
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useMyStore = defineStore('myStore', () => {
  // State (reactive references)
  const items = ref<Item[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  
  // Getters (computed properties)
  const itemCount = computed(() => items.value.length);
  const hasItems = computed(() => items.value.length > 0);
  
  // Actions (functions)
  const fetchItems = async () => {
    loading.value = true;
    error.value = null;
    try {
      const data = await api.getItems();
      items.value = data;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch';
      throw err;
    } finally {
      loading.value = false;
    }
  };
  
  const clearStore = () => {
    items.value = [];
    loading.value = false;
    error.value = null;
  };
  
  return {
    // State
    items,
    loading,
    error,
    // Getters
    itemCount,
    hasItems,
    // Actions
    fetchItems,
    clearStore,
  };
});
```

### Store Structure

#### Auth Store (`stores/auth.ts`)

**Purpose**: User authentication and session management

**State:**
- `user`: Current user information
- `accessToken`: JWT access token
- `refreshToken`: JWT refresh token

**Key Actions:**
- `register()`: User registration
- `login()`: User authentication
- `logout()`: Session cleanup
- `refreshAccessToken()`: Token renewal
- `fetchProfile()`: Get current user data

**Persistence:**
- Tokens stored in localStorage
- Auto-restore on app initialization
- Clear on logout

#### Diaries Store (`stores/diaries.ts`)

**Purpose**: Thought diary management and statistics

**State:**
- `entries`: Array of diary entries
- `currentDiary`: Single diary for detail view
- `stats`: Statistics (total, positive, negative, neutral)
- `pagination`: Page info (page, per_page, total)
- `loading`: Loading state flag

**Key Actions:**
- `fetchDiaries()`: List diaries with pagination
- `fetchDiary()`: Get single diary
- `createDiary()`: Create new entry
- `updateDiary()`: Update existing entry
- `deleteDiary()`: Remove entry
- `fetchStats()`: Get statistics

**Patterns:**
- Optimistic UI updates
- Automatic list refresh after mutations
- Pagination state management

#### UI Store (`stores/ui.ts`)

**Purpose**: Global UI state

**State:**
- `isLoading`: Global loading indicator
- `loadingMessage`: Optional loading text

**Key Actions:**
- `setLoading()`: Show loading state
- `clearLoading()`: Hide loading state

**Usage:**
- API call loading overlays
- Navigation loading states
- Long-running operations

### Store Best Practices

1. **Single Responsibility**: One store per domain
2. **Type Safety**: Use TypeScript interfaces
3. **Error Handling**: Catch and expose errors
4. **Loading States**: Track async operations
5. **Cleanup**: Provide `clearStore()` method
6. **Immutability**: Replace objects, don't mutate
7. **Computed Values**: Use for derived state

## Routing Architecture

### Route Configuration

Routes are defined in `src/router/index.ts`:

```typescript
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue'),
      meta: { title: 'Home' },
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true, title: 'Dashboard' },
    },
    // ... more routes
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    return { top: 0 };
  },
});
```

### Route Meta Fields

```typescript
interface RouteMeta {
  requiresAuth?: boolean;  // Requires authentication
  guestOnly?: boolean;     // Only for unauthenticated users
  title?: string;          // Page title
}
```

### Navigation Guards

**Authentication Guard:**

```typescript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.meta.requiresAuth;
  const guestOnly = to.meta.guestOnly;
  const isAuthenticated = authStore.isAuthenticated;

  if (requiresAuth && !isAuthenticated) {
    // Redirect to login, save intended destination
    next({
      name: 'Login',
      query: { redirect: to.fullPath },
    });
  } else if (guestOnly && isAuthenticated) {
    // Redirect authenticated users to dashboard
    next({ name: 'Dashboard' });
  } else {
    next();
  }
});
```

**Title Guard:**

```typescript
router.afterEach((to) => {
  const appName = import.meta.env.VITE_APP_NAME || 'Thought Diary';
  document.title = to.meta.title 
    ? `${to.meta.title} - ${appName}` 
    : appName;
});
```

### Lazy Loading

All routes use dynamic imports for code splitting:

```typescript
// Creates separate chunks for each route
component: () => import('@/views/Dashboard.vue')
```

**Benefits:**
- Smaller initial bundle size
- Faster initial page load
- Routes loaded on demand

## Component Architecture

### Component Hierarchy

```
App.vue
├── MainLayout
│   ├── Navbar
│   └── RouterView
│       ├── Dashboard
│       │   ├── StatsCard (×4)
│       │   └── DiaryCard (×N)
│       ├── Diaries
│       │   ├── DiaryForm
│       │   ├── DiaryCard (×N)
│       │   ├── Pagination
│       │   └── EmptyState
│       └── DiaryDetail
│           ├── DiaryForm
│           └── DeleteConfirmationModal
└── AuthLayout
    └── RouterView
        ├── Login
        └── Register
```

### Component Types

#### 1. Layout Components

**Purpose**: Wrap pages with common UI structure

```vue
<!-- MainLayout.vue -->
<script setup lang="ts">
import Navbar from '@/components/Navbar.vue';
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />
    <main class="container mx-auto px-4 py-8">
      <slot />
    </main>
  </div>
</template>
```

**Layout Components:**
- `MainLayout`: For authenticated pages with navbar
- `AuthLayout`: For login/register with centered card

#### 2. View Components (Pages)

**Purpose**: Route-level components, orchestrate child components

**Characteristics:**
- Use Pinia stores
- Handle route parameters
- Coordinate multiple components
- Manage page-level state

**Example:**
```vue
<script setup lang="ts">
import { onMounted } from 'vue';
import { useDiariesStore } from '@/stores/diaries';
import DiaryCard from '@/components/DiaryCard.vue';

const diariesStore = useDiariesStore();

onMounted(() => {
  diariesStore.fetchDiaries();
});
</script>
```

#### 3. UI Components

**Purpose**: Reusable, presentational components

**Characteristics:**
- Accept props for data
- Emit events for interactions
- No direct store access
- Fully typed with TypeScript

**Example:**
```vue
<script setup lang="ts">
interface Props {
  title: string;
  description?: string;
}

const props = withDefaults(defineProps<Props>(), {
  description: '',
});

const emit = defineEmits<{
  click: [];
}>();
</script>
```

See [Frontend Components](./frontend-components.md) for complete component library.

#### 4. Composables

**Purpose**: Reusable composition logic

**Example:**
```typescript
// src/composables/useToast.ts
import { useToast as useVueToast } from 'vue-toastification';

export function useToast() {
  const toast = useVueToast();

  const showSuccess = (message: string) => {
    toast.success(message, { timeout: 3000 });
  };

  const showError = (message: string) => {
    toast.error(message, { timeout: 5000 });
  };

  return {
    showSuccess,
    showError,
  };
}
```

## Styling System

### Tailwind CSS Configuration

```javascript
// tailwind.config.js
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: colors.indigo,
        success: colors.green,
        danger: colors.red,
      },
    },
  },
  plugins: [],
};
```

### Styling Approach

**1. Utility-First with Tailwind:**

```vue
<template>
  <div class="flex items-center justify-between p-4 bg-white rounded-lg shadow-md">
    <h2 class="text-xl font-semibold text-gray-800">Title</h2>
    <button class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
      Action
    </button>
  </div>
</template>
```

**Benefits:**
- Consistent design system
- Responsive utilities (`md:`, `lg:`)
- No CSS naming conflicts
- Tree-shakable (unused styles removed)

**2. Scoped Styles for Specificity:**

```vue
<style scoped>
/* Component-specific styles */
.custom-component {
  /* Styles that don't fit Tailwind patterns */
}

/* Sentiment highlighting (from backend) */
:deep(.positive) {
  background-color: #10b981;
  color: white;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}

:deep(.negative) {
  background-color: #ef4444;
  color: white;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}
</style>
```

**3. Global Styles:**

```css
/* src/style.css */
@import 'tailwindcss';

/* Custom global styles */
body {
  font-family: 'Inter', sans-serif;
}
```

### Responsive Design

**Mobile-First Breakpoints:**

```vue
<template>
  <!-- Mobile: stack vertically, Desktop: side-by-side -->
  <div class="flex flex-col md:flex-row gap-4">
    <div class="w-full md:w-1/2">Column 1</div>
    <div class="w-full md:w-1/2">Column 2</div>
  </div>
</template>
```

**Tailwind Breakpoints:**
- `sm`: 640px and up
- `md`: 768px and up
- `lg`: 1024px and up
- `xl`: 1280px and up
- `2xl`: 1536px and up

## API Integration

### Axios Instance Configuration

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Request Interceptor

**Automatically add JWT token:**

```typescript
api.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);
```

### Response Interceptor

**Handle token refresh:**

```typescript
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const newToken = await refreshAccessToken();
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout
        clearTokens();
        window.location.href = '/login';
        throw refreshError;
      }
    }

    throw error;
  }
);
```

See [Frontend API Integration](./frontend-api.md) for detailed API patterns.

## Authentication Flow

### Registration Flow

```
User → Register Form → Validation → API Call → Success Toast → Redirect to Login
```

1. User fills registration form
2. VeeValidate validates email/password
3. Auth store `register()` action called
4. API: `POST /auth/register`
5. Success: Toast notification, redirect to `/login`
6. Error: Display error message

### Login Flow

```
User → Login Form → Validation → API Call → Store Tokens → Redirect to Dashboard
```

1. User fills login form
2. VeeValidate validates fields
3. Auth store `login()` action called
4. API: `POST /auth/login`
5. Success: Store JWT tokens in localStorage
6. Update auth store state
7. Redirect to intended route or `/dashboard`
8. Error: Display error message

### Protected Route Access

```
User → Navigate to Protected Route → Auth Guard → Check Token → Allow/Deny
```

1. User navigates to protected route
2. Router `beforeEach` guard checks `requiresAuth` meta
3. Check auth store `isAuthenticated`
4. If authenticated: Allow navigation
5. If not: Redirect to `/login` with `?redirect=` query

### Token Refresh Flow

```
API Call → 401 Response → Refresh Token → Retry Original Request
```

1. API request with expired access token
2. Backend returns 401 Unauthorized
3. Response interceptor catches error
4. Call `POST /auth/refresh` with refresh token
5. Receive new access token
6. Update localStorage and auth store
7. Retry original request with new token
8. If refresh fails: Logout and redirect to login

### Logout Flow

```
User → Click Logout → Clear Tokens → Clear Stores → Redirect to Home
```

1. User clicks logout button
2. Auth store `logout()` action called
3. API: `POST /auth/logout` (blacklist token)
4. Clear localStorage (tokens)
5. Clear all Pinia stores
6. Success toast notification
7. Redirect to `/` (home page)

## Error Handling

### Error Types

```typescript
// src/types/index.ts
export interface ApiError {
  message: string;
  code?: string;
  statusCode?: number;
  errors?: Record<string, string[]>;
}
```

### Error Handling Strategy

**1. API Service Level:**
```typescript
// Structured error responses
catch (error) {
  if (axios.isAxiosError(error)) {
    throw {
      message: error.response?.data?.message || 'Request failed',
      code: error.response?.data?.code,
      statusCode: error.response?.status,
      errors: error.response?.data?.errors,
    } as ApiError;
  }
  throw error;
}
```

**2. Store Level:**
```typescript
// Stores catch and expose errors
const fetchData = async () => {
  try {
    const data = await api.getData();
    items.value = data;
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch';
    throw err; // Re-throw for component handling
  }
};
```

**3. Component Level:**
```typescript
// Components handle UI feedback
const handleSubmit = async () => {
  try {
    await myStore.saveData();
    showSuccess('Saved successfully');
    router.push('/list');
  } catch (error) {
    const err = error as ApiError;
    showError(err.message || 'Failed to save');
  }
};
```

### Global Error Handling

**API Interceptor:**
- Network errors: Toast with retry button
- 401 Unauthorized: Auto token refresh or logout
- 403 Forbidden: Toast with appropriate message
- 500 Server errors: Toast with error message

**Form Validation:**
- Handled at component level
- Not shown in global toasts
- Inline error messages below fields

## Performance Considerations

### Code Splitting

**Route-level splitting:**
```typescript
// Each route is a separate chunk
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/Dashboard.vue'),
  },
];
```

**Component-level splitting:**
```typescript
// Heavy components loaded on demand
const HeavyComponent = defineAsyncComponent(
  () => import('@/components/HeavyComponent.vue')
);
```

### Lazy Loading

**Images:**
```vue
<img src="@/assets/image.jpg" loading="lazy" alt="Description" />
```

**Components:**
```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const DiaryDetail = defineAsyncComponent(
  () => import('@/components/DiaryDetail.vue')
);
</script>
```

### Optimization Strategies

1. **Vite Build Optimization:**
   - Automatic code splitting
   - Tree shaking
   - CSS minification
   - Asset optimization

2. **Vue Optimization:**
   - `v-once` for static content
   - `v-memo` for expensive renders
   - `KeepAlive` for cached routes

3. **Network Optimization:**
   - API request caching in stores
   - Debounced search inputs
   - Optimistic UI updates
   - Pagination for large lists

4. **Bundle Size:**
   - Tree-shakable imports
   - Lazy route loading
   - Tailwind CSS purging
   - No unnecessary dependencies

### Performance Metrics

**Development:**
- HMR: < 50ms for most changes
- TypeScript compilation: ~2-3s

**Production:**
- Initial bundle: ~200KB (gzipped)
- Route chunks: 20-50KB each
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s

## Security Considerations

### XSS Prevention

**1. Template Safety:**
```vue
<!-- SAFE: Vue escapes by default -->
<div>{{ userInput }}</div>

<!-- UNSAFE: v-html can execute scripts -->
<div v-html="untrustedContent"></div>

<!-- SAFE: v-html with backend-sanitized content -->
<div v-html="diary.analyzed_content"></div>
```

**2. Input Sanitization:**
- Backend sanitizes all user input
- Frontend validates before submission
- No direct HTML injection

### CSRF Protection

- JWT tokens in localStorage (not cookies)
- No CSRF tokens needed
- `Authorization` header for all protected endpoints

### Secure Token Storage

**localStorage vs sessionStorage:**
- Using localStorage for persistent sessions
- Tokens cleared on logout
- No sensitive data in localStorage beyond tokens

**Token Exposure:**
- Tokens only sent via HTTPS in production
- Not exposed in URLs or logs
- Automatic expiration handling

### Input Validation

**Client-side validation:**
- VeeValidate + Yup schemas
- Real-time feedback
- Type-safe validation rules

**Server-side validation:**
- Backend validates all inputs
- Client validation is UX enhancement
- Never trust client-side validation alone

## Scalability Considerations

### State Management Scaling

**Current:**
- 3 stores (auth, diaries, ui)
- ~50 lines per store

**Future Scaling:**
- Add stores per feature domain
- Use store composition for shared logic
- Consider Pinia plugins for cross-cutting concerns

### Component Library

**Current:**
- 8 reusable components
- Basic component patterns

**Future Scaling:**
- Extract to separate package
- Add Storybook documentation
- Version component library separately

### Code Organization

**As App Grows:**
```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── stores/
│   │   └── views/
│   ├── diaries/
│   │   ├── components/
│   │   ├── stores/
│   │   └── views/
│   └── shared/
│       ├── components/
│       └── composables/
```

## Design Patterns

### Composition Pattern

**Reusable logic via composables:**

```typescript
// composables/useAsync.ts
export function useAsync<T>(fn: () => Promise<T>) {
  const data = ref<T | null>(null);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  const execute = async () => {
    loading.value = true;
    error.value = null;
    try {
      data.value = await fn();
    } catch (err) {
      error.value = err as Error;
    } finally {
      loading.value = false;
    }
  };

  return { data, loading, error, execute };
}
```

### Provide/Inject Pattern

**For deeply nested components:**

```typescript
// Parent
provide('theme', 'dark');

// Child (deep)
const theme = inject<string>('theme');
```

### Slots Pattern

**For flexible component composition:**

```vue
<template>
  <div class="card">
    <header>
      <slot name="header">Default Header</slot>
    </header>
    <main>
      <slot>Default Content</slot>
    </main>
    <footer>
      <slot name="footer">Default Footer</slot>
    </footer>
  </div>
</template>
```

## Related Documentation

- [Frontend Development](./frontend-development.md) - Setup and workflow
- [Frontend Components](./frontend-components.md) - Component library
- [Frontend API Integration](./frontend-api.md) - Backend communication
- [Frontend Testing](./frontend-testing.md) - Testing strategies
- [Frontend Deployment](./frontend-deployment.md) - Production deployment
