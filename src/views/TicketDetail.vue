<template>
    <div class="ticket-detail-container">
        <el-card v-loading="loading">
            <template #header>
                <div class="card-header">
                    <el-button link @click="$router.back()">← 返回列表</el-button>
                    <span>票根详情</span>
                </div>
            </template>

            <div v-if="ticketInfo.id" class="detail-content">
                <h1>{{ ticketInfo.title }}</h1>
                <div class="meta-info">
                    <el-tag type="success" size="large">{{ ticketInfo.type }}</el-tag>
                    <span style="margin-left: 15px; color: gray;">记录时间: {{ ticketInfo.createTime }}</span>
                </div>

                <div class="rating-box">
                    <span>我的评分：</span>
                    <el-rate v-model="ticketInfo.rating" disabled show-score text-color="#ff9900" />
                </div>

                <el-divider />

                <div class="content-box">
                    <h3>体验笔记</h3>
                    <p style="white-space: pre-wrap;">{{ ticketInfo.content || '暂无评价内容' }}</p>
                </div>
            </div>

            <el-empty v-else-if="!loading" description="未找到该票根信息" />
        </el-card>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import { useRoute } from 'vue-router'
    import { getTicketDetailApi } from '../api/ticket'

    const route = useRoute()
    const loading = ref(false)
    const ticketInfo = ref({})

    onMounted(async () => {
    const id = route.params.id
    if (id) {
    loading.value = true
    try {
    const res = await getTicketDetailApi(id)
    ticketInfo.value = res.data || {}
    } catch (error) {
    console.error('获取详情失败', error)
    } finally {
    loading.value = false
    }
    }
    })
</script>

<style scoped>
    .ticket-detail-container {
        padding: 40px;
        background-color: #f5f7fa;
        min-height: 100vh;
        max-width: 900px;
        margin: 0 auto;
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 20px;
        font-weight: bold;
    }

    .meta-info {
        margin: 15px 0;
    }

    .rating-box {
        margin-top: 20px;
        display: flex;
        align-items: center;
    }

    .content-box {
        margin-top: 20px;
        line-height: 1.8;
    }
</style>