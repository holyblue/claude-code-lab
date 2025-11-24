<template>
  <div class="milestone-manager">
    <el-button type="primary" @click="handleAdd" :icon="Plus">新增里程碑</el-button>

    <el-table :data="milestones" style="margin-top: 16px" v-loading="loading" border stripe>
      <el-table-column prop="name" label="里程碑" min-width="180" />
      <el-table-column prop="start_date" label="起始日" width="120" align="center">
        <template #default="{ row }">
          {{ formatDate(row.start_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="end_date" label="完成日" width="120" align="center">
        <template #default="{ row }">
          {{ formatDate(row.end_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="說明" min-width="200" show-overflow-tooltip />
      <el-table-column label="操作" width="150" align="center" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleEdit(row)">編輯</el-button>
          <el-button link type="danger" @click="handleDelete(row)">刪除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/編輯對話框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '編輯里程碑' : '新增里程碑'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="名稱" prop="name">
          <el-input v-model="form.name" placeholder="請輸入里程碑名稱" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="起始日" prop="start_date">
          <el-date-picker
            v-model="form.start_date"
            type="date"
            format="YYYY/MM/DD"
            value-format="YYYY-MM-DD"
            placeholder="選擇起始日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="完成日" prop="end_date">
          <el-date-picker
            v-model="form.end_date"
            type="date"
            format="YYYY/MM/DD"
            value-format="YYYY-MM-DD"
            placeholder="選擇完成日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="說明" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="選填"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">確定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { milestonesApi } from '@/api/milestones'
import type { Milestone, MilestoneCreate, MilestoneUpdate } from '@/types'

const props = defineProps<{
  projectId: number
}>()

const emit = defineEmits<{
  refresh: []
}>()

const milestones = ref<Milestone[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const saving = ref(false)
const formRef = ref<FormInstance>()

/**
 * 獲取今天的日期字串 (YYYY-MM-DD)
 */
const getTodayDate = (): string => {
  return new Date().toISOString().split('T')[0]
}

const form = reactive<MilestoneCreate & { id?: number }>({
  name: '',
  start_date: getTodayDate(),
  end_date: getTodayDate(),
  description: '',
  display_order: 0
})

// 表單驗證規則
const rules: FormRules = {
  name: [{ required: true, message: '請輸入里程碑名稱', trigger: 'blur' }],
  start_date: [{ required: true, message: '請選擇起始日期', trigger: 'change' }],
  end_date: [
    { required: true, message: '請選擇完成日期', trigger: 'change' },
    {
      validator: (rule, value, callback) => {
        if (value && form.start_date && value < form.start_date) {
          callback(new Error('完成日期不能早於起始日期'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

/**
 * 載入里程碑列表
 */
const loadMilestones = async () => {
  loading.value = true
  try {
    const res = await milestonesApi.getProjectMilestones(props.projectId)
    milestones.value = res.data
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '載入里程碑失敗')
  } finally {
    loading.value = false
  }
}

/**
 * 格式化日期顯示（YYYY-MM-DD -> YYYY/MM/DD）
 */
const formatDate = (date: string) => {
  return date.replace(/-/g, '/')
}

/**
 * 新增里程碑
 */
const handleAdd = () => {
  isEdit.value = false
  Object.assign(form, {
    name: '',
    start_date: getTodayDate(),
    end_date: getTodayDate(),
    description: '',
    display_order: milestones.value.length
  })
  dialogVisible.value = true
}

/**
 * 編輯里程碑
 */
const handleEdit = (row: Milestone) => {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    name: row.name,
    start_date: row.start_date,
    end_date: row.end_date,
    description: row.description || '',
    display_order: row.display_order
  })
  dialogVisible.value = true
}

/**
 * 保存里程碑（新增或編輯）
 */
const handleSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  saving.value = true
  try {
    if (isEdit.value && form.id) {
      // 編輯
      const updateData: MilestoneUpdate = {
        name: form.name,
        start_date: form.start_date,
        end_date: form.end_date,
        description: form.description || undefined,
        display_order: form.display_order
      }
      await milestonesApi.updateMilestone(form.id, updateData)
      ElMessage.success('更新成功')
    } else {
      // 新增
      const createData: MilestoneCreate = {
        name: form.name,
        start_date: form.start_date,
        end_date: form.end_date,
        description: form.description || undefined,
        display_order: form.display_order
      }
      await milestonesApi.createMilestone(props.projectId, createData)
      ElMessage.success('新增成功')
    }

    dialogVisible.value = false
    await loadMilestones()
    emit('refresh')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失敗')
  } finally {
    saving.value = false
  }
}

/**
 * 刪除里程碑
 */
const handleDelete = async (row: Milestone) => {
  try {
    await ElMessageBox.confirm(`確定要刪除里程碑「${row.name}」嗎？`, '確認刪除', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await milestonesApi.deleteMilestone(row.id)
    ElMessage.success('刪除成功')
    await loadMilestones()
    emit('refresh')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '刪除失敗')
    }
  }
}

// 組件掛載時載入里程碑
onMounted(() => {
  loadMilestones()
})
</script>

<style scoped>
.milestone-manager {
  padding: 20px 0;
}
</style>

