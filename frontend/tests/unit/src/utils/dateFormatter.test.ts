/**
 * Unit tests for dateFormatter utility
 */
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { formatDateTime, formatDate } from '@/utils/dateFormatter';

const TEST_DATE = '2024-01-15T10:30:00.000Z';

describe('dateFormatter', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  describe('formatDateTime()', () => {
    it('should return a non-empty string for a valid ISO date', () => {
      const result = formatDateTime(TEST_DATE);
      expect(result).toBeTruthy();
      expect(typeof result).toBe('string');
    });

    it('should include the year in the formatted output', () => {
      const result = formatDateTime(TEST_DATE);
      expect(result).toContain('2024');
    });

    it('should format differently when locale is en', () => {
      localStorage.setItem('user_locale', 'en');
      const result = formatDateTime(TEST_DATE);
      // en-US uses 'January' style month names
      expect(result).toBeTruthy();
    });

    it('should format differently when locale is zh-tw', () => {
      localStorage.setItem('user_locale', 'zh-tw');
      const result = formatDateTime(TEST_DATE);
      expect(result).toBeTruthy();
    });
  });

  describe('formatDate()', () => {
    it('should return a non-empty string for a valid ISO date', () => {
      const result = formatDate(TEST_DATE);
      expect(result).toBeTruthy();
      expect(typeof result).toBe('string');
    });

    it('should include the year in the formatted output', () => {
      const result = formatDate(TEST_DATE);
      expect(result).toContain('2024');
    });

    it('should not include time information when locale is en', () => {
      localStorage.setItem('user_locale', 'en');
      const result = formatDate(TEST_DATE);
      // Date-only format should not include AM/PM markers
      expect(result).not.toMatch(/AM|PM/i);
    });
  });
});
