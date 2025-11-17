import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { workCategoriesApi } from '../api'
import type { WorkCategory, WorkCategoryCreate } from '../types'

export const useWorkCategoryStore = defineStore('workCategory', () => {
  // State
  const workCategories = ref<WorkCategory[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const defaultWorkCategories = computed(() =>
    workCategories.value.filter((wc) => wc.is_default)
  )

  const deductWorkCategories = computed(() =>
    workCategories.value.filter((wc) => wc.deduct_approved_hours)
  )

  const nonDeductWorkCategories = computed(() =>
    workCategories.value.filter((wc) => !wc.deduct_approved_hours)
  )

  const getWorkCategoryById = computed(() => (id: number) =>
    workCategories.value.find((wc) => wc.id === id)
  )

  // Actions
  async function fetchWorkCategories(params?: { skip?: number; limit?: number }) {
    loading.value = true
    error.value = null
    try {
      const response = await workCategoriesApi.getAll(params)
      workCategories.value = response.items
      return response
    } catch (e) {
      error.value = e instanceof Error ? e.message : '載入工作類別失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function createWorkCategory(data: WorkCategoryCreate) {
    loading.value = true
    error.value = null
    try {
      const workCategory = await workCategoriesApi.create(data)
      workCategories.value.push(workCategory)
      return workCategory
    } catch (e) {
      error.value = e instanceof Error ? e.message : '新增工作類別失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateWorkCategory(id: number, data: Partial<WorkCategoryCreate>) {
    loading.value = true
    error.value = null
    try {
      const workCategory = await workCategoriesApi.update(id, data)
      const index = workCategories.value.findIndex((wc) => wc.id === id)
      if (index !== -1) {
        workCategories.value[index] = workCategory
      }
      return workCategory
    } catch (e) {
      error.value = e instanceof Error ? e.message : '更新工作類別失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteWorkCategory(id: number) {
    loading.value = true
    error.value = null
    try {
      await workCategoriesApi.delete(id)
      const index = workCategories.value.findIndex((wc) => wc.id === id)
      if (index !== -1) {
        workCategories.value.splice(index, 1)
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : '刪除工作類別失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    workCategories,
    loading,
    error,
    // Getters
    defaultWorkCategories,
    deductWorkCategories,
    nonDeductWorkCategories,
    getWorkCategoryById,
    // Actions
    fetchWorkCategories,
    createWorkCategory,
    updateWorkCategory,
    deleteWorkCategory,
  }
})
