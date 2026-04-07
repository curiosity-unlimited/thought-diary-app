/**
 * Date Formatter Utility
 * Provides locale-aware date formatting functions that respect the current
 * application locale stored in localStorage.
 */

import { LOCALE_STORAGE_KEY } from '@/i18n';

/**
 * Maps application locale codes to BCP 47 language tags used by the
 * Intl.DateTimeFormat API.
 */
const LOCALE_MAP: Record<string, string> = {
  en: 'en-US',
  'zh-tw': 'zh-TW',
};

/**
 * Resolve the current Intl locale from the persisted application locale.
 */
const resolveIntlLocale = (): string => {
  const stored = localStorage.getItem(LOCALE_STORAGE_KEY);
  return LOCALE_MAP[stored ?? ''] ?? 'en-US';
};

/**
 * Format a date string to a human-readable date and time.
 *
 * @param dateString - ISO 8601 date string
 * @returns Localised date-time string (e.g. "January 1, 2024, 12:00 PM")
 *
 * @example
 * formatDateTime('2024-01-01T12:00:00Z') // "January 1, 2024, 12:00 PM"
 */
export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString(resolveIntlLocale(), {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Format a date string to a human-readable date (without time).
 *
 * @param dateString - ISO 8601 date string
 * @returns Localised date string (e.g. "January 1, 2024")
 *
 * @example
 * formatDate('2024-01-01T12:00:00Z') // "January 1, 2024"
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString(resolveIntlLocale(), {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};
