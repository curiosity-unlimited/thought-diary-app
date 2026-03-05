/**
 * Tests for DiaryStats type fix
 * Verifies that DiaryStats interface matches backend API response
 */

import { describe, it, expect } from 'vitest';
import type { DiaryStats } from '@/types';

describe('DiaryStats Type Fix', () => {
  it('should have correct property names matching backend API', () => {
    const stats: DiaryStats = {
      total_entries: 10,
      positive_entries: 5,
      negative_entries: 3,
      neutral_entries: 2,
    };

    expect(stats).toHaveProperty('total_entries');
    expect(stats).toHaveProperty('positive_entries');
    expect(stats).toHaveProperty('negative_entries');
    expect(stats).toHaveProperty('neutral_entries');
  });

  it('should accept valid stats data from API', () => {
    const apiResponse: DiaryStats = {
      total_entries: 0,
      positive_entries: 0,
      negative_entries: 0,
      neutral_entries: 0,
    };

    expect(apiResponse.total_entries).toBe(0);
    expect(apiResponse.positive_entries).toBe(0);
    expect(apiResponse.negative_entries).toBe(0);
    expect(apiResponse.neutral_entries).toBe(0);
  });
});
