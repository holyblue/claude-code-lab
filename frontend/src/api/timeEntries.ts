import { apiClient } from './client'
import type { TimeEntry, TimeEntryCreate, TimeEntryUpdate, PaginatedResponse } from '../types'

export const timeEntriesApi = {
  // 取得所有工時記錄
  getAll: (params?: {
    skip?: number
    limit?: number
    start_date?: string
    end_date?: string
    project_id?: number
  }) => {
    return apiClient.get<PaginatedResponse<TimeEntry>>('/api/time-entries', { params })
  },

  // 取得單一工時記錄
  getById: (id: number) => {
    return apiClient.get<TimeEntry>(`/api/time-entries/${id}`)
  },

  // 新增工時記錄
  create: (data: TimeEntryCreate) => {
    return apiClient.post<TimeEntry>('/api/time-entries', data)
  },

  // 更新工時記錄
  update: (id: number, data: TimeEntryUpdate) => {
    return apiClient.put<TimeEntry>(`/api/time-entries/${id}`, data)
  },

  // 刪除工時記錄
  delete: (id: number) => {
    return apiClient.delete<{ message: string }>(`/api/time-entries/${id}`)
  },

  // 取得指定日期範圍的工時記錄
  getByDateRange: (startDate: string, endDate: string) => {
    return apiClient.get<TimeEntry[]>('/api/time-entries', {
      params: { start_date: startDate, end_date: endDate },
    })
  },
}
