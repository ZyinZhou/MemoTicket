<template>
    <div class="ticket-list-container">
        <el-card>
            <div class="header">
                <h2>我的票夹</h2>
                <div>
                    <el-button @click="$router.push('/profile')" style="margin-right: 15px;">返回个人中心</el-button>
                    <el-button type="primary" @click="$router.push('/ticket/edit')">记录新票根</el-button>
                </div>
            </div>

            <el-table :data="tickets" style="width: 100%" v-loading="loading" border>
                <el-table-column prop="title" label="体验名称" min-width="150" />
                <el-table-column prop="type" label="类型" width="120">
                    <template #default="scope">
                        <el-tag>{{ scope.row.type || '未分类' }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="rating" label="评分" width="150">
                    <template #default="scope">
                        <el-rate v-model="scope.row.rating" disabled />
                    </template>
                </el-table-column>
                <el-table-column prop="eventDate" label="活动日期" width="150" />
                <el-table-column prop="venue" label="地点" width="150" />
                <el-table-column label="操作" width="220" fixed="right">
                    <template #default="scope">
                        <el-button size="small" type="info" @click="$router.push(`/ticket/${scope.row.id}`)">详情</el-button>
                        <el-button size="small" type="primary" @click="$router.push(`/ticket/edit/${scope.row.id}`)">编辑</el-button>

                        <el-popconfirm title="确定要删除这张票根吗？" @confirm="handleDelete(scope.row.id)">
                            <template #reference>
                                <el-button size="small" type="danger">删除</el-button>
                            </template>
                        </el-popconfirm>
                    </template>
                </el-table-column>
            </el-table>

            <el-empty v-if="tickets.length === 0 && !loading" description="还没有记录过票根哦~" />
        </el-card>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import request from '../utils/request' // 直接引入 request
    import { ElMessage } from 'element-plus'

    const tickets = ref([])
    const loading = ref(false)

    // 获取列表数据
    const fetchList = async () => {
    loading.value = true
    try {
    const res = await request.get('/api/tickets')
    tickets.value = res.data || []
    } catch (error) {
    console.error('获取列表失败', error)
    } finally {
    loading.value = false
    }
    }

    // 删除票根
    const handleDelete = async (id) => {
    try {
    await request.delete(`/api/tickets/${id}`)
    ElMessage.success('删除成功')
    fetchList() // 刷新列表
    } catch (error) {
    console.error('删除失败', error)
    }
    }

    onMounted(() => {
    fetchList()
    })
</script>

<style scoped>
    .ticket-list-container {
        padding: 20px;
        background-color: #f5f7fa;
        min-height: 100vh;
    }

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
</style>