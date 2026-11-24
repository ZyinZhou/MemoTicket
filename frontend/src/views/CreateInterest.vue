<template>
  <div class="create-page">
    <h2>自定义兴趣创建</h2>
    <div class="form-box">
      <label>兴趣名称：</label>
      <input v-model="interestName" placeholder="请输入兴趣名称" />
      
      <label>兴趣简介：</label>
      <textarea v-model="interestDesc" placeholder="介绍一下这个兴趣吧"></textarea>
      
      <button @click="submitInterest" :disabled="isLoading">
        {{ isLoading ? '创建中...' : '提交创建' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const interestName = ref('')
const interestDesc = ref('')
const isLoading = ref(false)

const submitInterest = async () => {
  if (!interestName.value) {
    alert('兴趣名称不能为空！')
    return
  }
  if (interestDesc.value.length > 100) {
    alert('简介不能超过100字！')
    return
  }

  isLoading.value = true
  try {
    // 【真实接口对接点】替换为你后端的真实地址
    // const res = await axios.post('/api/interests/create', {
    //   name: interestName.value,
    //   description: interestDesc.value
    // })
    // if (res.data.code === 200) { alert('创建成功！') }
    
    // 模拟异步请求（为了测试防抖和加载状态）
    await new Promise(resolve => setTimeout(resolve, 800))
    alert(`创建成功！兴趣：${interestName.value}`)
    interestName.value = ''
    interestDesc.value = ''
  } catch (error) {
    console.error('创建失败', error)
    alert('网络开小差了，请稍后再试')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.create-page { padding: 20px; max-width: 500px; margin: 0 auto; }
h2 { text-align: center; color: #333; }
.form-box { display: flex; flex-direction: column; gap: 15px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
input, textarea { padding: 10px; border: 1px solid #ccc; border-radius: 5px; width: 100%; box-sizing: border-box; }
button { padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
button:disabled { background-color: #a5d6a7; cursor: not-allowed; }
</style>········································································································································································
