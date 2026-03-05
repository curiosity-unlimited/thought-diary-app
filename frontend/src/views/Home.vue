<script setup lang="ts">
// Home/Landing page - Public route
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
    <div class="max-w-4xl mx-auto px-4 py-16 text-center">
      <h1 class="text-5xl font-bold text-gray-900 dark:text-gray-100 mb-4">
        Welcome to Thought Diary App
      </h1>
      <p class="text-xl text-gray-600 dark:text-gray-400 mb-8">
        Track your thoughts, analyze your emotions, and build healthier mental
        habits.
      </p>
      <div class="space-x-4">
        <router-link
          to="/register"
          class="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
        >
          Get Started
        </router-link>
        <router-link
          to="/login"
          class="inline-block bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 dark:hover:bg-gray-600 transition"
        >
          Login
        </router-link>
      </div>
      <div class="mt-12">
        <router-link to="/about" class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300">
          Learn more about Thought Diary →
        </router-link>
      </div>
    </div>
  </div>
</template>
