import { defineStore } from 'pinia'

export const useLanguageStore = defineStore('language', {
  state: () => ({
    currentLocale: 'en',
  }),
  
  actions: {
    setLocale(locale: string) {
      this.currentLocale = locale
      if (process.client) {
        localStorage.setItem('preferred_language', locale)
      }
    },
    
    initLocale() {
      if (process.client) {
        const saved = localStorage.getItem('preferred_language')
        if (saved) {
          this.currentLocale = saved
        }
      }
    },
  },
})