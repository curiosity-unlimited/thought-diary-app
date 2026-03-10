<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <!-- Total Entries -->
    <div
      class="stat-card rounded-lg border border-blue-200 dark:border-blue-700 bg-white dark:bg-slate-900 p-5 shadow-sm hover:shadow-md transition-shadow"
      :aria-label="`Total entries: ${total}`"
    >
      <div class="flex items-start justify-between gap-3">
        <div class="flex items-center gap-3">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-blue-50 dark:bg-blue-900/50 text-blue-900 dark:text-blue-100 ring-1 ring-blue-200 dark:ring-blue-500/60"
            aria-hidden="true"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
              <path
                fill-rule="evenodd"
                d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
          <span class="text-sm font-semibold text-gray-900 dark:text-gray-100">Total Entries</span>
        </div>
        <div class="text-3xl font-bold text-gray-900 dark:text-gray-100 leading-none">{{ total }}</div>
      </div>
      <p class="text-sm text-gray-700 dark:text-gray-300 mt-2">All diary entries recorded.</p>
    </div>

    <!-- Positive Entries -->
    <div
      class="stat-card rounded-lg border border-emerald-200 dark:border-emerald-700 bg-white dark:bg-slate-900 p-5 shadow-sm hover:shadow-md transition-shadow"
      :aria-label="`Positive entries: ${positive}`"
    >
      <div class="flex items-start justify-between gap-3">
        <div class="flex items-center gap-3">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-emerald-50 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-100 ring-1 ring-emerald-200 dark:ring-emerald-500/60"
            aria-hidden="true"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-.464 5.535a1 1 0 10-1.415-1.414 3 3 0 01-4.242 0 1 1 0 00-1.415 1.414 5 5 0 007.072 0z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
          <span class="text-sm font-semibold text-gray-900 dark:text-gray-100">Positive Entries</span>
        </div>
        <div class="text-3xl font-bold text-gray-900 dark:text-gray-100 leading-none">{{ positive }}</div>
      </div>
      <p class="text-sm text-gray-700 dark:text-gray-300 mt-2">Entries with more positive than negative markers.</p>
    </div>

    <!-- Negative Entries -->
    <div
      class="stat-card rounded-lg border border-rose-200 dark:border-rose-700 bg-white dark:bg-slate-900 p-5 shadow-sm hover:shadow-md transition-shadow"
      :aria-label="`Negative entries: ${negative}`"
    >
      <div class="flex items-start justify-between gap-3">
        <div class="flex items-center gap-3">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-rose-50 dark:bg-rose-900/60 text-rose-800 dark:text-rose-100 ring-1 ring-rose-200 dark:ring-rose-500/60"
            aria-hidden="true"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-7.536 5.879a1 1 0 001.415 0 3 3 0 014.242 0 1 1 0 001.415-1.415 5 5 0 00-7.072 0 1 1 0 000 1.415z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
          <span class="text-sm font-semibold text-gray-900 dark:text-gray-100">Negative Entries</span>
        </div>
        <div class="text-3xl font-bold text-gray-900 dark:text-gray-100 leading-none">{{ negative }}</div>
      </div>
      <p class="text-sm text-gray-700 dark:text-gray-300 mt-2">Entries with more negative than positive markers.</p>
    </div>

    <!-- Neutral Entries -->
    <div
      class="stat-card rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-5 shadow-sm hover:shadow-md transition-shadow"
      :aria-label="`Neutral entries: ${neutral}`"
    >
      <div class="flex items-start justify-between gap-3">
        <div class="flex items-center gap-3">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 ring-1 ring-slate-200 dark:ring-slate-500/70"
            aria-hidden="true"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-3 6a1 1 0 011-1h.01a1 1 0 110 2H11a1 1 0 01-1-1z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
          <span class="text-sm font-semibold text-gray-900 dark:text-gray-100">Neutral Entries</span>
        </div>
        <div class="text-3xl font-bold text-gray-900 dark:text-gray-100 leading-none">{{ neutral }}</div>
      </div>
      <p class="text-sm text-gray-700 dark:text-gray-300 mt-2">Entries balanced between positive and negative markers.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DiaryStats } from '@/types';

interface Props {
  stats: DiaryStats;
}

const props = defineProps<Props>();

// Provide safe access to stats with defaults
const total = props.stats?.total_entries ?? 0;
const positive = props.stats?.positive_entries ?? 0;
const negative = props.stats?.negative_entries ?? 0;
const neutral = props.stats?.neutral_entries ?? 0;
</script>
