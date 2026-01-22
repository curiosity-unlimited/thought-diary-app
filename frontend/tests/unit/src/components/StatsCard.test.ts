import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import StatsCard from '@/components/StatsCard.vue';

describe('StatsCard', () => {
  const mockStats = {
    total: 42,
    positive: 25,
    negative: 10,
    neutral: 7,
  };

  it('should render all stat cards', () => {
    const wrapper = mount(StatsCard, {
      props: { stats: mockStats },
    });
    
    expect(wrapper.findAll('.bg-gradient-to-br')).toHaveLength(4);
  });

  it('should display correct total count', () => {
    const wrapper = mount(StatsCard, {
      props: { stats: mockStats },
    });
    
    const cards = wrapper.findAll('.bg-gradient-to-br');
    expect(cards[0].text()).toContain('42');
    expect(cards[0].text()).toContain('Total Entries');
  });

  it('should display correct positive count', () => {
    const wrapper = mount(StatsCard, {
      props: { stats: mockStats },
    });
    
    const cards = wrapper.findAll('.bg-gradient-to-br');
    expect(cards[1].text()).toContain('25');
    expect(cards[1].text()).toContain('Positive');
  });

  it('should display correct negative count', () => {
    const wrapper = mount(StatsCard, {
      props: { stats: mockStats },
    });
    
    const cards = wrapper.findAll('.bg-gradient-to-br');
    expect(cards[2].text()).toContain('10');
    expect(cards[2].text()).toContain('Negative');
  });

  it('should display correct neutral count', () => {
    const wrapper = mount(StatsCard, {
      props: { stats: mockStats },
    });
    
    const cards = wrapper.findAll('.bg-gradient-to-br');
    expect(cards[3].text()).toContain('7');
    expect(cards[3].text()).toContain('Neutral');
  });

  it('should handle zero values', () => {
    const zeroStats = {
      total: 0,
      positive: 0,
      negative: 0,
      neutral: 0,
    };
    
    const wrapper = mount(StatsCard, {
      props: { stats: zeroStats },
    });
    
    expect(wrapper.text()).toContain('0');
  });

  it('should render icons for each stat', () => {
    const wrapper = mount(StatsCard, {
      props: { stats: mockStats },
    });
    
    expect(wrapper.findAll('svg')).toHaveLength(4);
  });

  it('should use responsive grid layout', () => {
    const wrapper = mount(StatsCard, {
      props: { stats: mockStats },
    });
    
    const grid = wrapper.find('.grid');
    expect(grid.classes()).toContain('grid-cols-2');
    expect(grid.classes()).toContain('md:grid-cols-4');
  });
});
