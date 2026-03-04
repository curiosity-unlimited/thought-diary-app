/**
 * UI Store
 * Manages global UI state like loading indicators and theme
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

const THEME_STORAGE_KEY = 'theme';

export const useUIStore = defineStore('ui', () => {
  // State
  const isLoading = ref(false);
  const loadingMessage = ref<string>('');
  const theme = ref<'light' | 'dark'>('light');

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

  return {
    // State
    isLoading,
    loadingMessage,
    theme,

    // Computed
    hasLoadingMessage,
    isDark,

    // Actions
    setLoading,
    clearLoading,
    initTheme,
    toggleTheme,
  };
});
