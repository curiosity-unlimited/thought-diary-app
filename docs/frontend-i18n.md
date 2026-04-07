# Frontend Internationalization (i18n)

## Overview

The Thought Diary App supports multiple languages using [vue-i18n v9](https://vue-i18n.intlify.dev/) in Composition API mode. Currently supported locales are:

| Locale | Name | File |
|--------|------|------|
| `en` | English | `src/i18n/locales/en.json` |
| `zh-tw` | 繁體中文 (Traditional Chinese) | `src/i18n/locales/zh-tw.json` |

---

## Architecture

```
frontend/src/
├── i18n/
│   ├── index.ts              # vue-i18n instance + locale detection
│   └── locales/
│       ├── en.json           # English translations
│       └── zh-tw.json        # Traditional Chinese translations
├── stores/ui.ts              # locale state + setLocale() / initLocale()
├── utils/dateFormatter.ts    # locale-aware date formatting
└── components/Navbar.vue     # language switcher UI
```

### Key design decisions

| Concern | Decision | Rationale |
|---------|----------|-----------|
| Library | vue-i18n v9 (Composition API mode) | Official Vue 3 solution |
| Storage | `localStorage` key `user_locale` | No backend changes required |
| Default | Browser language auto-detection | Better UX |
| Fallback | English (`en`) | Existing complete translations |

---

## Locale detection flow

1. On app start, `detectLocale()` in `i18n/index.ts` is called.
2. If `localStorage.getItem('user_locale')` is a supported locale, it is used.
3. Otherwise `navigator.language` is checked – any Chinese browser language maps to `zh-tw`.
4. Falls back to `en` if neither condition matches.

```typescript
// i18n/index.ts
export const detectLocale = (): SupportedLocale => {
  const stored = localStorage.getItem(LOCALE_STORAGE_KEY);
  if (stored && SUPPORTED_LOCALES.includes(stored as SupportedLocale)) {
    return stored as SupportedLocale;
  }
  const browserLang = navigator.language.toLowerCase();
  if (browserLang.startsWith('zh')) return 'zh-tw';
  return 'en';
};
```

---

## Translation file structure

Both `en.json` and `zh-tw.json` share the same key hierarchy:

```json
{
  "common":       { "cancel": "...", "save": "..." },
  "auth":         { "signInTitle": "...", "emailLabel": "..." },
  "validation":   { "emailRequired": "...", "passwordMin": "..." },
  "nav":          { "dashboard": "...", "logout": "..." },
  "diary":        { "myDiaries": "...", "createEntry": "..." },
  "stats":        { "totalEntries": "...", "positiveEntries": "..." },
  "deleteModal":  { "title": "...", "confirm": "..." },
  "profile":      { "title": "...", "accountInfo": "..." },
  "about":        { "title": "...", "keyFeatures": "..." },
  "home":         { "title": "...", "getStarted": "..." },
  "notFound":     { "title": "...", "goHome": "..." },
  "loading":      { "loadingDashboard": "..." },
  "errors":       { "emailExists": "...", "sessionExpired": "..." },
  "success":      { "diaryDeleted": "...", "loggedOut": "..." },
  "pagination":   { "previousPage": "...", "nextPage": "..." },
  "router":       { "home": "...", "dashboard": "..." },
  "language":     { "english": "...", "traditionalChinese": "..." }
}
```

Interpolation: use `{variable}` in messages, e.g.:
```json
{ "contentMin": "Content must be at least {min} characters" }
```

In a component:
```vue
{{ $t('validation.contentMin', { min: 10 }) }}
```

---

## Adding a new translation key

1. Add the key to `src/i18n/locales/en.json` in the appropriate namespace.
2. Add the corresponding translation to `src/i18n/locales/zh-tw.json`.
3. Use `$t('namespace.key')` in templates or `t('namespace.key')` in `<script setup>`.

---

## Adding a new language

1. Create `src/i18n/locales/<locale>.json` with all keys from `en.json`.
2. In `src/i18n/index.ts`, add the locale to `SUPPORTED_LOCALES` and import the new file.
3. In `src/components/Navbar.vue`, add an entry to `availableLocales`.
4. In `src/utils/dateFormatter.ts`, add the locale mapping to `LOCALE_MAP`.

```typescript
// i18n/index.ts
import ja from './locales/ja.json';
export const SUPPORTED_LOCALES = ['en', 'zh-tw', 'ja'] as const;

const i18n = createI18n({
  messages: { en, 'zh-tw': zhTw, ja },
});
```

---

## Changing the active locale at runtime

Call `uiStore.setLocale()` from any component:

```typescript
import { useUIStore } from '@/stores/ui';
import type { SupportedLocale } from '@/i18n';

const uiStore = useUIStore();
uiStore.setLocale('zh-tw' as SupportedLocale);
```

This:
- Updates the `locale` ref in the store.
- Persists to `localStorage` under `user_locale`.
- Syncs with the vue-i18n global locale so all `$t()` calls re-render immediately.

---

## Locale-aware date formatting

Import from `utils/dateFormatter.ts`:

```typescript
import { formatDateTime, formatDate } from '@/utils/dateFormatter';

// "January 15, 2024, 10:30 AM" (en) or "2024年1月15日 上午10:30" (zh-TW)
const display = formatDateTime(diary.created_at);
```

The formatter reads `localStorage.getItem('user_locale')` at call time, so it always reflects the currently active locale.

---

## API error message translation

`services/api.ts` maps known English backend error strings to i18n keys:

```typescript
const errorMessageMap: Record<string, string> = {
  'Email already registered': 'errors.emailExists',
  'Token has expired': 'errors.tokenExpired',
  'Invalid token': 'errors.invalidToken',
  'Authorization token is missing': 'errors.authMissing',
};
```

Unknown backend messages fall through untranslated so no information is lost.

---

## Testing

The test setup file (`tests/unit/setup.ts`) registers a shared i18n instance (English locale) globally for all component tests:

```typescript
const testI18n = createI18n({ locale: 'en', messages: { en, 'zh-tw': zhTw }, legacy: false });
config.global.plugins = [...(config.global.plugins || []), testI18n];
```

This means individual test files do **not** need to configure i18n manually unless they are specifically testing locale-switching behaviour.
