/**
 * TCS 同步相關 API
 */
import { apiClient } from './client'
import type { TCSAutoFillResponse, TCSFormatResponse } from '../types'

export const tcsApi = {
  /**
   * 同步工時到 TCS 系統
   * @param date 日期 (YYYY-MM-DD)
   * @param dryRun 是否為預覽模式（預設 true）
   */
  async syncToTCS(date: string, dryRun: boolean = true): Promise<TCSAutoFillResponse> {
    return await apiClient.post<TCSAutoFillResponse>(
      '/api/tcs/auto-fill',
      {
        date,
        dry_run: dryRun
      },
      {
        timeout: 120000 // 120 秒（2 分鐘），Playwright 自動化需要較長時間
      }
    )
  },

  /**
   * 格式化預覽工時記錄
   * @param date 日期 (YYYY-MM-DD)
   */
  async formatPreview(date: string): Promise<TCSFormatResponse> {
    return await apiClient.post<TCSFormatResponse>(
      '/api/tcs/format',
      {
        date
      },
      {
        timeout: 30000 // 30 秒，格式化不需要太長時間
      }
    )
  }
}

