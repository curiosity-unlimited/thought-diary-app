/**
 * API Service for Thought Diary App
 * Handles all HTTP requests with token management and error handling
 */

import axios, {
  type AxiosInstance,
  type AxiosError,
  type InternalAxiosRequestConfig,
  type AxiosResponse,
} from 'axios';
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  RegisterResponse,
  TokenResponse,
  User,
  DiaryEntry,
  DiaryCreateRequest,
  DiaryUpdateRequest,
  DiaryListResponse,
  DiaryStats,
  ApiError,
} from '@/types';

// Token storage keys
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

// Create Axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000',
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Queue for handling multiple requests during token refresh
let isRefreshing = false;
let failedRequestsQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: Error) => void;
}> = [];

/**
 * Process queued requests after token refresh
 */
const processQueue = (error: Error | null, token: string | null = null) => {
  failedRequestsQueue.forEach((promise) => {
    if (error) {
      promise.reject(error);
    } else if (token) {
      promise.resolve(token);
    }
  });
  failedRequestsQueue = [];
};

/**
 * Get access token from localStorage
 */
export const getAccessToken = (): string | null => {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
};

/**
 * Get refresh token from localStorage
 */
export const getRefreshToken = (): string | null => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

/**
 * Store tokens in localStorage
 */
export const setTokens = (accessToken: string, refreshToken?: string): void => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
};

/**
 * Clear tokens from localStorage
 */
export const clearTokens = (): void => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

/**
 * Request interceptor - Add JWT token to requests
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Skip Authorization header for public endpoints
    const publicEndpoints = [
      '/auth/register',
      '/auth/login',
      '/health',
      '/version',
      '/docs',
    ];
    const isPublicEndpoint = publicEndpoints.some((endpoint) =>
      config.url?.includes(endpoint)
    );

    if (!isPublicEndpoint) {
      const token = getAccessToken();
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor - Handle 401 errors and token refresh
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError<ApiError>) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    // Handle 401 Unauthorized - Token expired
    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._retry
    ) {
      // Skip refresh for login/register failures
      if (
        originalRequest.url?.includes('/auth/login') ||
        originalRequest.url?.includes('/auth/register')
      ) {
        return Promise.reject(error);
      }

      originalRequest._retry = true;

      if (isRefreshing) {
        // Queue the request while refresh is in progress
        return new Promise((resolve, reject) => {
          failedRequestsQueue.push({
            resolve: (token: string) => {
              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${token}`;
              }
              resolve(apiClient(originalRequest));
            },
            reject: (err: Error) => {
              reject(err);
            },
          });
        });
      }

      isRefreshing = true;

      const refreshToken = getRefreshToken();
      if (!refreshToken) {
        // No refresh token, logout user
        clearTokens();
        isRefreshing = false;
        processQueue(new Error('No refresh token available'), null);
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        // Attempt to refresh the token
        const response = await axios.post<TokenResponse>(
          `${apiClient.defaults.baseURL}/auth/refresh`,
          {},
          {
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          }
        );

        const { access_token } = response.data;

        // Update tokens in localStorage (token rotation)
        setTokens(access_token);

        // Update authorization header
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
        }

        // Process queued requests
        processQueue(null, access_token);
        isRefreshing = false;

        // Retry original request
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        processQueue(refreshError as Error, null);
        isRefreshing = false;
        clearTokens();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    // Handle network errors (offline, timeout, connection refused)
    if (!error.response) {
      const networkError: ApiError = {
        error: 'network_error',
        message:
          error.message === 'Network Error'
            ? 'Unable to connect to server. Please check your internet connection.'
            : error.message || 'A network error occurred. Please try again.',
      };
      return Promise.reject(networkError);
    }

    // Transform backend errors to ApiError interface
    const apiError: ApiError = {
      error: error.response.data?.error || 'unknown_error',
      message:
        error.response.data?.message ||
        error.message ||
        'An unexpected error occurred. Please try again.',
    };

    return Promise.reject(apiError);
  }
);

// ============================================================================
// Auth API Methods
// ============================================================================

/**
 * Register a new user
 */
export const register = async (
  data: RegisterRequest
): Promise<RegisterResponse> => {
  const response = await apiClient.post<RegisterResponse>(
    '/auth/register',
    data
  );
  return response.data;
};

/**
 * Login user and receive JWT tokens
 */
export const login = async (data: LoginRequest): Promise<AuthResponse> => {
  const response = await apiClient.post<AuthResponse>('/auth/login', data);
  const { access_token, refresh_token } = response.data;

  // Store tokens in localStorage
  setTokens(access_token, refresh_token);

  return response.data;
};

/**
 * Logout current user
 */
export const logout = async (): Promise<void> => {
  try {
    await apiClient.post('/auth/logout');
  } finally {
    // Always clear tokens, even if API call fails
    clearTokens();
  }
};

/**
 * Refresh access token using refresh token
 */
export const refreshToken = async (): Promise<string> => {
  const refresh = getRefreshToken();
  if (!refresh) {
    throw new Error('No refresh token available');
  }

  const response = await axios.post<TokenResponse>(
    `${apiClient.defaults.baseURL}/auth/refresh`,
    {},
    {
      headers: {
        Authorization: `Bearer ${refresh}`,
      },
    }
  );

  const { access_token } = response.data;
  setTokens(access_token);

  return access_token;
};

/**
 * Get current user profile
 */
export const getCurrentUser = async (): Promise<User> => {
  const response = await apiClient.get<User>('/auth/me');
  return response.data;
};

// ============================================================================
// Diary API Methods
// ============================================================================

/**
 * Get paginated list of user's diaries
 */
export const getDiaries = async (
  page: number = 1,
  perPage: number = 10
): Promise<DiaryListResponse> => {
  const response = await apiClient.get<DiaryListResponse>('/diaries', {
    params: { page, per_page: perPage },
  });
  return response.data;
};

/**
 * Get a specific diary entry
 */
export const getDiary = async (id: number): Promise<DiaryEntry> => {
  const response = await apiClient.get<DiaryEntry>(`/diaries/${id}`);
  return response.data;
};

/**
 * Create a new diary entry with AI sentiment analysis
 */
export const createDiary = async (
  data: DiaryCreateRequest
): Promise<DiaryEntry> => {
  const response = await apiClient.post<DiaryEntry>('/diaries', data);
  return response.data;
};

/**
 * Update an existing diary entry
 */
export const updateDiary = async (
  id: number,
  data: DiaryUpdateRequest
): Promise<DiaryEntry> => {
  const response = await apiClient.put<DiaryEntry>(`/diaries/${id}`, data);
  return response.data;
};

/**
 * Delete a diary entry
 */
export const deleteDiary = async (id: number): Promise<void> => {
  await apiClient.delete(`/diaries/${id}`);
};

/**
 * Get diary statistics for current user
 */
export const getDiaryStats = async (): Promise<DiaryStats> => {
  const response = await apiClient.get<DiaryStats>('/diaries/stats');
  return response.data;
};

// Export the configured Axios instance as default
export default apiClient;
