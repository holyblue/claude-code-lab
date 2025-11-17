<template>
  <div class="time-entries">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ t('timeEntry.title') }}</h2>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            {{ t('common.add') }}
          </el-button>
        </div>
      </template>
      <div class="content">
        <p>工時記錄頁面（待實作）</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { Plus } from '@element-plus/icons-vue'

const { t } = useI18n()

const handleAdd = () => {
  console.log('新增工時記錄')
}
</script>

<style scoped>
.time-entries {
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

.content {
  padding: 20px;
}
</style>
