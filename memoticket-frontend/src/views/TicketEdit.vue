<template>
    <div class="ticket-edit-container">
        <el-card>
            <h2>{{ isEdit ? '编辑票根' : '记录新票根' }}</h2>

            <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" style="max-width: 600px; margin-top: 30px;">
                <el-form-item label="体验名称" prop="title">
                    <el-input v-model="form.title" placeholder="如：电影《奥本海默》、剧本杀《青川怪谈》" />
                </el-form-item>

                <el-form-item label="体验类型" prop="type">
                    <el-select v-model="form.type" placeholder="请选择类型" style="width: 100%">
                        <el-option label="电影" value="电影" />
                        <el-option label="书籍" value="书籍" />
                        <el-option label="剧本杀" value="剧本杀" />
                        <el-option label="密室" value="密室" />
                        <el-option label="旅游" value="旅游" />
                    </el-select>
                </el-form-item>

                <el-form-item label="活动日期" prop="event_date">
                    <el-date-picker v-model="form.event_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width: 100%" />
                </el-form-item>

                <el-form-item label="活动地点" prop="venue">
                    <el-input v-model="form.venue" placeholder="如：万达影城" />
                </el-form-item>

                <el-form-item label="我的评分" prop="rating">
                    <el-rate v-model="form.rating" show-text :texts="['避雷', '较差', '还行', '推荐', '神作']" />
                </el-form-item>

                <el-form-item label="体验笔记" prop="content">
                    <el-input v-model="form.content" type="textarea" :rows="6" placeholder="写下你的推荐或避雷建议..." maxlength="500" show-word-limit />
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="handleSubmit" :loading="loading">{{ isEdit ? '保存修改' : '确认记录' }}</el-button>
                    <el-button @click="$router.back()">取消</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
    import { ref, reactive, onMounted, computed } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import request from '../utils/request'
    import { ElMessage } from 'element-plus'

    const route = useRoute()
    const router = useRouter()
    const formRef = ref(null)
    const loading = ref(false)

    const isEdit = computed(() => !!route.params.id)

    // 表单字段（对应后端要求）
    const form = reactive({
    title: '',
    type: '',
    rating: 5,
    content: '',
    event_date: '', // 后端入参要求带下划线
    venue: ''
    })

    const rules = {
    title: [
    { required: true, message: '请输入体验名称', trigger: 'blur' },
    { max: 100, message: '不能超过 100 个字符', trigger: 'blur' }
    ],
    type: [{ required: true, message: '请选择类型', trigger: 'change' }]
    }

    onMounted(async () => {
    if (isEdit.value) {
    try {
    const res = await request.get(`/api/tickets/${route.params.id}`)
    if (res.data) {
    // 回显数据，注意把返回的 eventDate 赋给表单的 event_date
    Object.assign(form, {
    title: res.data.title,
    type: res.data.type,
    rating: res.data.rating || 5,
    content: res.data.content,
    event_date: res.data.eventDate || '',
    venue: res.data.venue || ''
    })
    }
    } catch (error) {
    ElMessage.error('获取数据失败')
    }
    }
    })

    const handleSubmit = () => {
    formRef.value.validate(async (valid) => {
    if (valid) {
    loading.value = true
    try {
    // 构造提交给后端的 payload
    const payload = { ...form }

    if (isEdit.value) {
    await request.put(`/api/tickets/${route.params.id}`, payload)
    ElMessage.success('更新成功')
    } else {
    await request.post('/api/tickets', payload)
    ElMessage.success('记录成功')
    }
    router.push('/tickets')
    } catch (error) {
    console.error(error)
    } finally {
    loading.value = false
    }
    }
    })
    }
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
</style>