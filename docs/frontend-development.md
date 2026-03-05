# Frontend Development Guide

This guide covers the development setup, workflow, and common tasks for the Thought Diary App frontend.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Common Tasks](#common-tasks)
- [Debugging](#debugging)
- [Code Quality](#code-quality)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting frontend development, ensure you have:

- **Node.js**: Version 18+ ([Download](https://nodejs.org/))
- **npm**: Comes with Node.js (verify with `npm --version`)
- **Git**: For version control
- **VS Code** (recommended): With Vue, ESLint, and Prettier extensions

## Initial Setup

### 1. Clone and Navigate to Frontend

```bash
# From project root
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

This installs all dependencies from `package.json`:
- **Runtime**: vue, vue-router, pinia, axios, vue-toastification
- **UI**: tailwindcss, @headlessui/vue
- **Validation**: vee-validate, yup
- **Dev Tools**: vite, typescript, vitest, eslint, prettier

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:5000

# App Information
VITE_APP_NAME=Thought Diary
VITE_APP_VERSION=0.1.0
```

**Environment Variable Rules:**
- All frontend environment variables must start with `VITE_`
- Changes require dev server restart
- Never commit `.env` file (use `.env.example` for documentation)

### 4. Start Development Server

```bash
npm run dev
```

The app will be available at:
- **Local**: http://localhost:5173
- **Network**: Check terminal output for network URL

**Hot Module Replacement (HMR):**
- Changes to Vue components reload instantly
- CSS/Tailwind changes apply without full reload
- TypeScript/config changes may require manual refresh

## Project Structure

```
frontend/
├── src/                      # Source code
│   ├── main.ts              # App entry point
│   ├── App.vue              # Root component
│   ├── style.css            # Global styles
│   ├── assets/              # Static assets
│   ├── components/          # Reusable components
│   │   ├── DeleteConfirmationModal.vue
│   │   ├── DiaryCard.vue
│   │   ├── DiaryForm.vue
│   │   ├── EmptyState.vue
│   │   ├── LoadingSpinner.vue
│   │   ├── Navbar.vue
│   │   ├── Pagination.vue
│   │   └── StatsCard.vue
│   ├── composables/         # Reusable composition functions
│   │   └── useToast.ts
│   ├── layouts/             # Layout components
│   │   ├── AuthLayout.vue
│   │   └── MainLayout.vue
│   ├── router/              # Vue Router configuration
│   │   └── index.ts
│   ├── services/            # API and external services
│   │   └── api.ts
│   ├── stores/              # Pinia state management
│   │   ├── auth.ts
│   │   ├── diaries.ts
│   │   └── ui.ts
│   ├── types/               # TypeScript type definitions
│   │   └── index.ts
│   ├── utils/               # Utility functions
│   │   └── validationSchemas.ts
│   └── views/               # Page components
│       ├── About.vue
│       ├── Dashboard.vue
│       ├── Diaries.vue
│       ├── DiaryDetail.vue
│       ├── Home.vue
│       ├── Login.vue
│       ├── NotFound.vue
│       ├── Profile.vue
│       └── Register.vue
├── tests/                   # Test files
│   ├── unit/               # Unit tests (*.test.ts)
│   └── integration/        # Integration tests (*.spec.ts)
├── public/                 # Static files (copied as-is)
├── index.html              # HTML entry point
├── vite.config.ts          # Vite configuration
├── vitest.config.ts        # Vitest test configuration
├── tsconfig.json           # TypeScript configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── postcss.config.js       # PostCSS configuration
├── eslint.config.js        # ESLint configuration
├── .prettierrc.json        # Prettier configuration
└── package.json            # Dependencies and scripts
```

**Directory Guidelines:**
- **components/**: Reusable UI components (buttons, cards, forms)
- **views/**: Page-level components (mapped to routes)
- **layouts/**: Wrapper components (main layout, auth layout)
- **stores/**: Pinia stores (one file per domain)
- **composables/**: Reusable Vue composition functions
- **utils/**: Pure utility functions (no Vue dependencies)

See [Frontend Architecture](./frontend-architecture.md) for detailed design patterns.

## Development Workflow

### Daily Development

1. **Pull Latest Changes**
   ```bash
   git pull origin develop
   ```

2. **Install New Dependencies** (if package.json changed)
   ```bash
   npm install
   ```

3. **Start Dev Server**
   ```bash
   npm run dev
   ```

4. **Make Changes**
   - Edit files in `src/`
   - Browser updates automatically via HMR

5. **Check Code Quality**
   ```bash
   # Lint code
   npm run lint

   # Format code
   npm run format

   # Run tests
   npm run test
   ```

6. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push
   ```

### Creating New Features

Follow this checklist for new features:

- [ ] Create TypeScript interfaces in `src/types/index.ts`
- [ ] Add API methods in `src/services/api.ts` (if needed)
- [ ] Create/update Pinia store in `src/stores/`
- [ ] Create components in `src/components/`
- [ ] Create views in `src/views/`
- [ ] Add routes in `src/router/index.ts`
- [ ] Write unit tests in `tests/unit/`
- [ ] Write integration tests in `tests/integration/`
- [ ] Update documentation

## Common Tasks

### Adding a New Component

1. **Create Component File**
   ```bash
   # Create in src/components/
   touch src/components/MyComponent.vue
   ```

2. **Component Template**
   ```vue
   <script setup lang="ts">
   import { ref } from 'vue';
   
   // Props
   interface Props {
     title: string;
     count?: number;
   }
   
   const props = withDefaults(defineProps<Props>(), {
     count: 0,
   });
   
   // Emits
   const emit = defineEmits<{
     click: [value: string];
   }>();
   
   // State
   const isActive = ref(false);
   
   // Methods
   const handleClick = () => {
     emit('click', 'value');
   };
   </script>
   
   <template>
     <div class="p-4">
       <h2>{{ title }}</h2>
       <button @click="handleClick">Click Me</button>
     </div>
   </template>
   
   <style scoped>
   /* Component-specific styles */
   </style>
   ```

3. **Create Test File**
   ```bash
   touch tests/unit/src/components/MyComponent.test.ts
   ```

See [Frontend Components](./frontend-components.md) for component patterns.

### Adding a New Route

1. **Create View Component**
   ```bash
   touch src/views/MyView.vue
   ```

2. **Add Route**
   ```typescript
   // src/router/index.ts
   {
     path: '/my-route',
     name: 'MyRoute',
     component: () => import('@/views/MyView.vue'),
     meta: {
       requiresAuth: true,
       title: 'My Page',
     },
   }
   ```

3. **Add Navigation Link**
   ```vue
   <!-- In Navbar.vue or other component -->
   <RouterLink to="/my-route">My Page</RouterLink>
   ```

### Adding API Integration

1. **Define Types**
   ```typescript
   // src/types/index.ts
   export interface MyData {
     id: number;
     name: string;
   }
   
   export interface MyDataResponse {
     data: MyData[];
     total: number;
   }
   ```

2. **Add API Method**
   ```typescript
   // src/services/api.ts
   export const getMyData = async (): Promise<MyDataResponse> => {
     const response = await api.get<MyDataResponse>('/my-endpoint');
     return response.data;
   };
   ```

3. **Use in Store or Component**
   ```typescript
   // In Pinia store
   import { getMyData } from '@/services/api';
   
   const myAction = async () => {
     try {
       const data = await getMyData();
       // Handle data
     } catch (error) {
       // Handle error
     }
   };
   ```

See [Frontend API Integration](./frontend-api.md) for detailed API patterns.

### Adding a Pinia Store

1. **Create Store File**
   ```bash
   touch src/stores/myStore.ts
   ```

2. **Store Template**
   ```typescript
   import { defineStore } from 'pinia';
   import { ref, computed } from 'vue';
   
   export const useMyStore = defineStore('my', () => {
     // State
     const items = ref<MyItem[]>([]);
     const loading = ref(false);
     
     // Getters
     const itemCount = computed(() => items.value.length);
     
     // Actions
     const fetchItems = async () => {
       loading.value = true;
       try {
         const data = await getItems();
         items.value = data;
       } catch (error) {
         console.error('Failed to fetch items:', error);
       } finally {
         loading.value = false;
       }
     };
     
     const clearStore = () => {
       items.value = [];
       loading.value = false;
     };
     
     return {
       items,
       loading,
       itemCount,
       fetchItems,
       clearStore,
     };
   });
   ```

See [Frontend Architecture - State Management](./frontend-architecture.md#state-management) for store patterns.

### Styling Components

**Tailwind CSS Classes:**
```vue
<template>
  <!-- Responsive design -->
  <div class="p-4 md:p-6 lg:p-8">
    <!-- Flex layout -->
    <div class="flex items-center justify-between">
      <!-- Button with states -->
      <button class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50">
        Click Me
      </button>
    </div>
  </div>
</template>
```

**Scoped Styles:**
```vue
<style scoped>
/* Sentiment highlighting from backend */
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

## Debugging

### Vue DevTools

1. **Install Extension**
   - Chrome: [Vue.js devtools](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
   - Firefox: [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)

2. **Features**
   - Inspect component hierarchy
   - View component props and state
   - Track Pinia store state
   - Monitor router navigation
   - View emitted events

### Browser DevTools

**Console Logging:**
```typescript
// Component debugging
console.log('Component mounted:', props);
console.log('State:', state.value);

// Store debugging
import { storeToRefs } from 'pinia';
const { items } = storeToRefs(useMyStore());
console.log('Store items:', items.value);
```

**Network Tab:**
- Monitor API requests
- Check request/response headers
- View JWT tokens
- Debug CORS issues

**Application Tab:**
- Inspect localStorage (JWT tokens)
- Check sessionStorage
- View cookies

### Common Issues

**Issue: Component Not Updating**
```typescript
// BAD: Mutating reactive object
state.user.name = 'New Name';

// GOOD: Replace entire object
state.user = { ...state.user, name: 'New Name' };
```

**Issue: API 401 Unauthorized**
```typescript
// Check token in localStorage
console.log('Access Token:', localStorage.getItem('access_token'));
console.log('Refresh Token:', localStorage.getItem('refresh_token'));

// Check if token is expired
const token = localStorage.getItem('access_token');
if (token) {
  const payload = JSON.parse(atob(token.split('.')[1]));
  console.log('Token expires:', new Date(payload.exp * 1000));
}
```

**Issue: Router Navigation Not Working**
```typescript
// Use router programmatically
import { useRouter } from 'vue-router';
const router = useRouter();

router.push('/dashboard'); // Navigate
router.replace('/login'); // Navigate without history
```

### VS Code Debugging

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Debug Frontend",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/frontend/src",
      "sourceMapPathOverrides": {
        "webpack:///src/*": "${webRoot}/*"
      }
    }
  ]
}
```

## Code Quality

### Linting

**Check for Issues:**
```bash
npm run lint
```

**Auto-fix Issues:**
```bash
npm run lint -- --fix
```

**ESLint Configuration:**
- Configured in `eslint.config.js` (Flat Config)
- Rules: Vue 3, TypeScript, Prettier integration
- Warnings: unused variables, missing types, accessibility

### Formatting

**Format All Files:**
```bash
npm run format
```

**Format Specific File:**
```bash
npx prettier --write src/components/MyComponent.vue
```

**VS Code Integration:**
- Install Prettier extension
- Enable "Format on Save" in settings
- Use `.prettierrc.json` configuration

### Type Checking

**Check Types:**
```bash
npm run type-check
```

**Common Type Errors:**

```typescript
// BAD: Using 'any'
const data: any = await fetchData();

// GOOD: Proper typing
const data: MyData = await fetchData();

// BAD: Implicit any
const handleClick = (event) => {};

// GOOD: Explicit types
const handleClick = (event: MouseEvent) => {};
```

### Testing

**Run All Tests:**
```bash
npm run test
```

**Run Unit Tests Only:**
```bash
npm run test:unit
```

**Run with Coverage:**
```bash
npm run test:coverage
```

**Watch Mode:**
```bash
npm run test -- --watch
```

See [Frontend Testing](./frontend-testing.md) for comprehensive testing guide.

## Troubleshooting

### Dev Server Issues

**Port Already in Use:**
```bash
# Kill process on port 5173
npx kill-port 5173

# Or use different port
npm run dev -- --port 5174
```

**HMR Not Working:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite

# Restart dev server
npm run dev
```

### Build Issues

**TypeScript Errors:**
```bash
# Check for type errors
npm run type-check

# View detailed errors
npx tsc --noEmit
```

**Module Not Found:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues

**CORS Errors:**
- Check backend CORS configuration in `backend/config.py`
- Ensure `VITE_API_BASE_URL` matches backend origin
- Backend should allow `http://localhost:5173` in development

**Network Errors:**
```bash
# Check backend is running
curl http://localhost:5000/health

# Check environment variables
cat .env | grep VITE_API_BASE_URL
```

### Test Issues

**Tests Failing:**
```bash
# Clear test cache
rm -rf node_modules/.vitest

# Run tests with verbose output
npm run test -- --reporter=verbose
```

**Coverage Not Generated:**
```bash
# Install coverage package
npm install --save-dev @vitest/coverage-v8

# Run with coverage
npm run test:coverage
```

## Performance Tips

### Development Performance

1. **Limit Console Logs**: Remove or comment out excessive logging
2. **Use Production Build**: Test with `npm run build` and `npm run preview`
3. **Monitor Bundle Size**: Use Vite bundle analyzer
4. **Lazy Load Routes**: Already configured with dynamic imports

### Code Splitting

Routes are automatically code-split:

```typescript
// This creates separate chunks
component: () => import('@/views/Dashboard.vue')
```

### Optimizing Images

```vue
<!-- Use appropriate image formats -->
<img src="@/assets/logo.svg" alt="Logo" />

<!-- Lazy load images -->
<img src="@/assets/large-image.jpg" loading="lazy" alt="Description" />
```

## Next Steps

- Review [Frontend Architecture](./frontend-architecture.md) for design patterns
- Check [Frontend Components](./frontend-components.md) for component library
- Read [Frontend Testing](./frontend-testing.md) for testing strategies
- See [Frontend API Integration](./frontend-api.md) for backend communication
- Review [Frontend Deployment](./frontend-deployment.md) for production setup

## Getting Help

**Resources:**
- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Pinia Documentation](https://pinia.vuejs.org/)

**Project-Specific:**
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Review [README.md](../README.md) for project overview
- See [Backend Development](./backend-development.md) for backend integration
