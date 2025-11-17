<template>
  <div class="settings">
    <el-card>
      <template #header>
        <h2>{{ t('nav.settings') }}</h2>
      </template>
      <div class="content">
        <p>系統設定（待實作）</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<style scoped>
.settings {
  height: 100%;
}

.content {
  padding: 20px;
}
</style>
