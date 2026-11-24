<template>
  <div class="home-page">
    <header class="topbar">
      <div class="brand">MemoTicket</div>

      <nav class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/interests">兴趣广场</router-link>
        <router-link v-if="isLoggedIn" to="/profile">个人主页</router-link>
      </nav>

      <div class="auth-links">
        <template v-if="isLoggedIn">
          <router-link to="/profile">已登录</router-link>
        </template>
        <template v-else>
          <router-link to="/login">登录</router-link>
          <router-link to="/register">注册</router-link>
        </template>
      </div>
    </header>

    <main class="home-content">
      <h1>记录每一次值得回忆的体验</h1>
      <p>浏览兴趣，管理票根，保存属于你的体验记录。</p>

      <div class="entry-cards">
        <router-link class="entry-card" to="/interests">
          <h2>兴趣广场</h2>
          <p>发现感兴趣的主题和内容。</p>
        </router-link>

        <router-link v-if="isLoggedIn" class="entry-card" to="/profile">
          <h2>个人主页</h2>
          <p>管理个人资料和我的票夹。</p>
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const isLoggedIn = computed(() => Boolean(localStorage.getItem('token')))
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.topbar {
  display: flex;
  align-items: center;
  padding: 18px 40px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.brand {
  font-size: 22px;
  font-weight: 700;
  margin-right: 40px;
}

.nav-links,
.auth-links {
  display: flex;
  gap: 20px;
}

.nav-links {
  flex: 1;
}

a {
  color: #333;
  text-decoration: none;
}

.router-link-active {
  color: #409eff;
}

.home-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 100px 24px;
  text-align: center;
}

.home-content h1 {
  font-size: 36px;
  margin-bottom: 16px;
}

.home-content p {
  color: #666;
}

.entry-cards {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 48px;
}

.entry-card {
  width: 260px;
  padding: 28px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
}

.entry-card h2 {
  margin-top: 0;
}
</style>