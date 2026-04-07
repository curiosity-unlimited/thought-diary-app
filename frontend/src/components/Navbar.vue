<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue';
import { useAuthStore } from '@/stores/auth';
import { useUIStore } from '@/stores/ui';
import type { SupportedLocale } from '@/i18n';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const uiStore = useUIStore();
const { t, locale } = useI18n();

// Get user email from auth store
const userEmail = computed(() => authStore.user?.email || 'User');

// Navigation links (reactive to locale changes)
const navLinks = computed(() => [
  { name: t('nav.dashboard'), path: '/dashboard' },
  { name: t('nav.diaries'), path: '/diaries' },
  { name: t('nav.profile'), path: '/profile' },
  { name: t('nav.about'), path: '/about' },
]);

// Check if route is active
const isActiveRoute = (path: string) => {
  return route.path === path || route.path.startsWith(path + '/');
};

// Handle logout
const handleLogout = async () => {
  try {
    await authStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout error:', error);
  }
};

// Mobile menu state
import { ref } from 'vue';
const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

// Language switcher
const availableLocales: { code: SupportedLocale; label: string }[] = [
  { code: 'en', label: 'English' },
  { code: 'zh-tw', label: '繁體中文' },
];

const currentLocaleLabel = computed(() => {
  return availableLocales.find((l) => l.code === locale.value)?.label ?? 'EN';
});

const switchLocale = (newLocale: SupportedLocale) => {
  locale.value = newLocale;
  uiStore.setLocale(newLocale);
};
</script>

<template>
  <nav
    class="bg-indigo-600 dark:bg-gray-900 shadow-lg"
    role="navigation"
    :aria-label="$t('nav.mainNavAriaLabel')"
  >
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between">
        <!-- Logo and App Name -->
        <div class="flex items-center">
          <router-link
            to="/dashboard"
            class="flex items-center text-white hover:text-indigo-100 dark:hover:text-gray-300 transition-colors"
            :aria-label="$t('nav.goDashboardAriaLabel')"
          >
            <svg
              class="h-8 w-8 mr-2"
              fill="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                d="M11.25 4.533A9.707 9.707 0 006 3a9.735 9.735 0 00-3.25.555.75.75 0 00-.5.707v14.25a.75.75 0 001 .707A8.237 8.237 0 016 18.75c1.995 0 3.823.707 5.25 1.886V4.533zM12.75 20.636A8.214 8.214 0 0118 18.75c.966 0 1.89.166 2.75.47a.75.75 0 001-.708V4.262a.75.75 0 00-.5-.707A9.735 9.735 0 0018 3a9.707 9.707 0 00-5.25 1.533v16.103z"
              />
            </svg>
            <span class="text-xl font-bold">Thought Diary</span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex md:items-center md:space-x-4">
          <!-- Navigation Links -->
          <div class="flex space-x-1">
            <router-link
              v-for="link in navLinks"
              :key="link.path"
              :to="link.path"
              :class="[
                'px-3 py-2 rounded-md text-sm font-medium transition-colors',
                isActiveRoute(link.path)
                  ? 'bg-indigo-700 dark:bg-gray-700 text-white'
                  : 'text-indigo-100 hover:bg-indigo-500 dark:hover:bg-gray-700 hover:text-white',
              ]"
              :aria-current="isActiveRoute(link.path) ? 'page' : undefined"
            >
              {{ link.name }}
            </router-link>
          </div>

          <!-- Language Switcher -->
          <Menu as="div" class="relative">
            <MenuButton
              class="flex items-center gap-1 p-2 rounded-md text-indigo-100 hover:bg-indigo-500 dark:hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white transition-colors text-sm font-medium"
              :aria-label="$t('nav.languageSwitcher')"
            >
              <svg
                class="h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"
                />
              </svg>
              <span>{{ currentLocaleLabel }}</span>
            </MenuButton>
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <MenuItems
                class="absolute right-0 z-10 mt-2 w-40 origin-top-right rounded-md bg-white dark:bg-gray-800 py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
              >
                <MenuItem v-for="loc in availableLocales" :key="loc.code" v-slot="{ active }">
                  <button
                    :class="[
                      active ? 'bg-gray-100 dark:bg-gray-700' : '',
                      locale === loc.code ? 'font-semibold' : '',
                      'block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-200',
                    ]"
                    @click="switchLocale(loc.code)"
                  >
                    {{ loc.label }}
                  </button>
                </MenuItem>
              </MenuItems>
            </transition>
          </Menu>

          <!-- Theme Toggle Button -->
          <button
            type="button"
            class="p-2 rounded-md text-indigo-100 hover:bg-indigo-500 dark:hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white transition-colors"
            :aria-label="uiStore.isDark ? $t('nav.switchToLight') : $t('nav.switchToDark')"
            @click="uiStore.toggleTheme()"
          >
            <!-- Moon icon (shown in light mode) -->
            <svg
              v-if="!uiStore.isDark"
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
              />
            </svg>
            <!-- Sun icon (shown in dark mode) -->
            <svg
              v-else
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
          </button>

          <!-- User Menu -->
          <Menu as="div" class="relative ml-3">
            <MenuButton
              class="flex items-center rounded-full bg-indigo-700 dark:bg-gray-700 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-800 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-600 dark:focus:ring-offset-gray-900"
              :aria-label="$t('nav.userMenuAriaLabel')"
            >
              <svg
                class="h-5 w-5 mr-2"
                fill="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"
                  clip-rule="evenodd"
                />
              </svg>
              <span class="truncate max-w-[150px]">{{ userEmail }}</span>
              <svg
                class="ml-2 h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </MenuButton>
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <MenuItems
                class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white dark:bg-gray-800 py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
              >
                <MenuItem v-slot="{ active }">
                  <button
                    :class="[
                      active ? 'bg-gray-100 dark:bg-gray-700' : '',
                      'block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-200',
                    ]"
                    @click="handleLogout"
                  >
                    <svg
                      class="inline-block h-4 w-4 mr-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                      aria-hidden="true"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                      />
                    </svg>
                    {{ $t('nav.logout') }}
                  </button>
                </MenuItem>
              </MenuItems>
            </transition>
          </Menu>
        </div>

        <!-- Mobile menu button -->
        <div class="flex items-center md:hidden">
          <!-- Theme Toggle Button (Mobile) -->
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-md p-2 text-indigo-100 hover:bg-indigo-500 dark:hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white mr-1"
            :aria-label="uiStore.isDark ? $t('nav.switchToLight') : $t('nav.switchToDark')"
            @click="uiStore.toggleTheme()"
          >
            <svg
              v-if="!uiStore.isDark"
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
              />
            </svg>
            <svg
              v-else
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
          </button>
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-md p-2 text-indigo-100 hover:bg-indigo-500 dark:hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            aria-controls="mobile-menu"
            :aria-expanded="isMobileMenuOpen"
            @click="toggleMobileMenu"
          >
            <span class="sr-only">{{ $t('nav.openMainMenuAriaLabel') }}</span>
            <svg
              v-if="!isMobileMenuOpen"
              class="block h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            <svg
              v-else
              class="block h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="isMobileMenuOpen" id="mobile-menu" class="md:hidden">
      <div class="space-y-1 px-2 pb-3 pt-2">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          :class="[
            'block rounded-md px-3 py-2 text-base font-medium',
            isActiveRoute(link.path)
              ? 'bg-indigo-700 dark:bg-gray-700 text-white'
              : 'text-indigo-100 hover:bg-indigo-500 dark:hover:bg-gray-700 hover:text-white',
          ]"
          :aria-current="isActiveRoute(link.path) ? 'page' : undefined"
          @click="isMobileMenuOpen = false"
        >
          {{ link.name }}
        </router-link>
      </div>
      <div class="border-t border-indigo-700 dark:border-gray-700 pb-3 pt-4">
        <div class="flex items-center px-5">
          <div class="flex-shrink-0">
            <svg
              class="h-10 w-10 text-indigo-100"
              fill="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
            >
              <path
                fill-rule="evenodd"
                d="M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div class="ml-3">
            <div class="text-base font-medium text-white">{{ userEmail }}</div>
          </div>
        </div>
        <!-- Language Switcher (Mobile) -->
        <div class="mt-3 space-y-1 px-2">
          <div class="px-3 py-2 text-xs font-medium text-indigo-300 dark:text-gray-400 uppercase tracking-wider">
            {{ $t('language.switchLanguage') }}
          </div>
          <button
            v-for="loc in availableLocales"
            :key="loc.code"
            :class="[
              'block w-full text-left rounded-md px-3 py-2 text-base font-medium transition-colors',
              locale === loc.code
                ? 'bg-indigo-700 dark:bg-gray-700 text-white'
                : 'text-indigo-100 hover:bg-indigo-500 dark:hover:bg-gray-700 hover:text-white',
            ]"
            @click="switchLocale(loc.code); isMobileMenuOpen = false"
          >
            {{ loc.label }}
          </button>
        </div>
        <div class="mt-3 space-y-1 px-2">
          <button
            class="block w-full text-left rounded-md px-3 py-2 text-base font-medium text-indigo-100 hover:bg-indigo-500 dark:hover:bg-gray-700 hover:text-white"
            @click="handleLogout"
          >
            {{ $t('nav.logout') }}
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* Additional styles if needed */
</style>
