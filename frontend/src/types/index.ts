/**
 * TypeScript type definitions for the Thought Diary App
 * These interfaces match the backend API responses and requests
 */

/**
 * User model representing an authenticated user
 */
export interface User {
  id: number;
  email: string;
  created_at: string;
  updated_at: string;
}

/**
 * Diary entry model with sentiment analysis
 */
export interface DiaryEntry {
  id: number;
  content: string;
  analyzed_content: string;
  positive_count: number;
  negative_count: number;
  created_at: string;
  updated_at: string;
}

/**
 * Statistics about user's diary entries
 */
export interface DiaryStats {
  total: number;
  positive: number;
  negative: number;
  neutral: number;
}

/**
 * Authentication state for Pinia store
 */
export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
}

/**
 * Login request payload
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Register request payload
 */
export interface RegisterRequest {
  email: string;
  password: string;
}

/**
 * Create diary request payload
 */
export interface DiaryCreateRequest {
  content: string;
}

/**
 * Update diary request payload
 */
export interface DiaryUpdateRequest {
  content: string;
}

/**
 * Pagination information from API responses
 */
export interface PaginationInfo {
  page: number;
  per_page: number;
  total: number;
  pages: number;
}

/**
 * List diaries API response
 */
export interface DiaryListResponse {
  diaries: DiaryEntry[];
  pagination: PaginationInfo;
}

/**
 * API error response structure
 */
export interface ApiError {
  error: string;
  message: string;
}

/**
 * Token response from login/register
 */
export interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  user?: User;
  message?: string;
}

/**
 * Login/Register response with user and tokens
 */
export interface AuthResponse {
  message: string;
  access_token: string;
  refresh_token: string;
  user: User;
}

/**
 * Register response
 */
export interface RegisterResponse {
  message: string;
  user: User;
}
