import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import LoadingSpinner from '@/components/LoadingSpinner.vue';

describe('LoadingSpinner', () => {
  it('should render spinner', () => {
    const wrapper = mount(LoadingSpinner);
    
    expect(wrapper.find('[role="status"]').exists()).toBe(true);
    expect(wrapper.find('svg').exists()).toBe(true);
  });

  it('should display message when provided', () => {
    const message = 'Loading data...';
    const wrapper = mount(LoadingSpinner, {
      props: { message },
    });
    
    expect(wrapper.text()).toContain(message);
  });

  it('should not display message when not provided', () => {
    const wrapper = mount(LoadingSpinner);
    
    expect(wrapper.find('.mt-3').exists()).toBe(false);
  });

  it('should render small size correctly', () => {
    const wrapper = mount(LoadingSpinner, {
      props: { size: 'sm' },
    });
    
    const svg = wrapper.find('svg');
    expect(svg.classes()).toContain('w-6');
    expect(svg.classes()).toContain('h-6');
  });

  it('should render medium size correctly (default)', () => {
    const wrapper = mount(LoadingSpinner);
    
    const svg = wrapper.find('svg');
    expect(svg.classes()).toContain('w-10');
    expect(svg.classes()).toContain('h-10');
  });

  it('should render large size correctly', () => {
    const wrapper = mount(LoadingSpinner, {
      props: { size: 'lg' },
    });
    
    const svg = wrapper.find('svg');
    expect(svg.classes()).toContain('w-16');
    expect(svg.classes()).toContain('h-16');
  });

  it('should have accessible aria-label', () => {
    const wrapper = mount(LoadingSpinner);
    
    const spinner = wrapper.find('[role="status"]');
    expect(spinner.attributes('aria-label')).toBe('Loading');
  });

  it('should center content when specified', () => {
    const wrapper = mount(LoadingSpinner, {
      props: { center: true },
    });
    
    const container = wrapper.find('.flex');
    expect(container.classes()).toContain('justify-center');
    expect(container.classes()).toContain('items-center');
  });
});
