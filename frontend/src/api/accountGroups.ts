import { apiClient } from './client'
import type { AccountGroup, AccountGroupCreate, PaginatedResponse } from '../types'

export const accountGroupsApi = {
  // 取得所有模組
  getAll: (params?: { skip?: number; limit?: number }) => {
    return apiClient.get<PaginatedResponse<AccountGroup>>('/api/account-groups', { params })
  },

  // 取得單一模組
  getById: (id: number) => {
    return apiClient.get<AccountGroup>(`/api/account-groups/${id}`)
  },

  // 新增模組
  create: (data: AccountGroupCreate) => {
    return apiClient.post<AccountGroup>('/api/account-groups', data)
  },

  // 更新模組
  update: (id: number, data: Partial<AccountGroupCreate>) => {
    return apiClient.patch<AccountGroup>(`/api/account-groups/${id}`, data)
  },

  // 刪除模組
  delete: (id: number) => {
    return apiClient.delete<{ message: string }>(`/api/account-groups/${id}`)
  },
}
