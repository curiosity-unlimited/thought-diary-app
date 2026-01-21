/**
 * Authentication Store
 * Manages user authentication state, tokens, and auth-related operations
 */

import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { login as apiLogin, register as apiRegister, logout as apiLogout, refreshToken as apiRefreshToken, getCurrentUser } from '@/services/api';
import type { User, LoginRequest, RegisterRequest } from '@/types';

// localStorage keys
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);

  // Computed
  const isAuthenticated = computed(() => !!accessToken.value && !!refreshToken.value);

  /**
   * Initialize store from localStorage
   * Called on app startup to restore auth state
   */
  const initializeAuth = () => {
    const storedAccessToken = localStorage.getItem(ACCESS_TOKEN_KEY);
    const storedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);

    if (storedAccessToken && storedRefreshToken) {
      accessToken.value = storedAccessToken;
      refreshToken.value = storedRefreshToken;
    }
  };

  /**
   * Store tokens in state and localStorage
   */
  const setTokens = (access: string, refresh: string) => {
    accessToken.value = access;
    refreshToken.value = refresh;
    localStorage.setItem(ACCESS_TOKEN_KEY, access);
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
  };

  /**
   * Clear tokens from state and localStorage
   */
  const clearTokens = () => {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  };

  /**
   * Register a new user
   * Note: Backend doesn't return tokens on registration - user must login after
   * @param email - User's email address
   * @param password - User's password
   * @throws {ApiError} - If registration fails
   */
  const register = async (email: string, password: string): Promise<void> => {
    const data: RegisterRequest = { email, password };
    const response = await apiRegister(data);
    
    // Set user data (no tokens on registration)
    user.value = response.user;
  };

  /**
   * Login user
   * @param email - User's email address
   * @param password - User's password
   * @throws {ApiError} - If login fails
   */
  const login = async (email: string, password: string): Promise<void> => {
    const data: LoginRequest = { email, password };
    const response = await apiLogin(data);

    // Store tokens
    setTokens(response.access_token, response.refresh_token);

    // Set user data
    user.value = response.user;
  };

  /**
   * Logout user
   * Clears tokens and user data from state and localStorage
   */
  const logout = async (): Promise<void> => {
    try {
      // Call API logout (best effort - don't fail if it errors)
      await apiLogout();
    } catch (error) {
      // Ignore logout API errors - clear tokens anyway
      console.error('Logout API call failed:', error);
    } finally {
      // Always clear local state
      clearTokens();
    }
  };

  /**
   * Refresh access token
   * Note: Backend only returns new access_token, refresh_token stays the same
   * @throws {ApiError} - If token refresh fails
   */
  const refreshAccessToken = async (): Promise<void> => {
    try {
      const newAccessToken = await apiRefreshToken();

      // Update only access token (refresh token stays the same)
      if (refreshToken.value) {
        setTokens(newAccessToken, refreshToken.value);
      }
    } catch (error) {
      // Clear tokens on refresh failure
      clearTokens();
      throw error;
    }
  };

  /**
   * Fetch current user profile
   * @throws {ApiError} - If fetching profile fails
   */
  const fetchProfile = async (): Promise<void> => {
    const userData = await getCurrentUser();
    user.value = userData;
  };

  // Initialize auth state from localStorage on store creation
  initializeAuth();

  return {
    // State
    user,
    accessToken,
    refreshToken,

    // Computed
    isAuthenticated,

    // Actions
    register,
    login,
    logout,
    refreshAccessToken,
    fetchProfile,
    clearTokens,
    setTokens,
  };
});
