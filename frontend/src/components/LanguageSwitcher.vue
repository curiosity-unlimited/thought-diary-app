<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { setLocale, getLocale } from '../i18n'

const { t } = useI18n()

const currentLocale = computed(() => getLocale())

function switchLocale(locale: 'en' | 'zh-tw') {
  setLocale(locale)
}
</script>

<template>
  <div class="language-switcher" :aria-label="t('language.label')">
    <button
      type="button"
      :class="{ active: currentLocale === 'en' }"
      @click="switchLocale('en')"
    >
      {{ t('language.en') }}
    </button>
    <button
      type="button"
      :class="{ active: currentLocale === 'zh-tw' }"
      @click="switchLocale('zh-tw')"
    >
      {{ t('language.zhTw') }}
    </button>
  </div>
</template>

<style scoped>
.language-switcher {
  display: inline-flex;
  gap: 0.4em;
}
.language-switcher button {
  padding: 0.3em 0.8em;
  font-size: 0.85em;
  border-radius: 4px;
  border: 1px solid #646cff;
  background: transparent;
  color: inherit;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}
.language-switcher button.active,
.language-switcher button:hover {
  background-color: #646cff;
  color: #fff;
}
</style>
