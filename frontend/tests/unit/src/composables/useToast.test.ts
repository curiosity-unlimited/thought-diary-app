import { describe, it, expect } from 'vitest';
import { useToast } from '@/composables/useToast';

describe('useToast Composable', () => {
  it('should have showSuccess function', () => {
    const toast = useToast();
    
    expect(toast.showSuccess).toBeDefined();
    expect(typeof toast.showSuccess).toBe('function');
  });

  it('should have showError function', () => {
    const toast = useToast();
    
    expect(toast.showError).toBeDefined();
    expect(typeof toast.showError).toBe('function');
  });

  it('should have showInfo function', () => {
    const toast = useToast();
    
    expect(toast.showInfo).toBeDefined();
    expect(typeof toast.showInfo).toBe('function');
  });

  it('should have showWarning function', () => {
    const toast = useToast();
    
    expect(toast.showWarning).toBeDefined();
    expect(typeof toast.showWarning).toBe('function');
  });

  it('should have showErrorWithRetry function', () => {
    const toast = useToast();
    
    expect(toast.showErrorWithRetry).toBeDefined();
    expect(typeof toast.showErrorWithRetry).toBe('function');
  });

  it('should call showSuccess without errors', () => {
    const toast = useToast();
    
    expect(() => {
      toast.showSuccess('Success message');
    }).not.toThrow();
  });

  it('should call showError without errors', () => {
    const toast = useToast();
    
    expect(() => {
      toast.showError('Error message');
    }).not.toThrow();
  });

  it('should call showInfo without errors', () => {
    const toast = useToast();
    
    expect(() => {
      toast.showInfo('Info message');
    }).not.toThrow();
  });

  it('should call showWarning without errors', () => {
    const toast = useToast();
    
    expect(() => {
      toast.showWarning('Warning message');
    }).not.toThrow();
  });

  it('should call showErrorWithRetry with callback', () => {
    const toast = useToast();
    const mockCallback = () => console.log('Retry');
    
    expect(() => {
      toast.showErrorWithRetry('Error message', mockCallback);
    }).not.toThrow();
  });
});
