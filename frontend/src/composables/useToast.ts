/**
 * Toast notification composable
 * Provides wrapper functions for vue-toastification with consistent styling
 */
import { useToast as useToastification } from 'vue-toastification';
import { h } from 'vue';

/**
 * Composable for displaying toast notifications
 * @returns Object with toast notification functions
 */
export function useToast() {
  const toast = useToastification();

  /**
   * Show a success toast notification
   * @param message - Success message to display
   */
  const showSuccess = (message: string): void => {
    toast.success(message, {
      timeout: 3000,
    });
  };

  /**
   * Show an error toast notification
   * @param message - Error message to display
   */
  const showError = (message: string): void => {
    toast.error(message, {
      timeout: 5000,
    });
  };

  /**
   * Show an info toast notification
   * @param message - Info message to display
   */
  const showInfo = (message: string): void => {
    toast.info(message, {
      timeout: 3000,
    });
  };

  /**
   * Show a warning toast notification
   * @param message - Warning message to display
   */
  const showWarning = (message: string): void => {
    toast.warning(message, {
      timeout: 4000,
    });
  };

  /**
   * Show an error toast with retry button
   * @param message - Error message to display
   * @param onRetry - Callback function to execute when retry button is clicked
   */
  const showErrorWithRetry = (message: string, onRetry: () => void): void => {
    toast.error(
      h(
        'div',
        {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '0.5rem',
          },
        },
        [
          h('p', { style: { margin: 0 } }, message),
          h(
            'button',
            {
              onClick: () => {
                toast.clear();
                onRetry();
              },
              style: {
                marginTop: '0.5rem',
                padding: '0.375rem 0.75rem',
                backgroundColor: '#fff',
                color: '#dc2626',
                border: '1px solid #dc2626',
                borderRadius: '0.375rem',
                cursor: 'pointer',
                fontWeight: '500',
                fontSize: '0.875rem',
              },
            },
            'Retry'
          ),
        ]
      ),
      {
        timeout: 0, // Don't auto-dismiss
        closeOnClick: false,
      }
    );
  };

  return {
    showSuccess,
    showError,
    showInfo,
    showWarning,
    showErrorWithRetry,
  };
}
