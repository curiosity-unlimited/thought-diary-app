<script setup lang="ts">
import MainLayout from '@/layouts/MainLayout.vue';

// Get app version from environment
const appVersion = import.meta.env.VITE_APP_VERSION || '0.1.0';
</script>

<template>
  <MainLayout>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Page Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          About Thought Diary App
        </h1>
        <p class="text-lg text-gray-600">
          An AI-powered journal for better mental health
        </p>
      </div>

      <!-- Description -->
      <div class="bg-white shadow rounded-lg p-8 mb-8">
        <div class="prose prose-lg max-w-none">
          <p class="text-gray-700 mb-4">
            Thought Diary App is an AI-powered tool designed to help you track
            and analyze your thoughts and emotions. Based on the principles of
            <a
              href="https://positivepsychology.com/thought-diary/"
              target="_blank"
              rel="noopener noreferrer"
              class="text-indigo-600 hover:text-indigo-800"
            >
              Thought Diaries
            </a>
            , our application helps you identify and challenge negative thinking
            patterns, promoting healthier mental habits.
          </p>
          <p class="text-gray-700 mb-4">
            By analyzing your diary entries with advanced sentiment analysis, you
            can gain insights into your emotional patterns and work towards
            improved well-being.
          </p>
        </div>
      </div>

      <!-- Features -->
      <div class="bg-white shadow rounded-lg p-8 mb-8">
        <h2 class="text-2xl font-semibold text-gray-900 mb-6">Key Features</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Feature 1 -->
          <div class="flex items-start">
            <div
              class="flex-shrink-0 h-10 w-10 rounded-lg bg-indigo-100 flex items-center justify-center"
            >
              <svg
                class="h-6 w-6 text-indigo-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">
                Diary Management
              </h3>
              <p class="mt-1 text-gray-600">
                Create, edit, and organize your thought diary entries with ease.
              </p>
            </div>
          </div>

          <!-- Feature 2 -->
          <div class="flex items-start">
            <div
              class="flex-shrink-0 h-10 w-10 rounded-lg bg-green-100 flex items-center justify-center"
            >
              <svg
                class="h-6 w-6 text-green-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">
                AI Sentiment Analysis
              </h3>
              <p class="mt-1 text-gray-600">
                Automatic analysis identifies positive and negative thinking
                patterns.
              </p>
            </div>
          </div>

          <!-- Feature 3 -->
          <div class="flex items-start">
            <div
              class="flex-shrink-0 h-10 w-10 rounded-lg bg-blue-100 flex items-center justify-center"
            >
              <svg
                class="h-6 w-6 text-blue-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">
                Statistics Dashboard
              </h3>
              <p class="mt-1 text-gray-600">
                View insights and trends about your emotional patterns over time.
              </p>
            </div>
          </div>

          <!-- Feature 4 -->
          <div class="flex items-start">
            <div
              class="flex-shrink-0 h-10 w-10 rounded-lg bg-purple-100 flex items-center justify-center"
            >
              <svg
                class="h-6 w-6 text-purple-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-medium text-gray-900">
                Secure & Private
              </h3>
              <p class="mt-1 text-gray-600">
                Your data is encrypted and protected with industry-standard
                security.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Credits & Version -->
      <div class="bg-white shadow rounded-lg p-8">
        <h2 class="text-2xl font-semibold text-gray-900 mb-4">
          Credits & Acknowledgments
        </h2>
        <p class="text-gray-700 mb-4">
          Built with Vue 3, TypeScript, and Flask. Sentiment analysis powered by
          GitHub Models API.
        </p>
        <div class="flex items-center text-sm text-gray-600">
          <svg
            class="h-5 w-5 mr-2 text-gray-400"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          Version {{ appVersion }}
        </div>
      </div>
    </div>
  </MainLayout>
</template>
