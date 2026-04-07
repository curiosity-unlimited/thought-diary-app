/**
 * UI Store
 * Manages global UI state like loading indicators, theme, and locale
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {
  LOCALE_STORAGE_KEY,
  SUPPORTED_LOCALES,
  detectLocale,
  type SupportedLocale,
} from '@/i18n';
import { useI18n } from 'vue-i18n';

const THEME_STORAGE_KEY = 'theme';

export const useUIStore = defineStore('ui', () => {
  // State
  const isLoading = ref(false);
  const loadingMessage = ref<string>('');
  const theme = ref<'light' | 'dark'>('light');
  const locale = ref<SupportedLocale>(detectLocale());

  // Computed
  const hasLoadingMessage = computed(() => !!loadingMessage.value);

  /** Whether dark mode is currently active */
  const isDark = computed(() => theme.value === 'dark');

  /**
   * Set global loading state
   * @param loading - Whether to show loading indicator
   * @param message - Optional loading message to display
   */
  const setLoading = (loading: boolean, message: string = ''): void => {
    isLoading.value = loading;
    loadingMessage.value = message;
  };

  /**
   * Clear loading state
   */
  const clearLoading = (): void => {
    isLoading.value = false;
    loadingMessage.value = '';
  };

  /**
   * Initialize theme from localStorage and apply to document
   */
  const initTheme = (): void => {
    const stored = localStorage.getItem(THEME_STORAGE_KEY);
    theme.value = stored === 'dark' ? 'dark' : 'light';
    applyTheme();
  };

  /**
   * Toggle between light and dark themes and persist to localStorage
   */
  const toggleTheme = (): void => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark';
    localStorage.setItem(THEME_STORAGE_KEY, theme.value);
    applyTheme();
  };

  /**
   * Apply the current theme to the document root element
   */
  const applyTheme = (): void => {
    if (theme.value === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  /**
   * Initialize locale from localStorage or browser language detection
   */
  const initLocale = (): void => {
    const detected = detectLocale();
    locale.value = detected;
    // Sync with vue-i18n global instance
    try {
      const { locale: i18nLocale } = useI18n({ useScope: 'global' });
      i18nLocale.value = detected;
    } catch {
      // useI18n may not be available outside of component context;
      // the i18n instance was already initialised with detectLocale() in i18n/index.ts
    }
  };

  /**
   * Set the active locale and persist to localStorage
   * @param newLocale - Locale code to activate
   */
  const setLocale = (newLocale: SupportedLocale): void => {
    if (!SUPPORTED_LOCALES.includes(newLocale)) {
      return;
    }
    locale.value = newLocale;
    localStorage.setItem(LOCALE_STORAGE_KEY, newLocale);
    // Sync with vue-i18n global instance
    try {
      const { locale: i18nLocale } = useI18n({ useScope: 'global' });
      i18nLocale.value = newLocale;
    } catch {
      // Outside component context – caller must sync manually if needed
    }
  };

  return {
    // State
    isLoading,
    loadingMessage,
    theme,
    locale,

    // Computed
    hasLoadingMessage,
    isDark,

    // Actions
    setLoading,
    clearLoading,
    initTheme,
    toggleTheme,
    initLocale,
    setLocale,
  };
});
