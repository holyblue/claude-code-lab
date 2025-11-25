<template>
  <el-dialog
    v-model="visible"
    title="同步工時到 TCS"
    width="600px"
    :close-on-click-modal="false"
    @closed="handleClosed"
  >
    <!-- 日期選擇 -->
    <el-form :model="form" label-width="80px" class="sync-form">
      <el-form-item label="選擇日期">
        <el-date-picker
          v-model="form.date"
          type="date"
          placeholder="選擇日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          style="width: 100%"
          @change="loadDateEntries"
        />
      </el-form-item>
    </el-form>

    <!-- Loading 狀態 -->
    <div v-if="loading" v-loading="true" style="height: 100px"></div>

    <!-- 工時記錄預覽 -->
    <el-alert
      v-else-if="dateEntries.length > 0"
      :title="`📊 當日工時記錄 (${dateEntries.length} 筆，共 ${totalHours ? totalHours.toFixed(1) : '0.0'} 小時)`"
      type="info"
      :closable="false"
      style="margin-bottom: 16px"
    >
      <div class="entries-list">
        <div v-for="entry in dateEntries" :key="entry.id" class="entry-item">
          <el-icon class="entry-icon"><CircleCheck /></el-icon>
          <span class="entry-project">{{ getProjectName(entry.project_id) }}</span>
          <span class="entry-desc">{{ getShortDescription(entry.description) }}</span>
          <strong class="entry-hours">({{ entry.hours }}h)</strong>
        </div>
      </div>
    </el-alert>

    <el-alert
      v-else-if="form.date && !loading"
      title="該日期沒有工時記錄"
      type="warning"
      :closable="false"
    />

    <!-- 警告訊息 -->
    <el-alert
      v-if="dateEntries.length > 0"
      title="⚠️ 注意: 將覆蓋 TCS 該日現有資料"
      type="warning"
      :closable="false"
      show-icon
      style="margin-top: 16px"
    />

    <!-- 已同步狀態提示 -->
    <el-alert
      v-if="form.date && tcsStore.hasSuccessfulSync(form.date)"
      title="✓ 此日期已同步過"
      type="success"
      :closable="false"
      style="margin-top: 8px"
    >
      可以重複同步以更新 TCS 資料
    </el-alert>

    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button
        type="info"
        :disabled="!canSync"
        :loading="previewLoading"
        @click="handlePreview"
      >
        <el-icon><View /></el-icon>
        預覽 (不寫入)
      </el-button>
      <el-button
        type="primary"
        :disabled="!canSync"
        :loading="syncLoading"
        @click="handleSync"
      >
        <el-icon><Upload /></el-icon>
        確認同步
      </el-button>
    </template>
  </el-dialog>

  <!-- 預覽結果對話框 -->
  <TcsPreviewDialog
    v-model="showPreviewDialog"
    :preview-result="previewResult"
    :date="form.date"
    @confirm-sync="handleConfirmSync"
  />

  <!-- 錯誤對話框 -->
  <TcsErrorDialog
    v-model="showErrorDialog"
    :error="lastError"
    :date="form.date"
    @retry="handleRetry"
  />
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { CircleCheck, View, Upload } from '@element-plus/icons-vue'
import { useTimeEntryStore } from '../stores/timeEntry'
import { useProjectStore } from '../stores/project'
import { useTCSStore } from '../stores/tcs'
import type { TimeEntry, TCSAutoFillResponse } from '../types'
import TcsPreviewDialog from './TcsPreviewDialog.vue'
import TcsErrorDialog from './TcsErrorDialog.vue'

// Props & Emits
const modelValue = defineModel<boolean>({ required: true })
const emit = defineEmits<{
  success: [result: TCSAutoFillResponse]
  error: [error: any]
}>()

// Stores
const timeEntryStore = useTimeEntryStore()
const projectStore = useProjectStore()
const tcsStore = useTCSStore()

// State
const visible = computed({
  get: () => modelValue.value,
  set: (val) => (modelValue.value = val)
})

const form = ref({
  date: new Date().toISOString().split('T')[0] // 預設今天
})

const dateEntries = ref<TimeEntry[]>([])
const loading = ref(false)
const previewLoading = ref(false)
const syncLoading = ref(false)
const showPreviewDialog = ref(false)
const showErrorDialog = ref(false)
const previewResult = ref<TCSAutoFillResponse | null>(null)
const lastError = ref<any>(null)

// Computed
const totalHours = computed(() => {
  if (!dateEntries.value || dateEntries.value.length === 0) {
    return 0
  }
  return dateEntries.value.reduce((sum, entry) => sum + (Number(entry.hours) || 0), 0)
})

const canSync = computed(() => 
  form.value.date && dateEntries.value.length > 0 && !loading.value
)

// Methods
const getProjectName = (projectId: number) => {
  const project = projectStore.projects.find(p => p.id === projectId)
  return project ? `${project.code} - ${project.name}` : '未知專案'
}

const getShortDescription = (description: string) => {
  const firstLine = description.split('\n')[0]
  return firstLine.length > 30 ? firstLine.slice(0, 30) + '...' : firstLine
}

const loadDateEntries = async () => {
  if (!form.value.date) {
    dateEntries.value = []
    return
  }

  loading.value = true
  try {
    // 載入當日所有工時記錄
    await timeEntryStore.fetchByDateRange(form.value.date, form.value.date)
    // 直接使用 store 中的 timeEntries，因為已經過濾了日期範圍
    dateEntries.value = timeEntryStore.timeEntries.filter(
      entry => entry.date === form.value.date
    )
  } catch (error) {
    console.error('載入工時記錄失敗:', error)
    ElMessage.error('載入工時記錄失敗')
    dateEntries.value = []
  } finally {
    loading.value = false
  }
}

const handlePreview = async () => {
  if (!form.value.date) return

  previewLoading.value = true
  try {
    const result = await tcsStore.syncToTCS(form.value.date, true)
    previewResult.value = result
    showPreviewDialog.value = true
    ElMessage.success('預覽成功')
  } catch (error: any) {
    console.error('預覽失敗:', error)
    lastError.value = error
    showErrorDialog.value = true
  } finally {
    previewLoading.value = false
  }
}

const handleSync = async () => {
  if (!form.value.date) return

  syncLoading.value = true
  try {
    const result = await tcsStore.syncToTCS(form.value.date, false)
    ElMessage.success({
      message: `同步成功！已填寫 ${result.filled_count} 筆記錄`,
      duration: 3000
    })
    emit('success', result)
    visible.value = false
  } catch (error: any) {
    console.error('同步失敗:', error)
    lastError.value = error
    showErrorDialog.value = true
    emit('error', error)
  } finally {
    syncLoading.value = false
  }
}

const handleConfirmSync = async () => {
  showPreviewDialog.value = false
  await handleSync()
}

const handleRetry = () => {
  showErrorDialog.value = false
  // 根據上次操作決定重試預覽還是同步
  if (previewResult.value) {
    handlePreview()
  } else {
    handleSync()
  }
}

const handleClosed = () => {
  // 重置狀態
  previewResult.value = null
  lastError.value = null
}

// Watchers
watch(visible, (newVal) => {
  if (newVal) {
    // 對話框打開時，載入今天的記錄
    loadDateEntries()
    // 確保載入專案列表
    if (projectStore.projects.length === 0) {
      projectStore.fetchProjects()
    }
  }
})
</script>

<style scoped>
.sync-form {
  margin-bottom: 16px;
}

.entries-list {
  margin-top: 12px;
}

.entry-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.entry-item:last-child {
  border-bottom: none;
}

.entry-icon {
  color: #67c23a;
  margin-right: 8px;
  flex-shrink: 0;
}

.entry-project {
  font-weight: 500;
  margin-right: 8px;
  flex-shrink: 0;
}

.entry-desc {
  color: #606266;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.entry-hours {
  color: #409eff;
  margin-left: 8px;
  flex-shrink: 0;
}
</style>

