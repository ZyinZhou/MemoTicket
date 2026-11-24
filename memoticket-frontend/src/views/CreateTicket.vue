<template>
    <div class="create-page">
        <h2>票根创建及关联兴趣</h2>
        <div class="form-box">
            <label>票根名称：</label>
            <input v-model="ticketName" placeholder="如：某某电影票根" />

            <label>关联兴趣（多选）：</label>
            <div class="checkbox-group" v-if="interests.length > 0">
                <label v-for="item in interests" :key="item.id">
                    <input type="checkbox" :value="item.id" v-model="selectedInterestIds" />
                    {{ item.name }}
                </label>
            </div>
            <div v-else class="loading-text">正在加载兴趣列表...</div>

            <button @click="submitTicket" :disabled="isLoading">
                {{ isLoading ? '提交中...' : '创建票根' }}
            </button>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import request from '../utils/request'
    import { ElMessage } from 'element-plus'

    const ticketName = ref('')
    const selectedInterestIds = ref([])
    const interests = ref([])
    const isLoading = ref(false)

    // 1. 真实拉取后端兴趣数据
    const fetchInterests = async () => {
    try {
    const res = await request.get('/api/interests')
    interests.value = res.data || []
    } catch (error) {
    console.error('获取兴趣失败', error)
    }
    }

    onMounted(() => {
    fetchInterests()
    })

    // 2. 真实提交数据给后端
    const submitTicket = async () => {
    if (!ticketName.value.trim()) {
    ElMessage.warning('票根名称不能为空！')
    return
    }
    if (selectedInterestIds.value.length === 0) {
    ElMessage.warning('请至少选择一个关联兴趣！')
    return
    }

    isLoading.value = true
    try {
    // 对接真实接口：传 title 和 interests
    await request.post('/api/tickets', {
    title: ticketName.value.trim(),
    interests: selectedInterestIds.value
    })
    ElMessage.success('票根创建成功！')

    // 成功后清空表单
    ticketName.value = ''
    selectedInterestIds.value = []
    } catch (error) {
    console.error('创建失败', error)
    // 错误提示已经由 request.js 的拦截器统一弹出了
    } finally {
    isLoading.value = false
    }
    }
</script>

<style scoped>
    .create-page {
        padding: 20px;
        max-width: 500px;
        margin: 0 auto;
    }

    h2 {
        text-align: center;
        color: #333;
    }

    .form-box {
        display: flex;
        flex-direction: column;
        gap: 15px;
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    input[type="text"], input:not([type="checkbox"]) {
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        width: 100%;
        box-sizing: border-box;
    }

    .checkbox-group {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

        .checkbox-group label {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }

    button {
        padding: 10px;
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
    }

        button:disabled {
            background-color: #90caf9;
            cursor: not-allowed;
        }

    .loading-text {
        color: #888;
        font-size: 14px;
    }
</style>