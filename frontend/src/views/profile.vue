<template>
    <div class="profile-container">
        <!-- 左侧侧边栏 -->
        <div class="sidebar">
            <el-avatar :size="80" :src="userInfo.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'" />
            <h3>{{ userInfo.nickname || '用户昵称' }}</h3>
            <p style="color: gray; font-size: 12px;">ID: {{ userInfo.id || '未获取' }}</p>

            <!-- 开启 router 模式，点击跳转 -->
            <el-menu :default-active="$route.path" class="menu" router>
                <el-menu-item index="/profile">账号设置</el-menu-item>
                <el-menu-item index="/tickets">我的票夹</el-menu-item>
            </el-menu>

            <el-button type="danger" plain style="margin-top: 20px; width: 80%;" @click="handleLogout">退出登录</el-button>
        </div>

        <!-- 右侧主体内容 (账号设置) -->
        <div class="main-content">
            <el-card v-if="$route.path === '/profile'">
                <h2>账号设置</h2>
                <el-form :model="userInfo" label-width="100px" style="max-width: 500px; margin-top: 20px;">
                    <el-form-item label="用户昵称">
                        <el-input v-model="userInfo.nickname" placeholder="请输入昵称"></el-input>
                    </el-form-item>
                    <el-form-item label="个人简介">
                        <el-input v-model="userInfo.bio" type="textarea" :rows="4" placeholder="介绍一下自己吧~"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="handleUpdate" :loading="loading">保存修改</el-button>
                    </el-form-item>
                </el-form>
            </el-card>

            <!-- 如果路由是 /tickets，这里会显示子路由，但为了简单，我们在菜单中做了路由跳转，所以这里不用写 router-view -->
        </div>
    </div>
</template>

<script setup>
    import { ref, reactive, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { getUserInfoApi, updateUserInfoApi } from '../api/user'
    import { ElMessage } from 'element-plus'

    const router = useRouter()
    const loading = ref(false)
    const userInfo = reactive({
    id: '',
    nickname: '',
    bio: '',
    avatar: ''
    })

    // 获取个人信息
    const fetchUserInfo = async () => {
    try {
    const res = await getUserInfoApi()
    Object.assign(userInfo, res.data) // 将后端数据合并到响应式对象中
    } catch (error) {
    console.error('获取信息失败', error)
    }
    }

    // 更新个人信息
    const handleUpdate = async () => {
    loading.value = true
    try {
    await updateUserInfoApi({
    nickname: userInfo.nickname,
    bio: userInfo.bio
    })
    ElMessage.success('信息更新成功')
    } catch (error) {
    console.error(error)
    } finally {
    loading.value = false
    }
    }

    // 退出登录
    const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    ElMessage.success('已退出登录')
    router.push('/login')
    }

    onMounted(() => {
    fetchUserInfo()
    })
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