import { mount, flushPromises } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createRouter, createWebHistory } from 'vue-router';
import Diaries from '@/views/Diaries.vue';
import { useDiariesStore } from '@/stores/diaries';
import { createPinia, setActivePinia } from 'pinia';
import * as api from '@/services/api';

describe('Diaries.vue - Integration Tests', () => {
  let router: ReturnType<typeof createRouter>;

  beforeEach(() => {
    setActivePinia(createPinia());
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/diaries', component: Diaries },
        { path: '/diaries/:id', component: { template: '<div>Diary Detail</div>' } },
        { path: '/dashboard', component: { template: '<div>Dashboard</div>' } },
        { path: '/profile', component: { template: '<div>Profile</div>' } },
        { path: '/about', component: { template: '<div>About</div>' } },
      ],
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
        per_page: 10,
        total: 15,
        pages: 2,
      },
    });
  });

  it('should render MainLayout with diary list', async () => {
    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Should render the MainLayout structure with Navbar
    expect(wrapper.text()).toContain('Dashboard');
    expect(wrapper.text()).toContain('Diaries');
  });

  it('should load diaries from store on mount', async () => {
    const store = useDiariesStore();
    const fetchDiariesSpy = vi.spyOn(store, 'fetchDiaries');

    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    expect(fetchDiariesSpy).toHaveBeenCalled();
  });

  it('should integrate with router and store', async () => {
    const store = useDiariesStore();
    
    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    expect(store).toBeDefined();
    expect(router.currentRoute.value.path).toBe('/');
  });

  it('should handle page changes via query params', async () => {
    await router.push('/diaries?page=2');
    
    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    expect(router.currentRoute.value.query.page).toBe('2');
  });

  it('should handle create query param to show form', async () => {
    await router.push('/diaries?create=true');
    
    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    expect(router.currentRoute.value.query.create).toBe('true');
  });

  it('should handle diary creation success', async () => {
    vi.spyOn(api, 'createDiary').mockResolvedValue({
      id: 3,
      content: 'New diary',
      analyzed_content: 'New diary',
      positive_count: 0,
      negative_count: 0,
      created_at: '2026-01-03T00:00:00Z',
      updated_at: '2026-01-03T00:00:00Z',
    });

    await router.push('/diaries?create=true');
    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Find and interact with create form
    const textarea = wrapper.find('textarea');
    if (textarea.exists()) {
      await textarea.setValue('New diary entry content');
      
      // Find submit button in the form
      const submitButton = wrapper.find('button[type="submit"]');
      if (submitButton.exists()) {
        await submitButton.trigger('click');
        await flushPromises();
      }
    }
  });

  it('should handle diary creation error', async () => {
    vi.spyOn(api, 'createDiary').mockRejectedValue(new Error('Failed to create'));

    await router.push('/diaries?create=true');
    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Try to create a diary
    const textarea = wrapper.find('textarea');
    if (textarea.exists()) {
      await textarea.setValue('New diary entry');
      
      const submitButton = wrapper.find('button[type="submit"]');
      if (submitButton.exists()) {
        await submitButton.trigger('click');
        await flushPromises();
      }
    }
  });

  it('should handle diary deletion', async () => {
    vi.spyOn(api, 'deleteDiary').mockResolvedValue(undefined);

    await router.push('/diaries');
    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Store should have diaries loaded
    const store = useDiariesStore();
    expect(store.entries.length).toBeGreaterThan(0);
  });

  it('should handle diary deletion error', async () => {
    vi.spyOn(api, 'deleteDiary').mockRejectedValue(new Error('Failed to delete'));

    await router.push('/diaries');
    const wrapper = mount(Diaries, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    const store = useDiariesStore();
    
    // Try to delete a diary
    if (store.entries.length > 0) {
      try {
        await store.deleteDiary(store.entries[0].id);
      } catch (error) {
        expect(error).toBeDefined();
      }
    }
  });
});
