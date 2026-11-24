<template>
    <div class="community-page">
        <header class="c-nav">
            <router-link to="/community" class="brand">
                <span class="brand-mark">🎫</span>
                <span class="brand-name">MemoTicket</span>
                <span class="brand-sub">社区</span>
            </router-link>

            <nav class="c-nav-links">
                <router-link to="/home" class="nav-link">首页</router-link>
                <router-link to="/community" class="nav-link" :class="{ active: active === 'home' }">社区广场</router-link>
                <router-link to="/community/feed" class="nav-link" :class="{ active: active === 'feed' }">社区动态</router-link>
                <router-link to="/tickets" class="nav-link">我的票夹</router-link>
            </nav>

            <div class="c-nav-actions">
                <el-button type="primary" round @click="router.push('/share/create')">✏️ 发布分享</el-button>

                <template v-if="isLoggedIn">
                    <router-link to="/profile" class="profile-link">
                        <el-avatar :size="30" class="nav-avatar">我</el-avatar>
                    </router-link>
                </template>
                <template v-else>
                    <router-link to="/login" class="nav-link login-link">登录</router-link>
                    <router-link to="/register" class="nav-link register-link">注册</router-link>
                </template>
            </div>
        </header>

        <main class="c-main">
            <slot />
        </main>

        <footer class="c-footer">
            MemoTicket · 记录每一次值得回忆的体验
        </footer>
    </div>
</template>

<script setup>
    import { ref, watch } from 'vue'
    import { useRoute, useRouter } from 'vue-router'

    defineProps({
    active: {
    type: String,
    default: ''
    }
    })

    const route = useRoute()
    const router = useRouter()
    const isLoggedIn = ref(Boolean(localStorage.getItem('token')))

    // 登录状态可能因跳转而变化，路由一变就重新读取
    watch(
    () => route.fullPath,
    () => {
    isLoggedIn.value = Boolean(localStorage.getItem('token'))
    }
    )
</script>

<style scoped>
    /* 社区页面不受默认模板 #app 定宽与居中限制 */
    :global(#app) {
        width: 100%;
        max-width: none;
        border-left: none;
        border-right: none;
        text-align: left;
        display: block;
    }

    .community-page {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        background: #f5f7fb;
        color: #303133;
        font-size: 15px;
        line-height: 1.6;
    }

    .c-nav {
        position: sticky;
        top: 0;
        z-index: 20;
        display: flex;
        align-items: center;
        gap: 26px;
        padding: 12px 32px;
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #ebeef5;
    }

    .brand {
        display: flex;
        align-items: baseline;
        gap: 6px;
        text-decoration: none;
        color: #303133;
    }

    .brand-mark {
        font-size: 20px;
    }

    .brand-name {
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 0.2px;
    }

    .brand-sub {
        padding: 1px 7px;
        font-size: 12px;
        color: #409eff;
        background: #ecf5ff;
        border-radius: 9px;
    }

    .c-nav-links {
        display: flex;
        flex: 1;
        gap: 22px;
        min-width: 0;
    }

    .nav-link {
        flex-shrink: 0;
        white-space: nowrap;
        color: #606266;
        font-size: 14px;
        text-decoration: none;
        padding: 4px 0;
        border-bottom: 2px solid transparent;
        transition: color 0.2s;
    }

    .nav-link:hover {
        color: #409eff;
    }

    .nav-link.active {
        color: #409eff;
        font-weight: 600;
        border-bottom-color: #409eff;
    }

    .c-nav-actions {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .profile-link {
        display: flex;
        align-items: center;
    }

    .nav-avatar {
        background: linear-gradient(135deg, #409eff, #7c4dff);
        color: #fff;
        font-size: 13px;
    }

    .login-link {
        font-weight: 600;
    }

    .register-link {
        padding: 4px 12px;
        border-radius: 14px;
        background: #f0f2f5;
    }

    .c-main {
        flex: 1;
        width: 100%;
        max-width: 1120px;
        margin: 0 auto;
        padding: 28px 24px 60px;
        box-sizing: border-box;
    }

    .c-footer {
        padding: 22px;
        text-align: center;
        font-size: 13px;
        color: #a8abb2;
        background: #fff;
        border-top: 1px solid #ebeef5;
    }

    @media (max-width: 900px) {
        .c-nav {
            flex-wrap: wrap;
            gap: 12px;
            padding: 10px 16px;
        }

        .c-nav-links {
            order: 3;
            flex: 1 0 100%;
            width: 100%;
            flex-wrap: wrap;
            gap: 10px 18px;
            padding-bottom: 2px;
        }

        .c-nav-actions {
            gap: 10px;
        }

        .c-nav-actions :deep(.el-button) {
            padding: 8px 13px;
            font-size: 13px;
        }

        .c-main {
            padding: 20px 14px 44px;
        }
    }

    @media (max-width: 560px) {
        .register-link {
            display: none;
        }
    }
</style>
