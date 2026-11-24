
<template>
  <div class="ticket-edit-container">
    <el-card>
      <h2>{{ isEdit ? '编辑票根' : '记录新票根' }}</h2>

      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-width="100px"
        style="max-width: 600px; margin-top: 30px"
      >
        <!-- 体验名称 -->
        <el-form-item label="体验名称" prop="title">
          <el-input
            v-model="form.title"
            placeholder="如：电影《奥本海默》"
          />
        </el-form-item>

        <!-- 体验类型 -->
        <el-form-item label="体验类型" prop="type">
          <el-select
            v-model="form.type"
            placeholder="请选择类型"
            style="width: 100%"
          >
            <el-option label="电影" value="电影" />
            <el-option label="书籍" value="书籍" />
            <el-option label="剧本杀" value="剧本杀" />
            <el-option label="密室" value="密室" />
            <el-option label="旅游" value="旅游" />
            <el-option label="演唱会" value="演唱会" />
            <el-option label="展览" value="展览" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>

        <!-- 个人评分 -->
        <el-form-item label="我的评分" prop="rating">
          <el-rate
            v-model="form.rating"
            show-text
            :texts="['避雷', '较差', '还行', '推荐', '神作']"
          />
        </el-form-item>

        <!-- 活动日期 -->
        <el-form-item label="活动日期">
          <el-date-picker
            v-model="form.event_date"
            type="date"
            placeholder="选择活动日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
            clearable
          />
        </el-form-item>

        <!-- 活动地点 -->
        <el-form-item label="活动地点">
          <el-input
            v-model="form.venue"
            placeholder="请输入活动地点"
          />
        </el-form-item>

        <!-- 关联兴趣 -->
        <el-form-item label="关联兴趣">
          <el-select
            v-model="form.interests"
            multiple
            collapse-tags
            collapse-tags-tooltip
            placeholder="请选择关联兴趣（可多选）"
            style="width: 100%"
            :loading="interestLoading"
          >
            <el-option
              v-for="item in interests"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>

          <div v-if="interestError" class="error-tip">
            {{ interestError }}
            <el-button
              link
              type="primary"
              @click="loadInterests"
            >
              重新加载
            </el-button>
          </div>
        </el-form-item>

        <!-- 体验笔记 -->
        <el-form-item label="体验笔记">
          <el-input
            v-model="form.memo"
            type="textarea"
            :rows="6"
            maxlength="500"
            show-word-limit
            placeholder="写下你的推荐或避雷建议..."
          />
        </el-form-item>

        <!-- 操作按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            @click="handleSubmit"
            :loading="loading"
          >
            {{ isEdit ? '保存修改' : '确认记录' }}
          </el-button>

          <el-button @click="$router.back()">
            取消
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  createTicketApi,
  updateTicketApi,
  getTicketDetailApi
} from '../api/ticket'
import { getInterestListApi } from '../api/interest'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const formRef = ref(null)
const loading = ref(false)
const interestLoading = ref(false)
const interestError = ref('')

// 判断是编辑还是新增
const isEdit = computed(() => !!route.params.id)

// 表单数据
const form = reactive({
  title: '',
  type: '',
  rating: 5,
  event_date: '',
  venue: '',
  memo: '',
  interests: []
})

// 表单校验
const rules = {
  title: [
    { required: true, message: '请输入体验名称', trigger: 'blur' },
    { max: 100, message: '名称不能超过100个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择体验类型', trigger: 'change' }
  ]
}

// 兴趣列表
const interests = ref([])

// 获取兴趣列表
const loadInterests = async () => {
  interestLoading.value = true
  interestError.value = ''

  try {
    const res = await getInterestListApi()
    interests.value = res.data || []
  } catch (error) {
    interestError.value = '兴趣列表加载失败，请检查后端服务'
    console.error('获取兴趣列表失败：', error)
  } finally {
    interestLoading.value = false
  }
}

// 编辑时获取原有票根
const loadTicketDetail = async () => {
  try {
    const res = await getTicketDetailApi(route.params.id)

    if (res.data) {
      Object.assign(form, {
        title: res.data.title || '',
        type: res.data.type || '',
        rating: res.data.rating ?? 5,
        venue: res.data.venue || '',
        memo: res.data.content ?? res.data.memo ?? '',
        event_date: res.data.eventDate ?? res.data.event_date ?? '',
        interests: res.data.interests || []
      })
    }
  } catch (error) {
    console.error('获取票根详情失败：', error)
    ElMessage.error('获取票根详情失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  const valid = await formRef.value.validate().catch(() => false)

  if (!valid) return

  loading.value = true

  try {
    const data = {
      title: form.title,
      type: form.type,
      rating: form.rating,
      event_date: form.event_date || null,
      venue: form.venue,
      content: form.memo,
      memo: form.memo,
      interests: form.interests
    }

    if (isEdit.value) {
      await updateTicketApi(route.params.id, data)
      ElMessage.success('更新请求已提交')
    } else {
      await createTicketApi(data)
      ElMessage.success('创建请求已提交')
    }

    router.push('/tickets')
  } catch (error) {
    console.error('提交票根失败：', error)
    ElMessage.error('提交失败，请检查后端接口')
  } finally {
    loading.value = false
  }
}

// 页面初始化
onMounted(async () => {
  await loadInterests()

  if (isEdit.value) {
    await loadTicketDetail()
  }
})
</script>

<style scoped>
.ticket-edit-container {
  padding: 40px;
  background-color: #f5f7fa;
  min-height: 100vh;
  display: flex;
  justify-content: center;
}

.el-card {
  width: 100%;
  max-width: 800px;
}

.error-tip {
  color: #f56c6c;
  font-size: 13px;
  margin-top: 5px;
}
</style>
