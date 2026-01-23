import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';
import Dashboard from '@/views/Dashboard.vue';
import { useDiariesStore } from '@/stores/diaries';

vi.mock('@/services/api');

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/dashboard', component: Dashboard },
    { path: '/diaries', component: { template: '<div>Diaries</div>' } },
  ],
});

describe('Dashboard View', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('should render dashboard', () => {
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    expect(wrapper.exists()).toBe(true);
  });

  it('should load stats on mount', async () => {
    const store = useDiariesStore();
    const fetchStatsSpy = vi.spyOn(store, 'fetchStats').mockResolvedValue();

    mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    await flushPromises();
    
    expect(fetchStatsSpy).toHaveBeenCalled();
  });

  it('should load recent diaries on mount', async () => {
    const store = useDiariesStore();
    const fetchDiariesSpy = vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    await flushPromises();
    
    expect(fetchDiariesSpy).toHaveBeenCalledWith(1, 5);
  });

  it('should display stats card when stats loaded', async () => {
    const store = useDiariesStore();
    store.stats = {
      total: 10,
      positive: 6,
      negative: 2,
      neutral: 2,
    };
    vi.spyOn(store, 'fetchStats').mockResolvedValue();
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
          MainLayout: {
            template: '<div><slot /></div>',
          },
        },
      },
    });
    
    // Wait for all async operations to complete
    await flushPromises();
    await wrapper.vm.$nextTick();
    await flushPromises();
    
    expect(wrapper.findComponent({ name: 'StatsCard' }).exists()).toBe(true);
  });

  it('should display diary cards when entries loaded', async () => {
    const store = useDiariesStore();
    store.entries = [
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
    ];
    vi.spyOn(store, 'fetchStats').mockResolvedValue();
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    await flushPromises();
    await wrapper.vm.$nextTick();
    await flushPromises();
    
    expect(wrapper.findAllComponents({ name: 'DiaryCard' }).length).toBeGreaterThan(0);
  });

  it('should show empty state when no diaries', async () => {
    const store = useDiariesStore();
    store.entries = [];
    vi.spyOn(store, 'fetchStats').mockResolvedValue();
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    await flushPromises();
    await wrapper.vm.$nextTick();
    await flushPromises();
    
    expect(wrapper.findComponent({ name: 'EmptyState' }).exists()).toBe(true);
  });

  it('should show loading spinner during data fetch', () => {
    const store = useDiariesStore();
    store.loading = true;
    vi.spyOn(store, 'fetchStats').mockImplementation(() => new Promise(() => {}));
    vi.spyOn(store, 'fetchDiaries').mockImplementation(() => new Promise(() => {}));

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    expect(wrapper.findComponent({ name: 'LoadingSpinner' }).exists()).toBe(true);
  });

  it('should have create entry button', async () => {
    const store = useDiariesStore();
    vi.spyOn(store, 'fetchStats').mockResolvedValue();
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    await flushPromises();
    await wrapper.vm.$nextTick();
    await flushPromises();
    
    const buttons = wrapper.findAll('button, a');
    const createButton = buttons.find(button => 
      button.text().includes('Create') || button.text().includes('New')
    );
    
    expect(createButton).toBeDefined();
  });

  it('should handle error when fetching stats fails', async () => {
    const store = useDiariesStore();
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(store, 'fetchStats').mockRejectedValue(new Error('Failed to fetch stats'));
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const _wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    await flushPromises();
    
    // Stats fetch error should be handled
    expect(store.fetchStats).toHaveBeenCalled();
    
    consoleSpy.mockRestore();
  });

  it('should handle error when fetching diaries fails', async () => {
    const store = useDiariesStore();
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(store, 'fetchStats').mockResolvedValue();
    vi.spyOn(store, 'fetchDiaries').mockRejectedValue(new Error('Failed to fetch diaries'));

    const _wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    await flushPromises();
    
    // Diaries fetch error should be handled
    expect(store.fetchDiaries).toHaveBeenCalled();
    
    consoleSpy.mockRestore();
  });

  it('should handle generic error when error is not an Error instance', async () => {
    const store = useDiariesStore();
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(store, 'fetchStats').mockRejectedValue('String error');
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const _wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    await flushPromises();
    
    expect(store.fetchStats).toHaveBeenCalled();
    
    consoleSpy.mockRestore();
  });

  it('should render the main container', async () => {
    const store = useDiariesStore();
    vi.spyOn(store, 'fetchStats').mockResolvedValue();
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          StatsCard: true,
          DiaryCard: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });
    
    await flushPromises();
    
    expect(wrapper.exists()).toBe(true);
  });
});
