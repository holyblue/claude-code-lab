<template>
  <div class="calendar">
    <el-card>
      <template #header>
        <h2>{{ t('nav.calendar') }}</h2>
      </template>
      <div class="content">
        <p>日曆視圖（待實作）</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.calendar {
  height: 100%;
}

.content {
  padding: 20px;
}
</style>
