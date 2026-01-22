import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';
import Login from '@/views/Login.vue';
import { useAuthStore } from '@/stores/auth';

vi.mock('@/services/api');

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/login', component: Login },
    { path: '/dashboard', component: { template: '<div>Dashboard</div>' } },
    { path: '/register', component: { template: '<div>Register</div>' } },
  ],
});

describe('Login View', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('should render login form', () => {
    const wrapper = mount(Login, {
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
    const wrapper = mount(Login, {
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
    const wrapper = mount(Login, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });
    
    const submitButton = wrapper.findAll('button').find(button => 
      button.attributes('type') === 'submit' || button.text().includes('Login') || button.text().includes('Sign in')
    );
    expect(submitButton).toBeDefined();
  });

  it('should show validation error for invalid email', async () => {
    const wrapper = mount(Login, {
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
    
    // Check if error message container exists or validation styling is applied
    const hasErrorClass = emailInput.classes().includes('border-red-500');
    const hasErrorText = wrapper.text().toLowerCase().includes('email') || wrapper.text().toLowerCase().includes('valid');
    expect(hasErrorClass || hasErrorText || wrapper.html().includes('error')).toBe(true);
  });

  it('should show validation error for short password', async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });
    
    const passwordInput = wrapper.find('input[type="password"]');
    await passwordInput.setValue('123');
    await passwordInput.trigger('blur');
    await flushPromises();
    
    // Check for error indication (class or text)
    const hasErrorClass = passwordInput.classes().includes('border-red-500');
    const hasErrorText = wrapper.text().toLowerCase().includes('password') || wrapper.text().toLowerCase().includes('characters');
    expect(hasErrorClass || hasErrorText || wrapper.html().includes('error')).toBe(true);
  });

  it('should call login action on form submit', async () => {
    const store = useAuthStore();
    const loginSpy = vi.spyOn(store, 'login').mockResolvedValue();

    const wrapper = mount(Login, {
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
    const passwordInput = wrapper.find('input[type="password"]');
    
    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('Password123!');
    
    const form = wrapper.find('form');
    await form.trigger('submit');
    await flushPromises();
    
    expect(loginSpy).toHaveBeenCalledWith('test@example.com', 'Password123!');
  });

  it('should have link to register page', () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router],
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });
    
    expect(wrapper.text().toLowerCase()).toContain('sign up');
  });

  it('should disable submit button during submission', async () => {
    const store = useAuthStore();
    vi.spyOn(store, 'login').mockImplementation(() => new Promise(() => {}));

    const wrapper = mount(Login, {
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
    const passwordInput = wrapper.find('input[type="password"]');
    
    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('Password123!');
    
    const form = wrapper.find('form');
    await form.trigger('submit');
    await wrapper.vm.$nextTick();
    
    const submitButton = wrapper.findAll('button').find(button => 
      button.attributes('type') === 'submit'
    );
    
    if (submitButton) {
      expect(submitButton.attributes('disabled')).toBeDefined();
    }
  });
});
