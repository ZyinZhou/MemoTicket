<template>
    <CommunityPage active="feed">
        <div class="page-head">
            <router-link to="/community/feed" class="back-link">← 返回社区动态</router-link>
            <h1>发布体验分享</h1>
            <p>记录真实的感受：好在哪里、踩了什么坑、值不值得推荐。</p>
        </div>

        <div class="create-layout">
            <!-- 表单 -->
            <el-card class="form-card" shadow="never">
                <el-form
                    ref="formRef"
                    :model="form"
                    :rules="rules"
                    label-position="top"
                    @submit.prevent
                >
                    <el-form-item label="分享标题" prop="title">
                        <el-input
                            v-model="form.title"
                            maxlength="40"
                            show-word-limit
                            placeholder="一句话说清楚这次体验，比如：IMAX 二刷《奥本海默》，声音先于画面击中我"
                        />
                    </el-form-item>

                    <div class="form-row">
                        <el-form-item label="所属兴趣" prop="interestId" class="form-col">
                            <el-select v-model="form.interestId" placeholder="选择兴趣分类" style="width: 100%">
                                <el-option
                                    v-for="interest in interests"
                                    :key="interest.id"
                                    :label="interest.name"
                                    :value="interest.id"
                                >
                                    <span>{{ interest.icon || '🌟' }} {{ interest.name }}</span>
                                </el-option>
                            </el-select>
                        </el-form-item>

                        <el-form-item label="关联票根（可选）" class="form-col">
                            <el-select
                                v-model="form.ticketId"
                                placeholder="从我的票夹中选择"
                                clearable
                                style="width: 100%"
                                @change="handleTicketChange"
                            >
                                <el-option
                                    v-for="ticket in tickets"
                                    :key="ticket.id"
                                    :label="`${ticket.title}（${ticket.type || '体验'}）`"
                                    :value="ticket.id"
                                />
                            </el-select>
                        </el-form-item>
                    </div>

                    <el-form-item label="我的评分" prop="rating">
                        <el-rate
                            v-model="form.rating"
                            show-text
                            :texts="['避雷', '较差', '还行', '推荐', '神作']"
                        />
                    </el-form-item>

                    <el-form-item label="标签（最多 5 个，可直接输入新标签）">
                        <el-select
                            v-model="form.tags"
                            multiple
                            filterable
                            allow-create
                            default-first-option
                            :multiple-limit="5"
                            placeholder="如：IMAX、避雷、二刷"
                            style="width: 100%"
                        />
                    </el-form-item>

                    <el-form-item label="分享正文" prop="content">
                        <el-input
                            v-model="form.content"
                            type="textarea"
                            :rows="9"
                            maxlength="1000"
                            show-word-limit
                            placeholder="可以分段写：这次体验的背景、最打动你的细节、面向同好的建议……"
                        />
                    </el-form-item>

                    <el-form-item label="配图链接（可选，最多 3 张）">
                        <div class="image-input-row">
                            <el-input
                                v-model="imageInput"
                                placeholder="粘贴图片 URL，例如 https://example.com/poster.jpg"
                                @keyup.enter="addImage"
                            />
                            <el-button :disabled="form.images.length >= 3" @click="addImage">添加</el-button>
                        </div>

                        <div v-if="form.images.length" class="image-preview-list">
                            <div v-for="(image, index) in form.images" :key="`${image}-${index}`" class="image-preview-item">
                                <el-image :src="image" fit="cover" class="image-preview" />
                                <button type="button" class="image-remove" @click="removeImage(index)">×</button>
                            </div>
                        </div>
                    </el-form-item>

                    <div class="form-actions">
                        <el-button type="primary" size="large" :loading="submitting" @click="handleSubmit">
                            {{ submitting ? '发布中…' : '发布分享' }}
                        </el-button>
                        <el-button size="large" @click="resetForm">清空</el-button>
                        <el-button size="large" text @click="goBack">取消</el-button>
                    </div>
                </el-form>
            </el-card>

            <!-- 实时预览 -->
            <aside class="preview-column">
                <div class="preview-card">
                    <div class="preview-title">
                        <span>实时预览</span>
                        <span class="preview-hint">别人看到的样子</span>
                    </div>
                    <ShareCard :share="previewShare" :clickable="false" />
                </div>

                <div class="tips-card">
                    <h3>写作小提示</h3>
                    <ul>
                        <li>标题写清楚“看了/玩了/去了什么”，方便同好搜索。</li>
                        <li>关联票根后，评分、地点、日期会自动带入。</li>
                        <li>具体细节比空泛夸赞更有用，比如座位、路线、设备。</li>
                        <li>有避雷信息时，请在正文里明确写出来。</li>
                    </ul>
                </div>
            </aside>
        </div>
    </CommunityPage>
</template>

<script setup>
    import { computed, onMounted, reactive, ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { ElMessage } from 'element-plus'
    import CommunityPage from '../components/CommunityPage.vue'
    import ShareCard from '../components/ShareCard.vue'
    import {
        createShareApi,
        getCommunityInterestsApi,
        getShareableTicketsApi
    } from '../api/community'

    const router = useRouter()

    const formRef = ref(null)
    const submitting = ref(false)
    const interests = ref([])
    const tickets = ref([])
    const imageInput = ref('')

    const form = reactive({
    title: '',
    interestId: '',
    ticketId: '',
    rating: 5,
    tags: [],
    images: [],
    content: ''
    })

    const rules = {
    title: [
    { required: true, message: '请输入分享标题', trigger: 'blur' },
    { min: 2, max: 40, message: '标题长度在 2 到 40 个字符', trigger: 'blur' }
    ],
    interestId: [{ required: true, message: '请选择所属兴趣', trigger: 'change' }],
    rating: [{ required: true, message: '请给出评分', trigger: 'change' }],
    content: [
    { required: true, message: '请填写分享正文', trigger: 'blur' },
    { min: 20, message: '正文至少 20 个字，多写点细节吧', trigger: 'blur' },
    { max: 1000, message: '正文不能超过 1000 个字', trigger: 'blur' }
    ]
    }

    const selectedTicket = computed(() =>
    tickets.value.find((ticket) => ticket.id === Number(form.ticketId)) || null
    )

    const selectedInterest = computed(() =>
    interests.value.find((interest) => interest.id === Number(form.interestId)) || null
    )

    // 预览用的分享对象，字段与动态卡片保持一致
    const previewShare = computed(() => ({
    id: 0,
    title: form.title || '你的体验标题会显示在这里',
    content: form.content || '正文预览：写清楚这次体验的背景、最打动你的细节，以及给同好的建议。',
    author: {
    nickname: localStorage.getItem('nickname') || '我'
    },
    interestId: form.interestId || null,
    interestName: selectedInterest.value ? selectedInterest.value.name : '',
    rating: form.rating,
    tags: form.tags,
    images: form.images,
    ticket: selectedTicket.value
    ? {
    id: selectedTicket.value.id,
    title: selectedTicket.value.title,
    type: selectedTicket.value.type
    }
    : null,
    likeCount: 0,
    favoriteCount: 0,
    commentCount: 0,
    liked: false,
    favorited: false,
    createTime: new Date().toISOString()
    }))

    const loadOptions = async () => {
    try {
    const [interestRes, ticketRes] = await Promise.all([
    getCommunityInterestsApi(),
    getShareableTicketsApi()
    ])
    interests.value = interestRes.data || []
    tickets.value = ticketRes.data || []
    } catch (error) {
    console.error('发布页选项加载失败', error)
    ElMessage.warning('兴趣或票根数据加载失败，仍可手动填写内容')
    }
    }

    const handleTicketChange = (ticketId) => {
    const ticket = tickets.value.find((item) => item.id === Number(ticketId))
    if (!ticket) return

    if (!form.title.trim()) {
    form.title = `${ticket.title} · 体验分享`
    }
    if (ticket.rating) {
    form.rating = ticket.rating
    }
    if (ticket.type && !form.tags.includes(ticket.type) && form.tags.length < 5) {
    form.tags.push(ticket.type)
    }
    }

    const addImage = () => {
    const url = imageInput.value.trim()
    if (!url) {
    ElMessage.warning('请先粘贴图片链接')
    return
    }
    if (!/^https?:\/\//i.test(url)) {
    ElMessage.warning('图片链接需要以 http:// 或 https:// 开头')
    return
    }
    if (form.images.length >= 3) {
    ElMessage.warning('最多添加 3 张配图')
    return
    }
    if (form.images.includes(url)) {
    ElMessage.warning('这张图已经添加过了')
    return
    }
    form.images.push(url)
    imageInput.value = ''
    }

    const removeImage = (index) => {
    form.images.splice(index, 1)
    }

    const handleSubmit = () => {
    formRef.value.validate(async (valid) => {
    if (!valid) return
    if (!localStorage.getItem('token')) {
    ElMessage.warning('登录后才能发布分享')
    router.push({ path: '/login', query: { redirect: '/share/create' } })
    return
    }

    submitting.value = true
    try {
    const res = await createShareApi({
    title: form.title.trim(),
    content: form.content.trim(),
    interestId: form.interestId,
    ticketId: form.ticketId || null,
    rating: form.rating,
    tags: form.tags,
    images: form.images
    })
    ElMessage.success('分享发布成功')
    const newId = res.data?.id
    router.push(newId ? `/share/${newId}` : '/community/feed')
    } catch (error) {
    console.error('发布失败', error)
    } finally {
    submitting.value = false
    }
    })
    }

    const resetForm = () => {
    formRef.value?.resetFields()
    form.tags = []
    form.images = []
    form.rating = 5
    form.ticketId = ''
    imageInput.value = ''
    }

    const goBack = () => router.push('/community/feed')

    onMounted(loadOptions)
</script>

<style scoped>
    .page-head {
        margin-bottom: 22px;
    }

    .back-link {
        font-size: 13px;
        color: #909399;
        text-decoration: none;
    }

    .back-link:hover {
        color: #409eff;
    }

    .page-head h1 {
        margin: 8px 0 4px;
        font-size: 30px;
        font-weight: 700;
        color: #1f2d3d;
    }

    .page-head p {
        margin: 0;
        font-size: 14px;
        color: #909399;
    }

    .create-layout {
        display: flex;
        align-items: flex-start;
        gap: 22px;
    }

    .form-card {
        flex: 1;
        min-width: 0;
        border-radius: 14px;
    }

    .form-card :deep(.el-card__body) {
        padding: 26px 28px;
    }

    .form-card :deep(.el-form-item__label) {
        font-weight: 600;
        color: #303133;
    }

    .form-row {
        display: flex;
        gap: 16px;
    }

    .form-col {
        flex: 1;
        min-width: 0;
    }

    .image-input-row {
        display: flex;
        gap: 10px;
        width: 100%;
    }

    .image-preview-list {
        display: flex;
        gap: 10px;
        margin-top: 12px;
    }

    .image-preview-item {
        position: relative;
        width: 96px;
        height: 96px;
    }

    .image-preview {
        width: 96px;
        height: 96px;
        border-radius: 8px;
        border: 1px solid #ebeef5;
    }

    .image-remove {
        position: absolute;
        top: -6px;
        right: -6px;
        width: 22px;
        height: 22px;
        font-size: 14px;
        line-height: 1;
        color: #fff;
        background: #f56c6c;
        border: none;
        border-radius: 50%;
        cursor: pointer;
    }

    .form-actions {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 8px;
    }

    .preview-column {
        position: sticky;
        top: 84px;
        display: flex;
        flex-direction: column;
        gap: 16px;
        width: 340px;
        flex-shrink: 0;
    }

    .preview-card {
        padding: 18px;
        background: linear-gradient(160deg, #f2f7ff, #ffffff);
        border: 1px solid #e6ecf9;
        border-radius: 16px;
    }

    .preview-title {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin-bottom: 12px;
        font-size: 14px;
        font-weight: 600;
        color: #303133;
    }

    .preview-hint {
        font-size: 12px;
        font-weight: 400;
        color: #a8abb2;
    }

    .tips-card {
        padding: 20px;
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 16px;
    }

    .tips-card h3 {
        margin: 0 0 10px;
        font-size: 15px;
        font-weight: 600;
        color: #1f2d3d;
    }

    .tips-card ul {
        margin: 0;
        padding-left: 16px;
        font-size: 13px;
        line-height: 1.9;
        color: #606266;
    }

    @media (max-width: 980px) {
        .create-layout {
            flex-direction: column-reverse;
        }

        .preview-column {
            position: static;
            width: 100%;
        }

        .form-card :deep(.el-card__body) {
            padding: 20px 16px;
        }

        .form-row {
            flex-direction: column;
            gap: 0;
        }

        .page-head h1 {
            font-size: 24px;
        }
    }
</style>
