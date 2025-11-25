<template>
  <el-dialog
    v-model="visible"
    title="❌ 同步失敗"
    width="600px"
    :close-on-click-modal="false"
  >
    <div v-if="error" class="error-content">
      <!-- 錯誤資訊 -->
      <el-result icon="error" title="同步失敗">
        <template #sub-title>
          <div class="error-subtitle">
            {{ errorMessage }}
          </div>
        </template>
      </el-result>

      <!-- 錯誤詳情 -->
      <el-descriptions :column="1" border class="error-details">
        <el-descriptions-item label="錯誤時間">
          {{ formatTime(new Date()) }}
        </el-descriptions-item>
        <el-descriptions-item label="目標日期">
          <el-tag type="danger">{{ date }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="錯誤類型">
          {{ errorType }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 可能原因 -->
      <el-card class="reasons-card" shadow="never">
        <template #header>
          <div class="card-header">
            <el-icon><Warning /></el-icon>
            <span>可能原因</span>
          </div>
        </template>
        <ul class="reasons-list">
          <li v-for="(reason, index) in possibleReasons" :key="index">
            {{ reason }}
          </li>
        </ul>
      </el-card>

      <!-- 錯誤詳情（可展開） -->
      <el-collapse class="error-collapse">
        <el-collapse-item title="📋 錯誤詳情（技術資訊）" name="1">
          <pre class="error-stack">{{ errorDetails }}</pre>
        </el-collapse-item>
      </el-collapse>

      <!-- 操作建議 -->
      <el-alert
        title="💡 建議操作"
        type="info"
        :closable="false"
        show-icon
        class="suggestion-alert"
      >
        <ol class="suggestion-list">
          <li>檢查是否在內網環境</li>
          <li>確認 TCS 系統是否正常運作</li>
          <li>檢查工時記錄資料是否完整</li>
          <li>嘗試重新同步</li>
        </ol>
      </el-alert>
    </div>

    <template #footer>
      <el-button @click="handleCopyError">
        <el-icon><CopyDocument /></el-icon>
        複製錯誤訊息
      </el-button>
      <el-button @click="visible = false">關閉</el-button>
      <el-button
        type="primary"
        @click="handleRetry"
        :icon="RefreshRight"
      >
        重試
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Warning, CopyDocument, RefreshRight } from '@element-plus/icons-vue'

// Props
const props = defineProps<{
  error: any
  date: string
}>()

// Model
const modelValue = defineModel<boolean>({ required: true })

// Emits
const emit = defineEmits<{
  retry: []
}>()

// Computed
const visible = computed({
  get: () => modelValue.value,
  set: (val) => (modelValue.value = val)
})

const errorMessage = computed(() => {
  if (!props.error) return '未知錯誤'
  
  // 從 axios 錯誤中提取訊息
  if (props.error.response?.data?.detail) {
    return props.error.response.data.detail
  }
  
  if (props.error.message) {
    return props.error.message
  }
  
  return '同步過程中發生錯誤'
})

const errorType = computed(() => {
  if (!props.error) return '未知錯誤'
  
  if (props.error.response) {
    const status = props.error.response.status
    if (status === 404) return '找不到資料'
    if (status === 400) return '資料驗證失敗'
    if (status === 500) return '伺服器錯誤'
    if (status === 503) return '服務不可用'
    return `HTTP ${status} 錯誤`
  }
  
  if (props.error.code === 'ECONNABORTED') return '連線逾時'
  if (props.error.code === 'ERR_NETWORK') return '網路錯誤'
  
  return '執行錯誤'
})

const possibleReasons = computed(() => {
  const reasons: string[] = []
  
  if (!props.error) return reasons
  
  const status = props.error.response?.status
  const message = errorMessage.value.toLowerCase()
  
  if (status === 404 || message.includes('找不到')) {
    reasons.push('該日期沒有工時記錄')
    reasons.push('資料庫中資料可能已被刪除')
  } else if (status === 400 || message.includes('驗證')) {
    reasons.push('專案代碼、模組或工作類別無效')
    reasons.push('總工時超過 18 小時限制')
    reasons.push('必填欄位缺失')
  } else if (status === 500 || message.includes('playwright')) {
    reasons.push('Playwright 執行失敗')
    reasons.push('無法連接 TCS 系統')
    reasons.push('TCS 系統維護中')
  } else if (message.includes('network') || message.includes('timeout')) {
    reasons.push('不在內網環境')
    reasons.push('網路連接問題')
    reasons.push('TCS 系統無回應')
  } else {
    reasons.push('系統暫時異常')
    reasons.push('請稍後重試')
  }
  
  return reasons
})

const errorDetails = computed(() => {
  if (!props.error) return '無詳細資訊'
  
  const details: string[] = []
  
  details.push(`錯誤訊息: ${errorMessage.value}`)
  
  if (props.error.response) {
    details.push(`HTTP 狀態碼: ${props.error.response.status}`)
    if (props.error.response.data) {
      details.push(`回應內容: ${JSON.stringify(props.error.response.data, null, 2)}`)
    }
  }
  
  if (props.error.stack) {
    details.push(`\n堆疊追蹤:\n${props.error.stack}`)
  }
  
  return details.join('\n')
})

// Methods
const formatTime = (date: Date) => {
  return date.toLocaleString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const handleCopyError = async () => {
  try {
    const text = `TCS 同步錯誤報告
時間: ${formatTime(new Date())}
日期: ${props.date}
錯誤類型: ${errorType.value}
錯誤訊息: ${errorMessage.value}

詳細資訊:
${errorDetails.value}`

    await navigator.clipboard.writeText(text)
    ElMessage.success('已複製錯誤訊息到剪貼簿')
  } catch (error) {
    ElMessage.error('複製失敗')
  }
}

const handleRetry = () => {
  emit('retry')
}
</script>

<style scoped>
.error-content {
  padding: 0;
}

.error-subtitle {
  color: #f56c6c;
  font-size: 14px;
  margin-top: 8px;
}

.error-details {
  margin: 24px 0 16px;
}

.reasons-card {
  margin: 16px 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.reasons-list {
  margin: 0;
  padding-left: 20px;
}

.reasons-list li {
  margin: 8px 0;
  color: #606266;
}

.error-collapse {
  margin: 16px 0;
}

.error-stack {
  background-color: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  font-size: 12px;
  color: #606266;
  overflow-x: auto;
  max-height: 300px;
  overflow-y: auto;
}

.suggestion-alert {
  margin-top: 16px;
}

.suggestion-list {
  margin: 8px 0 0 0;
  padding-left: 20px;
}

.suggestion-list li {
  margin: 4px 0;
}
</style>

