import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { accountGroupsApi } from '../api'
import type { AccountGroup, AccountGroupCreate } from '../types'

export const useAccountGroupStore = defineStore('accountGroup', () => {
  // State
  const accountGroups = ref<AccountGroup[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const defaultAccountGroups = computed(() =>
    accountGroups.value.filter((ag) => ag.is_default)
  )

  const getAccountGroupById = computed(() => (id: number) =>
    accountGroups.value.find((ag) => ag.id === id)
  )

  // Actions
  async function fetchAccountGroups(params?: { skip?: number; limit?: number }) {
    loading.value = true
    error.value = null
    try {
      const response = await accountGroupsApi.getAll(params)
      accountGroups.value = response.items
      return response
    } catch (e) {
      error.value = e instanceof Error ? e.message : '載入帳組失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function createAccountGroup(data: AccountGroupCreate) {
    loading.value = true
    error.value = null
    try {
      const accountGroup = await accountGroupsApi.create(data)
      accountGroups.value.push(accountGroup)
      return accountGroup
    } catch (e) {
      error.value = e instanceof Error ? e.message : '新增帳組失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateAccountGroup(id: number, data: Partial<AccountGroupCreate>) {
    loading.value = true
    error.value = null
    try {
      const accountGroup = await accountGroupsApi.update(id, data)
      const index = accountGroups.value.findIndex((ag) => ag.id === id)
      if (index !== -1) {
        accountGroups.value[index] = accountGroup
      }
      return accountGroup
    } catch (e) {
      error.value = e instanceof Error ? e.message : '更新帳組失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteAccountGroup(id: number) {
    loading.value = true
    error.value = null
    try {
      await accountGroupsApi.delete(id)
      const index = accountGroups.value.findIndex((ag) => ag.id === id)
      if (index !== -1) {
        accountGroups.value.splice(index, 1)
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : '刪除帳組失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    accountGroups,
    loading,
    error,
    // Getters
    defaultAccountGroups,
    getAccountGroupById,
    // Actions
    fetchAccountGroups,
    createAccountGroup,
    updateAccountGroup,
    deleteAccountGroup,
  }
})
