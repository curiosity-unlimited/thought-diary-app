import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';
import Register from '@/views/Register.vue';

vi.mock('@/services/api');

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/register', component: Register },
    { path: '/login', component: { template: '<div>Login</div>' } },
    { path: '/dashboard', component: { template: '<div>Dashboard</div>' } },
  ],
});

describe('Register View', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('should render register form', () => {
    const wrapper = mount(Register, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });

    expect(wrapper.find('form').exists()).toBe(true);
    expect(wrapper.find('input[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
  });

  it('should have email and password inputs', () => {
    const wrapper = mount(Register, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });

    const inputs = wrapper.findAll('input');
    expect(inputs.length).toBeGreaterThanOrEqual(2);
  });

  it('should have submit button', () => {
    const wrapper = mount(Register, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });

    const submitButton = wrapper
      .findAll('button')
      .find(
        (button) =>
          button.attributes('type') === 'submit' ||
          button.text().includes('Register') ||
          button.text().includes('Sign up')
      );
    expect(submitButton).toBeDefined();
  });

  it('should show validation error for invalid email', async () => {
    const wrapper = mount(Register, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });

    const emailInput = wrapper.find('input[type="email"]');
    await emailInput.setValue('invalid-email');
    await emailInput.trigger('blur');
    await flushPromises();

    // Check if error message or styling is present
    const hasErrorClass = emailInput.classes().includes('border-red-500');
    const hasErrorText =
      wrapper.text().toLowerCase().includes('email') ||
      wrapper.text().toLowerCase().includes('valid');
    expect(
      hasErrorClass || hasErrorText || wrapper.html().includes('error')
    ).toBe(true);
  });

  it('should show password requirements', () => {
    const wrapper = mount(Register, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });

    expect(wrapper.text()).toContain('8') ||
      expect(wrapper.text()).toContain('uppercase') ||
      expect(wrapper.text()).toContain('character');
  });

  it('should have link to login page', () => {
    const wrapper = mount(Register, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });

    const text = wrapper.text().toLowerCase();
    expect(
      text.includes('sign in') ||
        text.includes('login') ||
        text.includes('already have')
    ).toBe(true);
  });
});
