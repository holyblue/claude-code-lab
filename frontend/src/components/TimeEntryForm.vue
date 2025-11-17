<template>
  <el-form
    ref="formRef"
    :model="formData"
    :rules="rules"
    label-width="120px"
    label-position="top"
  >
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item :label="t('timeEntry.date')" prop="date">
          <el-date-picker
            v-model="formData.date"
            type="date"
            :placeholder="t('timeEntry.date')"
            style="width: 100%"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item :label="t('timeEntry.hours')" prop="hours">
          <el-input-number
            v-model="formData.hours"
            :min="0.5"
            :max="24"
            :step="0.5"
            :precision="1"
            style="width: 100%"
          />
        </el-form-item>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item :label="t('timeEntry.project')" prop="project_id">
          <el-select
            v-model="formData.project_id"
            :placeholder="t('timeEntry.project')"
            filterable
            style="width: 100%"
            :loading="projectStore.loading"
          >
            <el-option
              v-for="project in projectStore.activeProjects"
              :key="project.id"
              :label="`${project.code} - ${project.name}`"
              :value="project.id"
            />
          </el-select>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item :label="t('timeEntry.accountGroup')" prop="account_group_id">
          <el-select
            v-model="formData.account_group_id"
            :placeholder="t('timeEntry.accountGroup')"
            filterable
            style="width: 100%"
            :loading="accountGroupStore.loading"
          >
            <el-option
              v-for="group in accountGroupStore.accountGroups"
              :key="group.id"
              :label="group.full_name"
              :value="group.id"
            />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>

    <el-form-item :label="t('timeEntry.workCategory')" prop="work_category_id">
      <el-select
        v-model="formData.work_category_id"
        :placeholder="t('timeEntry.workCategory')"
        filterable
        style="width: 100%"
        :loading="workCategoryStore.loading"
      >
        <el-option
          v-for="category in workCategoryStore.workCategories"
          :key="category.id"
          :label="category.full_name"
          :value="category.id"
        >
          <span>{{ category.full_name }}</span>
          <el-tag
            v-if="!category.deduct_approved_hours"
            type="warning"
            size="small"
            style="margin-left: 8px"
          >
            不扣抵
          </el-tag>
        </el-option>
      </el-select>
    </el-form-item>

    <el-form-item :label="t('timeEntry.description')" prop="description">
      <el-input
        v-model="formData.description"
        type="textarea"
        :rows="6"
        :placeholder="t('timeEntry.description') + '（支援 Markdown）'"
      />
      <div class="markdown-hint">
        <el-text size="small" type="info">
          支援 Markdown 格式，例如：- [ ] 待辦事項、- [x] 已完成
        </el-text>
      </div>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="handleSubmit" :loading="loading">
        {{ t('common.save') }}
      </el-button>
      <el-button @click="handleCancel">{{ t('common.cancel') }}</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import type { FormInstance, FormRules } from 'element-plus'
import { useProjectStore } from '../stores/project'
import { useAccountGroupStore } from '../stores/accountGroup'
import { useWorkCategoryStore } from '../stores/workCategory'
import type { TimeEntryCreate } from '../types'

interface Props {
  initialData?: Partial<TimeEntryCreate>
  loading?: boolean
}

interface Emits {
  (e: 'submit', data: TimeEntryCreate): void
  (e: 'cancel'): void
}

const props = withDefaults(defineProps<Props>(), {
  initialData: () => ({}),
  loading: false,
})

const emit = defineEmits<Emits>()

const { t } = useI18n()
const projectStore = useProjectStore()
const accountGroupStore = useAccountGroupStore()
const workCategoryStore = useWorkCategoryStore()

const formRef = ref<FormInstance>()

const getDefaultDate = (): string => {
  const dateStr = new Date().toISOString().split('T')[0]
  return dateStr as string
}

const formData = reactive<TimeEntryCreate>({
  date: props.initialData.date || getDefaultDate(),
  project_id: props.initialData.project_id || 0,
  account_group_id: props.initialData.account_group_id || 0,
  work_category_id: props.initialData.work_category_id || 0,
  hours: props.initialData.hours || 0.5,
  description: props.initialData.description || '',
  display_order: props.initialData.display_order || 0,
})

const rules: FormRules = {
  date: [{ required: true, message: '請選擇日期', trigger: 'change' }],
  project_id: [{ required: true, message: '請選擇專案', trigger: 'change' }],
  account_group_id: [{ required: true, message: '請選擇帳組', trigger: 'change' }],
  work_category_id: [{ required: true, message: '請選擇工作類別', trigger: 'change' }],
  hours: [
    { required: true, message: '請輸入工時', trigger: 'blur' },
    {
      type: 'number',
      min: 0.5,
      max: 24,
      message: '工時必須在 0.5 到 24 小時之間',
      trigger: 'blur',
    },
  ],
  description: [{ required: true, message: '請輸入工作說明', trigger: 'blur' }],
}

// 監聽 initialData 變化
watch(
  () => props.initialData,
  (newData) => {
    if (newData) {
      Object.assign(formData, {
        date: newData.date || getDefaultDate(),
        project_id: newData.project_id || 0,
        account_group_id: newData.account_group_id || 0,
        work_category_id: newData.work_category_id || 0,
        hours: newData.hours || 0.5,
        description: newData.description || '',
        display_order: newData.display_order || 0,
      })
    }
  },
  { deep: true }
)

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      emit('submit', { ...formData })
    }
  })
}

const handleCancel = () => {
  emit('cancel')
}

// 載入選項資料
projectStore.fetchProjects({ limit: 1000 })
accountGroupStore.fetchAccountGroups({ limit: 100 })
workCategoryStore.fetchWorkCategories({ limit: 100 })
</script>

<style scoped>
.markdown-hint {
  margin-top: 8px;
}
</style>
