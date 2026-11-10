
<template>
  <div class="interest-square-page">
    <h1>🌟 兴趣广场</h1>

    <div v-if="loading" class="message">
      正在加载兴趣...
    </div>

    <div v-else-if="errorMessage" class="message error">
      {{ errorMessage }}
      <button @click="loadInterests">重新加载</button>
    </div>

    <div v-else-if="interests.length === 0" class="message">
      暂无兴趣数据
    </div>

    <div v-else class="square-container">
      <div
        class="interest-card"
        v-for="item in interests"
        :key="item.id"
        @click="openDetail(item)"
      >
        <div class="interest-icon">{{ item.icon || '🌟' }}</div>
        <h3 class="interest-name">{{ item.name }}</h3>
      </div>
    </div>

    <div
      class="modal-overlay"
      v-if="currentInterest"
      @click.self="closeDetail"
    >
      <div class="modal-content">
        <span class="close-btn" @click="closeDetail">&times;</span>
        <h2 class="modal-title">{{ currentInterest.name }}</h2>
        <p class="modal-desc">
          {{ currentInterest.desc || '欢迎探索这个兴趣分类。' }}
        </p>
        <p class="interest-id">
          兴趣编号：{{ currentInterest.id }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getInterestListApi } from '../api/interest'

const interests = ref([])
const currentInterest = ref(null)
const loading = ref(false)
const errorMessage = ref('')

const loadInterests = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await getInterestListApi()
    interests.value = response.data || []
  } catch (error) {
    errorMessage.value = '兴趣列表加载失败，请检查后端服务。'
    console.error('加载兴趣列表失败：', error)
  } finally {
    loading.value = false
  }
}

const openDetail = (item) => {
  currentInterest.value = item
}

const closeDetail = () => {
  currentInterest.value = null
}

onMounted(loadInterests)
</script>

<style scoped>
.interest-square-page {
  font-family: Arial, sans-serif;
  background-color: #f4f5f7;
  min-height: 100vh;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
}

.square-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  max-width: 1000px;
  margin: 0 auto;
}

.interest-card {
  background: white;
  width: 200px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s;
}

.interest-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.interest-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.interest-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 80%;
  max-width: 400px;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

.modal-title {
  font-size: 22px;
  margin-top: 0;
}

.modal-desc {
  color: #666;
  line-height: 1.6;
}

.interest-id {
  color: #888;
  font-size: 13px;
}

.message {
  text-align: center;
  padding: 30px;
  color: #666;
}

.error {
  color: #d93025;
}
</style>
