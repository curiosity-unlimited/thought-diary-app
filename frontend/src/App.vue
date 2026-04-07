<script setup lang="ts">
import { useI18n } from './composables/useI18n'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
import ThoughtDiary from './components/ThoughtDiary.vue'

const { t } = useI18n()
</script>

<template>
  <header class="app-header">
    <h1 class="app-title">{{ t.appTitle }}</h1>
    <LanguageSwitcher />
  </header>
  <main>
    <ThoughtDiary />
  </main>
</template>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 2rem;
}

.app-title {
  font-size: 1.75rem;
  margin: 0;
}

@media (prefers-color-scheme: light) {
  .app-header {
    border-bottom-color: rgba(0, 0, 0, 0.1);
  }
}
</style>
