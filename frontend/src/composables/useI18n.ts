import { ref, computed } from 'vue'
import en from '../locales/en'
import zhTw from '../locales/zh-tw'

export type SupportedLocale = 'en' | 'zh-tw'

const STORAGE_KEY = 'thought-diary-locale'

const messages: Record<SupportedLocale, typeof en> = {
  en,
  'zh-tw': zhTw,
}

const storedLocale = (() => {
  try {
    return localStorage.getItem(STORAGE_KEY) as SupportedLocale | null
  } catch {
    return null
  }
})()
const currentLocale = ref<SupportedLocale>(
  storedLocale && storedLocale in messages ? storedLocale : 'en',
)

export function useI18n() {
  const t = computed(() => messages[currentLocale.value])

  function setLocale(locale: SupportedLocale) {
    currentLocale.value = locale
    try {
      localStorage.setItem(STORAGE_KEY, locale)
    } catch {
      // localStorage unavailable (e.g. private browsing with strict settings)
    }
  }

  return { t, currentLocale, setLocale }
}
