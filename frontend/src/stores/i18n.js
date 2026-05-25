import { defineStore } from 'pinia'
import i18n from '../i18n'

const PREFERENCES_KEY = 'git-rg-preferences'

function loadPreferences() {
  try {
    const stored = localStorage.getItem(PREFERENCES_KEY)
    if (!stored) return null
    const preferences = JSON.parse(stored)
    if (typeof preferences !== 'object' || preferences === null) return null
    return preferences
  } catch (error) {
    console.warn('[I18n Store] Failed to load preferences:', error.message)
    try { localStorage.removeItem(PREFERENCES_KEY) } catch (_) {}
    return null
  }
}

function savePreferences(preferences) {
  try {
    localStorage.setItem(PREFERENCES_KEY, JSON.stringify(preferences))
  } catch (error) {
    console.warn('[I18n Store] Failed to save preferences:', error.message)
  }
}

export const useI18nStore = defineStore('i18n', {
  state: () => ({
    locale: 'zh-CN'
  }),

  getters: {
    currentLocale: (state) => state.locale
  },

  actions: {
    initLocale() {
      const preferences = loadPreferences()
      let localeToApply = 'zh-CN'

      if (preferences?.locale && ['zh-CN', 'en-US'].includes(preferences.locale)) {
        localeToApply = preferences.locale
      }

      this.setLocale(localeToApply)
    },

    setLocale(locale) {
      if (!['zh-CN', 'en-US'].includes(locale)) {
        throw new Error(`Invalid locale: "${locale}". Must be 'zh-CN' or 'en-US'.`)
      }

      this.locale = locale
      i18n.global.locale.value = locale
      document.documentElement.setAttribute('lang', locale)

      const preferences = loadPreferences() || {}
      preferences.locale = locale
      savePreferences(preferences)
    }
  }
})
