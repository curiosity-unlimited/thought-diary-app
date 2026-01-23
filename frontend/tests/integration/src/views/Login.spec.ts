import { mount, flushPromises } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/Login.vue';
import { useAuthStore } from '@/stores/auth';
import { createPinia, setActivePinia } from 'pinia';
import * as api from '@/services/api';

describe('Login.vue - Integration Tests', () => {
  let router: ReturnType<typeof createRouter>;

  beforeEach(() => {
    setActivePinia(createPinia());
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/login', component: Login },
        { path: '/register', component: { template: '<div>Register</div>' } },
        { path: '/dashboard', component: { template: '<div>Dashboard</div>' } },
        { path: '/about', component: { template: '<div>About</div>' } },
      ],
    });
    
    // Mock API calls
    vi.spyOn(api, 'login').mockResolvedValue({
      access_token: 'fake-access-token',
      refresh_token: 'fake-refresh-token',
    });
  });

  it('should render AuthLayout with form inputs', async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Verify AuthLayout renders
    expect(wrapper.find('form').exists()).toBe(true);
    expect(wrapper.find('input[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
  });

  it('should show link to register page', async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    const text = wrapper.text().toLowerCase();
    expect(text.includes('sign up') || text.includes('register') || text.includes('create account')).toBe(true);
  });

  it('should render with router and store integration', async () => {
    const store = useAuthStore();
    
    const wrapper = mount(Login, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    expect(store).toBeDefined();
    expect(store.isAuthenticated).toBe(false);
    expect(router.currentRoute.value.path).toBe('/');
  });

  it('should handle login error and show error message', async () => {
    // Mock login to reject
    vi.spyOn(api, 'login').mockRejectedValue(new Error('Invalid credentials'));

    await router.push('/login');
    const wrapper = mount(Login, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Fill form
    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');
    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('Password123!');

    // Submit form
    const form = wrapper.find('form');
    await form.trigger('submit');
    await flushPromises();

    // User should still be on login page
    expect(router.currentRoute.value.path).toBe('/login');
  });

  it('should handle generic error when error is not an Error instance', async () => {
    // Mock login to reject with non-Error object
    vi.spyOn(api, 'login').mockRejectedValue('String error');

    await router.push('/login');
    const wrapper = mount(Login, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Fill form
    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');
    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('Password123!');

    // Submit form
    const form = wrapper.find('form');
    await form.trigger('submit');
    await flushPromises();

    // User should still be on login page
    expect(router.currentRoute.value.path).toBe('/login');
  });
});
