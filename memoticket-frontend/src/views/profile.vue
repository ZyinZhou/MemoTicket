<template>
    <div class="profile-container">
        <div class="sidebar">
            <el-avatar :size="80" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
            <h3>用户 ID: {{ userId }}</h3>
            <p style="color: gray; font-size: 12px;">暂未对接用户信息接口</p>

            <el-menu :default-active="$route.path" class="menu" router>
                <el-menu-item index="/profile">账号设置</el-menu-item>
                <el-menu-item index="/tickets">我的票夹</el-menu-item>
            </el-menu>

            <el-button type="danger" plain style="margin-top: 20px; width: 80%;" @click="handleLogout">退出登录</el-button>
        </div>

        <div class="main-content">
            <el-card>
                <h2>账号设置</h2>
                <p style="color: #999; margin-top: 10px;">后端暂未提供此模块接口，目前仅作 UI 展示。</p>
                <el-form label-width="100px" style="max-width: 500px; margin-top: 20px;">
                    <el-form-item label="用户昵称">
                        <el-input placeholder="等待后端提供接口" disabled></el-input>
                    </el-form-item>
                    <el-form-item label="个人简介">
                        <el-input type="textarea" :rows="4" placeholder="等待后端提供接口" disabled></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" disabled>保存修改</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { ElMessage } from 'element-plus'

    const router = useRouter()
    const userId = ref(localStorage.getItem('user_id'))

    const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    ElMessage.success('已退出登录')
    router.push('/login')
    }
</script>

<style scoped>
    .profile-container {
        display: flex;
        height: 100vh;
        padding: 20px;
        box-sizing: border-box;
        background-color: #f5f7fa;
    }

    .sidebar {
        width: 250px;
        display: flex;
        flex-direction: column;
        align-items: center;
        background: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
        margin-right: 20px;
    }

    .menu {
        width: 100%;
        margin-top: 20px;
        border-right: none;
    }

    .main-content {
        flex: 1;
    }
</style>