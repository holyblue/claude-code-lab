import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { timeEntriesApi } from '../api'
import type { TimeEntry, TimeEntryCreate, TimeEntryUpdate } from '../types'

export const useTimeEntryStore = defineStore('timeEntry', () => {
  // State
  const timeEntries = ref<TimeEntry[]>([])
  const currentTimeEntry = ref<TimeEntry | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const getTimeEntriesByDate = computed(() => (date: string) =>
    timeEntries.value.filter((entry) => entry.date === date)
  )

  const getTotalHoursByDate = computed(() => (date: string) => {
    const entries = getTimeEntriesByDate.value(date)
    return entries.reduce((sum, entry) => sum + entry.hours, 0)
  })

  // Actions
  async function fetchTimeEntries(params?: {
    skip?: number
    limit?: number
    start_date?: string
    end_date?: string
    project_id?: number
  }) {
    loading.value = true
    error.value = null
    try {
      const response = await timeEntriesApi.getAll(params)
      timeEntries.value = response.items
      return response
    } catch (e) {
      error.value = e instanceof Error ? e.message : '載入工時記錄失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchTimeEntryById(id: number) {
    loading.value = true
    error.value = null
    try {
      const entry = await timeEntriesApi.getById(id)
      currentTimeEntry.value = entry
      return entry
    } catch (e) {
      error.value = e instanceof Error ? e.message : '載入工時記錄失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function createTimeEntry(data: TimeEntryCreate) {
    loading.value = true
    error.value = null
    try {
      const entry = await timeEntriesApi.create(data)
      timeEntries.value.push(entry)
      return entry
    } catch (e) {
      error.value = e instanceof Error ? e.message : '新增工時記錄失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateTimeEntry(id: number, data: TimeEntryUpdate) {
    loading.value = true
    error.value = null
    try {
      console.log('📡 Store: 發送 PATCH 請求，ID:', id, '資料:', data)
      const entry = await timeEntriesApi.update(id, data)
      console.log('📡 Store: 收到回應:', entry)
      const index = timeEntries.value.findIndex((e) => e.id === id)
      if (index !== -1) {
        timeEntries.value[index] = entry
      }
      if (currentTimeEntry.value?.id === id) {
        currentTimeEntry.value = entry
      }
      return entry
    } catch (e) {
      console.error('📡 Store: 請求失敗:', e)
      error.value = e instanceof Error ? e.message : '更新工時記錄失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteTimeEntry(id: number) {
    loading.value = true
    error.value = null
    try {
      await timeEntriesApi.delete(id)
      const index = timeEntries.value.findIndex((e) => e.id === id)
      if (index !== -1) {
        timeEntries.value.splice(index, 1)
      }
      if (currentTimeEntry.value?.id === id) {
        currentTimeEntry.value = null
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : '刪除工時記錄失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchByDateRange(startDate: string, endDate: string) {
    loading.value = true
    error.value = null
    try {
      const entries = await timeEntriesApi.getByDateRange(startDate, endDate)
      timeEntries.value = entries
      return entries
    } catch (e) {
      error.value = e instanceof Error ? e.message : '載入工時記錄失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    timeEntries,
    currentTimeEntry,
    loading,
    error,
    // Getters
    getTimeEntriesByDate,
    getTotalHoursByDate,
    // Actions
    fetchTimeEntries,
    fetchTimeEntryById,
    createTimeEntry,
    updateTimeEntry,
    deleteTimeEntry,
    fetchByDateRange,
  }
})
