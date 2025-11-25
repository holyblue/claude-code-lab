<template>
  <!-- 浮動同步按鈕 -->
  <el-tooltip
    :content="tooltipContent"
    placement="left"
    :disabled="tcsStore.syncing"
  >
    <el-button
      class="tcs-sync-fab"
      type="primary"
      :icon="Upload"
      circle
      size="large"
      @click="handleClick"
      :loading="tcsStore.syncing"
    />
  </el-tooltip>

  <!-- 同步對話框 -->
  <TcsSyncDialog
    v-model="showSyncDialog"
    @success="handleSyncSuccess"
    @error="handleSyncError"
  />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import { useTCSStore } from '../stores/tcs'
import TcsSyncDialog from './TcsSyncDialog.vue'
import type { TCSAutoFillResponse } from '../types'

// Stores
const tcsStore = useTCSStore()

// State
const showSyncDialog = ref(false)

// Computed
const tooltipContent = computed(() => {
  if (tcsStore.syncing) return '同步中...'
  return '同步工時到 TCS'
})

// Methods
const handleClick = () => {
  showSyncDialog.value = true
}

const handleSyncSuccess = (result: TCSAutoFillResponse) => {
  console.log('同步成功:', result)
  ElMessage.success({
    message: `✓ ${result.message}`,
    duration: 3000,
    showClose: true
  })
}

const handleSyncError = (error: any) => {
  console.error('同步失敗:', error)
  // 錯誤訊息已在對話框中顯示，這裡不重複提示
}
</script>

<style scoped>
.tcs-sync-fab {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 56px;
  height: 56px;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
  z-index: 999;
  transition: all 0.3s ease;
}

.tcs-sync-fab:hover {
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.5);
  transform: translateY(-2px);
}

.tcs-sync-fab:active {
  transform: translateY(0);
}

/* Loading 狀態時的脈動效果 */
.tcs-sync-fab.is-loading {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
  }
  50% {
    box-shadow: 0 6px 20px rgba(64, 158, 255, 0.6);
  }
}

/* 響應式設計 */
@media (max-width: 768px) {
  .tcs-sync-fab {
    right: 16px;
    bottom: 16px;
    width: 48px;
    height: 48px;
  }
}
</style>

