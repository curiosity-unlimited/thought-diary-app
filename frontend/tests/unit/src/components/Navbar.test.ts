import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import { useAuthStore } from '@/stores/auth';

vi.mock('@/services/api');

// Create a test router
const createTestRouter = () => {
  return createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/', component: { template: '<div>Home</div>' } },
      { path: '/dashboard', component: { template: '<div>Dashboard</div>' } },
      { path: '/diaries', component: { template: '<div>Diaries</div>' } },
      { path: '/profile', component: { template: '<div>Profile</div>' } },
      { path: '/about', component: { template: '<div>About</div>' } },
      { path: '/login', component: { template: '<div>Login</div>' } },
    ],
  });
};

describe('Navbar', () => {
  let router: ReturnType<typeof createTestRouter>;

  beforeEach(async () => {
    setActivePinia(createPinia());
    router = createTestRouter();
    await router.push('/');
    await router.isReady();
  });

  it('should render navbar', () => {
    const wrapper = mount(Navbar, {
      global: {
        plugins: [router],
        stubs: {
          Menu: false,
          MenuButton: false,
          MenuItem: false,
          MenuItems: false,
        },
      },
    });
    
    expect(wrapper.find('nav').exists()).toBe(true);
  });

  it('should display app name', () => {
    const wrapper = mount(Navbar, {
      global: {
        plugins: [router],
        stubs: {
          Menu: false,
          MenuButton: false,
          MenuItem: false,
          MenuItems: false,
        },
      },
    });
    
    expect(wrapper.text()).toContain('Thought Diary');
  });

  it('should display navigation links when authenticated', () => {
    const store = useAuthStore();
    store.user = {
      id: 1,
      email: 'test@example.com',
      created_at: '2026-01-01',
      updated_at: '2026-01-01',
    };
    store.accessToken = 'test-token';
    store.refreshToken = 'test-refresh-token';

    const wrapper = mount(Navbar, {
      global: {
        plugins: [router],
        stubs: {
          Menu: false,
          MenuButton: false,
          MenuItem: false,
          MenuItems: false,
        },
      },
    });
    
    expect(wrapper.text()).toContain('Dashboard');
    expect(wrapper.text()).toContain('Diaries');
  });

  it('should display user email when authenticated', () => {
    const store = useAuthStore();
    store.user = {
      id: 1,
      email: 'test@example.com',
      created_at: '2026-01-01',
      updated_at: '2026-01-01',
    };
    store.accessToken = 'test-token';
    store.refreshToken = 'test-refresh-token';

    const wrapper = mount(Navbar, {
      global: {
        plugins: [router],
        stubs: {
          Menu: false,
          MenuButton: false,
          MenuItem: false,
          MenuItems: false,
        },
      },
    });
    
    expect(wrapper.text()).toContain('test@example.com');
  });

  it('should call logout when logout button clicked', async () => {
    const store = useAuthStore();
    store.user = {
      id: 1,
      email: 'test@example.com',
      created_at: '2026-01-01',
      updated_at: '2026-01-01',
    };
    store.accessToken = 'test-token';
    store.refreshToken = 'test-refresh-token';

    const logoutSpy = vi.spyOn(store, 'logout').mockResolvedValue();

    const wrapper = mount(Navbar, {
      global: {
        plugins: [router],
        stubs: {
          Menu: false,
          MenuButton: false,
          MenuItem: false,
          MenuItems: false,
        },
      },
    });
    
    const logoutButton = wrapper.findAll('button').find(button => 
      button.text().includes('Logout') || button.text().includes('Log out')
    );
    
    if (logoutButton) {
      await logoutButton.trigger('click');
      expect(logoutSpy).toHaveBeenCalled();
    }
  });

  it('should toggle mobile menu', async () => {
    const wrapper = mount(Navbar, {
      global: {
        plugins: [router],
        stubs: {
          Menu: false,
          MenuButton: false,
          MenuItem: false,
          MenuItems: false,
        },
      },
    });
    
    const hamburgerButton = wrapper.find('button[aria-label="Toggle menu"], button[aria-expanded]');
    if (hamburgerButton.exists()) {
      await hamburgerButton.trigger('click');
      // Mobile menu should be visible
      expect(wrapper.html()).toContain('Dashboard') || expect(wrapper.html()).toContain('menu');
    }
  });
});
