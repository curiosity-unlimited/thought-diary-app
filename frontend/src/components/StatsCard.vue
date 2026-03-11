<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
    <!-- Total Entries -->
    <article
      class="stat-card rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-5 shadow-sm"
      role="group"
      aria-label="Total entries"
    >
      <div class="flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100 shadow-inner"
            aria-hidden="true"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
              <path
                fill-rule="evenodd"
                d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
          <div>
            <p class="text-sm font-semibold text-slate-800 dark:text-slate-100">Total Entries</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">All diaries</p>
          </div>
        </div>
      </div>
      <div class="mt-3 text-3xl font-bold text-slate-900 dark:text-white" aria-live="polite">
        {{ total }}
      </div>
    </article>

    <!-- Positive Entries -->
    <article
      class="stat-card rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-5 shadow-sm"
      role="group"
      aria-label="Positive entries"
    >
      <div class="flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-100 shadow-inner"
            aria-hidden="true"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-.464 5.535a1 1 0 10-1.415-1.414 3 3 0 01-4.242 0 1 1 0 00-1.415 1.414 5 5 0 007.072 0z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
          <div>
            <p class="text-sm font-semibold text-slate-800 dark:text-slate-100">Positive Entries</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Encouraging moments</p>
          </div>
        </div>
      </div>
      <div class="mt-3 text-3xl font-bold text-slate-900 dark:text-white" aria-live="polite">
        {{ positive }}
      </div>
    </article>

    <!-- Negative Entries -->
    <article
      class="stat-card rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-5 shadow-sm"
      role="group"
      aria-label="Negative entries"
    >
      <div class="flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-rose-100 text-rose-800 dark:bg-rose-900 dark:text-rose-100 shadow-inner"
            aria-hidden="true"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-7.536 5.879a1 1 0 001.415 0 3 3 0 014.242 0 1 1 0 001.415-1.415 5 5 0 00-7.072 0 1 1 0 000 1.415z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
          <div>
            <p class="text-sm font-semibold text-slate-800 dark:text-slate-100">Negative Entries</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Challenging thoughts</p>
          </div>
        </div>
      </div>
      <div class="mt-3 text-3xl font-bold text-slate-900 dark:text-white" aria-live="polite">
        {{ negative }}
      </div>
    </article>

    <!-- Neutral Entries -->
    <article
      class="stat-card rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-5 shadow-sm"
      role="group"
      aria-label="Neutral entries"
    >
      <div class="flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-slate-200 text-slate-800 dark:bg-slate-800 dark:text-slate-100 shadow-inner"
            aria-hidden="true"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-3 6a1 1 0 011-1h.01a1 1 0 110 2H11a1 1 0 01-1-1z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
          <div>
            <p class="text-sm font-semibold text-slate-800 dark:text-slate-100">Neutral Entries</p>
            <p class="text-xs text-slate-600 dark:text-slate-400">Balanced reflections</p>
          </div>
        </div>
      </div>
      <div class="mt-3 text-3xl font-bold text-slate-900 dark:text-white" aria-live="polite">
        {{ neutral }}
      </div>
    </article>
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
