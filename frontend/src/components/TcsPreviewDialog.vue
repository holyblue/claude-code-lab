<template>
  <el-dialog
    v-model="visible"
    title="🔍 同步預覽結果"
    width="600px"
    :close-on-click-modal="false"
  >
    <div v-if="previewResult" class="preview-content">
      <!-- 成功狀態 -->
      <el-result icon="success" title="預覽成功！">
        <template #sub-title>
          <div class="preview-subtitle">
            以下資料將會填寫到 TCS 系統（目前僅為預覽，未真正寫入）
          </div>
        </template>
      </el-result>

      <!-- 資料摘要 -->
      <el-descriptions :column="2" border class="preview-summary">
        <el-descriptions-item label="日期">
          <el-tag type="primary">{{ date }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="記錄數">
          <el-tag>{{ previewResult.filled_count }} 筆</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="總工時">
          <el-tag type="success">{{ previewResult.total_hours }} 小時</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="狀態">
          <el-tag type="warning">預覽模式</el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <!-- 驗證結果 -->
      <el-card class="validation-card" shadow="never">
        <template #header>
          <div class="card-header">
            <el-icon><CircleCheck /></el-icon>
            <span>驗證結果</span>
          </div>
        </template>
        <div class="validation-list">
          <div class="validation-item">
            <el-icon class="check-icon"><CircleCheck /></el-icon>
            <span>專案代碼有效</span>
          </div>
          <div class="validation-item">
            <el-icon class="check-icon"><CircleCheck /></el-icon>
            <span>模組代碼有效</span>
          </div>
          <div class="validation-item">
            <el-icon class="check-icon"><CircleCheck /></el-icon>
            <span>工作類別有效</span>
          </div>
          <div class="validation-item">
            <el-icon class="check-icon"><CircleCheck /></el-icon>
            <span>總工時未超過 18 小時限制</span>
          </div>
        </div>
      </el-card>

      <!-- 提示訊息 -->
      <el-alert
        title="💡 提示"
        type="info"
        :closable="false"
        show-icon
        class="tip-alert"
      >
        <p>預覽成功代表資料格式正確，可以進行同步。</p>
        <p>點擊「確認真正同步」將會實際寫入 TCS 系統。</p>
      </el-alert>
    </div>

    <template #footer>
      <el-button @click="visible = false">關閉</el-button>
      <el-button
        type="primary"
        @click="handleConfirmSync"
        :icon="Upload"
      >
        確認真正同步
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { CircleCheck, Upload } from '@element-plus/icons-vue'
import type { TCSAutoFillResponse } from '../types'

// Props
const props = defineProps<{
  previewResult: TCSAutoFillResponse | null
  date: string
}>()

// Model
const modelValue = defineModel<boolean>({ required: true })

// Emits
const emit = defineEmits<{
  confirmSync: []
}>()

// Computed
const visible = computed({
  get: () => modelValue.value,
  set: (val) => (modelValue.value = val)
})

// Methods
const handleConfirmSync = () => {
  emit('confirmSync')
}
</script>

<style scoped>
.preview-content {
  padding: 0;
}

.preview-subtitle {
  color: #606266;
  font-size: 14px;
  margin-top: 8px;
}

.preview-summary {
  margin: 24px 0;
}

.validation-card {
  margin: 16px 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.validation-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.validation-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.check-icon {
  color: #67c23a;
  font-size: 18px;
}

.tip-alert {
  margin-top: 16px;
}

.tip-alert p {
  margin: 4px 0;
}
</style>

