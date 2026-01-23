import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '@/stores/auth';
import * as api from '@/services/api';

// Mock the API module
vi.mock('@/services/api', () => ({
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn(),
  refreshToken: vi.fn(),
  getCurrentUser: vi.fn(),
}));

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
    vi.clearAllMocks();
  });

  describe('State Initialization', () => {
    it('should initialize with null values', () => {
      const store = useAuthStore();
      
      expect(store.user).toBeNull();
      expect(store.accessToken).toBeNull();
      expect(store.refreshToken).toBeNull();
      expect(store.isAuthenticated).toBe(false);
    });

    it('should restore tokens from localStorage', () => {
      localStorage.setItem('access_token', 'test-access-token');
      localStorage.setItem('refresh_token', 'test-refresh-token');

      // Create a new store instance, which will auto-initialize from localStorage
      const store = useAuthStore();

      expect(store.accessToken).toBe('test-access-token');
      expect(store.refreshToken).toBe('test-refresh-token');
      expect(store.isAuthenticated).toBe(true);
    });
  });

  describe('register()', () => {
    it('should register successfully', async () => {
      const mockResponse = { 
        message: 'User registered successfully' 
      };
      vi.mocked(api.register).mockResolvedValue(mockResponse);

      const store = useAuthStore();
      await store.register('test@example.com', 'Password123!');

      expect(api.register).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'Password123!',
      });
    });

    it('should throw error on registration failure', async () => {
      vi.mocked(api.register).mockRejectedValue(new Error('Registration failed'));

      const store = useAuthStore();

      await expect(
        store.register('test@example.com', 'Password123!')
      ).rejects.toThrow('Registration failed');
    });
  });

  describe('login()', () => {
    it('should login successfully and store tokens', async () => {
      const mockResponse = {
        access_token: 'new-access-token',
        refresh_token: 'new-refresh-token',
      };
      vi.mocked(api.login).mockResolvedValue(mockResponse);

      const store = useAuthStore();
      await store.login('test@example.com', 'Password123!');

      expect(api.login).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'Password123!',
      });
      expect(store.accessToken).toBe('new-access-token');
      expect(store.refreshToken).toBe('new-refresh-token');
      expect(store.isAuthenticated).toBe(true);
      expect(localStorage.getItem('access_token')).toBe('new-access-token');
      expect(localStorage.getItem('refresh_token')).toBe('new-refresh-token');
    });

    it('should throw error on login failure', async () => {
      vi.mocked(api.login).mockRejectedValue(new Error('Invalid credentials'));

      const store = useAuthStore();

      await expect(
        store.login('test@example.com', 'wrong-password')
      ).rejects.toThrow('Invalid credentials');
    });
  });

  describe('logout()', () => {
    it('should clear tokens and call logout API', async () => {
      vi.mocked(api.logout).mockResolvedValue({ message: 'Logged out successfully' });

      const store = useAuthStore();
      store.accessToken = 'test-access-token';
      store.refreshToken = 'test-refresh-token';
      store.user = { id: 1, email: 'test@example.com', created_at: '2026-01-01', updated_at: '2026-01-01' };
      localStorage.setItem('access_token', 'test-access-token');
      localStorage.setItem('refresh_token', 'test-refresh-token');

      await store.logout();

      expect(api.logout).toHaveBeenCalled();
      expect(store.accessToken).toBeNull();
      expect(store.refreshToken).toBeNull();
      expect(store.user).toBeNull();
      expect(store.isAuthenticated).toBe(false);
      expect(localStorage.getItem('access_token')).toBeNull();
      expect(localStorage.getItem('refresh_token')).toBeNull();
    });

    it('should clear tokens even if API call fails', async () => {
      vi.mocked(api.logout).mockRejectedValue(new Error('Logout failed'));

      const store = useAuthStore();
      store.accessToken = 'test-access-token';
      store.refreshToken = 'test-refresh-token';

      await store.logout();

      expect(store.accessToken).toBeNull();
      expect(store.refreshToken).toBeNull();
      expect(store.isAuthenticated).toBe(false);
    });
  });

  describe('refreshAccessToken()', () => {
    it('should refresh access token successfully', async () => {
      const mockNewToken = 'new-access-token';
      vi.mocked(api.refreshToken).mockResolvedValue(mockNewToken);

      const store = useAuthStore();
      store.refreshToken = 'test-refresh-token';
      store.accessToken = 'old-access-token';

      await store.refreshAccessToken();

      expect(api.refreshToken).toHaveBeenCalled();
      expect(store.accessToken).toEqual(mockNewToken);
      expect(localStorage.getItem('access_token')).toEqual(mockNewToken);
    });

    it('should throw error if no refresh token available', async () => {
      const store = useAuthStore();
      store.refreshToken = null;

      await expect(store.refreshAccessToken()).rejects.toThrow();
    });
  });

  describe('fetchProfile()', () => {
    it('should fetch user profile successfully', async () => {
      const mockUser = {
        id: 1,
        email: 'test@example.com',
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-01T00:00:00Z',
      };
      vi.mocked(api.getCurrentUser).mockResolvedValue(mockUser);

      const store = useAuthStore();
      await store.fetchProfile();

      expect(api.getCurrentUser).toHaveBeenCalled();
      expect(store.user).toEqual(mockUser);
    });

    it('should throw error on profile fetch failure', async () => {
      vi.mocked(api.getCurrentUser).mockRejectedValue(new Error('Unauthorized'));

      const store = useAuthStore();

      await expect(store.fetchProfile()).rejects.toThrow('Unauthorized');
    });
  });

  describe('isAuthenticated computed', () => {
    it('should return false when no tokens', () => {
      const store = useAuthStore();
      
      expect(store.isAuthenticated).toBe(false);
    });

    it('should return false when only access token present', () => {
      const store = useAuthStore();
      store.accessToken = 'test-access-token';
      
      expect(store.isAuthenticated).toBe(false);
    });

    it('should return false when only refresh token present', () => {
      const store = useAuthStore();
      store.refreshToken = 'test-refresh-token';
      
      expect(store.isAuthenticated).toBe(false);
    });

    it('should return true when both tokens present', () => {
      const store = useAuthStore();
      store.accessToken = 'test-access-token';
      store.refreshToken = 'test-refresh-token';
      
      expect(store.isAuthenticated).toBe(true);
    });
  });

  describe('Token Persistence', () => {
    it('should persist tokens to localStorage on login', async () => {
      const mockResponse = {
        access_token: 'persisted-access-token',
        refresh_token: 'persisted-refresh-token',
      };
      vi.mocked(api.login).mockResolvedValue(mockResponse);

      const store = useAuthStore();
      await store.login('test@example.com', 'Password123!');

      expect(localStorage.getItem('access_token')).toBe('persisted-access-token');
      expect(localStorage.getItem('refresh_token')).toBe('persisted-refresh-token');
    });

    it('should clear tokens from localStorage on logout', async () => {
      vi.mocked(api.logout).mockResolvedValue({ message: 'Logged out' });

      localStorage.setItem('access_token', 'test-access-token');
      localStorage.setItem('refresh_token', 'test-refresh-token');

      const store = useAuthStore();
      store.accessToken = 'test-access-token';
      store.refreshToken = 'test-refresh-token';

      await store.logout();

      expect(localStorage.getItem('access_token')).toBeNull();
      expect(localStorage.getItem('refresh_token')).toBeNull();
    });
  });
});
