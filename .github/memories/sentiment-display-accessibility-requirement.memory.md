# Sentiment Display — WCAG 2.1 AA Compliance Gap Analysis

> Research date: 2026-03-10
> Scope: All UI surfaces that display sentiment data, without implementation detail

---

## Surfaces Under Review

| Surface | File | Sentiment features |
|---|---|---|
| Diary card (list) | `frontend/src/components/DiaryCard.vue` | Inline highlighted spans + positive/negative counts with icons |
| Diary detail view | `frontend/src/views/DiaryDetail.vue` | Inline highlighted spans + positive/negative counts with icons |
| Stats dashboard | `frontend/src/components/StatsCard.vue` | Coloured gradient cards (positive, negative, neutral, total entries) |
| Global styles | `frontend/src/style.css` | `.positive` / `.negative` span base rules |

### How sentiment markup is produced

The backend AI service (`backend/app/services/ai_service.py`) wraps sentiment-bearing words with plain HTML spans:

```html
<span class="positive">excitement</span>
<span class="negative">anxious</span>
```

These spans are injected into `analyzed_content`, which is rendered via `v-html` in both `DiaryCard.vue` and `DiaryDetail.vue`. No ARIA attributes, roles, or accessible names are added by either the backend or the frontend.

---

## WCAG 2.1 AA Criteria Examined

### 1. WCAG 1.4.3 — Contrast (Minimum) · Level AA

**Requirement:** Text against its background must meet a contrast ratio of at least **4.5:1** for normal text or **3:1** for large text (≥18 pt / ≥14 pt bold).

#### Inline sentiment spans — text contrast

The spans use `color: white` against coloured backgrounds. Computed relative-luminance contrast ratios (WCAG algorithm):

| Context | Background hex | Background name | vs white foreground | Ratio | Result |
|---|---|---|---|---|---|
| Light mode — positive | `#10b981` | Tailwind `emerald-500` | white | **2.53 : 1** | FAIL |
| Light mode — negative | `#ef4444` | Tailwind `red-500` | white | **3.76 : 1** | FAIL |
| Dark mode — positive | `#059669` | Tailwind `emerald-600` | white | **3.77 : 1** | FAIL |
| Dark mode — negative | `#dc2626` | Tailwind `red-600` | white | **4.83 : 1** | PASS |

Three of four combinations fail the 4.5:1 AA threshold. Text inside these spans is inline body copy, so the 3:1 large-text exception does not apply.

Sources:
- `frontend/src/style.css` lines 7–28 (global span rules)
- `frontend/src/components/DiaryCard.vue` lines 165–185 (scoped overrides)
- `frontend/src/views/DiaryDetail.vue` lines 331–352 (scoped overrides)

#### Stats cards — text contrast on gradient backgrounds

`StatsCard.vue` uses CSS gradients as backgrounds. WCAG requires that contrast be evaluated at the worst-case (lightest) point of the gradient.

| Card | Gradient start (worst case) | vs white text | Ratio | Text size | Result |
|---|---|---|---|---|---|
| Positive entries | `#22c55e` (`green-500`) | white | **2.28 : 1** | `text-3xl font-bold` (large) / `text-sm` (small) | FAIL (both sizes) |
| Negative entries | `#ef4444` (`red-500`) | white | **3.76 : 1** | `text-3xl font-bold` (large) / `text-sm` (small) | PASS large (3:1) / FAIL small (4.5:1) |
| Total entries | `#3b82f6` (`blue-500`) | white | **3.68 : 1** | `text-3xl font-bold` (large) / `text-sm` (small) | PASS large / FAIL small |
| Neutral entries | `#6b7280` (`gray-500`) | white | **4.83 : 1** | both sizes | PASS |

The label text (e.g., "Positive Entries", "Total Entries") is `text-sm font-medium` (~14 px, medium weight) — below the large-text threshold — so requires 4.5:1 and fails on the green, red, and blue cards.

Source: `frontend/src/components/StatsCard.vue` lines 2–91

---

### 2. WCAG 1.4.1 — Use of Color · Level A

**Requirement:** Color must not be the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element.

**Gap:** The `<span class="positive">` and `<span class="negative">` elements use background color as the **sole** indicator of sentiment polarity. There is no:

- icon or symbol embedded within the span
- underline, border, or non-colour visual treatment
- visible text label (e.g., "(positive)") inside the span

A user who cannot perceive colour differences (e.g., red-green colour blindness affects ~8% of males) cannot distinguish a positive highlight from a negative one, or from unhighlighted text.

This criterion is Level A (a baseline requirement, not just AA), making it the most critical gap in the sentiment display.

---

### 3. WCAG 1.3.1 — Info and Relationships · Level A

**Requirement:** Information conveyed through presentation (visual formatting) must also be determinable programmatically.

**Gap:** The semantic fact that a word is classified as *positive* or *negative* sentiment exists only in the CSS class name (`class="positive"`, `class="negative"`). CSS class names are not an accessible mechanism — assistive technologies do not interpret them as conveying meaning. The information relationship between a highlighted word and its sentiment category is therefore **not programmatically determinable**.

There is no:
- `role` attribute that categorises the span as a meaningful landmark or annotation
- `aria-label` or `aria-describedby` that names the sentiment type
- visually hidden text within the span describing the category

---

### 4. WCAG 4.1.2 — Name, Role, Value · Level A

**Requirement:** For all user interface components (including custom interactive widgets and informational regions), the name and role must be programmatically determinable.

**Gap:** While the sentiment spans are not interactive, they carry **informational role** that screen reader users need in order to understand the content. The spans have no `role`, no accessible name, and no value that communicates the sentiment type. A screen reader will simply announce the highlighted word's text with no indication that it has been categorised as positive or negative sentiment.

This is closely related to 1.3.1 but focuses on the component-level expectation that meaningful UI annotations expose their purpose programmatically.

---

### 5. WCAG 1.4.11 — Non-text Contrast · Level AA

**Requirement:** Visual presentation of UI components and graphical objects must have a contrast ratio of at least **3:1** against adjacent colour(s).

**Gap (partial):** The sentiment icon SVGs (smiley face / thumbs-face) in the positive/negative count rows of `DiaryCard.vue` and `DiaryDetail.vue` use:

- Light mode: `text-green-600` (`#16a34a`) and `text-red-600` (`#dc2626`) against white (`#ffffff`) background
  - Green-600 vs white: approx. **3.30 : 1** — marginally passes 3:1
  - Red-600 vs white: approx. **4.83 : 1** — passes

These icons pass for light mode but the evaluation should be re-verified in dark mode (backgrounds `gray-50` / `gray-700` depending on component region). The sentiment span backgrounds themselves also create a contrast boundary against adjacent body text / page backgrounds that would benefit from review under 1.4.11.

---

## Summary of Gaps by Criticality

| # | WCAG Criterion | Level | Surfaces Affected | Status |
|---|---|---|---|---|
| 1 | 1.4.1 Use of Color | **A** | DiaryCard, DiaryDetail (inline spans) | FAIL |
| 2 | 1.3.1 Info and Relationships | **A** | DiaryCard, DiaryDetail (inline spans) | FAIL |
| 3 | 4.1.2 Name, Role, Value | **A** | DiaryCard, DiaryDetail (inline spans) | FAIL |
| 4 | 1.4.3 Contrast (inline spans) | **AA** | DiaryCard, DiaryDetail — light mode positive, light mode negative, dark mode positive | FAIL |
| 5 | 1.4.3 Contrast (stats cards) | **AA** | StatsCard — green, red, blue card label text | FAIL |
| 6 | 1.4.11 Non-text Contrast | **AA** | DiaryCard, DiaryDetail icon colours | Marginal / needs dark-mode verification |

Three of the six gaps are Level A (more fundamental than AA). Notably, no sentiment information is accessible to screen reader users at all, since colour is the only distinguishing mechanism and no programmatic association of sentiment role/label exists.

---

## Reference: Relevant Backend Markup Structure

The backend produces spans such as:

```html
I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span> today.
```

Any accessibility solution will need to account for the fact that this markup originates from an LLM response and is stored in the database. Frontend post-processing or backend prompt engineering would be necessary to enrich the markup.
