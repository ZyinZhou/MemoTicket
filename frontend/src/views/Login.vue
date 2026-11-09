<template>
    <div class="auth-container">
        <el-card class="auth-card">
            <h2 style="text-align: center;">MemoTicket 登录</h2>
            <el-form :model="loginForm" :rules="rules" ref="loginRef" label-width="80px">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="loginForm.username" placeholder="请输入用户名" />
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleLogin" style="width: 100%;">登录</el-button>
                </el-form-item>
                <div style="text-align: right; font-size: 14px;">
                    还没有账号？<el-link type="primary" @click="$router.push('/register')">去注册</el-link>
                </div>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
    import { ref, reactive } from 'vue'
    import { useRouter } from 'vue-router'
    import { ElMessage } from 'element-plus'
    import request from '../utils/request'

    const router = useRouter()
    const loginRef = ref(null)

    const loginForm = reactive({
    username: '',
    password: ''
    })

    // 表单校验规则
    const rules = {
    username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 16, message: '长度在 3 到 16 个字符', trigger: 'blur' }
    ],
    password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
    ]
    }

    const handleLogin = () => {
    loginRef.value.validate(async (valid) => {
    if (valid) {
    try {
    const res = await request.post('/api/login', loginForm)
    // 保存 token 到 localStorage
    localStorage.setItem('token', res.token)
    localStorage.setItem('user_id', res.user_id)

    ElMessage.success('登录成功')
    router.push('/profile') // 登录成功跳转个人中心
    } catch (error) {
    console.error('登录失败', error)
    }
    }
    })
    }
</script>

<style scoped>
    .auth-container {
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f0f2f5;
    }

    .auth-card {
        width: 400px;
    }
</style>