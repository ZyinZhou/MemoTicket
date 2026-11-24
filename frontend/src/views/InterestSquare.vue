<template>
  <div class="interest-square-page">
    <div class="page-header"><div><h1>🌟 兴趣广场</h1><p>发现主题，也可以创建属于你的兴趣。</p></div><el-button type="primary" @click="openCreate">创建兴趣</el-button></div>
    <div v-if="loading" class="message">正在加载兴趣...</div>
    <div v-else-if="errorMessage" class="message error">{{ errorMessage }} <el-button link @click="loadInterests">重新加载</el-button></div>
    <template v-else>
      <section v-for="section in sections" :key="section.title" class="interest-section"><h2>{{ section.title }}</h2><div v-if="section.items.length" class="square-container"><div v-for="item in section.items" :key="item.id" class="interest-card" @click="openDetail(item)"><div class="interest-icon">{{ item.is_custom ? '✨' : '🌟' }}</div><h3 class="interest-name">{{ item.name }}</h3><small v-if="item.is_custom">由用户创建</small><div v-if="canManage(item)" class="card-actions" @click.stop><el-button link type="primary" @click="openEdit(item)">编辑</el-button><el-button link type="danger" @click="removeInterest(item)">删除</el-button></div></div></div><div v-else class="empty-section">暂无兴趣</div></section>
    </template>
    <el-dialog v-model="dialogVisible" :title="editing ? '编辑兴趣' : '创建兴趣'" width="420px"><el-input v-model="formName" maxlength="100" show-word-limit placeholder="请输入兴趣名称" @keyup.enter="saveInterest" /><template #footer><el-button @click="dialogVisible = false">取消</el-button><el-button type="primary" :loading="saving" @click="saveInterest">保存</el-button></template></el-dialog>
    <el-dialog v-if="currentInterest" v-model="detailVisible" :title="currentInterest.name" width="420px"><p>兴趣编号：{{ currentInterest.id }}</p><p>{{ currentInterest.is_custom ? '这是一个用户创建的自定义兴趣。' : '这是平台预设兴趣。' }}</p></el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { createInterestApi, deleteInterestApi, getInterestListApi, updateInterestApi } from '../api/interest'

const interests = ref([]), loading = ref(false), saving = ref(false), errorMessage = ref('')
const dialogVisible = ref(false), detailVisible = ref(false), editing = ref(null), currentInterest = ref(null), formName = ref('')
const currentUserId = computed(() => Number(localStorage.getItem('user_id')) || null)
const sections = computed(() => [{ title: '预设兴趣', items: interests.value.filter(item => !item.is_custom) }, { title: '自定义兴趣', items: interests.value.filter(item => item.is_custom) }])
const loadInterests = async () => { loading.value = true; errorMessage.value = ''; try { interests.value = (await getInterestListApi()).data || [] } catch (error) { errorMessage.value = '兴趣列表加载失败，请检查后端服务。' } finally { loading.value = false } }
const canManage = item => item.is_custom && currentUserId.value === Number(item.created_by)
const openCreate = () => { editing.value = null; formName.value = ''; dialogVisible.value = true }
const openEdit = item => { editing.value = item; formName.value = item.name; dialogVisible.value = true }
const openDetail = item => { currentInterest.value = item; detailVisible.value = true }
const saveInterest = async () => { if (!formName.value.trim()) return ElMessage.warning('请输入兴趣名称'); saving.value = true; try { if (editing.value) await updateInterestApi(editing.value.id, formName.value.trim()); else await createInterestApi(formName.value.trim()); ElMessage.success(editing.value ? '修改成功' : '创建成功'); dialogVisible.value = false; await loadInterests() } finally { saving.value = false } }
const removeInterest = async item => { try { await ElMessageBox.confirm(`确定删除“${item.name}”吗？`, '删除兴趣', { type: 'warning' }); await deleteInterestApi(item.id); ElMessage.success('删除成功'); await loadInterests() } catch (error) { if (error !== 'cancel') console.error(error) } }
onMounted(loadInterests)
</script>

<style scoped>
.interest-square-page { min-height: 100vh; padding: 30px; background: #f4f5f7; } .page-header { display: flex; align-items: center; justify-content: space-between; max-width: 1100px; margin: 0 auto 24px; } h1 { margin: 0; color: #333; } .page-header p { color: #777; } .interest-section { max-width: 1100px; margin: 24px auto; } .interest-section h2 { color: #444; } .square-container { display: flex; flex-wrap: wrap; gap: 18px; } .interest-card { width: 190px; padding: 20px; background: white; border-radius: 10px; text-align: center; box-shadow: 0 4px 10px #00000012; cursor: pointer; } .interest-card:hover { transform: translateY(-3px); } .interest-icon { font-size: 36px; } .interest-name { margin: 8px 0; color: #333; } .interest-card small { color: #999; } .card-actions { margin-top: 8px; } .empty-section, .message { padding: 25px; color: #777; text-align: center; } .error { color: #d93025; }
</style>
