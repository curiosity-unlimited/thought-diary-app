<script setup lang="ts">
// About page - Public route
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 py-16">
      <h1 class="text-4xl font-bold text-gray-900 mb-6">
        About Thought Diary App
      </h1>
      <div class="prose prose-lg">
        <p class="text-gray-600 mb-4">
          Thought Diary App is an AI-powered tool designed to help you track and
          analyze your thoughts and emotions.
        </p>
        <p class="text-gray-600 mb-4">
          By identifying patterns in your thinking, you can develop healthier
          mental habits and improve your overall well-being.
        </p>
        <h2 class="text-2xl font-semibold text-gray-900 mt-8 mb-4">Features</h2>
        <ul class="list-disc list-inside space-y-2 text-gray-600">
          <li>Track your daily thoughts and emotions</li>
          <li>AI-powered sentiment analysis</li>
          <li>Identify positive and negative thinking patterns</li>
          <li>View statistics and trends over time</li>
          <li>Secure and private data storage</li>
        </ul>
      </div>
      <div class="mt-12">
        <router-link
          to="/"
          class="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
        >
          ← Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>
