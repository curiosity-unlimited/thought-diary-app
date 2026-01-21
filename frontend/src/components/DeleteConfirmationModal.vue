<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" class="relative z-50" @close="$emit('cancel')">
      <!-- Overlay -->
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-25" />
      </TransitionChild>

      <!-- Modal Container -->
      <div class="fixed inset-0 overflow-y-auto">
        <div
          class="flex min-h-full items-center justify-center p-4 text-center"
        >
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
            >
              <!-- Icon -->
              <div
                class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100 mb-4"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-red-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>

              <!-- Title -->
              <DialogTitle
                as="h3"
                class="text-lg font-semibold leading-6 text-gray-900 text-center mb-2"
              >
                Delete Diary Entry?
              </DialogTitle>

              <!-- Description -->
              <DialogDescription class="text-sm text-gray-500 text-center mb-4">
                This action cannot be undone. This will permanently delete your
                diary entry.
              </DialogDescription>

              <!-- Diary Preview -->
              <div
                v-if="diaryPreview"
                class="bg-gray-50 rounded-lg p-4 mb-6 border border-gray-200"
              >
                <p class="text-sm text-gray-700 italic line-clamp-3">
                  "{{ diaryPreview }}"
                </p>
              </div>

              <!-- Action Buttons -->
              <div class="flex gap-3 justify-end">
                <button
                  type="button"
                  class="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-gray-300"
                  @click="$emit('cancel')"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  class="px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                  @click="$emit('confirm', diaryId)"
                >
                  Delete
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
  DialogDescription,
} from '@headlessui/vue';

interface Props {
  isOpen: boolean;
  diaryId: number;
  diaryPreview?: string;
}

defineProps<Props>();

defineEmits<{
  confirm: [id: number];
  cancel: [];
}>();
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
