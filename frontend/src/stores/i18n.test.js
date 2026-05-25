import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

// Mock i18n module before importing the store
vi.mock('../i18n', () => ({
  default: {
    global: {
      locale: {
        value: 'zh-CN'
      }
    }
  }
}))

// Mock Element Plus locales
vi.mock('element-plus/es/locale/lang/zh-cn', () => ({
  default: { name: 'zh-cn' }
}))

vi.mock('element-plus/es/locale/lang/en', () => ({
  default: { name: 'en' }
}))

import { useI18nStore } from './i18n'

const PREFERENCES_KEY = 'git-rg-preferences'

describe('I18n Store - Task 4.1 Basic Structure', () => {
  beforeEach(() => {
    // Create a fresh Pinia instance for each test
    setActivePinia(createPinia())
    // Clear localStorage before each test
    localStorage.clear()
  })

  afterEach(() => {
    // Clean up localStorage after each test
    localStorage.clear()
  })

  it('should initialize with default locale zh-CN (Requirement 4.1)', () => {
    const store = useI18nStore()
    expect(store.locale).toBe('zh-CN')
  })

  it('should provide currentLocale getter (Requirement 4.3)', () => {
    const store = useI18nStore()
    expect(store.currentLocale).toBe('zh-CN')
  })

  it('should have currentLocale getter return the same value as locale state', () => {
    const store = useI18nStore()
    expect(store.currentLocale).toBe(store.locale)
  })
})

describe('I18n Store - Task 4.2 Language Switching Actions', () => {
  beforeEach(() => {
    // Create a fresh Pinia instance for each test
    setActivePinia(createPinia())
    // Clear localStorage before each test
    localStorage.clear()
  })

  afterEach(() => {
    // Clean up localStorage after each test
    localStorage.clear()
  })

  describe('setLocale method', () => {
    it('should update locale state to zh-CN (Requirement 4.2)', () => {
      const store = useI18nStore()
      store.setLocale('zh-CN')
      expect(store.locale).toBe('zh-CN')
    })

    it('should update locale state to en-US (Requirement 4.2)', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      expect(store.locale).toBe('en-US')
    })

    it('should validate locale value and accept zh-CN (Requirement 14.2)', () => {
      const store = useI18nStore()
      expect(() => store.setLocale('zh-CN')).not.toThrow()
    })

    it('should validate locale value and accept en-US (Requirement 14.2)', () => {
      const store = useI18nStore()
      expect(() => store.setLocale('en-US')).not.toThrow()
    })

    it('should reject invalid locale value (Requirement 14.2, 14.4)', () => {
      const store = useI18nStore()
      expect(() => store.setLocale('fr-FR')).toThrow()
    })

    it('should reject empty string locale (Requirement 14.2, 14.4)', () => {
      const store = useI18nStore()
      expect(() => store.setLocale('')).toThrow()
    })

    it('should reject null locale (Requirement 14.2, 14.4)', () => {
      const store = useI18nStore()
      expect(() => store.setLocale(null)).toThrow()
    })

    it('should reject undefined locale (Requirement 14.2, 14.4)', () => {
      const store = useI18nStore()
      expect(() => store.setLocale(undefined)).toThrow()
    })

    it('should reject numeric locale (Requirement 14.2, 14.4)', () => {
      const store = useI18nStore()
      expect(() => store.setLocale(123)).toThrow()
    })

    it('should reject object locale (Requirement 14.2, 14.4)', () => {
      const store = useI18nStore()
      expect(() => store.setLocale({})).toThrow()
    })

    it('should throw error with descriptive message for invalid locale', () => {
      const store = useI18nStore()
      expect(() => store.setLocale('invalid')).toThrow(/Invalid locale/)
    })

    it('should save locale to localStorage when set (Requirement 6.1)', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      
      const stored = JSON.parse(localStorage.getItem(PREFERENCES_KEY))
      expect(stored.locale).toBe('en-US')
    })

    it('should preserve existing preferences when updating locale', () => {
      // Pre-populate localStorage with theme preference
      localStorage.setItem(PREFERENCES_KEY, JSON.stringify({ theme: 'dark' }))
      
      const store = useI18nStore()
      store.setLocale('en-US')
      
      const stored = JSON.parse(localStorage.getItem(PREFERENCES_KEY))
      expect(stored.locale).toBe('en-US')
      expect(stored.theme).toBe('dark')
    })

    it('should update currentLocale getter after setLocale (Requirement 4.3, 4.4)', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      expect(store.currentLocale).toBe('en-US')
    })

    it('should allow switching between locales multiple times', () => {
      const store = useI18nStore()
      
      store.setLocale('en-US')
      expect(store.locale).toBe('en-US')
      
      store.setLocale('zh-CN')
      expect(store.locale).toBe('zh-CN')
      
      store.setLocale('en-US')
      expect(store.locale).toBe('en-US')
    })

    it('should be idempotent - setting same locale multiple times', () => {
      const store = useI18nStore()
      
      store.setLocale('en-US')
      const firstState = store.locale
      
      store.setLocale('en-US')
      const secondState = store.locale
      
      expect(firstState).toBe(secondState)
      expect(store.locale).toBe('en-US')
    })
  })
})
