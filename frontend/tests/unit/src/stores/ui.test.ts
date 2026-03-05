import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useUIStore } from '@/stores/ui';

describe('UI Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
    // Reset the document class between tests
    document.documentElement.classList.remove('dark');
    vi.clearAllMocks();
  });

  describe('State Initialization', () => {
    it('should initialize with light theme by default', () => {
      const store = useUIStore();

      expect(store.theme).toBe('light');
      expect(store.isDark).toBe(false);
    });

    it('should initialize with false loading state', () => {
      const store = useUIStore();

      expect(store.isLoading).toBe(false);
      expect(store.loadingMessage).toBe('');
      expect(store.hasLoadingMessage).toBe(false);
    });
  });

  describe('initTheme()', () => {
    it('should default to light theme when localStorage is empty', () => {
      const store = useUIStore();
      store.initTheme();

      expect(store.theme).toBe('light');
      expect(store.isDark).toBe(false);
      expect(document.documentElement.classList.contains('dark')).toBe(false);
    });

    it('should load dark theme from localStorage', () => {
      localStorage.setItem('theme', 'dark');
      const store = useUIStore();
      store.initTheme();

      expect(store.theme).toBe('dark');
      expect(store.isDark).toBe(true);
      expect(document.documentElement.classList.contains('dark')).toBe(true);
    });

    it('should load light theme from localStorage', () => {
      localStorage.setItem('theme', 'light');
      const store = useUIStore();
      store.initTheme();

      expect(store.theme).toBe('light');
      expect(store.isDark).toBe(false);
      expect(document.documentElement.classList.contains('dark')).toBe(false);
    });

    it('should treat unknown localStorage values as light theme', () => {
      localStorage.setItem('theme', 'unknown-value');
      const store = useUIStore();
      store.initTheme();

      expect(store.theme).toBe('light');
      expect(store.isDark).toBe(false);
    });
  });

  describe('toggleTheme()', () => {
    it('should switch from light to dark', () => {
      const store = useUIStore();
      store.initTheme(); // starts light

      store.toggleTheme();

      expect(store.theme).toBe('dark');
      expect(store.isDark).toBe(true);
      expect(document.documentElement.classList.contains('dark')).toBe(true);
    });

    it('should switch from dark to light', () => {
      localStorage.setItem('theme', 'dark');
      const store = useUIStore();
      store.initTheme();

      store.toggleTheme();

      expect(store.theme).toBe('light');
      expect(store.isDark).toBe(false);
      expect(document.documentElement.classList.contains('dark')).toBe(false);
    });

    it('should persist theme to localStorage when toggling to dark', () => {
      const store = useUIStore();
      store.initTheme();

      store.toggleTheme();

      expect(localStorage.getItem('theme')).toBe('dark');
    });

    it('should persist theme to localStorage when toggling to light', () => {
      localStorage.setItem('theme', 'dark');
      const store = useUIStore();
      store.initTheme();

      store.toggleTheme();

      expect(localStorage.getItem('theme')).toBe('light');
    });

    it('should toggle back and forth correctly', () => {
      const store = useUIStore();
      store.initTheme();

      store.toggleTheme(); // dark
      expect(store.isDark).toBe(true);

      store.toggleTheme(); // light
      expect(store.isDark).toBe(false);

      store.toggleTheme(); // dark again
      expect(store.isDark).toBe(true);
    });
  });

  describe('setLoading()', () => {
    it('should set loading state with message', () => {
      const store = useUIStore();
      store.setLoading(true, 'Loading data...');

      expect(store.isLoading).toBe(true);
      expect(store.loadingMessage).toBe('Loading data...');
      expect(store.hasLoadingMessage).toBe(true);
    });

    it('should set loading state without message', () => {
      const store = useUIStore();
      store.setLoading(true);

      expect(store.isLoading).toBe(true);
      expect(store.loadingMessage).toBe('');
      expect(store.hasLoadingMessage).toBe(false);
    });

    it('should clear loading state', () => {
      const store = useUIStore();
      store.setLoading(true, 'Loading...');
      store.setLoading(false);

      expect(store.isLoading).toBe(false);
      expect(store.loadingMessage).toBe('');
    });
  });

  describe('clearLoading()', () => {
    it('should clear loading state and message', () => {
      const store = useUIStore();
      store.setLoading(true, 'Loading...');
      store.clearLoading();

      expect(store.isLoading).toBe(false);
      expect(store.loadingMessage).toBe('');
      expect(store.hasLoadingMessage).toBe(false);
    });
  });
});
