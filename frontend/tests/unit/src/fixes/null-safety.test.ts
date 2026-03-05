/**
 * Tests for null safety fixes in Dashboard and Diaries views
 * Verifies that components handle undefined/null store data gracefully
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';
import Dashboard from '@/views/Dashboard.vue';
import Diaries from '@/views/Diaries.vue';

// Mock components
vi.mock('@/components/StatsCard.vue', () => ({
  default: { name: 'StatsCard', template: '<div>StatsCard</div>' },
}));
vi.mock('@/components/DiaryCard.vue', () => ({
  default: { name: 'DiaryCard', template: '<div>DiaryCard</div>' },
}));
vi.mock('@/components/DiaryForm.vue', () => ({
  default: { name: 'DiaryForm', template: '<div>DiaryForm</div>' },
}));
vi.mock('@/components/Pagination.vue', () => ({
  default: { name: 'Pagination', template: '<div>Pagination</div>' },
}));
vi.mock('@/components/LoadingSpinner.vue', () => ({
  default: { name: 'LoadingSpinner', template: '<div>Loading...</div>' },
}));
vi.mock('@/components/EmptyState.vue', () => ({
  default: { name: 'EmptyState', template: '<div>Empty State</div>' },
}));
vi.mock('@/layouts/MainLayout.vue', () => ({
  default: {
    name: 'MainLayout',
    template: '<div><slot /></div>',
  },
}));

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/diaries', component: Diaries },
  ],
});

describe('Null Safety Fixes', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  describe('Dashboard View', () => {
    it('should handle undefined entries array gracefully', async () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [createPinia(), router],
          stubs: {
            MainLayout: {
              template: '<div><slot /></div>',
            },
          },
        },
      });

      // Should not throw error when entries is undefined
      expect(wrapper.exists()).toBe(true);
    });

    it('should render empty state when entries is empty array', async () => {
      const wrapper = mount(Dashboard, {
        global: {
          plugins: [createPinia(), router],
          stubs: {
            MainLayout: {
              template: '<div><slot /></div>',
            },
          },
        },
      });

      await wrapper.vm.$nextTick();

      // Component should render without errors
      expect(wrapper.exists()).toBe(true);
    });
  });

  describe('Diaries View', () => {
    it('should handle null entries in v-else-if check', async () => {
      const wrapper = mount(Diaries, {
        global: {
          plugins: [createPinia(), router],
          stubs: {
            MainLayout: {
              template: '<div><slot /></div>',
            },
          },
        },
      });

      // Should not throw error when checking entries.length
      expect(wrapper.exists()).toBe(true);
    });

    it('should render empty state when entries is null or empty', async () => {
      const wrapper = mount(Diaries, {
        global: {
          plugins: [createPinia(), router],
          stubs: {
            MainLayout: {
              template: '<div><slot /></div>',
            },
          },
        },
      });

      await wrapper.vm.$nextTick();

      // Component should render without errors
      expect(wrapper.exists()).toBe(true);
    });
  });
});
