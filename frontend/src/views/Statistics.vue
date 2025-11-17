<template>
  <div class="statistics">
    <el-card>
      <template #header>
        <h2>{{ t('stats.title') }}</h2>
      </template>
      <div class="content">
        <p>統計報表（待實作）</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.statistics {
  height: 100%;
}

.content {
  padding: 20px;
}
</style>
