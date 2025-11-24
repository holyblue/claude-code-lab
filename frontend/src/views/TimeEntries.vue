<template>
  <div class="time-entries">
    <!-- 篩選區域 -->
    <el-card class="filter-card" shadow="never">
      <el-row :gutter="20" align="middle">
        <el-col :span="8">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="-"
            start-placeholder="開始日期"
            end-placeholder="結束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleDateRangeChange"
          />
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="filterProjectId"
            placeholder="選擇專案"
            clearable
            filterable
            @change="handleFilterChange"
          >
            <el-option
              v-for="project in projectStore.activeProjects"
              :key="project.id"
              :label="`${project.code} - ${project.name}`"
              :value="project.id"
            />
          </el-select>
        </el-col>
        <el-col :span="10" style="text-align: right">
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            {{ t('common.add') }}
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 工時記錄列表 -->
    <el-card class="table-card">
      <el-table
        v-loading="timeEntryStore.loading"
        :data="timeEntryStore.timeEntries"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="date" label="日期" width="120" sortable>
          <template #default="{ row }">
            {{ formatDate(row.date) }}
          </template>
        </el-table-column>

        <el-table-column label="專案" min-width="200">
          <template #default="{ row }">
            <div v-if="getProject(row.project_id)">
              <el-tag :color="getProject(row.project_id)?.color" style="color: white;" size="small">
                {{ getProject(row.project_id)?.code }}
              </el-tag>
              <span class="project-name">
                {{ getProject(row.project_id)?.name }}
              </span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="帳組" width="150">
          <template #default="{ row }">
            {{ getAccountGroup(row.account_group_id)?.full_name || '-' }}
          </template>
        </el-table-column>

        <el-table-column label="工作類別" width="150">
          <template #default="{ row }">
            <span>{{ getWorkCategory(row.work_category_id)?.full_name || '-' }}</span>
            <el-tag
              v-if="!getWorkCategory(row.work_category_id)?.deduct_approved_hours"
              type="warning"
              size="small"
              style="margin-left: 4px"
            >
              不扣抵
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="hours" label="工時" width="100" align="right">
          <template #default="{ row }">
            <el-text type="primary" style="font-weight: bold">
              {{ row.hours }} 小時
            </el-text>
          </template>
        </el-table-column>

        <el-table-column label="工作說明" min-width="300">
          <template #default="{ row }">
            <div class="description-cell">
              {{ row.description }}
            </div>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="handleEdit(row)">
              <el-icon><Edit /></el-icon>
              編輯
            </el-button>
            <el-button type="danger" size="small" link @click="handleDelete(row)">
              <el-icon><Delete /></el-icon>
              刪除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 統計資訊 -->
      <div class="summary-row">
        <el-text size="large" type="primary">
          總計工時：<strong>{{ totalHours }} 小時</strong>
        </el-text>
      </div>
    </el-card>

    <!-- 新增/編輯對話框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="700px"
      :close-on-click-modal="false"
    >
      <TimeEntryForm
        :initial-data="currentEntry"
        :loading="formLoading"
        @submit="handleSubmit"
        @cancel="handleCancelDialog"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import TimeEntryForm from '../components/TimeEntryForm.vue'
import { useTimeEntryStore } from '../stores/timeEntry'
import { useProjectStore } from '../stores/project'
import { useAccountGroupStore } from '../stores/accountGroup'
import { useWorkCategoryStore } from '../stores/workCategory'
import type { TimeEntry, TimeEntryCreate, TimeEntryUpdate } from '../types'

const { t } = useI18n()
const timeEntryStore = useTimeEntryStore()
const projectStore = useProjectStore()
const accountGroupStore = useAccountGroupStore()
const workCategoryStore = useWorkCategoryStore()

// 篩選條件
const getTodayDate = (): string => {
  return new Date().toISOString().split('T')[0]
}

const dateRange = ref<[string, string] | null>([getTodayDate(), getTodayDate()])
const filterProjectId = ref<number | null>(null)

// 對話框狀態
const dialogVisible = ref(false)
const dialogTitle = ref('')
const currentEntry = ref<Partial<TimeEntryCreate>>({})
const isEditMode = ref(false)
const editingId = ref<number | null>(null)
const formLoading = ref(false)

// 計算總工時
const totalHours = computed(() => {
  return timeEntryStore.timeEntries.reduce((sum, entry) => sum + Number(entry.hours), 0).toFixed(1)
})

// 輔助函數
const getProject = (id: number) => {
  return projectStore.getProjectById(id)
}

const getAccountGroup = (id: number) => {
  return accountGroupStore.getAccountGroupById(id)
}

const getWorkCategory = (id: number) => {
  return workCategoryStore.getWorkCategoryById(id)
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

// 載入資料
const fetchData = async () => {
  const params: {
    start_date?: string
    end_date?: string
    project_id?: number
  } = {}

  if (dateRange.value) {
    params.start_date = dateRange.value[0]
    params.end_date = dateRange.value[1]
  }

  if (filterProjectId.value) {
    params.project_id = filterProjectId.value
  }

  try {
    await timeEntryStore.fetchTimeEntries(params)
  } catch (error) {
    ElMessage.error('載入工時記錄失敗')
  }
}

// 篩選處理
const handleDateRangeChange = () => {
  fetchData()
}

const handleFilterChange = () => {
  fetchData()
}

// 新增
const handleAdd = () => {
  isEditMode.value = false
  dialogTitle.value = '新增工時記錄'
  currentEntry.value = {
    date: new Date().toISOString().split('T')[0],
    hours: 0.5,
  }
  dialogVisible.value = true
}

// 編輯
const handleEdit = (entry: TimeEntry) => {
  isEditMode.value = true
  editingId.value = entry.id
  dialogTitle.value = '編輯工時記錄'
  currentEntry.value = {
    date: entry.date,
    project_id: entry.project_id,
    account_group_id: entry.account_group_id,
    work_category_id: entry.work_category_id,
    hours: entry.hours,
    description: entry.description,
    display_order: entry.display_order,
  }
  dialogVisible.value = true
}

// 刪除
const handleDelete = async (entry: TimeEntry) => {
  try {
    await ElMessageBox.confirm('確定要刪除這筆工時記錄嗎？', '確認刪除', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning',
    })

    await timeEntryStore.deleteTimeEntry(entry.id)
    ElMessage.success('刪除成功')
    await fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('刪除失敗')
    }
  }
}

// 提交表單
const handleSubmit = async (data: TimeEntryCreate) => {
  formLoading.value = true
  try {
    if (isEditMode.value && editingId.value) {
      // 編輯模式
      console.log('🔄 開始更新，ID:', editingId.value, '資料:', data)
      const updateData: TimeEntryUpdate = { ...data }
      const result = await timeEntryStore.updateTimeEntry(editingId.value, updateData)
      console.log('✅ 更新成功，回傳:', result)
      ElMessage.success('更新成功')
    } else {
      // 新增模式
      console.log('➕ 開始新增，資料:', data)
      const result = await timeEntryStore.createTimeEntry(data)
      console.log('✅ 新增成功，回傳:', result)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    await fetchData()
  } catch (error) {
    console.error('❌ 提交失敗:', error)
    ElMessage.error(isEditMode.value ? '更新失敗' : '新增失敗')
  } finally {
    formLoading.value = false
  }
}

// 取消對話框
const handleCancelDialog = () => {
  dialogVisible.value = false
}

// 初始化
onMounted(async () => {
  await Promise.all([
    projectStore.fetchProjects({ limit: 1000 }),
    accountGroupStore.fetchAccountGroups({ limit: 100 }),
    workCategoryStore.fetchWorkCategories({ limit: 100 }),
  ])
  await fetchData()
})
</script>

<style scoped>
.time-entries {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filter-card {
  flex-shrink: 0;
}

.table-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.description-cell {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary-row {
  margin-top: 16px;
  padding: 12px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
  text-align: right;
}

.project-name {
  margin-left: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}
</style>
