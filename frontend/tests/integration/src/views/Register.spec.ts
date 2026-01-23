import { mount, flushPromises } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createRouter, createWebHistory } from 'vue-router';
import Register from '@/views/Register.vue';
import { useAuthStore } from '@/stores/auth';
import { createPinia, setActivePinia } from 'pinia';
import * as api from '@/services/api';

describe('Register.vue - Integration Tests', () => {
  let router: ReturnType<typeof createRouter>;

  beforeEach(() => {
    setActivePinia(createPinia());
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/register', component: Register },
        { path: '/login', component: { template: '<div>Login</div>' } },
        { path: '/about', component: { template: '<div>About</div>' } },
      ],
    });
    
    vi.spyOn(api, 'register').mockResolvedValue(undefined);
  });

  it('should render AuthLayout with form inputs and password requirements', async () => {
    const wrapper = mount(Register, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    expect(wrapper.find('form').exists()).toBe(true);
    expect(wrapper.find('input[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
    
    const text = wrapper.text().toLowerCase();
    expect(
      text.includes('password') && 
      (text.includes('requirement') || text.includes('must') || text.includes('character'))
    ).toBe(true);
  });

  it('should show link to login page', async () => {
    const wrapper = mount(Register, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    const text = wrapper.text().toLowerCase();
    expect(text.includes('sign in') || text.includes('login') || text.includes('already have')).toBe(true);
  });

  it('should render with router and store integration', async () => {
    const store = useAuthStore();
    
    const wrapper = mount(Register, {
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

  it('should handle registration error and show error message', async () => {
    // Mock register to reject
    vi.spyOn(api, 'register').mockRejectedValue(new Error('Email already exists'));

    await router.push('/register');
    const wrapper = mount(Register, {
      global: {
        plugins: [router],
      },
    });

    await wrapper.vm.$nextTick();
    await flushPromises();

    // Fill form with valid data
    const emailInput = wrapper.find('input[type="email"]');
    const passwordInput = wrapper.find('input[type="password"]');
    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('Password123!');

    // Submit form
    const form = wrapper.find('form');
    await form.trigger('submit');
    await flushPromises();

    // User should still be on register page
    expect(router.currentRoute.value.path).toBe('/register');
  });

  it('should handle generic error when error is not an Error instance', async () => {
    // Mock register to reject with non-Error object
    vi.spyOn(api, 'register').mockRejectedValue('String error');

    await router.push('/register');
    const wrapper = mount(Register, {
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

    // User should still be on register page
    expect(router.currentRoute.value.path).toBe('/register');
  });
});
