<template>
    <div class="profile-container">
        <!-- 左侧侧边栏 -->
        <div class="sidebar">
            <el-avatar :size="80" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
            <h3>用户昵称</h3>
            <p style="color: gray; font-size: 12px;">ID: {{ userId }}</p>
            <el-menu default-active="1" class="menu">
                <el-menu-item index="1">我的主页</el-menu-item>
                <el-menu-item index="2">我的票根</el-menu-item>
                <el-menu-item index="3">账号设置</el-menu-item>
            </el-menu>
            <el-button type="danger" plain style="margin-top: 20px; width: 80%;" @click="handleLogout">退出登录</el-button>
        </div>

        <!-- 右侧主体内容 -->
        <div class="main-content">
            <el-card>
                <h2>欢迎回来！</h2>
                <p>这里将会展示你的票根记录和同好推荐。</p>
            </el-card>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()
    const userId = ref(localStorage.getItem('user_id'))

    // 退出登录：清除 token 并回到登录页
    const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    router.push('/login')
    }
</script>

<style scoped>
    .profile-container {
        display: flex;
        height: 100vh;
        padding: 20px;
        box-sizing: border-box;
    }

    .sidebar {
        width: 250px;
        display: flex;
        flex-direction: column;
        align-items: center;
        border-right: 1px solid #e0e0e0;
        padding-right: 20px;
    }

    .menu {
        width: 100%;
        margin-top: 20px;
        border-right: none;
    }

    .main-content {
        flex: 1;
        padding-left: 20px;
    }
</style>