<template>
  <div class="create-page">
    <h2>票根创建及关联兴趣</h2>
    <div class="form-box">
      <label>票根名称：</label>
      <input v-model="ticketName" placeholder="如：某某电影票根" />
      
      <label>关联兴趣（多选）：</label>
      <div class="checkbox-group">
        <label v-for="item in interests" :key="item.id">
          <input type="checkbox" :value="item.name" v-model="selectedInterests" />
          {{ item.name }}
        </label>
      </div>

      <button @click="submitTicket">创建票根</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const ticketName = ref('')
const selectedInterests = ref([])
// 模拟后端返回的兴趣列表
const interests = ref([
  { id: 1, name: '二次元动漫' },
  { id: 2, name: '独立游戏' },
  { id: 3, name: '户外徒步' }
])

const submitTicket = () => {
  // 表单校验模拟
  if (!ticketName.value) {
    alert('票根名称不能为空！')
    return
  }
  if (selectedInterests.value.length === 0) {
    alert('请至少选择一个关联兴趣！')
    return
  }
  alert(`票根创建成功！\n名称：${ticketName.value}\n关联兴趣：${selectedInterests.value.join(', ')}`)
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
button:hover { background-color: #1976D2; }
</style>
