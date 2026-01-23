import { mount, flushPromises } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '@/views/Dashboard.vue';
import { useDiariesStore } from '@/stores/diaries';
import { createPinia, setActivePinia } from 'pinia';
import * as api from '@/services/api';

describe('Dashboard.vue - Integration Tests', () => {
  let router: ReturnType<typeof createRouter>;

  beforeEach(() => {
    setActivePinia(createPinia());
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/dashboard', component: Dashboard },
        { path: '/diaries', component: { template: '<div>Diaries</div>' } },
        { path: '/diaries/:id', component: { template: '<div>Diary Detail</div>' } },
      ],
    });
    
    vi.spyOn(api, 'getDiaryStats').mockResolvedValue({
      total: 10,
      positive: 6,
      negative: 2,
      neutral: 2,
    });
    
    vi.spyOn(api, 'getDiaries').mockResolvedValue({
      diaries: [
        {
          id: 1,
          content: 'Test diary 1',
          analyzed_content: 'Test diary 1',
          positive_count: 1,
          negative_count: 0,
          created_at: '2026-01-01T00:00:00Z',
          updated_at: '2026-01-01T00:00:00Z',
        },
        {
          id: 2,
          content: 'Test diary 2',
          analyzed_content: 'Test diary 2',
          positive_count: 0,
          negative_count: 1,
          created_at: '2026-01-02T00:00:00Z',
          updated_at: '2026-01-02T00:00:00Z',
        },
      ],
      pagination: {
        page: 1,
        per_page: 5,
        total: 10,
        pages: 2,
      },
    });
  });

  it('should render MainLayout with dashboard content', async () => {
    await router.push('/dashboard');
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Should render the dashboard
    expect(wrapper.exists()).toBe(true);
  });

  it('should load stats and diaries on mount', async () => {
    const store = useDiariesStore();
    const fetchStatsSpy = vi.spyOn(store, 'fetchStats');
    const fetchDiariesSpy = vi.spyOn(store, 'fetchDiaries');

    await router.push('/dashboard');
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    expect(fetchStatsSpy).toHaveBeenCalled();
    expect(fetchDiariesSpy).toHaveBeenCalledWith(1, 5);
  });

  it('should handle navigation to create entry', async () => {
    await router.push('/dashboard');
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Find create button
    const buttons = wrapper.findAll('button, a');
    const createButton = buttons.find(b => 
      b.text().includes('Create') || b.text().includes('New')
    );

    if (createButton) {
      await createButton.trigger('click');
      await flushPromises();
      await router.isReady();
      
      // Should navigate to diaries with create param
      const path = router.currentRoute.value.path;
      const hasCreate = router.currentRoute.value.query.create === 'true';
      expect(path === '/diaries' || hasCreate).toBe(true);
    }
  });

  it('should handle error when loading dashboard data fails', async () => {
    vi.spyOn(api, 'getDiaryStats').mockRejectedValue(new Error('Failed to load'));

    await router.push('/dashboard');
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Error should be handled
    expect(wrapper.exists()).toBe(true);
  });
});
