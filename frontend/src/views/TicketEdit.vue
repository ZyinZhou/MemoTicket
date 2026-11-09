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

                <el-form-item label="我的评分" prop="rating">
                    <el-rate v-model="form.rating" show-text :texts="['避雷', '较差', '还行', '推荐', '神作']" />
                </el-form-item>

                <el-form-item label="体验笔记" prop="content">
                    <el-input v-model="form.content" type="textarea" :rows="6" placeholder="写下你的推荐或避雷建议..." />
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
    import { createTicketApi, updateTicketApi, getTicketDetailApi } from '../api/ticket'
    import { ElMessage } from 'element-plus'

    const route = useRoute()
    const router = useRouter()
    const formRef = ref(null)
    const loading = ref(false)

    // 判断是编辑还是新增
    const isEdit = computed(() => !!route.params.id)

    const form = reactive({
    title: '',
    type: '',
    rating: 5,
    content: ''
    })

    // 简单表单校验
    const rules = {
    title: [{ required: true, message: '请输入体验名称', trigger: 'blur' }],
    type: [{ required: true, message: '请选择类型', trigger: 'change' }]
    }

    // 如果是编辑，进入页面时拉取原有数据
    onMounted(async () => {
    if (isEdit.value) {
    try {
    const res = await getTicketDetailApi(route.params.id)
    if (res.data) {
    Object.assign(form, res.data) // 回显数据
    }
    } catch (error) {
    ElMessage.error('获取数据失败')
    }
    }
    })

    // 提交表单
    const handleSubmit = () => {
    formRef.value.validate(async (valid) => {
    if (valid) {
    loading.value = true
    try {
    if (isEdit.value) {
    await updateTicketApi(route.params.id, form)
    ElMessage.success('更新成功')
    } else {
    await createTicketApi(form)
    ElMessage.success('记录成功')
    }
    router.push('/tickets') // 成功后返回列表页
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