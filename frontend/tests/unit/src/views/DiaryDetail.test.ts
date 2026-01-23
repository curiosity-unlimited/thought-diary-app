import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';
import DiaryDetail from '@/views/DiaryDetail.vue';
import { useDiariesStore } from '@/stores/diaries';
import type { DiaryEntry } from '@/types';

vi.mock('@/services/api');

const mockDiary: DiaryEntry = {
  id: 1,
  content: 'Test diary content',
  analyzed_content: 'Test <span class="positive">diary</span> content',
  positive_count: 1,
  negative_count: 0,
  created_at: '2026-01-15T10:00:00Z',
  updated_at: '2026-01-15T10:00:00Z',
};

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/diaries/:id', name: 'diary-detail', component: DiaryDetail },
    { path: '/diaries', component: { template: '<div>Diaries</div>' } },
  ],
});

describe('DiaryDetail View', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('should render diary detail when loaded', async () => {
    const store = useDiariesStore();
    store.currentDiary = mockDiary;
    vi.spyOn(store, 'fetchDiary').mockResolvedValue();

    await router.push('/diaries/1');
    const wrapper = mount(DiaryDetail, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
        },
      },
    });

    await flushPromises();

    expect(wrapper.text()).toContain('Test');
  });

  it('should load diary on mount', async () => {
    const store = useDiariesStore();
    const fetchDiarySpy = vi.spyOn(store, 'fetchDiary').mockResolvedValue();

    await router.push('/diaries/1');
    const _wrapper = mount(DiaryDetail, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
        },
      },
    });

    await flushPromises();

    expect(fetchDiarySpy).toHaveBeenCalledWith(1);
  });

  it('should handle error when loading diary fails', async () => {
    const store = useDiariesStore();
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(store, 'fetchDiary').mockRejectedValue(new Error('Not found'));

    await router.push('/diaries/1');
    const _wrapper = mount(DiaryDetail, {
      global: {
        plugins: [router],
        stubs: {
          MainLayout: { template: '<div><slot /></div>' },
        },
      },
    });

    await flushPromises();

    expect(store.fetchDiary).toHaveBeenCalled();
    
    consoleSpy.mockRestore();
  });
});
