/**
 * i18n Configuration
 * Sets up vue-i18n with English (en) and Traditional Chinese (zh-tw) support.
 * User locale preference is persisted in localStorage with key 'user_locale'.
 * Falls back to browser language detection, defaulting to English.
 */

import { createI18n } from 'vue-i18n';
import en from './locales/en.json';
import zhTw from './locales/zh-tw.json';

export const SUPPORTED_LOCALES = ['en', 'zh-tw'] as const;
export type SupportedLocale = (typeof SUPPORTED_LOCALES)[number];

export const LOCALE_STORAGE_KEY = 'user_locale';

/**
 * Detect the initial locale from localStorage or browser language.
 * Falls back to English if neither is available or supported.
 */
export const detectLocale = (): SupportedLocale => {
  const stored = localStorage.getItem(LOCALE_STORAGE_KEY);
  if (stored && SUPPORTED_LOCALES.includes(stored as SupportedLocale)) {
    return stored as SupportedLocale;
  }

  const browserLang = navigator.language.toLowerCase();
  if (browserLang.startsWith('zh')) {
    return 'zh-tw';
  }

  return 'en';
};

const i18n = createI18n({
  locale: detectLocale(),
  fallbackLocale: 'en',
  legacy: false,
  messages: {
    en,
    'zh-tw': zhTw,
  },
});

export default i18n;
