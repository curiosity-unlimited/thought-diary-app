<script setup lang="ts">
import { useI18n, type SupportedLocale } from '../composables/useI18n'

const { t, currentLocale, setLocale } = useI18n()

const locales: { value: SupportedLocale; label: string }[] = [
  { value: 'en', label: 'English' },
  { value: 'zh-tw', label: '繁體中文' },
]
</script>

<template>
  <div class="language-switcher">
    <span class="language-label">{{ t.language }}:</span>
    <button
      v-for="locale in locales"
      :key="locale.value"
      :class="['lang-btn', { active: currentLocale === locale.value }]"
      @click="setLocale(locale.value)"
    >
      {{ locale.label }}
    </button>
  </div>
</template>

<style scoped>
.language-switcher {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.language-label {
  font-size: 0.875rem;
  opacity: 0.7;
}

.lang-btn {
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  border-radius: 1rem;
  border: 1px solid #646cff;
  background: transparent;
  color: inherit;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}

.lang-btn:hover,
.lang-btn.active {
  background-color: #646cff;
  color: #fff;
}

.lang-btn:focus,
.lang-btn:focus-visible {
  outline: 2px solid #646cff;
  outline-offset: 2px;
}
</style>
