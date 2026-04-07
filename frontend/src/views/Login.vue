<script setup lang="ts">
/**
 * Login View
 * Guest-only authentication page with VeeValidate form validation
 */

import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useForm, useField } from 'vee-validate';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/stores/auth';
import { useToast } from '@/composables/useToast';
import AuthLayout from '@/layouts/AuthLayout.vue';
import { createLoginSchema } from '@/utils/validationSchemas';

const router = useRouter();
const authStore = useAuthStore();
const { showError } = useToast();
const { t } = useI18n();

// Form state
const isSubmitting = ref(false);

// Setup VeeValidate form with i18n-aware Yup schema
const validationSchema = computed(() => createLoginSchema(t));
const { handleSubmit, errors } = useForm({
  validationSchema,
});

// Setup form fields with real-time validation
const { value: email } = useField<string>('email');
const { value: password } = useField<string>('password');

/**
 * Handle form submission
 */
const onSubmit = handleSubmit(async (values) => {
  isSubmitting.value = true;

  try {
    await authStore.login(values.email, values.password);

    // Redirect to intended route or dashboard
    const redirect = router.currentRoute.value.query.redirect as string;
    router.push(redirect || '/dashboard');
  } catch (error) {
    // Show error toast for API errors
    const errorMessage =
      error instanceof Error
        ? error.message
        : t('auth.loginFailed');
    showError(errorMessage);
  } finally {
    isSubmitting.value = false;
  }
});
</script>

<template>
  <AuthLayout>
    <!-- Page Title -->
    <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 text-center mb-6">
      {{ $t('auth.signInTitle') }}
    </h2>

    <!-- Login Form -->
    <form class="space-y-6" @submit="onSubmit">
      <!-- Email Field -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {{ $t('auth.emailLabel') }}
        </label>
        <input
          id="email"
          v-model="email"
          type="email"
          autocomplete="email"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 dark:placeholder-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
          :class="{
            'border-red-500 focus:ring-red-500 focus:border-red-500':
              errors.email,
          }"
          :placeholder="$t('auth.emailPlaceholder')"
        />
        <!-- Inline Error Message -->
        <p v-if="errors.email" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ errors.email }}
        </p>
      </div>

      <!-- Password Field -->
      <div>
        <label
          for="password"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
        >
          {{ $t('auth.passwordLabel') }}
        </label>
        <input
          id="password"
          v-model="password"
          type="password"
          autocomplete="current-password"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 dark:placeholder-gray-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
          :class="{
            'border-red-500 focus:ring-red-500 focus:border-red-500':
              errors.password,
          }"
          :placeholder="$t('auth.passwordPlaceholder')"
        />
        <!-- Inline Error Message -->
        <p v-if="errors.password" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ errors.password }}
        </p>
      </div>

      <!-- Submit Button -->
      <div>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <!-- Loading Spinner -->
          <svg
            v-if="isSubmitting"
            class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          <span v-if="isSubmitting">{{ $t('auth.signingIn') }}</span>
          <span v-else>{{ $t('auth.signIn') }}</span>
        </button>
      </div>
    </form>

    <!-- Link to Register -->
    <div class="mt-6 text-center">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        {{ $t('auth.dontHaveAccount') }}
        <router-link
          to="/register"
          class="font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 dark:hover:text-indigo-300 transition-colors"
        >
          {{ $t('auth.signUp') }}
        </router-link>
      </p>
    </div>
  </AuthLayout>
</template>
