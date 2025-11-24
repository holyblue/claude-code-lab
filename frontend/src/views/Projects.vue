<template>
  <div class="projects">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ t('project.title') }}</h2>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            {{ t('common.add') }}
          </el-button>
        </div>
      </template>

      <!-- 搜尋與篩選區域 -->
      <div class="filter-section">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchKeyword"
              placeholder="搜尋專案代碼、需求單代碼或名稱"
              clearable
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :span="6">
            <el-select
              v-model="statusFilter"
              placeholder="專案狀態"
              clearable
              @change="handleFilterChange"
            >
              <el-option label="進行中" value="active" />
              <el-option label="已完成" value="completed" />
              <el-option label="已歸檔" value="archived" />
            </el-select>
          </el-col>
        </el-row>
      </div>

      <!-- 專案列表 -->
      <el-table
        v-loading="loading"
        :data="filteredProjects"
        style="width: 100%"
        :empty-text="emptyText"
      >
        <el-table-column prop="code" label="專案代碼" width="150" />
        <el-table-column prop="requirement_code" label="需求單代碼" width="150" />
        <el-table-column prop="name" label="專案名稱" min-width="180">
          <template #default="{ row }">
            <el-tag :color="row.color" style="margin-right: 8px; color: white;" size="small">
              {{ row.code }}
            </el-tag>
            <span class="project-name">{{ row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="狀態" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="核定工時使用率" width="280">
          <template #default="{ row }">
            <div v-if="row.approved_man_days">
              <template v-if="projectStats[row.id]">
                <el-progress
                  :percentage="Math.min(Number(projectStats[row.id]!.usage_rate), 100)"
                  :color="getProgressColor(projectStats[row.id]!.warning_level)"
                  :format="() => formatUsageRate(projectStats[row.id]!)"
                />
                <div class="usage-detail">
                  已用 {{ Number(projectStats[row.id]!.used_hours).toFixed(1) }}h / 
                  共 {{ (Number(row.approved_man_days) * 7.5).toFixed(1) }}h ({{ Number(row.approved_man_days).toFixed(1) }} 人天)
                </div>
              </template>
              <template v-else>
                <el-progress :percentage="0" />
                <div class="usage-detail">
                  已用 0.0h / 共 {{ (Number(row.approved_man_days) * 7.5).toFixed(1) }}h ({{ Number(row.approved_man_days).toFixed(1) }} 人天)
                </div>
              </template>
            </div>
            <span v-else class="no-data">未設定核定工時</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="handleEdit(row)">
              編輯
            </el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">
              刪除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/編輯對話框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      :close-on-click-modal="false"
    >
      <el-tabs v-model="activeTab" v-if="dialogMode === 'edit' && currentProject">
        <el-tab-pane label="基本資訊" name="basic">
          <ProjectForm
            ref="projectFormRef"
            :project="currentProject"
            :mode="dialogMode"
            @submit="handleSubmit"
          />
        </el-tab-pane>
        <el-tab-pane label="里程碑" name="milestones">
          <MilestoneManager :project-id="currentProject.id" @refresh="handleMilestoneRefresh" />
        </el-tab-pane>
      </el-tabs>
      <ProjectForm
        v-else
        ref="projectFormRef"
        :project="currentProject"
        :mode="dialogMode"
        @submit="handleSubmit"
      />
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleDialogConfirm" :loading="submitting" v-if="activeTab === 'basic' || dialogMode === 'create'">
          確定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { useProjectStore } from '../stores/project'
import ProjectForm from '../components/ProjectForm.vue'
import MilestoneManager from '../components/project/MilestoneManager.vue'
import { projectsApi } from '../api'
import type { Project, ProjectCreate, ProjectUpdate, ProjectStats } from '../types'

const { t } = useI18n()
const route = useRoute()

// Stores
const projectStore = useProjectStore()

// Refs
const projectFormRef = ref<InstanceType<typeof ProjectForm>>()
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentProject = ref<Project | null>(null)
const searchKeyword = ref('')
const statusFilter = ref<string>('')
const projectStats = ref<Record<number, ProjectStats>>({})
const activeTab = ref<string>('basic')

// Computed
const dialogTitle = computed(() => {
  return dialogMode.value === 'create' ? '新增專案' : '編輯專案'
})

const filteredProjects = computed(() => {
  let projects = projectStore.projects

  // 搜尋過濾
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    projects = projects.filter(
      (p) =>
        p.code.toLowerCase().includes(keyword) ||
        p.requirement_code.toLowerCase().includes(keyword) ||
        p.name.toLowerCase().includes(keyword)
    )
  }

  // 狀態過濾
  if (statusFilter.value) {
    projects = projects.filter((p) => p.status === statusFilter.value)
  }

  return projects
})

const emptyText = computed(() => {
  if (loading.value) return '載入中...'
  if (searchKeyword.value || statusFilter.value) return '沒有符合條件的專案'
  return '尚未建立專案'
})

// Methods
const getStatusType = (status: string) => {
  const typeMap: Record<string, any> = {
    active: 'success',
    completed: 'info',
    archived: 'warning',
  }
  return typeMap[status] || ''
}

const getStatusLabel = (status: string) => {
  const labelMap: Record<string, string> = {
    active: '進行中',
    completed: '已完成',
    archived: '已歸檔',
  }
  return labelMap[status] || status
}

const getProgressColor = (warningLevel: string) => {
  if (warningLevel === 'danger') return '#F56C6C'
  if (warningLevel === 'warning') return '#E6A23C'
  return '#67C23A'
}

const formatUsageRate = (stats: ProjectStats) => {
  return `${Number(stats.usage_rate).toFixed(1)}%`
}

const handleSearch = () => {
  // 搜尋由 computed 自動處理
}

const handleFilterChange = () => {
  // 篩選由 computed 自動處理
}

const handleAdd = () => {
  dialogMode.value = 'create'
  currentProject.value = null
  activeTab.value = 'basic'
  dialogVisible.value = true
  setTimeout(() => {
    projectFormRef.value?.reset()
  }, 100)
}

const handleEdit = (project: Project) => {
  dialogMode.value = 'edit'
  currentProject.value = project
  activeTab.value = 'basic'
  dialogVisible.value = true
}

const handleMilestoneRefresh = () => {
  // 里程碑更新後的回調，可以在這裡做額外處理
  console.log('Milestone updated')
}

const handleDelete = async (project: Project) => {
  try {
    await ElMessageBox.confirm(
      `確定要刪除專案「${project.name}」嗎？此操作無法復原。`,
      '刪除確認',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    await projectStore.deleteProject(project.id)
    ElMessage.success('專案刪除成功')
    await loadProjects()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '刪除失敗')
    }
  }
}

const handleDialogConfirm = async () => {
  const isValid = await projectFormRef.value?.validate()
  if (!isValid) return

  await projectFormRef.value?.submit()
}

const handleSubmit = async (data: ProjectCreate | ProjectUpdate) => {
  submitting.value = true
  try {
    if (dialogMode.value === 'create') {
      await projectStore.createProject(data as ProjectCreate)
      ElMessage.success('專案新增成功')
    } else {
      await projectStore.updateProject(currentProject.value!.id, data as ProjectUpdate)
      ElMessage.success('專案更新成功')
    }
    dialogVisible.value = false
    await loadProjects()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失敗')
  } finally {
    submitting.value = false
  }
}

const loadProjects = async () => {
  loading.value = true
  try {
    await projectStore.fetchProjects()
    await loadProjectStats()
  } catch (error) {
    console.error('載入專案失敗:', error)
    ElMessage.error('載入專案失敗')
  } finally {
    loading.value = false
  }
}

const loadProjectStats = async () => {
  try {
    console.log('📊 開始載入專案統計...')
    const response = await projectsApi.getAllStats()
    console.log('📊 收到統計資料:', response)
    const statsMap: Record<number, ProjectStats> = {}
    response.forEach((stat) => {
      statsMap[stat.project_id] = stat
    })
    projectStats.value = statsMap
    console.log('📊 統計資料已更新:', projectStats.value)
  } catch (error) {
    console.error('❌ 載入專案統計失敗:', error)
  }
}

// Lifecycle
onMounted(() => {
  loadProjects()
})

// 監聽路由變化，當進入專案頁面時重新載入統計
watch(
  () => route.path,
  (newPath, oldPath) => {
    console.log('🔄 路由變化:', oldPath, '→', newPath)
    if (newPath === '/projects') {
      console.log('✅ 進入專案頁面，重新載入統計資料')
      loadProjectStats()
    }
  }
)
</script>

<style scoped>
.projects {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}

.filter-section {
  padding: 0 20px 20px 20px;
}

.usage-detail {
  font-size: 12px;
  color: #606266;
  margin-top: 8px;
  font-weight: 500;
}

.no-data {
  color: #909399;
  font-size: 14px;
}

.project-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}
</style>
