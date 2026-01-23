import { createApp } from 'vue';
import { createPinia } from 'pinia';
import Toast, { POSITION, type PluginOptions } from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import './style.css';
import App from './App.vue';
import router from './router';
import { useAuthStore } from './stores/auth';

const app = createApp(App);
const pinia = createPinia();

// Toast configuration
const toastOptions: PluginOptions = {
  position: POSITION.TOP_RIGHT,
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
};

// Register plugins
app.use(pinia);
app.use(router);
app.use(Toast, toastOptions);

// Initialize auth store and fetch user profile if tokens exist
const authStore = useAuthStore();
if (authStore.isAuthenticated) {
  // Try to fetch user profile - if it fails, tokens are invalid
  authStore.fetchProfile().catch(() => {
    // Tokens are invalid, clear them silently
    // The router guard will redirect to login on next navigation
    authStore.logout().catch(() => {
      // Ignore logout errors
    });
  });
}

app.mount('#app');
