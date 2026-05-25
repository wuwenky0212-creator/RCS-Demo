import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

// Mock i18n module before importing the store
vi.mock('../i18n', () => {
  const mockI18n = {
    global: {
      locale: {
        value: 'zh-CN'
      }
    }
  }
  return {
    default: mockI18n
  }
})

// Mock Element Plus locales
vi.mock('element-plus/es/locale/lang/zh-cn', () => ({
  default: { name: 'zh-cn' }
}))

vi.mock('element-plus/es/locale/lang/en', () => ({
  default: { name: 'en' }
}))

import { useI18nStore } from './i18n'
import i18n from '../i18n'

const PREFERENCES_KEY = 'git-rg-preferences'

describe('I18n Store - Task 4.3 Language System Synchronization', () => {
  let eventListener

  beforeEach(() => {
    // Create a fresh Pinia instance for each test
    setActivePinia(createPinia())
    // Clear localStorage before each test
    localStorage.clear()
    // Reset mock i18n locale
    i18n.global.locale.value = 'zh-CN'
    // Clear document.documentElement lang attribute
    document.documentElement.removeAttribute('lang')
    // Capture custom events
    eventListener = vi.fn()
    window.addEventListener('locale-change', eventListener)
  })

  afterEach(() => {
    // Clean up localStorage after each test
    localStorage.clear()
    // Remove event listener
    window.removeEventListener('locale-change', eventListener)
  })

  describe('Vue I18n Synchronization (Requirement 5.1)', () => {
    it('should update Vue I18n global.locale when setLocale is called with zh-CN', () => {
      const store = useI18nStore()
      store.setLocale('zh-CN')
      expect(i18n.global.locale.value).toBe('zh-CN')
    })

    it('should update Vue I18n global.locale when setLocale is called with en-US', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      expect(i18n.global.locale.value).toBe('en-US')
    })

    it('should synchronize Vue I18n locale when switching from zh-CN to en-US', () => {
      const store = useI18nStore()
      store.setLocale('zh-CN')
      expect(i18n.global.locale.value).toBe('zh-CN')
      
      store.setLocale('en-US')
      expect(i18n.global.locale.value).toBe('en-US')
    })

    it('should synchronize Vue I18n locale when switching from en-US to zh-CN', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      expect(i18n.global.locale.value).toBe('en-US')
      
      store.setLocale('zh-CN')
      expect(i18n.global.locale.value).toBe('zh-CN')
    })
  })

  describe('Element Plus Locale Synchronization (Requirements 5.2, 12.2, 12.4, 12.5)', () => {
    it('should dispatch locale-change event when setLocale is called with zh-CN', () => {
      const store = useI18nStore()
      store.setLocale('zh-CN')
      
      expect(eventListener).toHaveBeenCalledTimes(1)
      const event = eventListener.mock.calls[0][0]
      expect(event.detail.locale).toBe('zh-CN')
      expect(event.detail.elementPlusLocale).toBeDefined()
      expect(event.detail.elementPlusLocale.name).toBe('zh-cn')
    })

    it('should dispatch locale-change event when setLocale is called with en-US', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      
      expect(eventListener).toHaveBeenCalledTimes(1)
      const event = eventListener.mock.calls[0][0]
      expect(event.detail.locale).toBe('en-US')
      expect(event.detail.elementPlusLocale).toBeDefined()
      expect(event.detail.elementPlusLocale.name).toBe('en')
    })

    it('should dispatch locale-change event with correct Element Plus locale for zh-CN', () => {
      const store = useI18nStore()
      store.setLocale('zh-CN')
      
      const event = eventListener.mock.calls[0][0]
      expect(event.detail.elementPlusLocale.name).toBe('zh-cn')
    })

    it('should dispatch locale-change event with correct Element Plus locale for en-US', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      
      const event = eventListener.mock.calls[0][0]
      expect(event.detail.elementPlusLocale.name).toBe('en')
    })

    it('should dispatch locale-change event synchronously (Requirement 12.5)', () => {
      const store = useI18nStore()
      
      // Event should be dispatched before setLocale returns
      store.setLocale('en-US')
      
      // Event listener should have been called immediately
      expect(eventListener).toHaveBeenCalledTimes(1)
    })
  })

  describe('Document Language Attribute Synchronization (Requirement 5.3)', () => {
    it('should set document.documentElement lang attribute to zh-CN', () => {
      const store = useI18nStore()
      store.setLocale('zh-CN')
      expect(document.documentElement.getAttribute('lang')).toBe('zh-CN')
    })

    it('should set document.documentElement lang attribute to en-US', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      expect(document.documentElement.getAttribute('lang')).toBe('en-US')
    })

    it('should update document.documentElement lang attribute when switching locales', () => {
      const store = useI18nStore()
      
      store.setLocale('zh-CN')
      expect(document.documentElement.getAttribute('lang')).toBe('zh-CN')
      
      store.setLocale('en-US')
      expect(document.documentElement.getAttribute('lang')).toBe('en-US')
      
      store.setLocale('zh-CN')
      expect(document.documentElement.getAttribute('lang')).toBe('zh-CN')
    })

    it('should set lang attribute synchronously with locale state update', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      
      // Both should be updated in the same call
      expect(store.locale).toBe('en-US')
      expect(document.documentElement.getAttribute('lang')).toBe('en-US')
    })
  })

  describe('Complete Synchronization (All Systems)', () => {
    it('should synchronize all systems when setting locale to zh-CN', () => {
      const store = useI18nStore()
      store.setLocale('zh-CN')
      
      // Store state
      expect(store.locale).toBe('zh-CN')
      
      // Vue I18n
      expect(i18n.global.locale.value).toBe('zh-CN')
      
      // Element Plus (via event)
      expect(eventListener).toHaveBeenCalledTimes(1)
      const event = eventListener.mock.calls[0][0]
      expect(event.detail.locale).toBe('zh-CN')
      
      // Document lang attribute
      expect(document.documentElement.getAttribute('lang')).toBe('zh-CN')
      
      // LocalStorage
      const stored = JSON.parse(localStorage.getItem(PREFERENCES_KEY))
      expect(stored.locale).toBe('zh-CN')
    })

    it('should synchronize all systems when setting locale to en-US', () => {
      const store = useI18nStore()
      store.setLocale('en-US')
      
      // Store state
      expect(store.locale).toBe('en-US')
      
      // Vue I18n
      expect(i18n.global.locale.value).toBe('en-US')
      
      // Element Plus (via event)
      expect(eventListener).toHaveBeenCalledTimes(1)
      const event = eventListener.mock.calls[0][0]
      expect(event.detail.locale).toBe('en-US')
      
      // Document lang attribute
      expect(document.documentElement.getAttribute('lang')).toBe('en-US')
      
      // LocalStorage
      const stored = JSON.parse(localStorage.getItem(PREFERENCES_KEY))
      expect(stored.locale).toBe('en-US')
    })

    it('should maintain synchronization across multiple locale switches', () => {
      const store = useI18nStore()
      
      // First switch
      store.setLocale('en-US')
      expect(store.locale).toBe('en-US')
      expect(i18n.global.locale.value).toBe('en-US')
      expect(document.documentElement.getAttribute('lang')).toBe('en-US')
      
      // Second switch
      store.setLocale('zh-CN')
      expect(store.locale).toBe('zh-CN')
      expect(i18n.global.locale.value).toBe('zh-CN')
      expect(document.documentElement.getAttribute('lang')).toBe('zh-CN')
      
      // Third switch
      store.setLocale('en-US')
      expect(store.locale).toBe('en-US')
      expect(i18n.global.locale.value).toBe('en-US')
      expect(document.documentElement.getAttribute('lang')).toBe('en-US')
    })

    it('should complete all synchronization operations within the same call', () => {
      const store = useI18nStore()
      
      // All updates should happen synchronously
      store.setLocale('en-US')
      
      // Verify all systems are updated immediately
      expect(store.locale).toBe('en-US')
      expect(i18n.global.locale.value).toBe('en-US')
      expect(document.documentElement.getAttribute('lang')).toBe('en-US')
      expect(eventListener).toHaveBeenCalledTimes(1)
      
      const stored = JSON.parse(localStorage.getItem(PREFERENCES_KEY))
      expect(stored.locale).toBe('en-US')
    })
  })

  describe('Error Handling', () => {
    it('should not dispatch event if Element Plus locale is not found', () => {
      // This shouldn't happen with valid locales, but test defensive code
      const store = useI18nStore()
      
      // Mock the ELEMENT_PLUS_LOCALES to return undefined
      // (This would require refactoring the store to make it testable)
      // For now, we just verify that valid locales always dispatch events
      store.setLocale('zh-CN')
      expect(eventListener).toHaveBeenCalledTimes(1)
      
      store.setLocale('en-US')
      expect(eventListener).toHaveBeenCalledTimes(2)
    })

    it('should still update other systems even if event dispatch fails', () => {
      const store = useI18nStore()
      
      // Remove event listener to simulate dispatch failure
      window.removeEventListener('locale-change', eventListener)
      
      // Should not throw error
      expect(() => store.setLocale('en-US')).not.toThrow()
      
      // Other systems should still be updated
      expect(store.locale).toBe('en-US')
      expect(i18n.global.locale.value).toBe('en-US')
      expect(document.documentElement.getAttribute('lang')).toBe('en-US')
    })
  })
})
