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
        <el-form-item label="專案代碼" prop="code">
          <el-input
            v-model="formData.code"
            placeholder="例如：需2025單001"
            :disabled="isEdit"
          />
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item label="需求單代碼" prop="requirement_code">
          <el-input
            v-model="formData.requirement_code"
            placeholder="例如：R202511146001"
          />
        </el-form-item>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="專案名稱" prop="name">
          <el-input v-model="formData.name" placeholder="請輸入專案名稱" />
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item label="核定工時（人天）" prop="approved_man_days">
          <el-input-number
            v-model="formData.approved_man_days"
            :min="0"
            :max="999"
            :step="1"
            :precision="1"
            placeholder="選填"
            style="width: 100%"
          />
          <div class="field-hint" v-if="formData.approved_man_days">
            約 {{ (formData.approved_man_days * 7.5).toFixed(1) }} 小時
          </div>
        </el-form-item>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="預設模組" prop="default_account_group_id">
          <el-select
            v-model="formData.default_account_group_id"
            placeholder="選擇預設模組（選填）"
            clearable
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="group in accountGroups"
              :key="group.id"
              :label="group.full_name"
              :value="group.id"
            />
          </el-select>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item label="預設工作類別" prop="default_work_category_id">
          <el-select
            v-model="formData.default_work_category_id"
            placeholder="選擇預設工作類別（選填）"
            clearable
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="category in workCategories"
              :key="category.id"
              :label="category.full_name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="專案狀態" prop="status">
          <el-select
            v-model="formData.status"
            placeholder="選擇狀態"
            style="width: 100%"
          >
            <el-option label="進行中" value="active" />
            <el-option label="已完成" value="completed" />
            <el-option label="已歸檔" value="archived" />
          </el-select>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item label="專案顏色" prop="color">
          <el-color-picker v-model="formData.color" :predefine="predefineColors" />
        </el-form-item>
      </el-col>
    </el-row>

    <el-form-item label="備註說明" prop="description">
      <el-input
        v-model="formData.description"
        type="textarea"
        :rows="3"
        placeholder="專案備註說明（選填）"
      />
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useAccountGroupStore } from '../stores/accountGroup'
import { useWorkCategoryStore } from '../stores/workCategory'
import type { Project, ProjectCreate, ProjectUpdate } from '../types'

// Props
interface Props {
  project?: Project | null
  mode?: 'create' | 'edit'
}

const props = withDefaults(defineProps<Props>(), {
  project: null,
  mode: 'create',
})

// Emits
const emit = defineEmits<{
  submit: [data: ProjectCreate | ProjectUpdate]
}>()

// Stores
const accountGroupStore = useAccountGroupStore()
const workCategoryStore = useWorkCategoryStore()

// Refs
const formRef = ref<FormInstance>()

// Computed
const isEdit = computed(() => props.mode === 'edit')

const accountGroups = computed(() => accountGroupStore.accountGroups)
const workCategories = computed(() => workCategoryStore.workCategories)

// 預定義顏色
const predefineColors = ref([
  '#409EFF', // 藍色
  '#67C23A', // 綠色
  '#E6A23C', // 橙色
  '#F56C6C', // 紅色
  '#909399', // 灰色
  '#00D2D3', // 青色
  '#9B59B6', // 紫色
  '#F39C12', // 黃色
])

// Form data
const formData = ref<ProjectCreate>({
  code: '',
  requirement_code: '',
  name: '',
  approved_man_days: undefined,
  default_account_group_id: undefined,
  default_work_category_id: undefined,
  description: '',
  status: 'active',
  color: '#409EFF',
})

// 需求單代碼格式驗證
const validateRequirementCode = (_rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('請輸入需求單代碼'))
    return
  }
  // 格式：R + 年月日(8位) + 流水號(4位)
  const pattern = /^R\d{12}$/
  if (!pattern.test(value)) {
    callback(new Error('需求單代碼格式錯誤（例如：R202511146001）'))
    return
  }
  callback()
}

// Validation rules
const rules = ref<FormRules>({
  code: [
    { required: true, message: '請輸入專案代碼', trigger: 'blur' },
    { min: 3, max: 50, message: '專案代碼長度為 3-50 字元', trigger: 'blur' },
  ],
  requirement_code: [
    { required: true, validator: validateRequirementCode, trigger: 'blur' },
  ],
  name: [
    { required: true, message: '請輸入專案名稱', trigger: 'blur' },
    { min: 2, max: 200, message: '專案名稱長度為 2-200 字元', trigger: 'blur' },
  ],
  status: [{ required: true, message: '請選擇專案狀態', trigger: 'change' }],
  color: [{ required: true, message: '請選擇專案顏色', trigger: 'change' }],
})

// Watch for project changes (edit mode)
watch(
  () => props.project,
  (newProject) => {
    if (newProject && props.mode === 'edit') {
      formData.value = {
        code: newProject.code,
        requirement_code: newProject.requirement_code,
        name: newProject.name,
        approved_man_days: newProject.approved_man_days,
        default_account_group_id: newProject.default_account_group_id,
        default_work_category_id: newProject.default_work_category_id,
        description: newProject.description,
        status: newProject.status,
        color: newProject.color,
      }
    }
  },
  { immediate: true }
)

// 將顏色轉換為十六進制格式
const convertToHex = (color: string): string => {
  // 如果已經是十六進制格式，直接返回
  if (/^#[0-9A-Fa-f]{6}$/.test(color)) {
    return color.toUpperCase()
  }

  // 處理 RGB 或 RGBA 格式
  const rgbMatch = color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/)
  if (rgbMatch) {
    const r = parseInt(rgbMatch[1])
    const g = parseInt(rgbMatch[2])
    const b = parseInt(rgbMatch[3])
    return '#' + [r, g, b].map(x => {
      const hex = x.toString(16)
      return hex.length === 1 ? '0' + hex : hex
    }).join('').toUpperCase()
  }

  // 如果無法識別格式，返回預設顏色
  return '#409EFF'
}

// Methods
const validate = async (): Promise<boolean> => {
  if (!formRef.value) return false
  try {
    await formRef.value.validate()
    return true
  } catch {
    return false
  }
}

const submit = async () => {
  const isValid = await validate()
  if (!isValid) return

  // 確保顏色格式正確
  const submitData = {
    ...formData.value,
    color: convertToHex(formData.value.color)
  }

  emit('submit', submitData)
}

const reset = () => {
  formRef.value?.resetFields()
  formData.value = {
    code: '',
    requirement_code: '',
    name: '',
    approved_man_days: undefined,
    default_account_group_id: undefined,
    default_work_category_id: undefined,
    description: '',
    status: 'active',
    color: '#409EFF',
  }
}

// Load data on mount
onMounted(async () => {
  try {
    await Promise.all([
      accountGroupStore.fetchAccountGroups(),
      workCategoryStore.fetchWorkCategories(),
    ])
  } catch (error) {
    console.error('載入選項資料失敗:', error)
  }
})

// Expose methods
defineExpose({
  validate,
  submit,
  reset,
})
</script>

<style scoped>
.field-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>

