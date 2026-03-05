import { createI18n } from 'vue-i18n'
import en from './locales/en'
import zhTw from './locales/zh-tw'

const LOCALE_KEY = 'thought-diary-locale'

const savedLocale = localStorage.getItem(LOCALE_KEY)
const defaultLocale = (savedLocale === 'zh-tw' || savedLocale === 'en') ? savedLocale : 'en'

const i18n = createI18n({
  legacy: false,
  locale: defaultLocale,
  fallbackLocale: 'en',
  messages: {
    en,
    'zh-tw': zhTw,
  },
})

export function setLocale(locale: 'en' | 'zh-tw') {
  ;(i18n.global.locale as import('vue').Ref<string>).value = locale
  localStorage.setItem(LOCALE_KEY, locale)
  document.documentElement.lang = locale
}

export function getLocale(): string {
  return (i18n.global.locale as import('vue').Ref<string>).value
}

// Apply stored locale to <html lang> on startup
document.documentElement.lang = defaultLocale

export default i18n
