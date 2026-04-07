<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from '../composables/useI18n'

interface DiaryEntry {
  id: string
  title: string
  content: string
  createdAt: string
}

const ENTRIES_KEY = 'thought-diary-entries'

function loadEntries(): DiaryEntry[] {
  try {
    const raw = localStorage.getItem(ENTRIES_KEY)
    return raw ? (JSON.parse(raw) as DiaryEntry[]) : []
  } catch {
    return []
  }
}

function saveEntries(entries: DiaryEntry[]) {
  localStorage.setItem(ENTRIES_KEY, JSON.stringify(entries))
}

const { t, currentLocale } = useI18n()
const entries = ref<DiaryEntry[]>(loadEntries())
const showForm = ref(false)
const editingId = ref<string | null>(null)
const formTitle = ref('')
const formContent = ref('')

const entryCount = computed(() => t.value.entriesCount(entries.value.length))

function openNewForm() {
  editingId.value = null
  formTitle.value = ''
  formContent.value = ''
  showForm.value = true
}

function editEntry(entry: DiaryEntry) {
  editingId.value = entry.id
  formTitle.value = entry.title
  formContent.value = entry.content
  showForm.value = true
}

function cancelForm() {
  showForm.value = false
  editingId.value = null
  formTitle.value = ''
  formContent.value = ''
}

function submitForm() {
  if (!formTitle.value.trim() && !formContent.value.trim()) return

  if (editingId.value) {
    const idx = entries.value.findIndex((e) => e.id === editingId.value)
    if (idx !== -1) {
      const existing = entries.value[idx]
      if (existing) {
        entries.value[idx] = {
          id: existing.id,
          createdAt: existing.createdAt,
          title: formTitle.value.trim(),
          content: formContent.value.trim(),
        }
      }
    }
  } else {
    entries.value.unshift({
      id: generateId(),
      title: formTitle.value.trim(),
      content: formContent.value.trim(),
      createdAt: new Date().toISOString(),
    })
  }

  saveEntries(entries.value)
  cancelForm()
}

function deleteEntry(id: string) {
  if (!window.confirm(t.value.confirmDelete)) return
  entries.value = entries.value.filter((e) => e.id !== id)
  saveEntries(entries.value)
}

function generateId(): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  return Date.now().toString(36) + Math.random().toString(36).slice(2)
}

function formatDate(iso: string): string {
  const localeTag = currentLocale.value === 'zh-tw' ? 'zh-TW' : 'en'
  return new Date(iso).toLocaleDateString(localeTag, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}
</script>

<template>
  <div class="diary">
    <div class="diary-header">
      <span class="entry-count">{{ entryCount }}</span>
      <button class="btn-primary" @click="openNewForm">{{ t.newEntry }}</button>
    </div>

    <!-- Entry form -->
    <div v-if="showForm" class="form-card">
      <div class="form-group">
        <label for="entry-title">{{ t.titleLabel }}</label>
        <input
          id="entry-title"
          v-model="formTitle"
          type="text"
          :placeholder="t.titlePlaceholder"
          class="form-input"
        />
      </div>
      <div class="form-group">
        <label for="entry-content">{{ t.contentLabel }}</label>
        <textarea
          id="entry-content"
          v-model="formContent"
          :placeholder="t.contentPlaceholder"
          class="form-textarea"
          rows="5"
        />
      </div>
      <div class="form-actions">
        <button class="btn-primary" @click="submitForm">{{ t.save }}</button>
        <button class="btn-secondary" @click="cancelForm">{{ t.cancel }}</button>
      </div>
    </div>

    <!-- Empty state -->
    <p v-if="entries.length === 0 && !showForm" class="empty-state">
      {{ t.emptyState }}
    </p>

    <!-- Entry list -->
    <ul v-else class="entry-list">
      <li v-for="entry in entries" :key="entry.id" class="entry-card">
        <div class="entry-header">
          <h2 class="entry-title">{{ entry.title || '…' }}</h2>
          <span class="entry-date">{{ formatDate(entry.createdAt) }}</span>
        </div>
        <p class="entry-content">{{ entry.content }}</p>
        <div class="entry-actions">
          <button class="btn-secondary btn-sm" @click="editEntry(entry)">✏️</button>
          <button class="btn-danger btn-sm" @click="deleteEntry(entry.id)">🗑️</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.diary {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
}

.diary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.entry-count {
  font-size: 0.9rem;
  opacity: 0.6;
}

.form-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  opacity: 0.8;
  text-align: left;
}

.form-input,
.form-textarea {
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.08);
  color: inherit;
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
}

.form-input:focus,
.form-textarea:focus {
  outline: 2px solid #646cff;
  border-color: #646cff;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
}

.empty-state {
  opacity: 0.55;
  font-size: 1rem;
  margin-top: 2rem;
}

.entry-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.entry-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  text-align: left;
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.5rem;
}

.entry-title {
  font-size: 1.1rem;
  margin: 0;
}

.entry-date {
  font-size: 0.8rem;
  opacity: 0.55;
}

.entry-content {
  margin: 0 0 0.75rem;
  white-space: pre-wrap;
  line-height: 1.6;
}

.entry-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-primary {
  background-color: #646cff;
  color: #fff;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #535bf2;
}

.btn-secondary {
  background: transparent;
  color: inherit;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: border-color 0.2s;
}

.btn-secondary:hover {
  border-color: #646cff;
}

.btn-danger {
  background: transparent;
  color: #ff6b6b;
  border: 1px solid rgba(255, 107, 107, 0.4);
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-danger:hover {
  background-color: rgba(255, 107, 107, 0.15);
}

.btn-sm {
  padding: 0.3rem 0.6rem;
  font-size: 0.85rem;
}

@media (prefers-color-scheme: light) {
  .form-card,
  .entry-card {
    background: rgba(0, 0, 0, 0.03);
    border-color: rgba(0, 0, 0, 0.1);
  }

  .form-input,
  .form-textarea {
    background: #fff;
    border-color: rgba(0, 0, 0, 0.2);
    color: #213547;
  }

  .btn-secondary {
    border-color: rgba(0, 0, 0, 0.25);
  }
}
</style>
