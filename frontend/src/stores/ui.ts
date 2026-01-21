/**
 * UI Store
 * Manages global UI state like loading indicators
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUIStore = defineStore('ui', () => {
  // State
  const isLoading = ref(false);
  const loadingMessage = ref<string>('');

  // Computed
  const hasLoadingMessage = computed(() => !!loadingMessage.value);

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

  return {
    // State
    isLoading,
    loadingMessage,

    // Computed
    hasLoadingMessage,

    // Actions
    setLoading,
    clearLoading,
  };
});
