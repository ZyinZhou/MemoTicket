<template>
    <div class="auth-container">
        <el-card class="auth-card">
            <h2 style="text-align: center;">MemoTicket 注册</h2>
            <el-form :model="registerForm" :rules="rules" ref="registerRef" label-width="80px">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="registerForm.username" placeholder="请输入用户名" />
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" show-password />
                </el-form-item>
                <el-form-item label="确认密码" prop="confirmPassword">
                    <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码" show-password />
                </el-form-item>
                <el-form-item label="兴趣标签" prop="interests">
                    <el-select v-model="registerForm.interests" multiple placeholder="请选择你的兴趣" style="width: 100%;">
                        <el-option v-for="item in interestList"
                                   :key="item.id"
                                   :label="item.name"
                                   :value="item.id" />
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="success" @click="handleRegister" style="width: 100%;">注册</el-button>
                </el-form-item>
                <div style="text-align: right; font-size: 14px;">
                    已有账号？<el-link type="primary" @click="$router.push('/login')">去登录</el-link>
                </div>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
    import { ref, reactive, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { ElMessage } from 'element-plus'
    import request from '../utils/request'

    const router = useRouter()
    const registerRef = ref(null)
    const interestList = ref([])

    const registerForm = reactive({
    username: '',
    password: '',
    confirmPassword: '',
    interests: []
    })

    // 自定义校验规则：确认密码
    const validatePass2 = (rule, value, callback) => {
    if (value === '') {
    callback(new Error('请再次输入密码'))
    } else if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致!'))
    } else {
    callback()
    }
    }

    const rules = {
    username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 16, message: '长度在 3 到 16 个字符', trigger: 'blur' }
    ],
    password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
    ],
    confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
    ]
    }

    // 页面加载时请求兴趣列表
    onMounted(async () => {
    try {
    const res = await request.get('/api/interests')
    interestList.value = res.data
    } catch (error) {
    console.error('获取兴趣失败', error)
    }
    })

    const handleRegister = () => {
    registerRef.value.validate(async (valid) => {
    if (valid) {
    try {
    // 构造后端需要的请求体
    const payload = {
    username: registerForm.username,
    password: registerForm.password,
    interests: registerForm.interests
    }
    await request.post('/api/register', payload)
    ElMessage.success('注册成功，请登录')
    router.push('/login')
    } catch (error) {
    console.error('注册失败', error)
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
        width: 450px;
    }
</style>