import { apiClient } from './client'
import type { WorkCategory, WorkCategoryCreate, PaginatedResponse } from '../types'

export const workCategoriesApi = {
  // 取得所有工作類別
  getAll: (params?: { skip?: number; limit?: number }) => {
    return apiClient.get<PaginatedResponse<WorkCategory>>('/api/work-categories', { params })
  },

  // 取得單一工作類別
  getById: (id: number) => {
    return apiClient.get<WorkCategory>(`/api/work-categories/${id}`)
  },

  // 新增工作類別
  create: (data: WorkCategoryCreate) => {
    return apiClient.post<WorkCategory>('/api/work-categories', data)
  },

  // 更新工作類別
  update: (id: number, data: Partial<WorkCategoryCreate>) => {
    return apiClient.put<WorkCategory>(`/api/work-categories/${id}`, data)
  },

  // 刪除工作類別
  delete: (id: number) => {
    return apiClient.delete<{ message: string }>(`/api/work-categories/${id}`)
  },
}
