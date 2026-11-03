<template>
  <div class="interest-square-page">
    <h1>🌟 兴趣广场</h1>
    
    <!-- 兴趣广场网格 -->
    <div class="square-container">
      <div 
        class="interest-card" 
        v-for="item in interests" 
        :key="item.id"
        @click="openDetail(item)"
      >
        <div class="interest-icon">{{ item.icon }}</div>
        <h3 class="interest-name">{{ item.name }}</h3>
      </div>
    </div>

    <!-- 兴趣详情基础页面 (弹窗) -->
    <div class="modal-overlay" v-if="currentInterest" @click.self="closeDetail">
      <div class="modal-content">
        <span class="close-btn" @click="closeDetail">&times;</span>
        <h2 class="modal-title">{{ currentInterest.name }}</h2>
        <p class="modal-desc">{{ currentInterest.desc }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 预设兴趣数据
const interests = ref([
  { id: 1, name: "二次元动漫", icon: "🎨", desc: "这里是二次元爱好者的聚集地，分享新番、漫展、手办等。" },
  { id: 2, name: "独立游戏", icon: "🎮", desc: "探讨不随波逐流的独立游戏，如《空洞骑士》《星露谷物语》。" },
  { id: 3, name: "户外徒步", icon: "🏕️", desc: "周末一起去爬山、徒步，感受大自然的魅力。" },
  { id: 4, name: "美食探店", icon: "🍔", desc: "寻找城市角落里的美味，分享探店心得。" }
])

// 当前选中的兴趣（控制弹窗）
const currentInterest = ref(null)

// 打开详情
const openDetail = (item) => {
  currentInterest.value = item
}

// 关闭详情
const closeDetail = () => {
  currentInterest.value = null
}
</script>

<style scoped>
/* 基础样式 */
.interest-square-page { font-family: Arial, sans-serif; background-color: #f4f5f7; min-height: 100vh; padding: 20px; }
h1 { text-align: center; color: #333; }

/* 网格布局 */
.square-container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; max-width: 1000px; margin: 0 auto; }

/* 卡片样式 */
.interest-card {
  background: white; width: 200px; padding: 20px; border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; cursor: pointer;
  transition: transform 0.2s;
}
.interest-card:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
.interest-icon { font-size: 40px; margin-bottom: 10px; }
.interest-name { font-size: 18px; font-weight: bold; color: #333; margin: 0; }

/* 弹窗样式 */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center;
}
.modal-content {
  background: white; padding: 30px; border-radius: 12px; width: 80%; max-width: 400px;
  position: relative;
}
.close-btn { position: absolute; top: 10px; right: 15px; font-size: 24px; cursor: pointer; color: #999; }
.close-btn:hover { color: #333; }
.modal-title { font-size: 22px; margin-top: 0; }
.modal-desc { color: #666; line-height: 1.6; }
</style>
