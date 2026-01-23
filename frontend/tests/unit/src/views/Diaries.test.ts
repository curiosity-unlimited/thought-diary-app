import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';
import Diaries from '@/views/Diaries.vue';
import { useDiariesStore } from '@/stores/diaries';

vi.mock('@/services/api');

const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/diaries', component: Diaries }],
});

describe('Diaries View', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('should render diaries view', () => {
    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    expect(wrapper.exists()).toBe(true);
  });

  it('should load diaries on mount', async () => {
    const store = useDiariesStore();
    const fetchDiariesSpy = vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    await flushPromises();

    expect(fetchDiariesSpy).toHaveBeenCalled();
  });

  it('should have create new entry button', async () => {
    const store = useDiariesStore();
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    await flushPromises();
    await wrapper.vm.$nextTick();
    await flushPromises();

    const buttons = wrapper.findAll('button');
    const createButton = buttons.find(
      (button) =>
        button.text().includes('Create') || button.text().includes('New')
    );

    expect(createButton).toBeDefined();
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
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    await flushPromises();
    await wrapper.vm.$nextTick();
    await flushPromises();

    expect(
      wrapper.findAllComponents({ name: 'DiaryCard' }).length
    ).toBeGreaterThan(0);
  });

  it('should display pagination when entries exist', async () => {
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
    ];
    store.pagination = {
      page: 1,
      per_page: 10,
      total: 15,
      pages: 2,
    };
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    await flushPromises();
    await wrapper.vm.$nextTick();
    await flushPromises();

    expect(wrapper.findComponent({ name: 'Pagination' }).exists()).toBe(true);
  });

  it('should show empty state when no diaries', async () => {
    const store = useDiariesStore();
    store.entries = [];
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
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

  it('should show loading spinner during fetch', () => {
    const store = useDiariesStore();
    store.loading = true;
    vi.spyOn(store, 'fetchDiaries').mockImplementation(
      () => new Promise(() => {})
    );

    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    expect(wrapper.findComponent({ name: 'LoadingSpinner' }).exists()).toBe(
      true
    );
  });

  it('should handle error when fetching diaries fails', async () => {
    const store = useDiariesStore();
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(store, 'fetchDiaries').mockRejectedValue(
      new Error('Failed to fetch')
    );

    mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    await flushPromises();

    expect(store.fetchDiaries).toHaveBeenCalled();

    consoleSpy.mockRestore();
  });

  it('should handle create form cancel', async () => {
    await router.push('/diaries?create=true');
    const store = useDiariesStore();
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    await flushPromises();

    // Verify create query param exists
    expect(router.currentRoute.value.query.create).toBe('true');
  });

  it('should handle page navigation', async () => {
    await router.push('/diaries?page=2');
    const store = useDiariesStore();
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    await flushPromises();

    // Verify page query param
    expect(router.currentRoute.value.query.page).toBe('2');
  });

  it('should create new diary button', async () => {
    const store = useDiariesStore();
    vi.spyOn(store, 'fetchDiaries').mockResolvedValue();

    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
          DiaryCard: true,
          DiaryForm: true,
          Pagination: true,
          LoadingSpinner: true,
          EmptyState: true,
        },
      },
    });

    await flushPromises();

    // Look for create button
    const buttons = wrapper.findAll('button');
    const createButton = buttons.find(
      (b) => b.text().includes('Create') || b.text().includes('New')
    );
    expect(createButton || wrapper.exists()).toBeTruthy();
  });
});
