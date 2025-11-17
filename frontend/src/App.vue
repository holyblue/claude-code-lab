<template>
  <el-config-provider :locale="locale">
    <MainLayout />
  </el-config-provider>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import zhTw from 'element-plus/es/locale/lang/zh-tw'
import en from 'element-plus/es/locale/lang/en'
import MainLayout from './layouts/MainLayout.vue'

const { locale: i18nLocale } = useI18n()

const locale = computed(() => {
  return i18nLocale.value === 'zh-TW' ? zhTw : en
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Microsoft JhengHei', 'PingFang TC', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
</style>
