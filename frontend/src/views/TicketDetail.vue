
<template>
  <div class="ticket-detail-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <el-button link @click="$router.back()">← 返回列表</el-button>
          <span>票根详情</span>
        </div>
      </template>

      <div v-if="ticketInfo.ticket_id" class="detail-content">
        <h1>{{ ticketInfo.title }}</h1>

        <div class="meta-info">
          <el-tag v-if="ticketInfo.type" type="success" size="large">
            {{ ticketInfo.type }}
          </el-tag>
          <el-tag v-else type="info">未填写类型</el-tag>

          <span class="create-time">
            记录时间：{{ ticketInfo.create_time || '未知' }}
          </span>
        </div>

        <div class="rating-box">
          <span>我的评分：</span>
          <el-rate
            :model-value="ticketInfo.rating ?? 0"
            disabled
            show-score
            text-color="#ff9900"
          />
          <span v-if="ticketInfo.rating == null">暂未评分</span>
        </div>

        <el-divider />

        <div class="extra-info">
          <p><strong>活动日期：</strong>{{ ticketInfo.event_date || '未填写' }}</p>
          <p><strong>活动地点：</strong>{{ ticketInfo.venue || '未填写' }}</p>
          <p>
            <strong>关联兴趣：</strong>
            {{ ticketInfo.interests?.length ? ticketInfo.interests.join('、') : '暂无关联兴趣' }}
          </p>
        </div>

        <el-divider />

        <div class="content-box">
          <h3>体验笔记</h3>
          <p>{{ ticketInfo.memo || '暂无评价内容' }}</p>
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
  if (!id) return

  loading.value = true
  try {
    const res = await getTicketDetailApi(id)
    ticketInfo.value = res.data || {}
  } catch (error) {
    console.error('获取详情失败', error)
  } finally {
    loading.value = false
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
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.create-time {
  color: gray;
}

.rating-box {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.extra-info {
  line-height: 1.8;
  color: #606266;
}

.content-box {
  margin-top: 20px;
  line-height: 1.8;
}

.content-box p {
  white-space: pre-wrap;
}
</style>
