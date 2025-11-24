/**
 * Milestone API client
 * 
 * Handles all API requests related to project milestones.
 */

import { apiClient } from './client'
import type { Milestone, MilestoneCreate, MilestoneUpdate } from '@/types'

export const milestonesApi = {
  /**
   * Get all milestones for a specific project
   * @param projectId - Project ID
   * @returns Promise with array of milestones
   */
  getProjectMilestones(projectId: number) {
    return apiClient.get<Milestone[]>(`/api/projects/${projectId}/milestones/`)
  },

  /**
   * Create a new milestone for a project
   * @param projectId - Project ID
   * @param data - Milestone data
   * @returns Promise with created milestone
   */
  createMilestone(projectId: number, data: MilestoneCreate) {
    return apiClient.post<Milestone>(`/api/projects/${projectId}/milestones/`, data)
  },

  /**
   * Get a specific milestone by ID
   * @param id - Milestone ID
   * @returns Promise with milestone details
   */
  getMilestone(id: number) {
    return apiClient.get<Milestone>(`/api/milestones/${id}`)
  },

  /**
   * Update an existing milestone
   * @param id - Milestone ID
   * @param data - Milestone data to update
   * @returns Promise with updated milestone
   */
  updateMilestone(id: number, data: MilestoneUpdate) {
    return apiClient.patch<Milestone>(`/api/milestones/${id}`, data)
  },

  /**
   * Delete a milestone
   * @param id - Milestone ID
   * @returns Promise
   */
  deleteMilestone(id: number) {
    return apiClient.delete(`/api/milestones/${id}`)
  }
}

export default milestonesApi

