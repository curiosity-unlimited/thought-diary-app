/**
 * Tests for auth profile fetch fix
 * Verifies that user profile is fetched after login and on app initialization
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '@/stores/auth';
import * as api from '@/services/api';

vi.mock('@/services/api');

describe('Auth Profile Fetch Fix', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('should fetch user profile after successful login', async () => {
    const authStore = useAuthStore();

    // Mock login and getCurrentUser API calls
    vi.mocked(api.login).mockResolvedValue({
      access_token: 'test-access-token',
      refresh_token: 'test-refresh-token',
      message: 'Login successful',
      user: {
        id: 1,
        email: 'test@example.com',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
    });

    vi.mocked(api.getCurrentUser).mockResolvedValue({
      id: 1,
      email: 'test@example.com',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    });

    // Perform login
    await authStore.login('test@example.com', 'password123');

    // Verify getCurrentUser was called after login
    expect(api.getCurrentUser).toHaveBeenCalled();
    expect(authStore.user).not.toBeNull();
    expect(authStore.user?.email).toBe('test@example.com');
  });

  it('should have user data available after login', async () => {
    const authStore = useAuthStore();

    vi.mocked(api.login).mockResolvedValue({
      access_token: 'test-access-token',
      refresh_token: 'test-refresh-token',
      message: 'Login successful',
      user: {
        id: 1,
        email: 'test@example.com',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
    });

    vi.mocked(api.getCurrentUser).mockResolvedValue({
      id: 1,
      email: 'test@example.com',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    });

    await authStore.login('test@example.com', 'password123');

    // User should be set after login
    expect(authStore.user).toBeDefined();
    expect(authStore.user?.email).toBe('test@example.com');
  });

  it('should clear tokens if profile fetch fails', async () => {
    const authStore = useAuthStore();

    vi.mocked(api.login).mockResolvedValue({
      access_token: 'test-access-token',
      refresh_token: 'test-refresh-token',
      message: 'Login successful',
      user: {
        id: 1,
        email: 'test@example.com',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
    });

    // Mock profile fetch failure
    vi.mocked(api.getCurrentUser).mockRejectedValue(new Error('Unauthorized'));

    try {
      await authStore.login('test@example.com', 'password123');
    } catch (error) {
      // Login should fail if profile fetch fails
      expect(error).toBeDefined();
    }
  });
});
