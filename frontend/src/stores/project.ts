import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { projectsApi } from '../api'
import type { Project, ProjectCreate, ProjectUpdate } from '../types'

export const useProjectStore = defineStore('project', () => {
  // State
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const activeProjects = computed(() =>
    projects.value.filter((p) => p.status === 'active')
  )

  const getProjectById = computed(() => (id: number) =>
    projects.value.find((p) => p.id === id)
  )

  // Actions
  async function fetchProjects(params?: { skip?: number; limit?: number }) {
    loading.value = true
    error.value = null
    try {
      const response = await projectsApi.getAll(params)
      projects.value = response.items
      return response
    } catch (e) {
      error.value = e instanceof Error ? e.message : '載入專案失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchProjectById(id: number) {
    loading.value = true
    error.value = null
    try {
      const project = await projectsApi.getById(id)
      currentProject.value = project
      return project
    } catch (e) {
      error.value = e instanceof Error ? e.message : '載入專案失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function createProject(data: ProjectCreate) {
    loading.value = true
    error.value = null
    try {
      const project = await projectsApi.create(data)
      projects.value.push(project)
      return project
    } catch (e) {
      error.value = e instanceof Error ? e.message : '新增專案失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateProject(id: number, data: ProjectUpdate) {
    loading.value = true
    error.value = null
    try {
      const project = await projectsApi.update(id, data)
      const index = projects.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        projects.value[index] = project
      }
      if (currentProject.value?.id === id) {
        currentProject.value = project
      }
      return project
    } catch (e) {
      error.value = e instanceof Error ? e.message : '更新專案失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteProject(id: number) {
    loading.value = true
    error.value = null
    try {
      await projectsApi.delete(id)
      const index = projects.value.findIndex((p) => p.id === id)
      if (index !== -1) {
        projects.value.splice(index, 1)
      }
      if (currentProject.value?.id === id) {
        currentProject.value = null
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : '刪除專案失敗'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    projects,
    currentProject,
    loading,
    error,
    // Getters
    activeProjects,
    getProjectById,
    // Actions
    fetchProjects,
    fetchProjectById,
    createProject,
    updateProject,
    deleteProject,
  }
})
