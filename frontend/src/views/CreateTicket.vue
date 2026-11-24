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

const ticketName = ref('')
const selectedInterestIds = ref([])
const interests = ref([])
const isLoading = ref(false)

// 1. 获取真实接口数据
const fetchInterests = async () => {
  try {
    // 【真实接口对接点】后续换成 axios
    // const res = await axios.get('/api/interests/list')
    // interests.value = res.data.data
    
    // 模拟接口返回
    await new Promise(resolve => setTimeout(resolve, 500))
    interests.value = [
      { id: 101, name: '二次元动漫' },
      { id: 102, name: '独立游戏' },
      { id: 103, name: '户外徒步' }
    ]
  } catch (error) {
    alert('获取兴趣列表失败')
  }
}

// 2. 页面加载时请求数据
onMounted(() => {
  fetchInterests()
})

// 3. 提交表单
const submitTicket = async () => {
  if (!ticketName.value) {
    alert('票根名称不能为空！')
    return
  }
  if (selectedInterestIds.value.length === 0) {
    alert('请至少选择一个关联兴趣！')
    return
  }

  isLoading.value = true
  try {
    // 【真实接口对接点】后续换成 axios
    // await axios.post('/api/tickets/create', {
    //   title: ticketName.value,
    //   interestIds: selectedInterestIds.value
    // })
    
    await new Promise(resolve => setTimeout(resolve, 800))
    alert(`票根创建成功！\n关联了 ${selectedInterestIds.value.length} 个兴趣`)
  } catch (error) {
    alert('创建失败，请检查网络')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.create-page { padding: 20px; max-width: 500px; margin: 0 auto; }
h2 { text-align: center; color: #333; }
.form-box { display: flex; flex-direction: column; gap: 15px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
input[type="text"], input:not([type="checkbox"]) { padding: 10px; border: 1px solid #ccc; border-radius: 5px; width: 100%; box-sizing: border-box; }
.checkbox-group { display: flex; flex-direction: column; gap: 8px; }
.checkbox-group label { display: flex; align-items: center; gap: 8px; cursor: pointer; }
button { padding: 10px; background-color: #2196F3; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px;}
button:disabled { background-color: #90caf9; cursor: not-allowed; }
.loading-text { color: #888; font-size: 14px; }
</style>
