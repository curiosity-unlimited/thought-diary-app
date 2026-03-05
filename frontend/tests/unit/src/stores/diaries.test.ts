import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useDiariesStore } from '@/stores/diaries';
import * as api from '@/services/api';

// Mock the API module
vi.mock('@/services/api', () => ({
  getDiaries: vi.fn(),
  getDiary: vi.fn(),
  createDiary: vi.fn(),
  updateDiary: vi.fn(),
  deleteDiary: vi.fn(),
  getDiaryStats: vi.fn(),
}));

describe('Diaries Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  describe('State Initialization', () => {
    it('should initialize with empty values', () => {
      const store = useDiariesStore();

      expect(store.entries).toEqual([]);
      expect(store.currentDiary).toBeNull();
      expect(store.stats).toBeNull();
      expect(store.pagination).toBeNull();
      expect(store.loading).toBe(false);
    });
  });

  describe('fetchDiaries()', () => {
    it('should fetch diaries with pagination successfully', async () => {
      const mockResponse = {
        diaries: [
          {
            id: 1,
            content: 'Test diary 1',
            analyzed_content: 'Test diary 1',
            positive_count: 0,
            negative_count: 0,
            created_at: '2026-01-01T00:00:00Z',
            updated_at: '2026-01-01T00:00:00Z',
          },
          {
            id: 2,
            content: 'Test diary 2',
            analyzed_content: 'Test diary 2',
            positive_count: 1,
            negative_count: 0,
            created_at: '2026-01-02T00:00:00Z',
            updated_at: '2026-01-02T00:00:00Z',
          },
        ],
        pagination: {
          page: 1,
          per_page: 10,
          total: 2,
          pages: 1,
        },
      };
      vi.mocked(api.getDiaries).mockResolvedValue(mockResponse);

      const store = useDiariesStore();
      await store.fetchDiaries();

      expect(api.getDiaries).toHaveBeenCalledWith(1, 10);
      expect(store.entries).toEqual(mockResponse.diaries);
      expect(store.pagination).toEqual(mockResponse.pagination);
      expect(store.loading).toBe(false);
    });

    it('should handle pagination parameters', async () => {
      const mockResponse = {
        diaries: [],
        pagination: {
          page: 2,
          per_page: 5,
          total: 0,
          pages: 0,
        },
      };
      vi.mocked(api.getDiaries).mockResolvedValue(mockResponse);

      const store = useDiariesStore();
      await store.fetchDiaries(2, 5);

      expect(api.getDiaries).toHaveBeenCalledWith(2, 5);
      expect(store.pagination?.page).toBe(2);
      expect(store.pagination?.per_page).toBe(5);
    });

    it('should set loading state during fetch', async () => {
      const mockResponse = {
        diaries: [],
        pagination: { page: 1, per_page: 10, total: 0, pages: 0 },
      };

      let loadingDuringFetch = false;
      vi.mocked(api.getDiaries).mockImplementation(async () => {
        const store = useDiariesStore();
        loadingDuringFetch = store.loading;
        return mockResponse;
      });

      const store = useDiariesStore();
      await store.fetchDiaries();

      expect(loadingDuringFetch).toBe(true);
      expect(store.loading).toBe(false);
    });

    it('should throw error on fetch failure', async () => {
      vi.mocked(api.getDiaries).mockRejectedValue(new Error('Fetch failed'));

      const store = useDiariesStore();

      await expect(store.fetchDiaries()).rejects.toThrow('Fetch failed');
      expect(store.loading).toBe(false);
    });
  });

  describe('fetchDiary()', () => {
    it('should fetch single diary successfully', async () => {
      const mockDiary = {
        id: 1,
        content: 'Test diary',
        analyzed_content: '<span class="positive">Test</span> diary',
        positive_count: 1,
        negative_count: 0,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-01T00:00:00Z',
      };
      vi.mocked(api.getDiary).mockResolvedValue(mockDiary);

      const store = useDiariesStore();
      await store.fetchDiary(1);

      expect(api.getDiary).toHaveBeenCalledWith(1);
      expect(store.currentDiary).toEqual(mockDiary);
    });

    it('should throw error on fetch diary failure', async () => {
      vi.mocked(api.getDiary).mockRejectedValue(new Error('Diary not found'));

      const store = useDiariesStore();

      await expect(store.fetchDiary(999)).rejects.toThrow('Diary not found');
    });
  });

  describe('createDiary()', () => {
    it('should create diary successfully', async () => {
      const mockDiary = {
        id: 3,
        content: 'New diary entry',
        analyzed_content: 'New diary entry',
        positive_count: 0,
        negative_count: 0,
        created_at: '2026-01-03T00:00:00Z',
        updated_at: '2026-01-03T00:00:00Z',
      };
      vi.mocked(api.createDiary).mockResolvedValue(mockDiary);

      const store = useDiariesStore();
      const result = await store.createDiary('New diary entry');

      expect(api.createDiary).toHaveBeenCalledWith({
        content: 'New diary entry',
      });
      expect(result).toEqual(mockDiary);
    });

    it('should throw error on create failure', async () => {
      vi.mocked(api.createDiary).mockRejectedValue(new Error('Create failed'));

      const store = useDiariesStore();

      await expect(store.createDiary('New diary')).rejects.toThrow(
        'Create failed'
      );
    });
  });

  describe('updateDiary()', () => {
    it('should update diary successfully', async () => {
      const mockDiary = {
        id: 1,
        content: 'Updated content',
        analyzed_content: 'Updated content',
        positive_count: 0,
        negative_count: 0,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-03T00:00:00Z',
      };
      vi.mocked(api.updateDiary).mockResolvedValue(mockDiary);

      const store = useDiariesStore();
      store.entries = [
        {
          id: 1,
          content: 'Old content',
          analyzed_content: 'Old content',
          positive_count: 0,
          negative_count: 0,
          created_at: '2026-01-01T00:00:00Z',
          updated_at: '2026-01-01T00:00:00Z',
        },
      ];

      const result = await store.updateDiary(1, 'Updated content');

      expect(api.updateDiary).toHaveBeenCalledWith(1, {
        content: 'Updated content',
      });
      expect(result).toEqual(mockDiary);
    });

    it('should throw error on update failure', async () => {
      vi.mocked(api.updateDiary).mockRejectedValue(new Error('Update failed'));

      const store = useDiariesStore();

      await expect(store.updateDiary(1, 'Updated content')).rejects.toThrow(
        'Update failed'
      );
    });
  });

  describe('deleteDiary()', () => {
    it('should delete diary successfully', async () => {
      vi.mocked(api.deleteDiary).mockResolvedValue(undefined);

      const store = useDiariesStore();
      store.entries = [
        {
          id: 1,
          content: 'To be deleted',
          analyzed_content: 'To be deleted',
          positive_count: 0,
          negative_count: 0,
          created_at: '2026-01-01T00:00:00Z',
          updated_at: '2026-01-01T00:00:00Z',
        },
        {
          id: 2,
          content: 'Keep this',
          analyzed_content: 'Keep this',
          positive_count: 0,
          negative_count: 0,
          created_at: '2026-01-02T00:00:00Z',
          updated_at: '2026-01-02T00:00:00Z',
        },
      ];

      await store.deleteDiary(1);

      expect(api.deleteDiary).toHaveBeenCalledWith(1);
      expect(store.entries).toHaveLength(1);
      expect(store.entries[0].id).toBe(2);
    });

    it('should throw error on delete failure', async () => {
      vi.mocked(api.deleteDiary).mockRejectedValue(new Error('Delete failed'));

      const store = useDiariesStore();

      await expect(store.deleteDiary(1)).rejects.toThrow('Delete failed');
    });
  });

  describe('fetchStats()', () => {
    it('should fetch statistics successfully', async () => {
      const mockStats = {
        total: 10,
        positive: 6,
        negative: 2,
        neutral: 2,
      };
      vi.mocked(api.getDiaryStats).mockResolvedValue(mockStats);

      const store = useDiariesStore();
      await store.fetchStats();

      expect(api.getDiaryStats).toHaveBeenCalled();
      expect(store.stats).toEqual(mockStats);
    });

    it('should throw error on stats fetch failure', async () => {
      vi.mocked(api.getDiaryStats).mockRejectedValue(
        new Error('Stats fetch failed')
      );

      const store = useDiariesStore();

      await expect(store.fetchStats()).rejects.toThrow('Stats fetch failed');
    });
  });

  describe('Edge Cases', () => {
    it('should handle fetchDiaries with no results', async () => {
      const mockResponse = {
        diaries: [],
        pagination: { page: 1, per_page: 10, total: 0, pages: 0 },
      };
      vi.mocked(api.getDiaries).mockResolvedValue(mockResponse);

      const store = useDiariesStore();
      await store.fetchDiaries();

      expect(store.entries).toEqual([]);
      expect(store.pagination?.total).toBe(0);
    });

    it('should handle updateDiary when currentDiary is null', async () => {
      const mockDiary = {
        id: 1,
        content: 'Updated',
        analyzed_content: 'Updated',
        positive_count: 1,
        negative_count: 0,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-02T00:00:00Z',
      };
      vi.mocked(api.updateDiary).mockResolvedValue(mockDiary);

      const store = useDiariesStore();
      store.currentDiary = null;

      await store.updateDiary(1, { content: 'Updated' });

      expect(api.updateDiary).toHaveBeenCalled();
    });

    it('should handle deleteDiary when diary not in entries', async () => {
      vi.mocked(api.deleteDiary).mockResolvedValue();

      const store = useDiariesStore();
      store.entries = [
        {
          id: 2,
          content: 'Test',
          analyzed_content: 'Test',
          positive_count: 0,
          negative_count: 0,
          created_at: '2026-01-01T00:00:00Z',
          updated_at: '2026-01-01T00:00:00Z',
        },
      ];

      await store.deleteDiary(999);

      expect(api.deleteDiary).toHaveBeenCalledWith(999);
      expect(store.entries).toHaveLength(1);
    });

    it('should not add to entries when creating diary on page 2', async () => {
      const mockDiary = {
        id: 3,
        content: 'New diary',
        analyzed_content: 'New diary',
        positive_count: 0,
        negative_count: 0,
        created_at: '2026-01-03T00:00:00Z',
        updated_at: '2026-01-03T00:00:00Z',
      };
      vi.mocked(api.createDiary).mockResolvedValue(mockDiary);

      const store = useDiariesStore();
      store.pagination = { page: 2, per_page: 10, total: 15, pages: 2 };
      store.entries = [];

      await store.createDiary({ content: 'New diary' });

      // Should not add to entries when not on page 1
      expect(store.entries).toHaveLength(0);
      // Should still increment total
      expect(store.pagination?.total).toBe(16);
    });

    it('should not update stats when pagination is null during create', async () => {
      const mockDiary = {
        id: 3,
        content: 'New diary',
        analyzed_content: 'New diary',
        positive_count: 0,
        negative_count: 0,
        created_at: '2026-01-03T00:00:00Z',
        updated_at: '2026-01-03T00:00:00Z',
      };
      vi.mocked(api.createDiary).mockResolvedValue(mockDiary);

      const store = useDiariesStore();
      store.pagination = null;

      await store.createDiary({ content: 'New diary' });

      // Pagination should still be null
      expect(store.pagination).toBeNull();
    });
  });

  describe('clearStore()', () => {
    it('should clear all store data', () => {
      const store = useDiariesStore();
      store.entries = [
        {
          id: 1,
          content: 'Test',
          analyzed_content: 'Test',
          positive_count: 0,
          negative_count: 0,
          created_at: '2026-01-01T00:00:00Z',
          updated_at: '2026-01-01T00:00:00Z',
        },
      ];
      store.currentDiary = {
        id: 1,
        content: 'Test',
        analyzed_content: 'Test',
        positive_count: 0,
        negative_count: 0,
        created_at: '2026-01-01T00:00:00Z',
        updated_at: '2026-01-01T00:00:00Z',
      };
      store.stats = { total: 1, positive: 0, negative: 0, neutral: 1 };
      store.pagination = { page: 1, per_page: 10, total: 1, pages: 1 };

      store.clearStore();

      expect(store.entries).toEqual([]);
      expect(store.currentDiary).toBeNull();
      expect(store.stats).toBeNull();
      expect(store.pagination).toBeNull();
    });
  });
});
