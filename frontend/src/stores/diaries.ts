/**
 * Diaries Store
 * Manages diary entries, statistics, and pagination
 */

import { defineStore } from 'pinia';
import { ref } from 'vue';
import {
  getDiaries,
  getDiary,
  createDiary as apiCreateDiary,
  updateDiary as apiUpdateDiary,
  deleteDiary as apiDeleteDiary,
  getDiaryStats,
} from '@/services/api';
import type { DiaryEntry, DiaryStats, PaginationInfo } from '@/types';

export const useDiariesStore = defineStore('diaries', () => {
  // State
  const entries = ref<DiaryEntry[]>([]);
  const currentDiary = ref<DiaryEntry | null>(null);
  const stats = ref<DiaryStats>({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0,
  });
  const pagination = ref<PaginationInfo>({
    page: 1,
    per_page: 10,
    total: 0,
    pages: 0,
  });
  const loading = ref(false);

  /**
   * Fetch diaries with pagination
   * @param page - Page number (default: 1)
   * @param perPage - Items per page (default: 10)
   * @throws {ApiError} - If fetching diaries fails
   */
  const fetchDiaries = async (page: number = 1, perPage: number = 10): Promise<void> => {
    loading.value = true;
    try {
      const response = await getDiaries(page, perPage);
      entries.value = response.diaries;
      pagination.value = response.pagination;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Fetch a single diary entry by ID
   * @param id - Diary entry ID
   * @throws {ApiError} - If fetching diary fails
   */
  const fetchDiary = async (id: number): Promise<void> => {
    loading.value = true;
    try {
      const diary = await getDiary(id);
      currentDiary.value = diary;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Create a new diary entry
   * @param content - Diary content
   * @returns Created diary entry
   * @throws {ApiError} - If creating diary fails
   */
  const createDiary = async (content: string): Promise<DiaryEntry> => {
    loading.value = true;
    try {
      const diary = await apiCreateDiary({ content });

      // Add to entries list if we're on the first page
      if (pagination.value.page === 1) {
        entries.value.unshift(diary);
        // Remove last item if we exceed per_page limit
        if (entries.value.length > pagination.value.per_page) {
          entries.value.pop();
        }
      }

      // Update stats
      pagination.value.total += 1;

      return diary;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Update an existing diary entry
   * @param id - Diary entry ID
   * @param content - Updated diary content
   * @returns Updated diary entry
   * @throws {ApiError} - If updating diary fails
   */
  const updateDiary = async (id: number, content: string): Promise<DiaryEntry> => {
    loading.value = true;
    try {
      const diary = await apiUpdateDiary(id, { content });

      // Update in entries list
      const index = entries.value.findIndex((d) => d.id === id);
      if (index !== -1) {
        entries.value[index] = diary;
      }

      // Update currentDiary if it's the one being edited
      if (currentDiary.value?.id === id) {
        currentDiary.value = diary;
      }

      return diary;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Delete a diary entry
   * @param id - Diary entry ID
   * @throws {ApiError} - If deleting diary fails
   */
  const deleteDiary = async (id: number): Promise<void> => {
    loading.value = true;
    try {
      await apiDeleteDiary(id);

      // Remove from entries list
      entries.value = entries.value.filter((d) => d.id !== id);

      // Clear currentDiary if it's the one being deleted
      if (currentDiary.value?.id === id) {
        currentDiary.value = null;
      }

      // Update stats
      pagination.value.total = Math.max(0, pagination.value.total - 1);
    } finally {
      loading.value = false;
    }
  };

  /**
   * Fetch diary statistics
   * @throws {ApiError} - If fetching stats fails
   */
  const fetchStats = async (): Promise<void> => {
    loading.value = true;
    try {
      const statsData = await getDiaryStats();
      stats.value = statsData;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Clear all diary data from store
   * Called on logout
   */
  const clearStore = () => {
    entries.value = [];
    currentDiary.value = null;
    stats.value = {
      total: 0,
      positive: 0,
      negative: 0,
      neutral: 0,
    };
    pagination.value = {
      page: 1,
      per_page: 10,
      total: 0,
      pages: 0,
    };
    loading.value = false;
  };

  return {
    // State
    entries,
    currentDiary,
    stats,
    pagination,
    loading,

    // Actions
    fetchDiaries,
    fetchDiary,
    createDiary,
    updateDiary,
    deleteDiary,
    fetchStats,
    clearStore,
  };
});
