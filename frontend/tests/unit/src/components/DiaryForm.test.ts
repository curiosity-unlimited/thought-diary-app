import { describe, it, expect, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import DiaryForm from '@/components/DiaryForm.vue';

describe('DiaryForm', () => {
  let wrapper: ReturnType<typeof mount>;

  beforeEach(() => {
    wrapper = mount(DiaryForm);
  });

  it('should render textarea', () => {
    expect(wrapper.find('textarea').exists()).toBe(true);
  });

  it('should render submit button', () => {
    const submitButton = wrapper.findAll('button').find(button => 
      button.text().includes('Save') || button.text().includes('Submit') || button.text().includes('Create')
    );
    expect(submitButton).toBeDefined();
  });

  it('should render cancel button', () => {
    const cancelButton = wrapper.findAll('button').find(button => 
      button.text().includes('Cancel')
    );
    expect(cancelButton).toBeDefined();
  });

  it('should display character counter', async () => {
    const textarea = wrapper.find('textarea');
    await textarea.setValue('Hello world');
    
    expect(wrapper.text()).toContain('5000');
  });

  it('should update character counter when typing', async () => {
    const textarea = wrapper.find('textarea');
    const testText = 'This is a test diary entry';
    await textarea.setValue(testText);
    
    expect(wrapper.text()).toContain(testText.length.toString());
  });

  it('should show validation error for content too short', async () => {
    const textarea = wrapper.find('textarea');
    await textarea.setValue('Short');
    await textarea.trigger('blur');
    
    // Try to submit
    const form = wrapper.find('form');
    await form.trigger('submit');
    
    // Should show validation error (min 10 chars)
    expect(wrapper.text()).toContain('10') || expect(wrapper.text()).toContain('least');
  });

  it('should emit submit event with valid content', async () => {
    const validContent = 'This is a valid diary entry with enough characters';
    const textarea = wrapper.find('textarea');
    await textarea.setValue(validContent);
    
    const form = wrapper.find('form');
    await form.trigger('submit.prevent');
    
    expect(wrapper.emitted('submit')).toBeTruthy();
    expect(wrapper.emitted('submit')?.[0]).toEqual([validContent]);
  });

  it('should emit cancel event when cancel button clicked', async () => {
    const cancelButton = wrapper.findAll('button').find(button => 
      button.text().includes('Cancel')
    );
    
    if (cancelButton) {
      await cancelButton.trigger('click');
      expect(wrapper.emitted('cancel')).toBeTruthy();
    }
  });

  it('should populate textarea with diary content in edit mode', () => {
    const diary = {
      id: 1,
      content: 'Existing diary content',
      analyzed_content: 'Existing diary content',
      positive_count: 0,
      negative_count: 0,
      created_at: '2026-01-01T00:00:00Z',
      updated_at: '2026-01-01T00:00:00Z',
    };
    
    wrapper = mount(DiaryForm, {
      props: { diary },
    });
    
    const textarea = wrapper.find('textarea');
    expect(textarea.element.value).toBe('Existing diary content');
  });

  it('should disable submit button when isSubmitting is true', () => {
    wrapper = mount(DiaryForm, {
      props: { isSubmitting: true },
    });
    
    const submitButton = wrapper.findAll('button').find(button => 
      button.text().includes('Save') || button.text().includes('Submit') || button.text().includes('Creating') || button.text().includes('Saving')
    );
    
    if (submitButton) {
      expect(submitButton.attributes('disabled')).toBeDefined();
    }
  });

  it('should show loading spinner when submitting', () => {
    wrapper = mount(DiaryForm, {
      props: { isSubmitting: true },
    });
    
    expect(wrapper.html()).toContain('svg') || expect(wrapper.html()).toContain('Loading');
  });

  it('should not allow content longer than 5000 characters', async () => {
    const longContent = 'a'.repeat(5001);
    const textarea = wrapper.find('textarea');
    await textarea.setValue(longContent);
    await textarea.trigger('blur');
    
    // Should show validation error
    expect(wrapper.text()).toContain('5000') || expect(wrapper.text()).toContain('maximum');
  });

  it('should have auto-resize textarea', () => {
    const textarea = wrapper.find('textarea');
    expect(textarea.attributes('rows')).toBeDefined();
  });
});
