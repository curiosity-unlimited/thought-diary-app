<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import HelloWorld from './components/HelloWorld.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

const { t } = useI18n()
</script>

<template>
  <header class="app-header">
    <h2 class="app-title">{{ t('app.title') }}</h2>
    <LanguageSwitcher />
  </header>
  <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld :msg="t('diary.greeting')" />
</template>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 1em;
}
.app-title {
  margin: 0;
  font-size: 1.4em;
}
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
