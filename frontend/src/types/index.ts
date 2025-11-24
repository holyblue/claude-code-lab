// 專案相關類型
export interface Project {
  id: number
  code: string
  requirement_code: string
  name: string
  approved_man_days: number
  default_account_group_id?: number
  default_work_category_id?: number
  description?: string
  status: 'active' | 'completed' | 'archived'
  color: string
  created_at: string
  updated_at: string
  deleted_at?: string
}

export interface ProjectCreate {
  code: string
  requirement_code: string
  name: string
  approved_man_days?: number
  default_account_group_id?: number
  default_work_category_id?: number
  description?: string
  status?: string
  color?: string
}

export interface ProjectUpdate {
  code?: string
  requirement_code?: string
  name?: string
  approved_man_days?: number
  default_account_group_id?: number
  default_work_category_id?: number
  description?: string
  status?: string
  color?: string
}

// 帳組相關類型
export interface AccountGroup {
  id: number
  code: string
  name: string
  full_name: string
  is_default: boolean
  created_at: string
  updated_at: string
}

export interface AccountGroupCreate {
  code: string
  name: string
  is_default?: boolean
}

// 工作類別相關類型
export interface WorkCategory {
  id: number
  code: string
  name: string
  full_name: string
  deduct_approved_hours: boolean
  is_default: boolean
  created_at: string
  updated_at: string
}

export interface WorkCategoryCreate {
  code: string
  name: string
  deduct_approved_hours?: boolean
  is_default?: boolean
}

// 工時記錄相關類型
export interface TimeEntry {
  id: number
  date: string
  project_id: number
  account_group_id: number | null  // 模組改為選填，允許 null
  work_category_id: number
  hours: number
  description: string
  account_item?: string
  display_order: number
  created_at: string
  updated_at: string
}

export interface TimeEntryCreate {
  date: string
  project_id: number
  account_group_id: number | null  // 模組改為選填，允許 null
  work_category_id: number
  hours: number
  description: string
  account_item?: string
  display_order?: number
}

export interface TimeEntryUpdate {
  date?: string
  project_id?: number
  account_group_id?: number | null  // 模組改為選填，允許 null
  work_category_id?: number
  hours?: number
  description?: string
  account_item?: string
  display_order?: number
}

// 統計相關類型
export interface ProjectStats {
  project_id: number
  project_code: string
  project_name: string
  approved_hours: number
  used_hours: number
  non_deduct_hours: number
  remaining_hours: number
  usage_rate: number
  warning_level: 'none' | 'warning' | 'danger'
  is_over_budget: boolean
}

export interface DailyStats {
  date: string
  total_hours: number
  normal_hours: number
  overtime_hours: number
  status: string
}

// 里程碑相關類型
export interface Milestone {
  id: number
  project_id: number
  name: string
  start_date: string // YYYY-MM-DD
  end_date: string // YYYY-MM-DD
  description?: string
  display_order: number
  created_at: string
  updated_at: string
}

export interface MilestoneCreate {
  name: string
  start_date: string
  end_date: string
  description?: string
  display_order?: number
}

export interface MilestoneUpdate {
  name?: string
  start_date?: string
  end_date?: string
  description?: string
  display_order?: number
}

// API 回應類型
export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}
