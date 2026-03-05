# Frontend Implementation Plan

**Objective**: Build a complete Vue 3 + TypeScript frontend for the Thought Diary application, including authentication, diary management, sentiment analysis display, localStorage token storage with rotation, toast notifications, real-time form validation, ESLint/Prettier tooling, and comprehensive Vitest unit tests achieving 80%+ coverage.

**Date**: January 16, 2026

---

## Step 1: Foundation Setup - Dependencies and Configuration

### Tasks

1. Install core dependencies via `npm install`:
   - Routing: `vue-router@4`
   - State Management: `pinia`
   - HTTP Client: `axios`
   - Notifications: `vue-toastification`

2. Install UI framework dependencies via `npm install`:
   - Tailwind CSS: `tailwindcss@latest postcss@latest autoprefixer@latest` (dev)
   - Headless UI: `@headlessui/vue`

3. Install form validation dependencies via `npm install`:
   - Form handling: `vee-validate`
   - Validation schemas: `yup`

4. Install linting and formatting tools via `npm install --save-dev`:
   - ESLint: `eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-vue`
   - Prettier: `prettier eslint-config-prettier`

5. Initialize Tailwind CSS:
   - Run: `npx tailwindcss init -p`
   - Configure `tailwind.config.js` with content paths
   - Create `postcss.config.js` for Tailwind processing
   - Import Tailwind directives in `src/style.css`

6. Create environment files:
   - Create `.env` with development values
   - Create `.env.example` with placeholder values
   - Configure `VITE_API_BASE_URL=http://localhost:5000`
   - Add `VITE_APP_NAME=Thought Diary App`
   - Add `VITE_APP_VERSION=0.1.0`

7. Configure ESLint:
   - Create `.eslintrc.cjs` with Vue 3 + TypeScript rules
   - Extend recommended Vue and TypeScript configs
   - Configure parser options for latest ECMAScript
   - Set environment (browser, es2021, node)

8. Configure Prettier:
   - Create `.prettierrc.json` with formatting rules
   - Create `.prettierignore` for build outputs
   - Configure single quotes, semi: true, trailing commas

9. Update `package.json` scripts:
   - Add `"lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx --fix"`
   - Add `"format": "prettier --write src/"`

10. Update `vite.config.ts`:
    - Configure Tailwind CSS processing
    - Set up path aliases (`@/` for `src/`)
    - Configure development server port (5173)

### Checklist

- [ ] All core dependencies installed (vue-router, pinia, axios, vue-toastification)
- [ ] UI framework dependencies installed (tailwindcss, @headlessui/vue)
- [ ] Form validation dependencies installed (vee-validate, yup)
- [ ] ESLint and Prettier dependencies installed
- [ ] `package.json` updated with all dependencies
- [ ] `tailwind.config.js` created and configured
- [ ] `postcss.config.js` created
- [ ] Tailwind directives added to `src/style.css`
- [ ] `.env` created with `VITE_API_BASE_URL=http://localhost:5000`
- [ ] `.env.example` created with placeholder values
- [ ] `.eslintrc.cjs` created with Vue 3 + TypeScript rules
- [ ] `.prettierrc.json` created with formatting config
- [ ] `.prettierignore` created
- [ ] `package.json` updated with `lint` and `format` scripts
- [ ] `vite.config.ts` configured with aliases and Tailwind
- [ ] `npm run lint` executes successfully
- [ ] `npm run format` executes successfully
- [ ] Dev server starts: `npm run dev`

---

## Step 2: TypeScript Interfaces and API Service Layer

### Tasks

1. Create TypeScript interfaces in `src/types/index.ts`:
   - `User` interface (id, email, created_at, updated_at)
   - `DiaryEntry` interface (all fields including analyzed_content, sentiment counts)
   - `DiaryStats` interface (total, positive, negative, neutral counts)
   - `AuthState` interface (user, accessToken, refreshToken, isAuthenticated)
   - `LoginRequest` interface (email, password)
   - `RegisterRequest` interface (email, password)
   - `DiaryCreateRequest` interface (content)
   - `DiaryUpdateRequest` interface (content)
   - `DiaryListResponse` interface (diaries array, pagination)
   - `PaginationInfo` interface (page, per_page, total, pages)
   - `ApiError` interface (error, message)
   - `TokenResponse` interface (access_token, refresh_token)
   - Export all interfaces

2. Create Axios API service in `src/services/api.ts`:
   - Create Axios instance with baseURL from `VITE_API_BASE_URL`
   - Configure timeout (30 seconds)
   - Set default headers (Content-Type: application/json)

3. Implement request interceptor in `src/services/api.ts`:
   - Get access token from localStorage
   - Add Authorization header: `Bearer <token>`
   - Skip Authorization for public endpoints (register, login)

4. Implement response interceptor in `src/services/api.ts`:
   - Handle 401 Unauthorized responses
   - Attempt token refresh with refresh token from localStorage
   - Implement request queue to prevent multiple refresh calls
   - Update localStorage with new tokens on successful refresh
   - Retry original failed request with new token
   - Logout user if refresh token is expired (redirect to login)

5. Implement error transformation in response interceptor:
   - Transform backend errors to `ApiError` interface
   - Handle network errors (offline, timeout, connection refused)
   - Provide retry mechanism for network failures
   - Return structured error object

6. Create API client methods in `src/services/api.ts`:
   - Export configured Axios instance as default
   - Create helper functions for auth endpoints:
     - `register(data: RegisterRequest)`
     - `login(data: LoginRequest)`
     - `logout()`
     - `refreshToken()`
     - `getCurrentUser()`
   - Create helper functions for diary endpoints:
     - `getDiaries(page?: number, perPage?: number)`
     - `getDiary(id: number)`
     - `createDiary(data: DiaryCreateRequest)`
     - `updateDiary(id: number, data: DiaryUpdateRequest)`
     - `deleteDiary(id: number)`
     - `getDiaryStats()`

7. Implement token rotation logic:
   - On refresh, replace old tokens with new ones from backend
   - Update localStorage immediately after successful refresh
   - Clear tokens on logout or refresh failure

### Checklist

- [ ] `src/types/index.ts` created
- [ ] All interfaces defined with proper TypeScript types
- [ ] User interface matches backend response
- [ ] DiaryEntry interface includes all fields
- [ ] DiaryStats interface for statistics
- [ ] AuthState interface for Pinia store
- [ ] Request/Response interfaces for all API calls
- [ ] ApiError interface for error handling
- [ ] `src/services/api.ts` created
- [ ] Axios instance created with baseURL from env
- [ ] Timeout set to 30 seconds
- [ ] Request interceptor adds JWT token from localStorage
- [ ] Response interceptor handles 401 errors
- [ ] Token refresh implemented with queue mechanism
- [ ] Tokens updated in localStorage on refresh
- [ ] Request retried after successful token refresh
- [ ] Logout triggered on refresh token expiry
- [ ] Network errors handled gracefully
- [ ] Error transformation to ApiError interface
- [ ] All auth API methods implemented
- [ ] All diary API methods implemented
- [ ] Token rotation logic implemented

---

## Step 3: Pinia Store Implementation

### Tasks

1. Create auth store in `src/stores/auth.ts`:
   - Define state: `user`, `accessToken`, `refreshToken`, `isAuthenticated`
   - Implement `register(email, password)` action
   - Implement `login(email, password)` action
   - Implement `logout()` action
   - Implement `refreshToken()` action
   - Implement `fetchProfile()` action
   - Store tokens in localStorage on login/register
   - Load tokens from localStorage on store initialization
   - Clear tokens from localStorage on logout
   - Update `isAuthenticated` computed property based on token presence
   - Handle API errors and re-throw for component handling

2. Create diaries store in `src/stores/diaries.ts`:
   - Define state: `entries`, `currentDiary`, `stats`, `pagination`, `loading`
   - Implement `fetchDiaries(page?: number)` action
   - Implement `fetchDiary(id: number)` action
   - Implement `createDiary(content: string)` action
   - Implement `updateDiary(id: number, content: string)` action
   - Implement `deleteDiary(id: number)` action
   - Implement `fetchStats()` action
   - Update pagination state from API responses
   - Handle loading states for each action
   - Clear store on logout

3. Create UI store in `src/stores/ui.ts`:
   - Define state: `isLoading`, `loadingMessage`
   - Implement `setLoading(isLoading: boolean, message?: string)` action
   - Create computed properties for loading state
   - Provide global loading overlay control

4. Configure Pinia in `src/main.ts`:
   - Import and create Pinia instance
   - Register Pinia with Vue app
   - Ensure stores are initialized before router navigation

5. Implement store persistence:
   - Auth tokens persist in localStorage
   - Restore auth state on page reload
   - Clear persisted state on logout

### Checklist

- [ ] `src/stores/auth.ts` created
- [ ] Auth state defined (user, tokens, isAuthenticated)
- [ ] `register()` action implemented
- [ ] `login()` action implemented
- [ ] `logout()` action implemented
- [ ] `refreshToken()` action implemented
- [ ] `fetchProfile()` action implemented
- [ ] Tokens stored in localStorage on login/register
- [ ] Tokens loaded from localStorage on initialization
- [ ] Tokens cleared from localStorage on logout
- [ ] `isAuthenticated` computed property implemented
- [ ] `src/stores/diaries.ts` created
- [ ] Diary state defined (entries, currentDiary, stats, pagination, loading)
- [ ] `fetchDiaries()` action implemented with pagination
- [ ] `fetchDiary()` action implemented
- [ ] `createDiary()` action implemented
- [ ] `updateDiary()` action implemented
- [ ] `deleteDiary()` action implemented
- [ ] `fetchStats()` action implemented
- [ ] Pagination state updated from API
- [ ] Loading states handled in all actions
- [ ] `src/stores/ui.ts` created
- [ ] Global loading state managed
- [ ] Pinia configured in `src/main.ts`
- [ ] Store persistence working correctly

---

## Step 4: Toast Notification System

### Tasks

1. Install and configure vue-toastification in `src/main.ts`:
   - Import Toast plugin and CSS
   - Configure toast options (position: top-right, timeout: 3000ms)
   - Register plugin with Vue app
   - Set up default toast styling

2. Create toast composable in `src/composables/useToast.ts`:
   - Import `useToast` from vue-toastification
   - Create wrapper functions:
     - `showSuccess(message: string)` - Green success toast
     - `showError(message: string)` - Red error toast
     - `showInfo(message: string)` - Blue info toast
     - `showWarning(message: string)` - Yellow warning toast
     - `showErrorWithRetry(message: string, onRetry: () => void)` - Error with retry button
   - Export composable function
   - Add TypeScript types for all functions

3. Integrate with API service error interceptor:
   - Import toast composable in `src/services/api.ts`
   - Show error toast for global API errors
   - Show retry toast for network failures
   - Exclude inline form validation errors (handle in components)
   - Show success toast on logout

4. Handle network errors with retry:
   - Detect network errors (offline, timeout, connection refused)
   - Show toast with retry button
   - On retry, re-execute failed request
   - Show loading state during retry

### Checklist

- [ ] vue-toastification installed
- [ ] Toast plugin configured in `src/main.ts`
- [ ] Toast CSS imported
- [ ] Toast options set (position, timeout)
- [ ] `src/composables/useToast.ts` created
- [ ] `showSuccess()` function implemented
- [ ] `showError()` function implemented
- [ ] `showInfo()` function implemented
- [ ] `showWarning()` function implemented
- [ ] `showErrorWithRetry()` function with callback implemented
- [ ] Toast composable exported
- [ ] TypeScript types added
- [ ] Toast integrated with API service errors
- [ ] Network errors show retry toast
- [ ] Form validation errors excluded from global toast
- [ ] Retry mechanism working for failed requests
- [ ] Success toast on logout
- [ ] Toast notifications tested manually

---

## Step 5: Vue Router Configuration

### Tasks

1. Create router configuration in `src/router/index.ts`:
   - Import createRouter, createWebHistory
   - Define route array with all routes:
     - `/` - Home/Landing page (public)
     - `/login` - Login page (guest only)
     - `/register` - Register page (guest only)
     - `/dashboard` - Dashboard page (protected)
     - `/diaries` - Diaries list page (protected)
     - `/diaries/:id` - Diary detail page (protected)
     - `/profile` - User profile page (protected)
     - `/about` - About page (public)
   - Configure lazy loading for all route components
   - Set route meta fields (requiresAuth, guestOnly, title)

2. Implement authentication guard:
   - Create `beforeEach` navigation guard
   - Check route meta `requiresAuth` field
   - Get auth state from auth store
   - Redirect to `/login` if not authenticated
   - Save intended route for redirect after login

3. Implement guest-only guard:
   - Check route meta `guestOnly` field
   - Redirect authenticated users to `/dashboard`
   - Prevent access to login/register when logged in

4. Set page titles:
   - Use route meta `title` field
   - Update document.title on navigation
   - Format: `{Page Title} - Thought Diary App`

5. Handle 404 routes:
   - Add catch-all route for undefined paths
   - Create 404 Not Found component
   - Redirect or show 404 page

6. Configure router options:
   - Use web history mode
   - Set scroll behavior (scroll to top on navigation)

### Checklist

- [ ] `src/router/index.ts` created
- [ ] All routes defined with paths
- [ ] Home route (`/`) configured
- [ ] Login route (`/login`) configured
- [ ] Register route (`/register`) configured
- [ ] Dashboard route (`/dashboard`) configured
- [ ] Diaries list route (`/diaries`) configured
- [ ] Diary detail route (`/diaries/:id`) configured
- [ ] Profile route (`/profile`) configured
- [ ] About route (`/about`) configured
- [ ] All routes use lazy loading (`component: () => import()`)
- [ ] Route meta fields set (requiresAuth, guestOnly, title)
- [ ] Authentication guard implemented in `beforeEach`
- [ ] Unauthenticated users redirected to `/login`
- [ ] Intended route saved for post-login redirect
- [ ] Guest-only guard implemented
- [ ] Authenticated users redirected from login/register
- [ ] Page titles updated on navigation
- [ ] 404 catch-all route added
- [ ] Web history mode configured
- [ ] Scroll behavior set to top
- [ ] Router registered in `src/main.ts`

---

## Step 6: Layout Components

### Tasks

1. Create main layout in `src/layouts/MainLayout.vue`:
   - Template structure: Navbar + main content area + footer (optional)
   - Use `<router-view>` for nested routes
   - Add responsive container with Tailwind classes
   - Import and use Navbar component
   - Use `<script setup>` syntax with TypeScript
   - Add proper TypeScript types for props/emits

2. Create auth layout in `src/layouts/AuthLayout.vue`:
   - Centered card design for login/register
   - Background with gradient or image
   - Responsive design for mobile/tablet/desktop
   - Logo or app name at top
   - `<slot>` for page content
   - No navbar (guest layout)
   - Use Tailwind for styling

3. Create navbar component in `src/components/Navbar.vue`:
   - Logo/app name on left
   - Navigation links: Dashboard, Diaries, Profile, About
   - User email display on right
   - Logout button
   - Mobile hamburger menu
   - Use Headless UI Menu component for dropdown
   - Highlight active route
   - Use auth store to get user data
   - Call logout action on button click

4. Style layouts with Tailwind CSS:
   - Mobile-first responsive design
   - Proper spacing and padding
   - Consistent color scheme
   - Accessible navigation (ARIA labels)

### Checklist

- [ ] `src/layouts/MainLayout.vue` created
- [ ] MainLayout includes Navbar component
- [ ] MainLayout uses `<router-view>` for content
- [ ] MainLayout has responsive container
- [ ] MainLayout uses `<script setup>` with TypeScript
- [ ] `src/layouts/AuthLayout.vue` created
- [ ] AuthLayout has centered card design
- [ ] AuthLayout is responsive
- [ ] AuthLayout has `<slot>` for content
- [ ] AuthLayout styled with Tailwind
- [ ] `src/components/Navbar.vue` created
- [ ] Navbar shows logo/app name
- [ ] Navbar has navigation links
- [ ] Navbar shows user email from auth store
- [ ] Navbar has logout button
- [ ] Navbar has mobile hamburger menu
- [ ] Navbar uses Headless UI Menu for dropdown
- [ ] Active route highlighted
- [ ] Logout action called on button click
- [ ] All layouts follow responsive design
- [ ] Accessibility labels added (ARIA)
- [ ] Layouts tested on mobile/tablet/desktop

---

## Step 7: Authentication Views

### Tasks

1. Create login view in `src/views/Login.vue`:
   - Use AuthLayout as wrapper
   - Page title: "Login"
   - Form with email and password fields
   - Use VeeValidate for form handling
   - Use Yup for validation schema
   - Real-time validation on input (no debouncing)
   - Email validation: RFC 5322 format, max 120 chars
   - Password validation: min 8 chars, uppercase, lowercase, digit, special
   - Display inline validation errors below each field
   - Submit button disabled during loading
   - Call auth store `login()` action on submit
   - Show loading spinner in button during submission
   - Redirect to dashboard on success
   - Show toast notification for API errors
   - Link to register page

2. Create register view in `src/views/Register.vue`:
   - Use AuthLayout as wrapper
   - Page title: "Register"
   - Form with email and password fields
   - Use VeeValidate for form handling
   - Use Yup for validation schema
   - Real-time validation on input
   - Same validation rules as login
   - Display inline validation errors
   - Submit button disabled during loading
   - Call auth store `register()` action on submit
   - Show loading spinner in button during submission
   - Redirect to dashboard on success (auto-login)
   - Show toast notification for API errors
   - Link to login page

3. Create validation schemas:
   - Email validation: format, max length, required
   - Password validation: min length, complexity, required
   - Use Yup schema composition
   - Export reusable schemas

4. Style forms with Tailwind CSS:
   - Consistent input styling
   - Focus states and hover effects
   - Error message styling (red text)
   - Button states (normal, hover, disabled, loading)
   - Mobile-friendly form fields

### Checklist

- [ ] `src/views/Login.vue` created
- [ ] Login uses AuthLayout
- [ ] Login form has email and password fields
- [ ] VeeValidate configured for login form
- [ ] Yup validation schema for login
- [ ] Real-time validation on input
- [ ] Email validation: RFC 5322, max 120 chars
- [ ] Password validation: min 8 chars with complexity
- [ ] Inline error messages below fields
- [ ] Submit button disabled during loading
- [ ] Loading spinner shown in button
- [ ] Auth store `login()` called on submit
- [ ] Redirect to dashboard on success
- [ ] Toast shown for API errors
- [ ] Link to register page included
- [ ] `src/views/Register.vue` created
- [ ] Register uses AuthLayout
- [ ] Register form has email and password fields
- [ ] VeeValidate configured for register form
- [ ] Yup validation schema for register
- [ ] Same validation rules as login
- [ ] Auth store `register()` called on submit
- [ ] Redirect to dashboard after registration
- [ ] Link to login page included
- [ ] Validation schemas exported from separate file
- [ ] Forms styled with Tailwind CSS
- [ ] Input focus and hover states styled
- [ ] Error messages styled (red text)
- [ ] Button states styled
- [ ] Forms responsive on mobile

---

## Step 8: Core Diary Components

### Tasks

1. Create diary card component in `src/components/DiaryCard.vue`:
   - Props: `diary` (DiaryEntry interface)
   - Display diary content with sentiment highlighting
   - Use `v-html` to render `analyzed_content` field
   - CSS for sentiment spans:
     - `.positive` - green background, white text
     - `.negative` - red background, white text
   - Display absolute date (created_at) formatted
   - Show positive/negative counts with icons
   - Edit and delete action buttons
   - Emit events: `@edit`, `@delete`
   - Responsive card design with Tailwind
   - Truncate long content with "Read more" link

2. Create diary form component in `src/components/DiaryForm.vue`:
   - Props: `diary` (optional, for edit mode), `isSubmitting` (boolean)
   - Emit: `@submit` with content
   - Textarea for content input
   - Use VeeValidate for validation
   - Content validation: min 10 chars, max 5000 chars, required
   - Real-time character counter: "XXX / 5000"
   - Show validation error if below min or above max
   - Submit and cancel buttons
   - Loading state on submit button
   - Auto-resize textarea based on content
   - Mobile-friendly textarea

3. Create stats card component in `src/components/StatsCard.vue`:
   - Props: `stats` (DiaryStats interface)
   - Display four stat cards:
     - Total Entries
     - Positive Entries
     - Negative Entries
     - Neutral Entries
   - Use grid layout (2x2 on mobile, 4x1 on desktop)
   - Color-coded cards (blue, green, red, gray)
   - Icons for each stat type
   - Large number display
   - Label below number
   - Responsive grid with Tailwind

4. Create pagination component in `src/components/Pagination.vue`:
   - Props: `pagination` (PaginationInfo interface)
   - Emit: `@page-change` with page number
   - Previous/Next buttons
   - Page numbers (current, adjacent, first, last)
   - Disable previous on first page
   - Disable next on last page
   - Current page highlighted
   - Ellipsis for skipped pages
   - Mobile-friendly button sizes
   - Use Tailwind for styling

5. Create loading spinner component in `src/components/LoadingSpinner.vue`:
   - Props: `size` (sm, md, lg), `message` (optional)
   - Animated spinner icon
   - Optional loading message below
   - Center in container
   - Use Tailwind for animation
   - Accessible (aria-label)

6. Create empty state component in `src/components/EmptyState.vue`:
   - Props: `title`, `message`, `actionText` (optional), `actionTo` (optional route)
   - Display icon (customizable)
   - Title and message text
   - Optional action button
   - Centered in container
   - Use Tailwind for styling

7. Create delete confirmation modal:
   - Use Headless UI Dialog component
   - Props: `isOpen`, `diaryId`, `diaryPreview`
   - Emit: `@confirm`, `@cancel`
   - Show diary preview (first 100 chars)
   - Warning message
   - Cancel and confirm buttons
   - Focus trap
   - Overlay background
   - Accessible (ARIA labels)

### Checklist

- [ ] `src/components/DiaryCard.vue` created
- [ ] DiaryCard accepts diary prop
- [ ] DiaryCard renders analyzed_content with v-html
- [ ] CSS for `.positive` span (green bg, white text)
- [ ] CSS for `.negative` span (red bg, white text)
- [ ] Absolute date displayed
- [ ] Positive/negative counts shown with icons
- [ ] Edit and delete buttons
- [ ] Events emitted: `@edit`, `@delete`
- [ ] Card is responsive
- [ ] Long content truncated with "Read more"
- [ ] `src/components/DiaryForm.vue` created
- [ ] DiaryForm accepts diary and isSubmitting props
- [ ] Textarea for content input
- [ ] VeeValidate validation: min 10, max 5000 chars
- [ ] Real-time character counter
- [ ] Validation error displayed
- [ ] Submit and cancel buttons
- [ ] Loading state on submit button
- [ ] Textarea auto-resizes
- [ ] Form is mobile-friendly
- [ ] `src/components/StatsCard.vue` created
- [ ] StatsCard accepts stats prop
- [ ] Four stat cards displayed
- [ ] Grid layout (2x2 mobile, 4x1 desktop)
- [ ] Color-coded cards
- [ ] Icons for each stat
- [ ] Responsive with Tailwind
- [ ] `src/components/Pagination.vue` created
- [ ] Pagination accepts pagination prop
- [ ] Previous/Next buttons
- [ ] Page numbers displayed
- [ ] Buttons disabled appropriately
- [ ] Current page highlighted
- [ ] Ellipsis for skipped pages
- [ ] Event emitted: `@page-change`
- [ ] Mobile-friendly
- [ ] `src/components/LoadingSpinner.vue` created
- [ ] Spinner accepts size and message props
- [ ] Animated spinner
- [ ] Optional message displayed
- [ ] Centered in container
- [ ] Accessible (aria-label)
- [ ] `src/components/EmptyState.vue` created
- [ ] EmptyState accepts title, message, actionText, actionTo
- [ ] Icon displayed
- [ ] Optional action button
- [ ] Centered layout
- [ ] Delete confirmation modal created
- [ ] Modal uses Headless UI Dialog
- [ ] Diary preview shown
- [ ] Warning message displayed
- [ ] Cancel and confirm buttons
- [ ] Focus trap working
- [ ] Overlay background
- [ ] Accessible (ARIA)

---

## Step 9: Dashboard and Diary Views

### Tasks

1. Create dashboard view in `src/views/Dashboard.vue`:
   - Use MainLayout
   - Page title: "Dashboard"
   - Load stats on mount from diaries store
   - Load recent 5 diaries on mount
   - Display StatsCard component with stats
   - Section title: "Recent Entries"
   - Display DiaryCard for each recent diary
   - Show EmptyState if no diaries
   - "Create Entry" button (opens form or navigates)
   - Handle loading state with LoadingSpinner
   - Handle errors with toast notification

2. Create diaries list view in `src/views/Diaries.vue`:
   - Use MainLayout
   - Page title: "My Diaries"
   - Load diaries with pagination on mount
   - "Create New Entry" button at top
   - Display DiaryCard for each diary
   - Show Pagination component
   - Handle page changes
   - Show LoadingSpinner while loading
   - Show EmptyState if no diaries
   - Handle errors with toast notification
   - Refresh list after create/update/delete

3. Create diary detail view in `src/views/DiaryDetail.vue`:
   - Use MainLayout
   - Page title: "Diary Entry"
   - Load diary by ID from route params on mount
   - Display full diary content with sentiment highlighting
   - Show absolute date
   - Show positive/negative counts
   - Edit button (inline editing or navigate to edit page)
   - Delete button (opens confirmation modal)
   - Use delete confirmation modal
   - Back to list button
   - Handle loading state
   - Handle errors (404 if not found)
   - Navigate to list after delete

4. Implement inline editing:
   - Toggle between view and edit mode
   - Show DiaryForm in edit mode
   - Cancel returns to view mode
   - Save updates diary and returns to view mode
   - Show loading state during save

5. Create profile view in `src/views/Profile.vue`:
   - Use MainLayout
   - Page title: "Profile"
   - Load user profile from auth store
   - Display user email
   - Display account created date (absolute)
   - Display last updated date
   - Placeholder for future features (change password, etc.)
   - Simple, clean layout

6. Create about view in `src/views/About.vue`:
   - Use MainLayout or simple layout
   - Page title: "About"
   - App description
   - Features list
   - Link to Thought Diary concept
   - Credits/acknowledgments
   - Version number from env

### Checklist

- [ ] `src/views/Dashboard.vue` created
- [ ] Dashboard uses MainLayout
- [ ] Stats loaded on mount
- [ ] Recent 5 diaries loaded on mount
- [ ] StatsCard component displayed
- [ ] DiaryCard components for recent entries
- [ ] EmptyState shown if no diaries
- [ ] "Create Entry" button
- [ ] LoadingSpinner shown while loading
- [ ] Errors handled with toast
- [ ] `src/views/Diaries.vue` created
- [ ] Diaries list uses MainLayout
- [ ] Diaries loaded with pagination
- [ ] "Create New Entry" button at top
- [ ] DiaryCard for each diary
- [ ] Pagination component displayed
- [ ] Page changes handled
- [ ] LoadingSpinner shown while loading
- [ ] EmptyState shown if no diaries
- [ ] List refreshed after create/update/delete
- [ ] `src/views/DiaryDetail.vue` created
- [ ] DiaryDetail uses MainLayout
- [ ] Diary loaded by ID from route params
- [ ] Full content displayed with sentiment highlighting
- [ ] Absolute date shown
- [ ] Positive/negative counts displayed
- [ ] Edit button implemented
- [ ] Delete button opens confirmation modal
- [ ] Delete confirmation modal integrated
- [ ] Back to list button
- [ ] Loading state handled
- [ ] 404 error handled
- [ ] Navigate to list after delete
- [ ] Inline editing implemented
- [ ] Toggle between view and edit mode
- [ ] DiaryForm shown in edit mode
- [ ] Cancel returns to view mode
- [ ] Save updates diary
- [ ] Loading state during save
- [ ] `src/views/Profile.vue` created
- [ ] Profile uses MainLayout
- [ ] User email displayed
- [ ] Account created date shown (absolute)
- [ ] Last updated date shown
- [ ] Clean layout
- [ ] `src/views/About.vue` created
- [ ] App description included
- [ ] Features list
- [ ] Version number from env

---

## Step 10: Testing Infrastructure with Vitest

### Tasks

1. Install Vitest dependencies via `npm install --save-dev`:
   - Testing framework: `vitest @vitest/ui`
   - DOM environment: `jsdom` or `happy-dom`
   - Vue testing: `@vue/test-utils`

2. Configure Vitest in `vitest.config.ts`:
   - Import Vue plugin
   - Configure test environment (jsdom)
   - Set up path aliases (`@/` for `src/`)
   - Configure globals (describe, it, expect)
   - Set up coverage reporting (istanbul or c8)
   - Configure test file patterns

3. Create test setup file in `tests/unit/setup.ts`:
   - Mock localStorage
   - Mock vue-toastification
   - Mock window.matchMedia (for responsive tests)
   - Setup global test utilities
   - Configure Vue Test Utils defaults

4. Create store tests in `tests/unit/src/stores/`:
   - `auth.test.ts`:
     - Test register action success
     - Test login action success
     - Test logout action
     - Test token persistence in localStorage
     - Test isAuthenticated computed
     - Test token refresh action
     - Mock API calls with success/error responses
   - `diaries.test.ts`:
     - Test fetchDiaries with pagination
     - Test createDiary action
     - Test updateDiary action
     - Test deleteDiary action
     - Test fetchStats action
     - Test loading states
     - Mock API calls

5. Create component tests in `tests/unit/src/components/`:
   - `Navbar.test.ts`:
     - Test renders user email
     - Test logout button calls action
     - Test navigation links
     - Test mobile menu toggle
   - `DiaryCard.test.ts`:
     - Test renders diary content
     - Test sentiment highlighting (v-html)
     - Test edit button emits event
     - Test delete button emits event
     - Test date formatting
   - `DiaryForm.test.ts`:
     - Test renders textarea
     - Test character counter updates
     - Test validation errors shown
     - Test submit button disabled when invalid
     - Test submit event emitted with content
     - Test cancel button emits event
   - `Pagination.test.ts`:
     - Test renders page numbers
     - Test previous button disabled on first page
     - Test next button disabled on last page
     - Test page change event emitted
   - `StatsCard.test.ts`:
     - Test renders all stats
     - Test correct numbers displayed
   - `LoadingSpinner.test.ts`:
     - Test renders spinner
     - Test message displayed
     - Test different sizes
   - `EmptyState.test.ts`:
     - Test renders title and message
     - Test action button
     - Test router link

6. Create view tests in `tests/unit/src/views/`:
   - `Login.test.ts`:
     - Test form renders
     - Test validation errors
     - Test login action called on submit
     - Test redirect on success
     - Test toast on error
     - Mock router and store
   - `Register.test.ts`:
     - Test form renders
     - Test validation errors
     - Test register action called
     - Test redirect on success
   - `Dashboard.test.ts`:
     - Test loads stats and recent diaries
     - Test displays stats card
     - Test displays diary cards
     - Test empty state shown
     - Mock store actions
   - `Diaries.test.ts`:
     - Test loads diaries with pagination
     - Test displays diary cards
     - Test pagination works
     - Test empty state shown
     - Mock store

7. Create service tests in `tests/unit/src/services/`:
   - `api.test.ts`:
     - Test request interceptor adds token
     - Test response interceptor handles 401
     - Test token refresh on 401
     - Test request retry after refresh
     - Test logout on refresh failure
     - Test network error handling
     - Test retry mechanism
     - Mock axios

8. Create composable tests in `tests/unit/src/composables/`:
   - `useToast.test.ts`:
     - Test showSuccess
     - Test showError
     - Test showInfo
     - Test showErrorWithRetry
     - Mock vue-toastification

9. Run tests and ensure coverage:
   - Run all tests: `npm run test`
   - Run tests with coverage: `npm run test:coverage`
   - Run tests in UI mode: `npm run test:ui`
   - Ensure 80%+ coverage
   - Generate HTML coverage report

10. Update `package.json` scripts:
    - Add `"test": "vitest"`
    - Add `"test:ui": "vitest --ui"`
    - Add `"test:coverage": "vitest --coverage"`

### Checklist

- [ ] Vitest dependencies installed
- [ ] `vitest.config.ts` created and configured
- [ ] Vue plugin configured
- [ ] Test environment set to jsdom
- [ ] Path aliases configured
- [ ] Coverage reporting configured
- [ ] `tests/unit/setup.ts` created
- [ ] localStorage mocked
- [ ] vue-toastification mocked
- [ ] window.matchMedia mocked
- [ ] Test directory structure mirrors src/
- [ ] `tests/unit/src/stores/auth.test.ts` created
- [ ] Auth store register tested
- [ ] Auth store login tested
- [ ] Auth store logout tested
- [ ] Token persistence tested
- [ ] isAuthenticated computed tested
- [ ] Token refresh tested
- [ ] `tests/unit/src/stores/diaries.test.ts` created
- [ ] All diary store actions tested
- [ ] Loading states tested
- [ ] `tests/unit/src/components/Navbar.test.ts` created
- [ ] Navbar rendering tested
- [ ] Navbar logout tested
- [ ] Navbar navigation tested
- [ ] `tests/unit/src/components/DiaryCard.test.ts` created
- [ ] DiaryCard content rendering tested
- [ ] Sentiment highlighting tested
- [ ] Edit/delete events tested
- [ ] `tests/unit/src/components/DiaryForm.test.ts` created
- [ ] Form validation tested
- [ ] Character counter tested
- [ ] Submit event tested
- [ ] `tests/unit/src/components/Pagination.test.ts` created
- [ ] Pagination rendering tested
- [ ] Page change event tested
- [ ] `tests/unit/src/components/StatsCard.test.ts` created
- [ ] Stats display tested
- [ ] `tests/unit/src/components/LoadingSpinner.test.ts` created
- [ ] Spinner rendering tested
- [ ] `tests/unit/src/components/EmptyState.test.ts` created
- [ ] Empty state rendering tested
- [ ] `tests/unit/src/views/Login.test.ts` created
- [ ] Login form tested comprehensively
- [ ] `tests/unit/src/views/Register.test.ts` created
- [ ] Register form tested comprehensively
- [ ] `tests/unit/src/views/Dashboard.test.ts` created
- [ ] Dashboard data loading tested
- [ ] `tests/unit/src/views/Diaries.test.ts` created
- [ ] Diaries list and pagination tested
- [ ] `tests/unit/src/services/api.test.ts` created
- [ ] API interceptors tested
- [ ] Token refresh tested
- [ ] Network error handling tested
- [ ] Retry mechanism tested
- [ ] `tests/unit/src/composables/useToast.test.ts` created
- [ ] Toast functions tested
- [ ] All tests pass: `npm run test`
- [ ] 80%+ test coverage achieved
- [ ] Coverage report generated
- [ ] Test scripts added to package.json

---

## Final Verification Checklist

### Application Structure
- [ ] Directory structure organized (src/components, src/views, src/stores, etc.)
- [ ] All modules properly organized
- [ ] TypeScript types defined in src/types
- [ ] Composables in src/composables
- [ ] Services in src/services
- [ ] Layouts in src/layouts

### Configuration & Environment
- [ ] `.env.example` complete and accurate
- [ ] `.env` created with actual values
- [ ] `VITE_API_BASE_URL=http://localhost:5000`
- [ ] Vite config with aliases and Tailwind
- [ ] ESLint configured and running
- [ ] Prettier configured and running
- [ ] Tailwind CSS configured

### Type Safety
- [ ] All TypeScript interfaces defined
- [ ] User interface matches backend
- [ ] DiaryEntry interface complete
- [ ] Request/Response types defined
- [ ] ApiError interface for errors
- [ ] No TypeScript errors: `npm run build`

### API Integration
- [ ] Axios service created
- [ ] Request interceptor adds JWT token
- [ ] Response interceptor handles 401
- [ ] Token refresh implemented with rotation
- [ ] Network errors handled with retry
- [ ] All API methods implemented
- [ ] Error transformation working

### State Management
- [ ] Auth store fully functional
- [ ] Register/login/logout working
- [ ] Token persistence in localStorage
- [ ] Diaries store fully functional
- [ ] All CRUD operations working
- [ ] Pagination state managed
- [ ] UI store for global loading

### Routing
- [ ] All routes defined
- [ ] Lazy loading configured
- [ ] Authentication guard working
- [ ] Guest-only guard working
- [ ] Page titles updating
- [ ] 404 route handling

### Authentication UI
- [ ] Login page functional
- [ ] Register page functional
- [ ] Real-time validation working
- [ ] Email validation: RFC 5322, max 120 chars
- [ ] Password validation: min 8 chars, complexity
- [ ] Inline errors displayed
- [ ] Toast notifications on API errors
- [ ] Redirect to dashboard on success

### Diary Management
- [ ] Dashboard showing stats and recent entries
- [ ] Diaries list with pagination
- [ ] Diary detail view
- [ ] Create diary functionality
- [ ] Edit diary functionality
- [ ] Delete diary with confirmation
- [ ] Sentiment highlighting working
- [ ] Empty states displayed

### Components
- [ ] Navbar with user info and logout
- [ ] DiaryCard with sentiment highlighting
- [ ] DiaryForm with validation
- [ ] StatsCard displaying statistics
- [ ] Pagination working correctly
- [ ] LoadingSpinner component
- [ ] EmptyState component
- [ ] Delete confirmation modal

### UI/UX
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Tailwind CSS styling applied
- [ ] Toast notifications working
- [ ] Loading states shown
- [ ] Empty states helpful
- [ ] Forms user-friendly
- [ ] Buttons have proper states

### Testing
- [ ] Vitest configured
- [ ] All store tests pass
- [ ] All component tests pass
- [ ] All view tests pass
- [ ] All service tests pass
- [ ] 80%+ test coverage achieved
- [ ] Coverage report generated
- [ ] Tests run in CI-ready mode

### Code Quality
- [ ] TypeScript strict mode enabled
- [ ] No ESLint errors: `npm run lint`
- [ ] Code formatted: `npm run format`
- [ ] Vue 3 Composition API used throughout
- [ ] `<script setup>` syntax used
- [ ] Proper component naming (PascalCase)
- [ ] Props and emits typed

### Integration with Backend
- [ ] API calls match backend endpoints
- [ ] Authentication flow working
- [ ] JWT tokens sent correctly
- [ ] Token refresh working
- [ ] Diary CRUD operations working
- [ ] Pagination working (10 per page)
- [ ] Statistics endpoint working
- [ ] Sentiment display correct

### Security
- [ ] No hardcoded secrets
- [ ] Tokens stored securely in localStorage
- [ ] Token rotation implemented
- [ ] Automatic logout on token expiry
- [ ] Protected routes enforced
- [ ] Input validation on frontend
- [ ] XSS protection (trust backend HTML)

### Documentation Updates
- [ ] Update [CHANGELOG.md](../../CHANGELOG.md) with frontend implementation
- [ ] Follow Keep a Changelog format
- [ ] Include version numbers and date
- [ ] List all added features
- [ ] Update [README.md](../../README.md) if needed
- [ ] Document environment variables

---

## Implementation Notes

### Key Decisions
- **Token Storage**: localStorage for persistence with rotation on refresh
- **Error Handling**: Toast for global errors, inline for form validation
- **Form Validation**: Real-time on input, no debouncing
- **Date Display**: Absolute dates for all diary entries
- **Loading States**: Simple spinner component, no skeleton loaders
- **Network Errors**: Toast with retry button
- **Delete Confirmation**: Headless UI Dialog modal
- **Empty States**: Helpful messages with call-to-action
- **Routing**: Lazy loading for performance
- **Styling**: Tailwind CSS with mobile-first approach

### Environment Variables Required
- `VITE_API_BASE_URL`: Backend API base URL (http://localhost:5000)
- `VITE_APP_NAME`: Application name (Thought Diary App)
- `VITE_APP_VERSION`: Application version (0.1.0)

### Testing Strategy
- Use Vitest as testing framework (Vite-native)
- Use Vue Test Utils for component testing
- Mock API calls with mock axios
- Mock localStorage for store tests
- Mock router for navigation tests
- Mock toast for notification tests
- Test user interactions (clicks, form inputs)
- Test computed properties and watchers
- Test edge cases and error handling
- Achieve 80%+ code coverage

### Package Management
- Use npm for dependency management
- Keep dependencies updated
- Regular security audits: `npm audit`
- Lock file (package-lock.json) committed

### Code Style
- Vue 3 Composition API with `<script setup>`
- TypeScript strict mode enabled
- ESLint for code quality
- Prettier for code formatting
- Consistent naming: PascalCase for components, camelCase for functions
- Props and emits typed
- TSDoc comments for public functions

### Accessibility
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus management in modals
- Color contrast compliance (WCAG 2.1 AA)
- Semantic HTML elements
- Screen reader friendly

### Performance
- Lazy loading for routes
- Optimized production builds
- Code splitting
- Minimal bundle size
- Efficient re-renders with Vue reactivity
- Debouncing not needed for current scope

---

## Success Criteria

✅ Vue 3 + TypeScript frontend fully functional
✅ Authentication working with localStorage token storage
✅ Token refresh with rotation implemented
✅ All diary CRUD operations working
✅ Sentiment analysis display with color-coded spans
✅ Pagination working (10 items per page)
✅ Real-time form validation (email, password)
✅ Toast notifications for global errors
✅ Inline validation errors in forms
✅ Network error retry mechanism
✅ Delete confirmation modal
✅ Empty states for no data
✅ Loading states with spinner
✅ Responsive design (mobile, tablet, desktop)
✅ ESLint and Prettier configured
✅ Tailwind CSS styling applied
✅ Comprehensive test suite with 80%+ coverage
✅ All routes with guards working
✅ Integration with backend API complete
✅ TypeScript strict mode with no errors
✅ CHANGELOG.md updated with implementation details
