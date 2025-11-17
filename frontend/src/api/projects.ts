import { apiClient } from './client'
import type { Project, ProjectCreate, ProjectUpdate, PaginatedResponse } from '../types'

export const projectsApi = {
  // 取得所有專案
  getAll: (params?: { skip?: number; limit?: number; include_deleted?: boolean }) => {
    return apiClient.get<PaginatedResponse<Project>>('/api/projects', { params })
  },

  // 取得單一專案
  getById: (id: number) => {
    return apiClient.get<Project>(`/api/projects/${id}`)
  },

  // 新增專案
  create: (data: ProjectCreate) => {
    return apiClient.post<Project>('/api/projects', data)
  },

  // 更新專案
  update: (id: number, data: ProjectUpdate) => {
    return apiClient.put<Project>(`/api/projects/${id}`, data)
  },

  // 刪除專案（軟刪除）
  delete: (id: number) => {
    return apiClient.delete<{ message: string }>(`/api/projects/${id}`)
  },
}
