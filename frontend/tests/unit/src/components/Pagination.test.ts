import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Pagination from '@/components/Pagination.vue';

describe('Pagination', () => {
  const mockPagination = {
    page: 2,
    per_page: 10,
    total: 45,
    pages: 5,
  };

  it('should render pagination controls', () => {
    const wrapper = mount(Pagination, {
      props: { pagination: mockPagination },
    });

    expect(wrapper.find('nav').exists()).toBe(true);
    expect(wrapper.findAll('button').length).toBeGreaterThan(0);
  });

  it('should display current page', () => {
    const wrapper = mount(Pagination, {
      props: { pagination: mockPagination },
    });

    expect(wrapper.text()).toContain('2');
  });

  it('should disable Previous button on first page', () => {
    const wrapper = mount(Pagination, {
      props: {
        pagination: { ...mockPagination, page: 1 },
      },
    });

    const prevButton = wrapper.findAll('button')[0];
    expect(prevButton.attributes('disabled')).toBeDefined();
  });

  it('should enable Previous button when not on first page', () => {
    const wrapper = mount(Pagination, {
      props: { pagination: mockPagination },
    });

    const prevButton = wrapper.findAll('button')[0];
    expect(prevButton.attributes('disabled')).toBeUndefined();
  });

  it('should disable Next button on last page', () => {
    const wrapper = mount(Pagination, {
      props: {
        pagination: { ...mockPagination, page: 5 },
      },
    });

    const buttons = wrapper.findAll('button');
    const nextButton = buttons[buttons.length - 1];
    expect(nextButton.attributes('disabled')).toBeDefined();
  });

  it('should enable Next button when not on last page', () => {
    const wrapper = mount(Pagination, {
      props: { pagination: mockPagination },
    });

    const buttons = wrapper.findAll('button');
    const nextButton = buttons[buttons.length - 1];
    expect(nextButton.attributes('disabled')).toBeUndefined();
  });

  it('should emit page-change event when clicking Previous', async () => {
    const wrapper = mount(Pagination, {
      props: { pagination: mockPagination },
    });

    const prevButton = wrapper.findAll('button')[0];
    await prevButton.trigger('click');

    expect(wrapper.emitted('pageChange')).toBeTruthy();
    expect(wrapper.emitted('pageChange')?.[0]).toEqual([1]);
  });

  it('should emit page-change event when clicking Next', async () => {
    const wrapper = mount(Pagination, {
      props: { pagination: mockPagination },
    });

    const buttons = wrapper.findAll('button');
    const nextButton = buttons[buttons.length - 1];
    await nextButton.trigger('click');

    expect(wrapper.emitted('pageChange')).toBeTruthy();
    expect(wrapper.emitted('pageChange')?.[0]).toEqual([3]);
  });

  it('should emit page-change event when clicking page number', async () => {
    const wrapper = mount(Pagination, {
      props: { pagination: mockPagination },
    });

    const pageButtons = wrapper
      .findAll('button')
      .filter(
        (button) =>
          !button.text().includes('Previous') &&
          !button.text().includes('Next') &&
          button.text().trim() === '1'
      );

    if (pageButtons.length > 0) {
      await pageButtons[0].trigger('click');
      expect(wrapper.emitted('pageChange')).toBeTruthy();
      expect(wrapper.emitted('pageChange')?.[0]).toEqual([1]);
    }
  });

  it('should highlight current page', () => {
    const wrapper = mount(Pagination, {
      props: { pagination: mockPagination },
    });

    const buttons = wrapper.findAll('button');
    const currentPageButton = buttons.find((button) =>
      button.classes().includes('bg-indigo-600')
    );

    expect(currentPageButton).toBeDefined();
  });

  it('should handle single page scenario', () => {
    const wrapper = mount(Pagination, {
      props: {
        pagination: {
          page: 1,
          per_page: 10,
          total: 5,
          pages: 1,
        },
      },
    });

    const buttons = wrapper.findAll('button');
    const prevButton = buttons[0];
    const nextButton = buttons[buttons.length - 1];

    expect(prevButton.attributes('disabled')).toBeDefined();
    expect(nextButton.attributes('disabled')).toBeDefined();
  });
});
