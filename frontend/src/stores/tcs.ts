/**
 * TCS 同步狀態管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { tcsApi } from '../api'
import type { TCSSyncLog, TCSAutoFillResponse } from '../types'

const SYNC_LOGS_KEY = 'tcs_sync_logs'
const MAX_LOGS = 50

export const useTCSStore = defineStore('tcs', () => {
  // State
  const syncing = ref(false)
  const syncLogs = ref<TCSSyncLog[]>([])
  const lastSyncResult = ref<TCSAutoFillResponse | null>(null)

  // 從 localStorage 載入日誌
  const loadLogs = () => {
    try {
      const stored = localStorage.getItem(SYNC_LOGS_KEY)
      if (stored) {
        const logs = JSON.parse(stored)
        // 轉換 timestamp 為 Date 物件
        syncLogs.value = logs.map((log: any) => ({
          ...log,
          timestamp: new Date(log.timestamp)
        }))
      }
    } catch (error) {
      console.error('載入同步日誌失敗:', error)
      syncLogs.value = []
    }
  }

  // 儲存日誌到 localStorage
  const saveLogs = () => {
    try {
      localStorage.setItem(SYNC_LOGS_KEY, JSON.stringify(syncLogs.value))
    } catch (error) {
      console.error('儲存同步日誌失敗:', error)
    }
  }

  // Getters
  const recentLogs = computed(() => syncLogs.value.slice(0, 10))
  
  const successCount = computed(() => 
    syncLogs.value.filter(log => log.status === 'success').length
  )
  
  const failedCount = computed(() => 
    syncLogs.value.filter(log => log.status === 'failed').length
  )

  const getLogsByDate = computed(() => (date: string) =>
    syncLogs.value.filter(log => log.date === date)
  )

  const hasSuccessfulSync = computed(() => (date: string) =>
    syncLogs.value.some(log => log.date === date && log.status === 'success' && !log.dry_run)
  )

  // Actions
  /**
   * 同步工時到 TCS 系統
   */
  async function syncToTCS(date: string, dryRun: boolean = true): Promise<TCSAutoFillResponse> {
    syncing.value = true
    const logId = `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

    try {
      const result = await tcsApi.syncToTCS(date, dryRun)

      // 記錄成功日誌
      const log: TCSSyncLog = {
        id: logId,
        date,
        status: dryRun ? 'preview' : 'success',
        timestamp: new Date(),
        message: result.message,
        filled_count: result.filled_count,
        dry_run: dryRun
      }

      syncLogs.value.unshift(log)
      clearOldLogs()
      saveLogs()

      lastSyncResult.value = result

      return result
    } catch (error: any) {
      // 記錄失敗日誌
      const errorMessage = error.response?.data?.detail || error.message || '未知錯誤'
      
      const log: TCSSyncLog = {
        id: logId,
        date,
        status: 'failed',
        timestamp: new Date(),
        message: '同步失敗',
        error: errorMessage,
        dry_run: dryRun
      }

      syncLogs.value.unshift(log)
      clearOldLogs()
      saveLogs()

      throw error
    } finally {
      syncing.value = false
    }
  }

  /**
   * 清除舊日誌（保留最近 50 筆）
   */
  function clearOldLogs() {
    if (syncLogs.value.length > MAX_LOGS) {
      syncLogs.value = syncLogs.value.slice(0, MAX_LOGS)
    }
  }

  /**
   * 清除所有日誌
   */
  function clearAllLogs() {
    syncLogs.value = []
    saveLogs()
  }

  /**
   * 刪除特定日誌
   */
  function deleteLog(logId: string) {
    const index = syncLogs.value.findIndex(log => log.id === logId)
    if (index !== -1) {
      syncLogs.value.splice(index, 1)
      saveLogs()
    }
  }

  // 初始化時載入日誌
  loadLogs()

  return {
    // State
    syncing,
    syncLogs,
    lastSyncResult,
    // Getters
    recentLogs,
    successCount,
    failedCount,
    getLogsByDate,
    hasSuccessfulSync,
    // Actions
    syncToTCS,
    clearOldLogs,
    clearAllLogs,
    deleteLog
  }
})

