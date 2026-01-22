import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import EmptyState from '@/components/EmptyState.vue';

describe('EmptyState', () => {
  it('should render title and message', () => {
    const wrapper = mount(EmptyState, {
      props: {
        title: 'No Data Found',
        message: 'There is no data to display.',
      },
    });
    
    expect(wrapper.text()).toContain('No Data Found');
    expect(wrapper.text()).toContain('There is no data to display.');
  });

  it('should render icon', () => {
    const wrapper = mount(EmptyState, {
      props: {
        title: 'No Data',
        message: 'Empty',
      },
    });
    
    expect(wrapper.find('svg').exists()).toBe(true);
  });

  it('should not render action button when actionText not provided', () => {
    const wrapper = mount(EmptyState, {
      props: {
        title: 'No Data',
        message: 'Empty',
      },
    });
    
    expect(wrapper.find('router-link').exists()).toBe(false);
    expect(wrapper.find('button').exists()).toBe(false);
  });

  it('should render action button when actionText provided', () => {
    const wrapper = mount(EmptyState, {
      props: {
        title: 'No Data',
        message: 'Empty',
        actionText: 'Create New',
        actionTo: '/create',
      },
      global: {
        stubs: {
          RouterLink: {
            template: '<a :to="to"><slot /></a>',
            props: ['to'],
          },
        },
      },
    });
    
    expect(wrapper.text()).toContain('Create New');
  });

  it('should have centered layout', () => {
    const wrapper = mount(EmptyState, {
      props: {
        title: 'No Data',
        message: 'Empty',
      },
    });
    
    const container = wrapper.find('.flex');
    expect(container.classes()).toContain('items-center');
    expect(container.classes()).toContain('justify-center');
  });
});
