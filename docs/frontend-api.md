# Frontend API Integration

This document describes how the frontend integrates with the backend API, including authentication, request handling, error management, and best practices.

## Table of Contents
- [Overview](#overview)
- [API Service Configuration](#api-service-configuration)
- [Authentication Integration](#authentication-integration)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Request Patterns](#request-patterns)
- [Type Safety](#type-safety)
- [Testing API Integration](#testing-api-integration)
- [Best Practices](#best-practices)

## Overview

The frontend communicates with the Flask backend through a RESTful API. All integration logic is centralized in `src/services/api.ts` using Axios for HTTP requests.

**Key Features:**
- Automatic JWT token attachment
- Token refresh on expiration
- Consistent error handling
- TypeScript type safety
- Request/response interceptors
- Timeout management

**Backend API Base URL:**
- Development: `http://localhost:5000`
- Production: Set via `VITE_API_BASE_URL` environment variable

For backend API details, see [Backend API Documentation](./backend-api.md).

## API Service Configuration

### Axios Instance

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});
```

**Configuration:**
- `baseURL`: Backend API endpoint
- `timeout`: 30-second request timeout
- `headers`: JSON content type by default

### Environment Configuration

```bash
# .env
VITE_API_BASE_URL=http://localhost:5000
```

**Production:**
```bash
# .env.production
VITE_API_BASE_URL=https://api.thoughtdiary.com
```

## Authentication Integration

### Request Interceptor

Automatically attaches JWT token to all requests:

```typescript
api.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
```

**Flow:**
1. Request initiated
2. Interceptor checks localStorage for access token
3. If token exists, add `Authorization: Bearer <token>` header
4. Request sent to backend

### Response Interceptor

Handles token expiration and automatic refresh:

```typescript
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value: unknown) => void;
  reject: (reason?: unknown) => void;
}> = [];

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Queue requests while refreshing
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const newToken = await refreshAccessToken();
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        processQueue(null, newToken);
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        clearTokens();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    // Transform error for consistent handling
    if (axios.isAxiosError(error)) {
      throw {
        message: error.response?.data?.message || error.message || 'Request failed',
        code: error.response?.data?.code,
        statusCode: error.response?.status,
        errors: error.response?.data?.errors,
      } as ApiError;
    }

    return Promise.reject(error);
  }
);
```

**Flow:**
1. API returns 401 Unauthorized
2. Interceptor catches error
3. If not already refreshing:
   - Call `/auth/refresh` with refresh token
   - Get new access token
   - Update localStorage
   - Retry original request with new token
4. If multiple requests fail simultaneously:
   - Queue failed requests
   - Refresh token once
   - Replay all queued requests
5. If refresh fails:
   - Clear tokens
   - Redirect to login

### Token Management

```typescript
// Token storage helpers
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

export const getAccessToken = (): string | null => {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
};

export const getRefreshToken = (): string | null => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

export const setTokens = (accessToken: string, refreshToken: string): void => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
};

export const clearTokens = (): void => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

// Token refresh
const refreshAccessToken = async (): Promise<string> => {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  const response = await api.post<TokenResponse>('/auth/refresh', {
    refresh_token: refreshToken,
  });

  const { access_token } = response.data;
  localStorage.setItem(ACCESS_TOKEN_KEY, access_token);

  return access_token;
};
```

## API Endpoints

### Authentication Endpoints

#### Register

```typescript
/**
 * Register a new user
 */
export const register = async (data: RegisterRequest): Promise<void> => {
  await api.post('/auth/register', data);
};

// Usage
import { register } from '@/services/api';

try {
  await register({
    email: 'user@example.com',
    password: 'SecurePass123!',
  });
  // Show success message, redirect to login
} catch (error) {
  // Handle error
}
```

**Backend:** `POST /auth/register`  
**Rate Limit:** 3 requests/hour  
**Response:** 201 Created (no body)

#### Login

```typescript
/**
 * Authenticate user and receive JWT tokens
 */
export const login = async (data: LoginRequest): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/auth/login', data);
  return response.data;
};

// Usage
const response = await login({
  email: 'user@example.com',
  password: 'SecurePass123!',
});

setTokens(response.access_token, response.refresh_token);
```

**Backend:** `POST /auth/login`  
**Rate Limit:** 5 requests/15 minutes  
**Response:** 200 OK with tokens and user data

#### Logout

```typescript
/**
 * Logout user and invalidate token
 */
export const logout = async (): Promise<void> => {
  await api.post('/auth/logout');
  clearTokens();
};
```

**Backend:** `POST /auth/logout`  
**Requires:** Valid access token  
**Response:** 200 OK (token blacklisted)

#### Get Current User

```typescript
/**
 * Get current user profile
 */
export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get<User>('/auth/me');
  return response.data;
};

// Usage
const user = await getCurrentUser();
console.log(user.email);
```

**Backend:** `GET /auth/me`  
**Requires:** Valid access token  
**Response:** 200 OK with user data

### Thought Diaries Endpoints

#### Get Diaries (List)

```typescript
/**
 * Get paginated list of user's diaries
 */
export const getDiaries = async (
  page: number = 1,
  perPage: number = 10
): Promise<DiaryListResponse> => {
  const response = await api.get<DiaryListResponse>('/diaries', {
    params: { page, per_page: perPage },
  });
  return response.data;
};

// Usage
const { data, pagination } = await getDiaries(1, 10);
console.log(`Total: ${pagination.total} diaries`);
```

**Backend:** `GET /diaries?page=1&per_page=10`  
**Requires:** Valid access token  
**Response:** 200 OK with diaries array and pagination info

#### Get Single Diary

```typescript
/**
 * Get a specific diary by ID
 */
export const getDiary = async (id: number): Promise<DiaryEntry> => {
  const response = await api.get<DiaryEntry>(`/diaries/${id}`);
  return response.data;
};

// Usage
const diary = await getDiary(123);
console.log(diary.content);
```

**Backend:** `GET /diaries/:id`  
**Requires:** Valid access token, diary ownership  
**Response:** 200 OK with diary data

#### Create Diary

```typescript
/**
 * Create a new diary entry
 * Backend automatically performs AI sentiment analysis
 */
export const createDiary = async (data: DiaryCreateRequest): Promise<DiaryEntry> => {
  const response = await api.post<DiaryEntry>('/diaries', data);
  return response.data;
};

// Usage
const newDiary = await createDiary({
  content: 'I felt both excitement and anxious today...',
});

// Backend returns with analyzed_content:
// "I felt both <span class='positive'>excitement</span> and <span class='negative'>anxious</span> today..."
```

**Backend:** `POST /diaries`  
**Requires:** Valid access token  
**Response:** 201 Created with diary data (including sentiment analysis)

#### Update Diary

```typescript
/**
 * Update an existing diary entry
 * Backend re-runs AI sentiment analysis
 */
export const updateDiary = async (
  id: number,
  data: DiaryUpdateRequest
): Promise<DiaryEntry> => {
  const response = await api.put<DiaryEntry>(`/diaries/${id}`, data);
  return response.data;
};

// Usage
const updatedDiary = await updateDiary(123, {
  content: 'Updated content with new sentiment...',
});
```

**Backend:** `PUT /diaries/:id`  
**Requires:** Valid access token, diary ownership  
**Response:** 200 OK with updated diary data

#### Delete Diary

```typescript
/**
 * Delete a diary entry
 */
export const deleteDiary = async (id: number): Promise<void> => {
  await api.delete(`/diaries/${id}`);
};

// Usage
await deleteDiary(123);
// Show success toast, refresh list
```

**Backend:** `DELETE /diaries/:id`  
**Requires:** Valid access token, diary ownership  
**Response:** 200 OK (no body)

#### Get Statistics

```typescript
/**
 * Get user's diary statistics
 */
export const getDiaryStats = async (): Promise<DiaryStats> => {
  const response = await api.get<DiaryStats>('/diaries/stats');
  return response.data;
};

// Usage
const stats = await getDiaryStats();
console.log(`Total: ${stats.total}, Positive: ${stats.positive}`);
```

**Backend:** `GET /diaries/stats`  
**Requires:** Valid access token  
**Response:** 200 OK with statistics

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

### Error Response Format

**Backend Error Response:**
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "errors": {
    "email": ["Invalid email format"],
    "password": ["Password too short"]
  }
}
```

**Frontend ApiError:**
```typescript
{
  message: "Validation failed",
  code: "VALIDATION_ERROR",
  statusCode: 400,
  errors: {
    email: ["Invalid email format"],
    password: ["Password too short"]
  }
}
```

### Error Handling Patterns

**1. Service Level (api.ts):**
```typescript
// Transform all errors to ApiError format
catch (error) {
  if (axios.isAxiosError(error)) {
    throw {
      message: error.response?.data?.error || error.message,
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
// Catch and expose errors
const fetchDiaries = async () => {
  try {
    const data = await getDiaries();
    entries.value = data.data;
  } catch (err) {
    const apiError = err as ApiError;
    error.value = apiError.message;
    throw err; // Re-throw for component
  }
};
```

**3. Component Level:**
```typescript
// Handle UI feedback
const handleSubmit = async () => {
  try {
    await diariesStore.createDiary(content);
    showSuccess('Diary created successfully');
    router.push('/diaries');
  } catch (error) {
    const apiError = error as ApiError;
    showError(apiError.message || 'Failed to create diary');
  }
};
```

### HTTP Status Code Handling

| Status | Meaning | Handling |
|--------|---------|----------|
| 200 | OK | Success, return data |
| 201 | Created | Success, return created resource |
| 400 | Bad Request | Validation error, show errors |
| 401 | Unauthorized | Token expired, refresh or logout |
| 403 | Forbidden | Permission denied, show error |
| 404 | Not Found | Resource not found, redirect or show error |
| 429 | Too Many Requests | Rate limit exceeded, show retry message |
| 500 | Internal Server Error | Server error, show generic error |
| 503 | Service Unavailable | Backend down, show maintenance message |

### Network Error Handling

```typescript
// Response interceptor handles network errors
if (error.code === 'ECONNABORTED') {
  // Timeout
  showError('Request timed out. Please try again.');
} else if (!error.response) {
  // Network error (no internet, CORS, etc.)
  showErrorWithRetry('Network error. Please check your connection.', () => {
    // Retry logic
  });
}
```

## Request Patterns

### Loading States

```typescript
// In Pinia store
const loading = ref(false);

const fetchData = async () => {
  loading.value = true;
  try {
    const data = await api.getData();
    items.value = data;
  } finally {
    loading.value = false; // Always clear loading
  }
};

// In component
<template>
  <LoadingSpinner v-if="store.loading" />
  <div v-else>{{ store.items }}</div>
</template>
```

### Optimistic Updates

```typescript
// Update UI immediately, rollback on error
const deleteDiary = async (id: number) => {
  // Optimistically remove from UI
  const index = entries.value.findIndex((d) => d.id === id);
  const removed = entries.value.splice(index, 1);

  try {
    await api.deleteDiary(id);
    // Success - UI already updated
  } catch (error) {
    // Rollback on error
    entries.value.splice(index, 0, ...removed);
    throw error;
  }
};
```

### Pagination

```typescript
const fetchDiaries = async (page: number = 1, perPage: number = 10) => {
  loading.value = true;
  try {
    const response = await getDiaries(page, perPage);
    entries.value = response.data;
    pagination.value = response.pagination;
  } finally {
    loading.value = false;
  }
};

// Usage
await fetchDiaries(2, 10); // Page 2, 10 items per page
```

### Debouncing Search

```typescript
import { ref, watch } from 'vue';
import { debounce } from 'lodash-es';

const searchQuery = ref('');
const results = ref([]);

const search = debounce(async (query: string) => {
  if (!query) {
    results.value = [];
    return;
  }

  try {
    const data = await api.search(query);
    results.value = data;
  } catch (error) {
    console.error('Search failed:', error);
  }
}, 300); // 300ms delay

watch(searchQuery, (newValue) => {
  search(newValue);
});
```

## Type Safety

### Request/Response Types

```typescript
// src/types/index.ts

// Authentication
export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
}

export interface AuthResponse extends TokenResponse {
  user: User;
}

export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
}

// Diaries
export interface DiaryEntry {
  id: number;
  user_id: number;
  content: string;
  analyzed_content: string;
  positive_count: number;
  negative_count: number;
  created_at: string;
  updated_at: string;
}

export interface DiaryCreateRequest {
  content: string;
}

export interface DiaryUpdateRequest {
  content: string;
}

export interface PaginationInfo {
  page: number;
  per_page: number;
  total: number;
  pages: number;
}

export interface DiaryListResponse {
  data: DiaryEntry[];
  pagination: PaginationInfo;
}

export interface DiaryStats {
  total_entries: number;
  positive_entries: number;
  negative_entries: number;
  neutral_entries: number;
}

// Errors
export interface ApiError {
  message: string;
  code?: string;
  statusCode?: number;
  errors?: Record<string, string[]>;
}
```

### Using Types in API Calls

```typescript
// Type-safe API methods
export const login = async (data: LoginRequest): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/auth/login', data);
  return response.data;
};

// Type-safe usage
const loginData: LoginRequest = {
  email: email.value,
  password: password.value,
};

try {
  const response: AuthResponse = await login(loginData);
  // TypeScript knows response has access_token, refresh_token, and user
  console.log(response.user.email);
} catch (error) {
  const apiError = error as ApiError;
  console.error(apiError.message);
}
```

## Testing API Integration

### Mocking Axios

```typescript
// tests/integration/src/services/api.spec.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import MockAdapter from 'axios-mock-adapter';
import { login, getDiaries } from '@/services/api';

describe('API Service', () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(api);
  });

  afterEach(() => {
    mock.reset();
  });

  it('should login successfully', async () => {
    const loginData = { email: 'test@example.com', password: 'password' };
    const response = {
      access_token: 'token123',
      refresh_token: 'refresh123',
      user: { id: 1, email: 'test@example.com' },
    };

    mock.onPost('/auth/login').reply(200, response);

    const result = await login(loginData);
    expect(result).toEqual(response);
  });

  it('should handle API errors', async () => {
    mock.onGet('/diaries').reply(500, {
      error: 'Internal server error',
      code: 'SERVER_ERROR',
    });

    await expect(getDiaries()).rejects.toMatchObject({
      message: 'Internal server error',
      code: 'SERVER_ERROR',
      statusCode: 500,
    });
  });
});
```

### Integration Tests

See [Frontend Testing](./frontend-testing.md) for comprehensive testing strategies.

## Best Practices

### 1. Centralize API Calls

**✅ Good:**
```typescript
// src/services/api.ts
export const createDiary = async (data: DiaryCreateRequest) => {
  const response = await api.post('/diaries', data);
  return response.data;
};

// In component
import { createDiary } from '@/services/api';
await createDiary({ content: 'text' });
```

**❌ Bad:**
```typescript
// In component - direct axios call
import axios from 'axios';
await axios.post('http://localhost:5000/diaries', { content: 'text' });
```

### 2. Type All API Methods

**✅ Good:**
```typescript
export const getDiary = async (id: number): Promise<DiaryEntry> => {
  const response = await api.get<DiaryEntry>(`/diaries/${id}`);
  return response.data;
};
```

**❌ Bad:**
```typescript
export const getDiary = async (id) => {
  const response = await api.get(`/diaries/${id}`);
  return response.data;
};
```

### 3. Handle Errors at Appropriate Level

**✅ Good:**
```typescript
// Store: Catch and expose
try {
  data = await api.getData();
} catch (err) {
  error.value = err.message;
  throw err; // Let component handle UI
}

// Component: Show user feedback
try {
  await store.fetchData();
} catch (error) {
  showError('Failed to load data');
}
```

**❌ Bad:**
```typescript
// Swallow errors silently
try {
  await api.getData();
} catch (err) {
  console.log(err);
}
```

### 4. Use Loading States

**✅ Good:**
```typescript
const loading = ref(false);

const fetchData = async () => {
  loading.value = true;
  try {
    await api.getData();
  } finally {
    loading.value = false; // Always clear
  }
};
```

**❌ Bad:**
```typescript
// No loading state, users don't know request is in progress
const fetchData = async () => {
  await api.getData();
};
```

### 5. Validate Before Sending

**✅ Good:**
```typescript
// Validate with Yup
const schema = yup.object({
  email: yup.string().email().required(),
  password: yup.string().min(8).required(),
});

await schema.validate(formData);
await api.register(formData);
```

**❌ Bad:**
```typescript
// Send without validation, get 400 error from backend
await api.register(formData);
```

### 6. Use Environment Variables

**✅ Good:**
```typescript
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
```

**❌ Bad:**
```typescript
const baseURL = 'http://localhost:5000'; // Hardcoded
```

### 7. Implement Retry Logic for Network Errors

**✅ Good:**
```typescript
const fetchWithRetry = async (fn: () => Promise<any>, retries = 3) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise((resolve) => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
};
```

### 8. Cache Frequently Accessed Data

**✅ Good:**
```typescript
// Cache in store
const stats = ref<DiaryStats | null>(null);
const lastFetch = ref<number>(0);

const fetchStats = async (force = false) => {
  const now = Date.now();
  // Cache for 5 minutes
  if (!force && stats.value && now - lastFetch.value < 300000) {
    return stats.value;
  }

  const data = await getDiaryStats();
  stats.value = data;
  lastFetch.value = now;
  return data;
};
```

## Related Documentation

- [Backend API Documentation](./backend-api.md) - Complete backend API reference
- [Frontend Architecture](./frontend-architecture.md) - Overall architecture patterns
- [Frontend Development](./frontend-development.md) - Development setup and workflow
- [Frontend Testing](./frontend-testing.md) - Testing strategies including API mocks
