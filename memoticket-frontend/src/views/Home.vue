<template>
  <div class="home-page">
    <header class="topbar">
      <div class="brand">MemoTicket</div>

      <nav class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/community">兴趣社区</router-link>
        <router-link to="/community/feed">社区动态</router-link>
        <router-link v-if="isLoggedIn" to="/tickets">我的票夹</router-link>
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
      <p>浏览兴趣社区的动态，分享你的体验，管理属于你的票根。</p>

      <div class="entry-cards">
        <router-link class="entry-card" to="/community">
          <h2>兴趣社区</h2>
          <p>找同好，看大家在体验什么。</p>
        </router-link>

        <router-link class="entry-card" to="/community/feed">
          <h2>社区动态</h2>
          <p>按兴趣筛选最新的体验分享。</p>
        </router-link>

        <router-link class="entry-card" to="/share/create">
          <h2>发布分享</h2>
          <p>把这次体验写成一张票根。</p>
        </router-link>

        <router-link v-if="isLoggedIn" class="entry-card" to="/tickets">
          <h2>我的票夹</h2>
          <p>管理已记录的票根。</p>
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
    import { ref, watch } from 'vue'
    import { useRoute } from 'vue-router'

    const route = useRoute()
    const isLoggedIn = ref(Boolean(localStorage.getItem('token')))

    // 监听路由变化，一旦页面跳转（比如登录成功跳过来），重新检查 token
    watch(
    () => route.path,
    () => {
    isLoggedIn.value = Boolean(localStorage.getItem('token'))
    }
    )
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
  flex-wrap: wrap;
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