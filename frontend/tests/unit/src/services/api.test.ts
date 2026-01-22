import { describe, it, expect, beforeEach, vi } from 'vitest';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import apiClient, {
  login,
  register,
  logout,
  refreshToken,
  getCurrentUser,
  getDiaries,
  getDiary,
  createDiary,
  updateDiary,
  deleteDiary,
  getDiaryStats,
} from '@/services/api';

describe('API Service', () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(apiClient);
    localStorage.clear();
  });

  afterEach(() => {
    mock.reset();
  });

  describe('Authentication Endpoints', () => {
    it('should register user', async () => {
      const mockResponse = { message: 'User registered successfully' };
      mock.onPost('/auth/register').reply(200, mockResponse);

      const result = await register({
        email: 'test@example.com',
        password: 'Password123!',
      });

      expect(result).toEqual(mockResponse);
    });

    it('should login user', async () => {
      const mockResponse = {
        access_token: 'access-token',
        refresh_token: 'refresh-token',
      };
      mock.onPost('/auth/login').reply(200, mockResponse);

      const result = await login({
        email: 'test@example.com',
        password: 'Password123!',
      });

      expect(result).toEqual(mockResponse);
    });

    it('should logout user', async () => {
      mock.onPost('/auth/logout').reply(200, { message: 'Logged out successfully' });

      const result = await logout();

      expect(result).toBeUndefined();
    });

    it('should refresh token', async () => {
      const mockResponse = { access_token: 'new-access-token' };
      // Set refresh token in localStorage before testing
      localStorage.setItem('refresh_token', 'old-refresh-token');
      // Need to use import('axios').default for refreshToken since it bypasses apiClient
      const axios = await import('axios');
      const axiosMock = require('axios-mock-adapter');
      const mock2 = new axiosMock(axios.default);
      mock2.onPost('/auth/refresh').reply(200, mockResponse);

      const result = await refreshToken();

      expect(result).toEqual('new-access-token');
    });

    it('should get current user', async () => {
      const mockUser = {
        id: 1,
        email: 'test@example.com',
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-01T00:00:00Z',
      };
      mock.onGet('/auth/me').reply(200, mockUser);

      const result = await getCurrentUser();

      expect(result).toEqual(mockUser);
    });
  });

  describe('Diary Endpoints', () => {
    it('should get diaries with pagination', async () => {
      const mockResponse = {
        diaries: [
          {
            id: 1,
            content: 'Test',
            analyzed_content: 'Test',
            positive_count: 0,
            negative_count: 0,
            created_at: '2026-01-01T00:00:00Z',
            updated_at: '2026-01-01T00:00:00Z',
          },
        ],
        pagination: {
          page: 1,
          per_page: 10,
          total: 1,
          pages: 1,
        },
      };
      mock.onGet('/diaries').reply(200, mockResponse);

      const result = await getDiaries();

      expect(result).toEqual(mockResponse);
    });

    it('should get single diary', async () => {
      const mockDiary = {
        id: 1,
        content: 'Test',
        analyzed_content: 'Test',
        positive_count: 0,
        negative_count: 0,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-01T00:00:00Z',
      };
      mock.onGet('/diaries/1').reply(200, mockDiary);

      const result = await getDiary(1);

      expect(result).toEqual(mockDiary);
    });

    it('should create diary', async () => {
      const mockDiary = {
        id: 1,
        content: 'New diary',
        analyzed_content: 'New diary',
        positive_count: 0,
        negative_count: 0,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-01T00:00:00Z',
      };
      mock.onPost('/diaries').reply(201, mockDiary);

      const result = await createDiary({ content: 'New diary' });

      expect(result).toEqual(mockDiary);
    });

    it('should update diary', async () => {
      const mockDiary = {
        id: 1,
        content: 'Updated diary',
        analyzed_content: 'Updated diary',
        positive_count: 0,
        negative_count: 0,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-02T00:00:00Z',
      };
      mock.onPut('/diaries/1').reply(200, mockDiary);

      const result = await updateDiary(1, { content: 'Updated diary' });

      expect(result).toEqual(mockDiary);
    });

    it('should delete diary', async () => {
      mock.onDelete('/diaries/1').reply(200, { message: 'Diary deleted successfully' });

      const result = await deleteDiary(1);

      expect(result).toBeUndefined();
    });

    it('should get diary stats', async () => {
      const mockStats = {
        total: 10,
        positive: 6,
        negative: 2,
        neutral: 2,
      };
      mock.onGet('/diaries/stats').reply(200, mockStats);

      const result = await getDiaryStats();

      expect(result).toEqual(mockStats);
    });
  });

  describe('Request Interceptor', () => {
    it('should add authorization header when token exists', async () => {
      localStorage.setItem('access_token', 'test-token');
      
      mock.onGet('/auth/me').reply(config => {
        expect(config.headers?.Authorization).toBe('Bearer test-token');
        return [200, { id: 1, email: 'test@example.com' }];
      });

      await getCurrentUser();
    });

    it('should not add authorization header for public endpoints', async () => {
      mock.onPost('/auth/login').reply(config => {
        expect(config.headers?.Authorization).toBeUndefined();
        return [200, { access_token: 'token', refresh_token: 'refresh' }];
      });

      await login({ email: 'test@example.com', password: 'Password123!' });
    });
  });

  describe('Error Handling', () => {
    it('should handle 404 errors', async () => {
      mock.onGet('/diaries/999').reply(404, { error: 'Diary not found' });

      await expect(getDiary(999)).rejects.toThrow();
    });

    it('should handle 401 errors', async () => {
      mock.onGet('/auth/me').reply(401, { error: 'Unauthorized' });

      await expect(getCurrentUser()).rejects.toThrow();
    });

    it('should handle network errors', async () => {
      mock.onGet('/diaries').networkError();

      await expect(getDiaries()).rejects.toThrow();
    });

    it('should handle timeout errors', async () => {
      mock.onGet('/diaries').timeout();

      await expect(getDiaries()).rejects.toThrow();
    });
  });
});
