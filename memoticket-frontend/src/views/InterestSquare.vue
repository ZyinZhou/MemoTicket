<template>
    <div class="interest-square-page">
        <div class="page-header">
            <div>
                <h1>🌟 兴趣广场</h1>
                <p>发现主题，探索同好。</p>
            </div>
        </div>

        <div v-if="loading" class="message">正在加载兴趣...</div>
        <div v-else-if="errorMessage" class="message error">
            {{ errorMessage }} <el-button link @click="loadInterests">重新加载</el-button>
        </div>
        <template v-else>
            <div class="square-container">
                <div v-for="item in interests" :key="item.id" class="interest-card">
                    <div class="interest-icon">🌟</div>
                    <h3 class="interest-name">{{ item.name }}</h3>
                </div>
            </div>
            <el-empty v-if="interests.length === 0" description="暂无兴趣数据" />
        </template>
    </div>
</template>

<script setup>
    import { onMounted, ref } from 'vue'
    import { getInterestListApi } from '../api/interest'

    const interests = ref([])
    const loading = ref(false)
    const errorMessage = ref('')

    const loadInterests = async () => {
    loading.value = true
    errorMessage.value = ''
    try {
    const res = await getInterestListApi()
    interests.value = res.data || []
    } catch (error) {
    errorMessage.value = '兴趣列表加载失败，请检查后端服务。'
    } finally {
    loading.value = false
    }
    }

    onMounted(loadInterests)
</script>

<style scoped>
    .interest-square-page {
        min-height: 100vh;
        padding: 30px;
        background: #f4f5f7;
    }

    .page-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1100px;
        margin: 0 auto 24px;
    }

    h1 {
        margin: 0;
        color: #333;
    }

    .page-header p {
        color: #777;
    }

    .square-container {
        display: flex;
        flex-wrap: wrap;
        gap: 18px;
        max-width: 1100px;
        margin: 0 auto;
    }

    .interest-card {
        width: 190px;
        padding: 20px;
        background: white;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 10px #00000012;
        cursor: pointer;
        transition: transform 0.2s;
    }

        .interest-card:hover {
            transform: translateY(-3px);
        }

    .interest-icon {
        font-size: 36px;
    }

    .interest-name {
        margin: 8px 0;
        color: #333;
    }

    .message {
        padding: 25px;
        color: #777;
        text-align: center;
    }

    .error {
        color: #d93025;
    }
</style>