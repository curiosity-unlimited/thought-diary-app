# Frontend Components

This document provides a comprehensive reference for all reusable UI components in the Thought Diary App frontend.

## Table of Contents
- [Overview](#overview)
- [Component Guidelines](#component-guidelines)
- [Layout Components](#layout-components)
- [UI Components](#ui-components)
- [Form Components](#form-components)
- [Feedback Components](#feedback-components)
- [Navigation Components](#navigation-components)
- [Modal Components](#modal-components)
- [Component Patterns](#component-patterns)
- [Creating New Components](#creating-new-components)

## Overview

All components follow Vue 3 Composition API patterns with TypeScript. Components are designed to be:

- **Reusable**: Work in multiple contexts
- **Type-Safe**: Fully typed props and events
- **Accessible**: WCAG 2.1 AA compliant
- **Responsive**: Mobile-first design
- **Testable**: Easy to test in isolation

**Component Location:** `src/components/`  
**Test Location:** `tests/unit/src/components/`

## Component Guidelines

### Component Structure

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';

// Props definition with types
interface Props {
  title: string;
  description?: string;
  count?: number;
}

const props = withDefaults(defineProps<Props>(), {
  description: '',
  count: 0,
});

// Events definition with types
const emit = defineEmits<{
  click: [];
  update: [value: number];
}>();

// Component state
const isActive = ref(false);

// Computed properties
const displayText = computed(() => `${props.title}: ${props.count}`);

// Methods
const handleClick = () => {
  emit('click');
};
</script>

<template>
  <div class="component-wrapper">
    <h2>{{ displayText }}</h2>
    <p v-if="description">{{ description }}</p>
    <button @click="handleClick">Click Me</button>
  </div>
</template>

<style scoped>
/* Component-specific styles */
.component-wrapper {
  /* Styles here */
}
</style>
```

### Naming Conventions

- **PascalCase**: Component files and names (`DiaryCard.vue`)
- **kebab-case**: Custom events (`@update-diary`)
- **camelCase**: Props and methods (`userName`, `handleSubmit`)

### Prop Validation

```typescript
interface Props {
  // Required props
  id: number;
  title: string;

  // Optional with default
  description?: string;
  count?: number;

  // Union types
  size?: 'sm' | 'md' | 'lg';

  // Complex types
  user?: {
    id: number;
    name: string;
  };
}

const props = withDefaults(defineProps<Props>(), {
  description: '',
  count: 0,
  size: 'md',
});
```

## Layout Components

### MainLayout

**Purpose:** Standard layout for authenticated pages with navbar and footer.

**Location:** `src/layouts/MainLayout.vue`

**Usage:**
```vue
<template>
  <MainLayout>
    <h1>Page Content</h1>
  </MainLayout>
</template>
```

**Features:**
- Navbar with navigation links
- Responsive container
- Optional footer with copyright
- Slot for page content

**Structure:**
```vue
<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />
    <main class="container mx-auto px-4 py-8">
      <slot />
    </main>
    <footer class="border-t border-gray-200 py-4 text-center text-gray-600">
      © 2026 Thought Diary
    </footer>
  </div>
</template>
```

### AuthLayout

**Purpose:** Layout for authentication pages (login, register) with centered card.

**Location:** `src/layouts/AuthLayout.vue`

**Usage:**
```vue
<template>
  <AuthLayout>
    <h1>Login</h1>
    <LoginForm />
  </AuthLayout>
</template>
```

**Features:**
- Centered card design
- Gradient background
- Logo and app name at top
- Responsive for all screen sizes

**Structure:**
```vue
<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
      <div class="text-center mb-6">
        <h1 class="text-2xl font-bold">Thought Diary</h1>
      </div>
      <slot />
    </div>
  </div>
</template>
```

## UI Components

### LoadingSpinner

**Purpose:** Display loading indicator with optional message.

**Location:** `src/components/LoadingSpinner.vue`

**Props:**
```typescript
interface Props {
  size?: 'sm' | 'md' | 'lg';  // Spinner size
  message?: string;            // Optional loading message
  centered?: boolean;          // Center in container
}
```

**Usage:**
```vue
<!-- Small spinner -->
<LoadingSpinner size="sm" />

<!-- With message -->
<LoadingSpinner message="Loading diaries..." />

<!-- Centered in container -->
<LoadingSpinner size="lg" message="Please wait..." centered />
```

**Features:**
- Three size variants: sm (4), md (8), lg (12)
- Optional loading message below spinner
- Animated spinning SVG
- Centered layout option
- Accessible with aria-label

**Visual:**
```
┌─────────────────┐
│     ◯ ◯ ◯       │ ← Spinning animation
│  Loading...     │
└─────────────────┘
```

### EmptyState

**Purpose:** Show message when no data is available with optional action button.

**Location:** `src/components/EmptyState.vue`

**Props:**
```typescript
interface Props {
  title: string;          // Main heading
  message: string;        // Description text
  buttonText?: string;    // Optional button label
  buttonLink?: string;    // Optional router link
}
```

**Usage:**
```vue
<!-- Simple empty state -->
<EmptyState
  title="No Diaries Yet"
  message="Start writing your first thought diary!"
/>

<!-- With action button -->
<EmptyState
  title="No Diaries Yet"
  message="Start writing your first thought diary!"
  buttonText="Create Entry"
  buttonLink="/diaries"
/>
```

**Features:**
- Icon display (document/file icon)
- Title and message text
- Optional action button with RouterLink
- Centered layout with min-height
- Clean, minimalist design

**Visual:**
```
┌─────────────────┐
│      📄         │ ← Icon
│  No Diaries Yet │
│  Start writing  │
│   [Create]      │ ← Optional button
└─────────────────┘
```

### StatsCard

**Purpose:** Display statistics with icon and colored gradient background.

**Location:** `src/components/StatsCard.vue`

**Props:**
```typescript
interface Props {
  title: string;         // Card title (e.g., "Total Entries")
  value: number;         // Statistic value
  icon: string;          // Icon name (total, positive, negative, neutral)
  color: string;         // Color theme (blue, green, red, gray)
}
```

**Usage:**
```vue
<!-- Total entries -->
<StatsCard
  title="Total Entries"
  :value="stats.total"
  icon="total"
  color="blue"
/>

<!-- Positive entries -->
<StatsCard
  title="Positive Entries"
  :value="stats.positive"
  icon="positive"
  color="green"
/>

<!-- Negative entries -->
<StatsCard
  title="Negative Entries"
  :value="stats.negative"
  icon="negative"
  color="red"
/>

<!-- Neutral entries -->
<StatsCard
  title="Neutral Entries"
  :value="stats.neutral"
  icon="neutral"
  color="gray"
/>
```

**Features:**
- Color-coded gradient backgrounds
- Large number display
- Icon with opacity effects
- Hover effects with shadow transitions
- Responsive layout (2x2 on mobile, 4x1 on desktop)

**Visual:**
```
┌─────────────────┐
│  📊        42   │ ← Icon and value
│  Total Entries  │ ← Title
└─────────────────┘
```

## Form Components

### DiaryForm

**Purpose:** Form for creating or editing diary entries with validation.

**Location:** `src/components/DiaryForm.vue`

**Props:**
```typescript
interface Props {
  initialContent?: string;  // Pre-fill content for editing
  isLoading?: boolean;      // Loading state during submission
}
```

**Events:**
```typescript
{
  submit: [content: string];  // Emitted when form is submitted
  cancel: [];                 // Emitted when cancel is clicked
}
```

**Usage:**
```vue
<!-- Create mode -->
<DiaryForm
  :isLoading="diariesStore.loading"
  @submit="handleCreate"
  @cancel="closeForm"
/>

<!-- Edit mode -->
<DiaryForm
  :initialContent="diary.content"
  :isLoading="diariesStore.loading"
  @submit="handleUpdate"
  @cancel="cancelEdit"
/>
```

**Features:**
- Textarea with auto-resize (5-20 rows)
- Content validation: min 10 chars, max 5000 chars, required
- Real-time character counter (current / 5000)
- Validation error messages below textarea
- Submit and cancel buttons with proper states
- Loading state with animated spinner in submit button
- Mobile-friendly with responsive design

**Validation Rules:**
```typescript
const validate = (value: string): string | undefined => {
  if (!value) return 'Content is required';
  if (value.length < 10) return 'Content must be at least 10 characters';
  if (value.length > 5000) return 'Content must not exceed 5000 characters';
  return undefined;
};
```

**Visual:**
```
┌─────────────────────────────┐
│ ┌─────────────────────────┐ │
│ │ Write your thoughts...  │ │ ← Textarea
│ │                         │ │
│ └─────────────────────────┘ │
│ 42 / 5000 characters        │ ← Counter
│ [Cancel] [Submit Entry]     │ ← Actions
└─────────────────────────────┘
```

## Feedback Components

### DiaryCard

**Purpose:** Display a single diary entry with sentiment highlighting and actions.

**Location:** `src/components/DiaryCard.vue`

**Props:**
```typescript
interface Props {
  diary: DiaryEntry;  // Diary entry data
}
```

**Events:**
```typescript
{
  edit: [diary: DiaryEntry];    // Emitted when edit button clicked
  delete: [diary: DiaryEntry];  // Emitted when delete button clicked
}
```

**Usage:**
```vue
<DiaryCard
  :diary="entry"
  @edit="handleEdit"
  @delete="handleDelete"
/>
```

**Features:**
- Sentiment highlighting with v-html rendering (analyzed_content from backend)
- CSS styling for `.positive` (green) and `.negative` (red) spans
- Absolute date formatting (Month Day, Year at Time)
- Positive/negative sentiment count display with icons
- Edit and delete action buttons with icon buttons
- Responsive card design with hover effects
- Truncation of long content with "Read more" expand functionality

**Sentiment Display:**
```html
<!-- Backend returns analyzed_content: -->
I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span>

<!-- Rendered with CSS: -->
I felt both [excitement] and [anxious]
           ↑ green bg   ↑ red bg
```

**Visual:**
```
┌─────────────────────────────┐
│ January 15, 2026 at 2:30 PM │ ← Date
│ ─────────────────────────── │
│ I felt both [excitement] and│ ← Content with sentiment
│ [anxious] after the meeting │
│                             │
│ 👍 2  👎 1     [✏️] [🗑️]    │ ← Stats & Actions
└─────────────────────────────┘
```

### Pagination

**Purpose:** Navigate through paginated lists.

**Location:** `src/components/Pagination.vue`

**Props:**
```typescript
interface Props {
  currentPage: number;  // Current active page
  totalPages: number;   // Total number of pages
}
```

**Events:**
```typescript
{
  'page-change': [page: number];  // Emitted when page is changed
}
```

**Usage:**
```vue
<Pagination
  :currentPage="pagination.page"
  :totalPages="pagination.pages"
  @page-change="handlePageChange"
/>

<script setup>
const handlePageChange = (page: number) => {
  diariesStore.fetchDiaries(page);
};
</script>
```

**Features:**
- Previous/Next buttons with disabled states
- Page number display with ellipsis for skipped pages
- Current page highlighting with indigo background
- Mobile view showing "current / total" pages
- Desktop view with visible page numbers
- Proper ARIA labels for accessibility

**Visual (Desktop):**
```
[Previous] [1] [2] [3] ... [10] [Next]
            ↑ highlighted
```

**Visual (Mobile):**
```
[Previous]  Page 2 / 10  [Next]
```

## Navigation Components

### Navbar

**Purpose:** Main navigation bar with user menu and mobile support.

**Location:** `src/components/Navbar.vue`

**Features:**
- Logo/app name on left (book icon)
- Navigation links: Dashboard, Diaries, Profile, About
- User dropdown menu with email display
- Logout button in dropdown
- Mobile hamburger menu for small screens
- Active route highlighting with different background color
- Proper ARIA labels for accessibility

**Usage:**
```vue
<template>
  <MainLayout>
    <!-- Navbar is included in MainLayout -->
  </MainLayout>
</template>
```

**Desktop Layout:**
```
┌────────────────────────────────────────────┐
│ 📖 Thought Diary  [Dashboard] [Diaries]   │
│                   [Profile] [About]  [👤]  │ ← User menu
└────────────────────────────────────────────┘
```

**Mobile Layout:**
```
┌─────────────────────────┐
│ 📖 Thought Diary   [☰]  │ ← Hamburger
└─────────────────────────┘
  ┌─────────────────────┐
  │ Dashboard           │ ← Mobile menu
  │ Diaries             │
  │ Profile             │
  │ About               │
  │ user@example.com    │
  │ [Logout]            │
  └─────────────────────┘
```

**User Dropdown:**
- Uses Headless UI Menu component
- Displays user email from auth store
- Logout button calls auth store logout action
- Smooth transitions
- Click outside to close

## Modal Components

### DeleteConfirmationModal

**Purpose:** Confirm diary deletion with preview.

**Location:** `src/components/DeleteConfirmationModal.vue`

**Props:**
```typescript
interface Props {
  isOpen: boolean;    // Control modal visibility
  diary: DiaryEntry;  // Diary to delete
}
```

**Events:**
```typescript
{
  confirm: [];  // Emitted when delete is confirmed
  cancel: [];   // Emitted when cancel is clicked
}
```

**Usage:**
```vue
<template>
  <DeleteConfirmationModal
    :isOpen="showDeleteModal"
    :diary="diaryToDelete"
    @confirm="confirmDelete"
    @cancel="cancelDelete"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue';

const showDeleteModal = ref(false);
const diaryToDelete = ref<DiaryEntry | null>(null);

const handleDelete = (diary: DiaryEntry) => {
  diaryToDelete.value = diary;
  showDeleteModal.value = true;
};

const confirmDelete = async () => {
  if (diaryToDelete.value) {
    await diariesStore.deleteDiary(diaryToDelete.value.id);
    showDeleteModal.value = false;
  }
};

const cancelDelete = () => {
  showDeleteModal.value = false;
  diaryToDelete.value = null;
};
</script>
```

**Features:**
- Uses Headless UI Dialog component
- Modal overlay with backdrop blur and opacity transition
- Diary preview showing first 100 characters with line-clamp
- Warning icon in red circle
- Confirmation dialog with title and description
- Cancel and Delete buttons with proper styling
- Focus trap for keyboard navigation
- Smooth enter/exit transitions
- Accessible ARIA labels and roles

**Visual:**
```
┌─────────────────────────────────┐
│ ⚠️  Delete Diary Entry?         │
│                                 │
│ "I felt both excitement and..." │ ← Preview
│                                 │
│ This action cannot be undone.   │
│                                 │
│ [Cancel]  [Delete]              │
└─────────────────────────────────┘
```

## Component Patterns

### Composables Integration

```vue
<script setup lang="ts">
import { useToast } from '@/composables/useToast';

const { showSuccess, showError } = useToast();

const handleAction = async () => {
  try {
    await performAction();
    showSuccess('Action completed');
  } catch (error) {
    showError('Action failed');
  }
};
</script>
```

### Store Integration

```vue
<script setup lang="ts">
import { useDiariesStore } from '@/stores/diaries';
import { storeToRefs } from 'pinia';

const diariesStore = useDiariesStore();
const { entries, loading } = storeToRefs(diariesStore);

const handleCreate = async (content: string) => {
  await diariesStore.createDiary({ content });
};
</script>
```

### Router Integration

```vue
<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateToDiary = (id: number) => {
  router.push(`/diaries/${id}`);
};
</script>
```

### Conditional Rendering

```vue
<template>
  <!-- Loading state -->
  <LoadingSpinner v-if="loading" />

  <!-- Empty state -->
  <EmptyState
    v-else-if="!entries.length"
    title="No Diaries"
    message="Create your first entry"
  />

  <!-- Content -->
  <div v-else>
    <DiaryCard
      v-for="entry in entries"
      :key="entry.id"
      :diary="entry"
    />
  </div>
</template>
```

### Event Handling

```vue
<template>
  <DiaryCard
    :diary="entry"
    @edit="handleEdit"
    @delete="handleDelete"
  />
</template>

<script setup lang="ts">
const handleEdit = (diary: DiaryEntry) => {
  router.push(`/diaries/${diary.id}`);
};

const handleDelete = async (diary: DiaryEntry) => {
  try {
    await diariesStore.deleteDiary(diary.id);
    showSuccess('Diary deleted');
  } catch (error) {
    showError('Failed to delete');
  }
};
</script>
```

## Creating New Components

### Step-by-Step Process

1. **Create Component File**
   ```bash
   touch src/components/MyComponent.vue
   ```

2. **Define Component Structure**
   ```vue
   <script setup lang="ts">
   // Props
   interface Props {
     title: string;
   }
   const props = defineProps<Props>();

   // Events
   const emit = defineEmits<{
     click: [];
   }>();

   // State and logic
   </script>

   <template>
     <div>{{ title }}</div>
   </template>

   <style scoped>
   /* Styles */
   </style>
   ```

3. **Add Types**
   ```typescript
   // src/types/index.ts
   export interface MyComponentData {
     id: number;
     name: string;
   }
   ```

4. **Create Test**
   ```bash
   touch tests/unit/src/components/MyComponent.test.ts
   ```

   ```typescript
   import { describe, it, expect } from 'vitest';
   import { mount } from '@vue/test-utils';
   import MyComponent from '@/components/MyComponent.vue';

   describe('MyComponent', () => {
     it('renders properly', () => {
       const wrapper = mount(MyComponent, {
         props: { title: 'Test' },
       });
       expect(wrapper.text()).toContain('Test');
     });
   });
   ```

5. **Document Component**
   - Add to this documentation
   - Include props, events, and usage examples
   - Document accessibility features

### Component Checklist

- [ ] TypeScript interfaces for props and events
- [ ] Default values for optional props
- [ ] Proper event naming (kebab-case)
- [ ] Accessible ARIA labels
- [ ] Responsive design (mobile-first)
- [ ] Loading states (if async)
- [ ] Error handling
- [ ] Unit tests with good coverage
- [ ] Documentation in this file
- [ ] Storybook story (future)

## Accessibility Guidelines

### ARIA Labels

```vue
<button aria-label="Delete diary entry">
  <TrashIcon />
</button>
```

### Keyboard Navigation

```vue
<div
  role="button"
  tabindex="0"
  @click="handleClick"
  @keydown.enter="handleClick"
  @keydown.space.prevent="handleClick"
>
  Clickable Element
</div>
```

### Focus Management

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue';

const inputRef = ref<HTMLInputElement>();

onMounted(() => {
  inputRef.value?.focus();
});
</script>

<template>
  <input ref="inputRef" type="text" />
</template>
```

### Screen Reader Support

```vue
<div
  role="alert"
  aria-live="polite"
  aria-atomic="true"
>
  {{ errorMessage }}
</div>
```

## Styling Guidelines

### Tailwind Utilities

```vue
<template>
  <!-- Responsive spacing -->
  <div class="p-4 md:p-6 lg:p-8">
    
    <!-- Flex layout -->
    <div class="flex items-center justify-between">
      
      <!-- Button states -->
      <button class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50">
        Button
      </button>
    </div>
  </div>
</template>
```

### Scoped Styles

```vue
<style scoped>
/* Component-specific styles */
.custom-class {
  /* Custom styles that don't fit Tailwind */
}

/* Deep selectors for child components */
:deep(.child-class) {
  /* Styles for child components */
}
</style>
```

## Related Documentation

- [Frontend Architecture](./frontend-architecture.md) - Overall architecture patterns
- [Frontend Development](./frontend-development.md) - Development setup and workflow
- [Frontend Testing](./frontend-testing.md) - Testing strategies for components
- [Frontend API Integration](./frontend-api.md) - Backend communication patterns
