# Frontend Testing

This document describes the testing strategy, setup, and best practices for the Thought Diary App frontend.

## Table of Contents
- [Overview](#overview)
- [Testing Infrastructure](#testing-infrastructure)
- [Testing Strategy](#testing-strategy)
- [Unit Testing](#unit-testing)
- [Integration Testing](#integration-testing)
- [Component Testing Patterns](#component-testing-patterns)
- [Store Testing](#store-testing)
- [API Testing](#api-testing)
- [Test Coverage](#test-coverage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The frontend uses **Vitest** as the primary testing framework with **Vue Test Utils** for component testing and **axios-mock-adapter** for API mocking.

**Testing Goals:**
- 80%+ code coverage across all metrics
- Test critical user paths
- Catch regressions early
- Document component behavior
- Enable confident refactoring

**Test Types:**
- **Unit Tests**: Isolated component/function tests (*.test.ts)
- **Integration Tests**: Component integration and API tests (*.spec.ts)

## Testing Infrastructure

### Dependencies

```json
{
  "vitest": "^2.1.8",
  "@vitest/ui": "^2.1.8",
  "@vitest/coverage-v8": "^2.1.8",
  "@vue/test-utils": "^2.4.6",
  "axios-mock-adapter": "^2.1.0",
  "jsdom": "^25.0.1"
}
```

### Configuration

**vitest.config.ts:**
```typescript
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/unit/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '*.config.*',
        'src/main.ts',
      ],
      // 80%+ coverage requirements
      thresholds: {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80,
      },
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
});
```

### Test Setup

**tests/unit/setup.ts:**
```typescript
import { vi } from 'vitest';

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
global.localStorage = localStorageMock as Storage;

// Mock toast
vi.mock('vue-toastification', () => ({
  useToast: () => ({
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
    warning: vi.fn(),
  }),
  POSITION: {
    TOP_RIGHT: 'top-right',
  },
}));

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});
```

### Test Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:unit": "vitest --run tests/unit",
    "test:integration": "vitest --run tests/integration",
    "test:coverage": "vitest --coverage"
  }
}
```

## Testing Strategy

### Test Organization

```
tests/
├── unit/                    # Unit tests (*.test.ts)
│   ├── setup.ts            # Global test setup
│   └── src/
│       ├── components/     # Component unit tests
│       ├── composables/    # Composable tests
│       ├── stores/         # Store tests
│       ├── utils/          # Utility function tests
│       └── views/          # View unit tests (with stubs)
└── integration/            # Integration tests (*.spec.ts)
    └── src/
        ├── services/       # API integration tests
        └── views/          # View integration tests (no stubs)
```

**Directory Rules:**
- Mirror source code structure
- Unit tests: Isolated with stubs/mocks
- Integration tests: Test component/service integration
- Place tests next to what they test conceptually

### Test Naming

**Files:**
- Unit tests: `ComponentName.test.ts`
- Integration tests: `ComponentName.spec.ts`

**Test Suites:**
```typescript
describe('ComponentName', () => {
  describe('Feature/Method', () => {
    it('should do something specific', () => {
      // Test
    });
  });
});
```

## Unit Testing

### Component Unit Tests

**Example: LoadingSpinner.test.ts**

```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import LoadingSpinner from '@/components/LoadingSpinner.vue';

describe('LoadingSpinner', () => {
  describe('rendering', () => {
    it('should render with default props', () => {
      const wrapper = mount(LoadingSpinner);
      expect(wrapper.find('svg').exists()).toBe(true);
    });

    it('should render with custom size', () => {
      const wrapper = mount(LoadingSpinner, {
        props: { size: 'lg' },
      });
      expect(wrapper.find('.h-12.w-12').exists()).toBe(true);
    });

    it('should display loading message when provided', () => {
      const wrapper = mount(LoadingSpinner, {
        props: { message: 'Loading data...' },
      });
      expect(wrapper.text()).toContain('Loading data...');
    });
  });

  describe('centering', () => {
    it('should apply centered classes when centered prop is true', () => {
      const wrapper = mount(LoadingSpinner, {
        props: { centered: true },
      });
      expect(wrapper.find('.flex.items-center.justify-center').exists()).toBe(true);
    });
  });
});
```

### View Unit Tests (With Stubs)

**Example: Dashboard.test.ts**

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, VueWrapper } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import Dashboard from '@/views/Dashboard.vue';
import { useDiariesStore } from '@/stores/diaries';

// Stub child components
vi.mock('@/components/StatsCard.vue', () => ({
  default: { template: '<div class="stats-card-stub"></div>' },
}));

vi.mock('@/components/DiaryCard.vue', () => ({
  default: { template: '<div class="diary-card-stub"></div>' },
}));

describe('Dashboard', () => {
  let wrapper: VueWrapper;
  let diariesStore: ReturnType<typeof useDiariesStore>;

  beforeEach(() => {
    setActivePinia(createPinia());
    diariesStore = useDiariesStore();

    // Mock store data
    diariesStore.stats = {
      total: 10,
      positive: 5,
      negative: 3,
      neutral: 2,
    };
    diariesStore.entries = [
      {
        id: 1,
        content: 'Test diary',
        analyzed_content: 'Test diary',
        positive_count: 1,
        negative_count: 0,
        created_at: '2026-01-01T00:00:00',
        updated_at: '2026-01-01T00:00:00',
        user_id: 1,
      },
    ];

    wrapper = mount(Dashboard, {
      global: {
        plugins: [createPinia()],
        stubs: {
          RouterLink: true,
          StatsCard: true,
          DiaryCard: true,
        },
      },
    });
  });

  it('should render dashboard title', () => {
    expect(wrapper.text()).toContain('Dashboard');
  });

  it('should display stats cards', () => {
    const statsCards = wrapper.findAll('.stats-card-stub');
    expect(statsCards).toHaveLength(4); // Total, Positive, Negative, Neutral
  });

  it('should display recent diaries', () => {
    const diaryCards = wrapper.findAll('.diary-card-stub');
    expect(diaryCards.length).toBeGreaterThan(0);
  });

  it('should call fetchStats on mount', () => {
    const fetchStatsSpy = vi.spyOn(diariesStore, 'fetchStats');
    mount(Dashboard, {
      global: {
        plugins: [createPinia()],
      },
    });
    expect(fetchStatsSpy).toHaveBeenCalled();
  });
});
```

### Utility Function Tests

**Example: validationSchemas.test.ts**

```typescript
import { describe, it, expect } from 'vitest';
import { emailSchema, passwordSchema } from '@/utils/validationSchemas';

describe('validationSchemas', () => {
  describe('emailSchema', () => {
    it('should validate correct email', async () => {
      const result = await emailSchema.isValid('test@example.com');
      expect(result).toBe(true);
    });

    it('should reject invalid email format', async () => {
      const result = await emailSchema.isValid('invalid-email');
      expect(result).toBe(false);
    });

    it('should reject email exceeding max length', async () => {
      const longEmail = 'a'.repeat(110) + '@example.com';
      const result = await emailSchema.isValid(longEmail);
      expect(result).toBe(false);
    });
  });

  describe('passwordSchema', () => {
    it('should validate strong password', async () => {
      const result = await passwordSchema.isValid('SecurePass123!');
      expect(result).toBe(true);
    });

    it('should reject password without uppercase', async () => {
      const result = await passwordSchema.isValid('securepass123!');
      expect(result).toBe(false);
    });

    it('should reject password without digit', async () => {
      const result = await passwordSchema.isValid('SecurePass!');
      expect(result).toBe(false);
    });

    it('should reject password without special character', async () => {
      const result = await passwordSchema.isValid('SecurePass123');
      expect(result).toBe(false);
    });
  });
});
```

### Composable Tests

**Example: useToast.test.ts**

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useToast } from '@/composables/useToast';

describe('useToast', () => {
  let toast: ReturnType<typeof useToast>;

  beforeEach(() => {
    toast = useToast();
  });

  it('should call success toast with correct parameters', () => {
    const mockSuccess = vi.fn();
    vi.mocked(toast.showSuccess).mockImplementation(mockSuccess);

    toast.showSuccess('Success message');
    expect(mockSuccess).toHaveBeenCalledWith('Success message');
  });

  it('should call error toast with correct parameters', () => {
    const mockError = vi.fn();
    vi.mocked(toast.showError).mockImplementation(mockError);

    toast.showError('Error message');
    expect(mockError).toHaveBeenCalledWith('Error message');
  });
});
```

## Integration Testing

### View Integration Tests (No Stubs)

**Example: Login.spec.ts**

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, VueWrapper } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/Login.vue';
import { useAuthStore } from '@/stores/auth';

describe('Login Integration', () => {
  let wrapper: VueWrapper;
  let authStore: ReturnType<typeof useAuthStore>;
  let router: ReturnType<typeof createRouter>;

  beforeEach(async () => {
    setActivePinia(createPinia());
    authStore = useAuthStore();

    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/login', component: Login },
        { path: '/dashboard', component: { template: '<div>Dashboard</div>' } },
      ],
    });

    await router.push('/login');
    await router.isReady();

    wrapper = mount(Login, {
      global: {
        plugins: [createPinia(), router],
      },
    });
  });

  it('should integrate form validation with submission', async () => {
    // Fill form with valid data
    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');
    const form = wrapper.find('form');

    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('ValidPass123!');

    // Mock successful login
    vi.spyOn(authStore, 'login').mockResolvedValue();

    await form.trigger('submit');

    // Verify login was called
    expect(authStore.login).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'ValidPass123!',
    });
  });

  it('should display validation errors on invalid submission', async () => {
    const form = wrapper.find('form');

    // Submit empty form
    await form.trigger('submit');

    // Check for validation errors
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain('required');
  });

  it('should redirect to dashboard after successful login', async () => {
    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');
    const form = wrapper.find('form');

    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('ValidPass123!');

    vi.spyOn(authStore, 'login').mockResolvedValue();

    await form.trigger('submit');
    await wrapper.vm.$nextTick();

    // Verify redirect
    expect(router.currentRoute.value.path).toBe('/dashboard');
  });
});
```

### API Integration Tests

**Example: api.spec.ts**

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import MockAdapter from 'axios-mock-adapter';
import { login, getDiaries, createDiary } from '@/services/api';
import api from '@/services/api';

describe('API Service Integration', () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(api);
  });

  afterEach(() => {
    mock.reset();
  });

  describe('Authentication', () => {
    it('should login and return tokens', async () => {
      const loginData = {
        email: 'test@example.com',
        password: 'password123',
      };

      const response = {
        access_token: 'access123',
        refresh_token: 'refresh123',
        user: {
          id: 1,
          email: 'test@example.com',
          created_at: '2026-01-01T00:00:00',
          updated_at: '2026-01-01T00:00:00',
        },
      };

      mock.onPost('/auth/login').reply(200, response);

      const result = await login(loginData);

      expect(result).toEqual(response);
      expect(result.access_token).toBe('access123');
    });

    it('should handle login errors', async () => {
      mock.onPost('/auth/login').reply(401, {
        error: 'Invalid credentials',
        code: 'INVALID_CREDENTIALS',
      });

      await expect(login({
        email: 'test@example.com',
        password: 'wrong',
      })).rejects.toMatchObject({
        message: 'Invalid credentials',
        statusCode: 401,
      });
    });
  });

  describe('Diaries', () => {
    it('should fetch diaries with pagination', async () => {
      const response = {
        data: [
          {
            id: 1,
            content: 'Test diary',
            analyzed_content: 'Test diary',
            positive_count: 1,
            negative_count: 0,
            created_at: '2026-01-01T00:00:00',
            updated_at: '2026-01-01T00:00:00',
            user_id: 1,
          },
        ],
        pagination: {
          page: 1,
          per_page: 10,
          total: 1,
          pages: 1,
        },
      };

      mock.onGet('/diaries').reply(200, response);

      const result = await getDiaries(1, 10);

      expect(result).toEqual(response);
      expect(result.data).toHaveLength(1);
      expect(result.pagination.total).toBe(1);
    });

    it('should create diary with sentiment analysis', async () => {
      const createData = {
        content: 'I felt both excitement and anxious',
      };

      const response = {
        id: 1,
        content: 'I felt both excitement and anxious',
        analyzed_content: 'I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span>',
        positive_count: 1,
        negative_count: 1,
        created_at: '2026-01-01T00:00:00',
        updated_at: '2026-01-01T00:00:00',
        user_id: 1,
      };

      mock.onPost('/diaries').reply(201, response);

      const result = await createDiary(createData);

      expect(result).toEqual(response);
      expect(result.analyzed_content).toContain('<span class="positive">');
      expect(result.analyzed_content).toContain('<span class="negative">');
    });
  });

  describe('Token Refresh', () => {
    it('should automatically refresh token on 401', async () => {
      // First request fails with 401
      mock.onGet('/diaries').replyOnce(401);

      // Refresh token succeeds
      mock.onPost('/auth/refresh').reply(200, {
        access_token: 'new_access_token',
      });

      // Retry original request succeeds
      mock.onGet('/diaries').reply(200, { data: [], pagination: {} });

      localStorage.setItem('refresh_token', 'refresh123');

      await getDiaries();

      // Verify refresh was called
      expect(mock.history.post.some(req => req.url === '/auth/refresh')).toBe(true);
    });
  });
});
```

## Component Testing Patterns

### Testing Props

```typescript
it('should render with provided props', () => {
  const wrapper = mount(MyComponent, {
    props: {
      title: 'Test Title',
      count: 5,
    },
  });

  expect(wrapper.text()).toContain('Test Title');
  expect(wrapper.text()).toContain('5');
});
```

### Testing Events

```typescript
it('should emit event on button click', async () => {
  const wrapper = mount(MyComponent);
  const button = wrapper.find('button');

  await button.trigger('click');

  expect(wrapper.emitted('click')).toBeTruthy();
  expect(wrapper.emitted('click')).toHaveLength(1);
});

it('should emit event with payload', async () => {
  const wrapper = mount(MyComponent);

  await wrapper.vm.handleUpdate(42);

  expect(wrapper.emitted('update')).toBeTruthy();
  expect(wrapper.emitted('update')?.[0]).toEqual([42]);
});
```

### Testing Slots

```typescript
it('should render slot content', () => {
  const wrapper = mount(MyComponent, {
    slots: {
      default: '<div>Slot Content</div>',
      header: '<h1>Header Slot</h1>',
    },
  });

  expect(wrapper.html()).toContain('Slot Content');
  expect(wrapper.html()).toContain('Header Slot');
});
```

### Testing Conditional Rendering

```typescript
it('should show loading spinner when loading', async () => {
  const wrapper = mount(MyComponent, {
    props: { loading: true },
  });

  expect(wrapper.findComponent(LoadingSpinner).exists()).toBe(true);
});

it('should show content when not loading', async () => {
  const wrapper = mount(MyComponent, {
    props: { loading: false },
  });

  expect(wrapper.findComponent(LoadingSpinner).exists()).toBe(false);
  expect(wrapper.find('.content').exists()).toBe(true);
});
```

### Testing User Interactions

```typescript
it('should toggle state on button click', async () => {
  const wrapper = mount(MyComponent);

  expect(wrapper.find('.active').exists()).toBe(false);

  await wrapper.find('button').trigger('click');

  expect(wrapper.find('.active').exists()).toBe(true);
});

it('should update input value', async () => {
  const wrapper = mount(MyComponent);
  const input = wrapper.find('input');

  await input.setValue('new value');

  expect(input.element.value).toBe('new value');
});
```

## Store Testing

### Testing Store State

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '@/stores/auth';

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('should initialize with default state', () => {
    const authStore = useAuthStore();

    expect(authStore.user).toBeNull();
    expect(authStore.accessToken).toBeNull();
    expect(authStore.refreshToken).toBeNull();
    expect(authStore.isAuthenticated).toBe(false);
  });

  it('should update state after login', async () => {
    const authStore = useAuthStore();

    vi.spyOn(api, 'login').mockResolvedValue({
      access_token: 'access123',
      refresh_token: 'refresh123',
      user: {
        id: 1,
        email: 'test@example.com',
        created_at: '2026-01-01',
        updated_at: '2026-01-01',
      },
    });

    await authStore.login({
      email: 'test@example.com',
      password: 'password',
    });

    expect(authStore.user).not.toBeNull();
    expect(authStore.accessToken).toBe('access123');
    expect(authStore.isAuthenticated).toBe(true);
  });
});
```

### Testing Store Actions

```typescript
it('should handle login error', async () => {
  const authStore = useAuthStore();

  vi.spyOn(api, 'login').mockRejectedValue({
    message: 'Invalid credentials',
    statusCode: 401,
  });

  await expect(authStore.login({
    email: 'test@example.com',
    password: 'wrong',
  })).rejects.toMatchObject({
    message: 'Invalid credentials',
  });

  expect(authStore.user).toBeNull();
  expect(authStore.isAuthenticated).toBe(false);
});
```

### Testing Store Getters

```typescript
it('should compute diary count correctly', () => {
  const diariesStore = useDiariesStore();

  diariesStore.entries = [
    { id: 1, /* ... */ },
    { id: 2, /* ... */ },
  ];

  expect(diariesStore.diaryCount).toBe(2);
});
```

## API Testing

### Mocking Axios

```typescript
import MockAdapter from 'axios-mock-adapter';
import api from '@/services/api';

let mock: MockAdapter;

beforeEach(() => {
  mock = new MockAdapter(api);
});

afterEach(() => {
  mock.reset();
});

it('should make GET request', async () => {
  mock.onGet('/diaries').reply(200, {
    data: [],
    pagination: {},
  });

  const result = await getDiaries();

  expect(result).toEqual({ data: [], pagination: {} });
});
```

### Testing Error Handling

```typescript
it('should handle network errors', async () => {
  mock.onGet('/diaries').networkError();

  await expect(getDiaries()).rejects.toThrow();
});

it('should handle timeout', async () => {
  mock.onGet('/diaries').timeout();

  await expect(getDiaries()).rejects.toThrow();
});
```

## Test Coverage

### Running Coverage

```bash
npm run test:coverage
```

### Coverage Output

```
------------------------|---------|----------|---------|---------|
File                    | % Stmts | % Branch | % Funcs | % Lines |
------------------------|---------|----------|---------|---------|
All files               |   95.32 |    92.15 |   94.87 |   95.32 |
 src                    |     100 |      100 |     100 |     100 |
  App.vue               |     100 |      100 |     100 |     100 |
  main.ts               |       0 |        0 |       0 |       0 | (excluded)
 src/components         |   96.15 |    93.75 |   95.23 |   96.15 |
  DiaryCard.vue         |   97.14 |    95.83 |     100 |   97.14 |
  DiaryForm.vue         |   95.23 |    91.66 |   90.47 |   95.23 |
  LoadingSpinner.vue    |     100 |      100 |     100 |     100 |
  ...                   |     ... |      ... |     ... |     ... |
 src/stores             |   94.73 |    89.47 |   93.75 |   94.73 |
  auth.ts               |   95.45 |    88.88 |   93.33 |   95.45 |
  diaries.ts            |   94.11 |    90.00 |   94.11 |   94.11 |
------------------------|---------|----------|---------|---------|
```

### Coverage Requirements

**Thresholds (80%+):**
- Statements: 80%
- Branches: 80%
- Functions: 80%
- Lines: 80%

**Current Coverage: 95%+ across all metrics**

### Viewing Coverage Report

```bash
npm run test:coverage
open coverage/index.html
```

## Best Practices

### 1. Arrange-Act-Assert Pattern

```typescript
it('should update diary count', async () => {
  // Arrange
  const diariesStore = useDiariesStore();
  diariesStore.entries = [];

  // Act
  await diariesStore.createDiary({ content: 'New diary' });

  // Assert
  expect(diariesStore.entries).toHaveLength(1);
});
```

### 2. Test One Thing at a Time

```typescript
// ✅ Good: Focused test
it('should display error message on login failure', async () => {
  // ... test error display only
});

// ❌ Bad: Testing multiple things
it('should handle login flow', async () => {
  // ... tests validation, submission, success, error
});
```

### 3. Use Descriptive Test Names

```typescript
// ✅ Good: Clear what is being tested
it('should disable submit button when form is invalid', () => {});

// ❌ Bad: Vague description
it('should work', () => {});
```

### 4. Avoid Implementation Details

```typescript
// ✅ Good: Test behavior
it('should display user email in navbar', () => {
  expect(wrapper.text()).toContain('user@example.com');
});

// ❌ Bad: Test implementation
it('should set userEmail ref to user.email', () => {
  expect(wrapper.vm.userEmail).toBe('user@example.com');
});
```

### 5. Mock External Dependencies

```typescript
// ✅ Good: Mock API calls
vi.spyOn(api, 'getDiaries').mockResolvedValue({ data: [], pagination: {} });

// ❌ Bad: Real API calls in tests
await api.getDiaries(); // Makes actual HTTP request
```

### 6. Clean Up After Tests

```typescript
afterEach(() => {
  mock.reset();
  localStorage.clear();
  vi.clearAllMocks();
});
```

### 7. Test Edge Cases

```typescript
describe('Pagination', () => {
  it('should handle first page', () => {});
  it('should handle last page', () => {});
  it('should handle single page', () => {});
  it('should handle no results', () => {});
});
```

## Troubleshooting

### Common Issues

**Issue: Tests Timing Out**
```typescript
// Increase timeout for specific test
it('should load data', async () => {
  // ...
}, 10000); // 10 second timeout
```

**Issue: Async Test Failures**
```typescript
// ✅ Good: Await all async operations
await wrapper.vm.$nextTick();
await flushPromises();

// ❌ Bad: Missing awaits
wrapper.vm.$nextTick();
```

**Issue: Component Not Found**
```typescript
// ✅ Good: Use findComponent for components
wrapper.findComponent(LoadingSpinner);

// ❌ Bad: Use find for components
wrapper.find('LoadingSpinner');
```

**Issue: Store Not Updating**
```typescript
// ✅ Good: Use storeToRefs for reactivity
const { loading } = storeToRefs(diariesStore);

// ❌ Bad: Direct access loses reactivity
const loading = diariesStore.loading;
```

### Debugging Tests

**Console Logging:**
```typescript
it('should render correctly', () => {
  const wrapper = mount(MyComponent);

  // Debug: Print wrapper HTML
  console.log(wrapper.html());

  // Debug: Print component data
  console.log(wrapper.vm.$data);
});
```

**Running Single Test:**
```bash
# Run specific test file
npm run test Login.test.ts

# Run single test with grep
npm run test -- -t "should display error"
```

**Watch Mode:**
```bash
npm run test -- --watch
```

## Related Documentation

- [Frontend Development](./frontend-development.md) - Development setup
- [Frontend Architecture](./frontend-architecture.md) - Architecture patterns
- [Frontend Components](./frontend-components.md) - Component library
- [Frontend API Integration](./frontend-api.md) - API testing patterns
